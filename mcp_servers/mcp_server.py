"""
MCP (Model Context Protocol) Server for Agent Communication

This module provides the MCP server implementation for coordinating
communication between agents in the autonomous multi-agent simulation system.
"""

import asyncio
import json
import websockets
from typing import Dict, Set, Optional, Any, List
from datetime import datetime
import uuid
from websockets.server import WebSocketServerProtocol

from agents.base_agent import AgentMessage
from utils.logging_handler import get_logger


logger = get_logger(__name__)


class ConnectedAgent:
    """Represents a connected agent in the MCP server."""
    
    def __init__(self, agent_id: str, websocket: WebSocketServerProtocol):
        self.agent_id = agent_id
        self.websocket = websocket
        self.connected_at = datetime.now()
        self.last_ping = datetime.now()
        self.message_count = 0
        self.agent_type = "unknown"
    
    def update_stats(self) -> None:
        """Update agent statistics."""
        self.message_count += 1
        self.last_ping = datetime.now()
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "connected_at": self.connected_at.isoformat(),
            "last_ping": self.last_ping.isoformat(),
            "message_count": self.message_count
        }


class MCPServer:
    """
    MCP server for coordinating agent communication.
    
    Provides:
    - WebSocket-based message routing
    - Agent registration and management
    - Message broadcasting
    - Connection monitoring
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        max_connections: int = 50
    ):
        """
        Initialize MCP server.
        
        Args:
            host: Server host
            port: Server port
            max_connections: Maximum number of concurrent connections
        """
        self.host = host
        self.port = port
        self.max_connections = max_connections
        
        # Connected agents
        self.connected_agents: Dict[str, ConnectedAgent] = {}
        self.agent_types: Dict[str, str] = {}
        
        # Server state
        self.server: Optional[websockets.WebSocketServer] = None
        self.is_running = False
        
        # Message routing
        self.message_queue = asyncio.Queue()
        self.broadcast_queue = asyncio.Queue()
        
        # Statistics
        self.total_connections = 0
        self.total_messages = 0
        self.server_start_time: Optional[datetime] = None
    
    async def start(self) -> None:
        """Start the MCP server."""
        self.is_running = True
        self.server_start_time = datetime.now()
        
        # Start WebSocket server
        self.server = await websockets.serve(
            self._handle_connection,
            self.host,
            self.port,
            max_size=10 * 1024 * 1024,  # 10MB max message size
            ping_interval=20,
            ping_timeout=10
        )
        
        # Start background tasks
        asyncio.create_task(self._message_processor())
        asyncio.create_task(self._connection_monitor())
        
        logger.info(f"MCP server started at ws://{self.host}:{self.port}")
    
    async def stop(self) -> None:
        """Stop the MCP server."""
        self.is_running = False
        
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.server = None
        
        # Disconnect all agents
        for agent in list(self.connected_agents.values()):
            try:
                await agent.websocket.close()
            except:
                pass
        
        self.connected_agents.clear()
        logger.info("MCP server stopped")
    
    async def _handle_connection(self, websocket: WebSocketServerProtocol, path: str) -> None:
        """
        Handle a new WebSocket connection.
        
        Args:
            websocket: WebSocket connection
            path: Connection path (contains agent_id)
        """
        # Extract agent_id from path
        try:
            parts = path.strip("/").split("/")
            if len(parts) < 2 or parts[0] != "ws":
                await websocket.close(1003, "Invalid path")
                return
            
            agent_id = parts[1]
            
            # Check if agent already connected
            if agent_id in self.connected_agents:
                logger.warning(f"Agent {agent_id} already connected, closing old connection")
                old_agent = self.connected_agents.pop(agent_id)
                await old_agent.websocket.close()
            
            # Check connection limit
            if len(self.connected_agents) >= self.max_connections:
                await websocket.close(1013, "Server overloaded")
                return
            
            # Register agent
            agent = ConnectedAgent(agent_id, websocket)
            self.connected_agents[agent_id] = agent
            self.total_connections += 1
            
            logger.info(f"Agent {agent_id} connected from {websocket.remote_address}")
            
            # Handle messages from this agent
            await self._handle_agent_messages(agent)
            
        except Exception as e:
            logger.error(f"Error handling connection: {e}")
            await websocket.close(1011, "Internal server error")
    
    async def _handle_agent_messages(self, agent: ConnectedAgent) -> None:
        """
        Handle messages from a connected agent.
        
        Args:
            agent: Connected agent
        """
        try:
            async for message in agent.websocket:
                await self._process_message(agent, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Agent {agent.agent_id} disconnected")
        except Exception as e:
            logger.error(f"Error handling messages from {agent.agent_id}: {e}")
        finally:
            # Remove agent from connected list
            self.connected_agents.pop(agent.agent_id, None)
            logger.info(f"Agent {agent.agent_id} removed from active connections")
    
    async def _process_message(self, agent: ConnectedAgent, raw_message: str) -> None:
        """
        Process a message from an agent.
        
        Args:
            agent: Sending agent
            raw_message: Raw message string
        """
        try:
            message_data = json.loads(raw_message)
            agent.update_stats()
            self.total_messages += 1
            
            # Handle registration message
            if message_data.get("type") == "register":
                await self._handle_registration(agent, message_data)
                return
            
            # Convert to AgentMessage
            message = AgentMessage(
                id=message_data.get("id", str(uuid.uuid4())),
                sender_id=message_data.get("sender_id", agent.agent_id),
                receiver_id=message_data.get("receiver_id", ""),
                message_type=message_data.get("message_type", "command"),
                content=message_data.get("content", {}),
                timestamp=datetime.fromisoformat(
                    message_data.get("timestamp", datetime.now().isoformat())
                ),
                priority=message_data.get("priority", "normal"),
                requires_response=message_data.get("requires_response", False)
            )
            
            # Route message
            await self._route_message(agent, message)
            
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON from agent {agent.agent_id}")
        except Exception as e:
            logger.error(f"Error processing message from {agent.agent_id}: {e}")
    
    async def _handle_registration(self, agent: ConnectedAgent, message_data: Dict[str, Any]) -> None:
        """
        Handle agent registration.
        
        Args:
            agent: Registering agent
            message_data: Registration message data
        """
        agent.agent_type = message_data.get("agent_type", "unknown")
        self.agent_types[agent.agent_id] = agent.agent_type
        
        logger.info(f"Agent {agent.agent_id} registered as {agent.agent_type}")
        
        # Send confirmation
        confirmation = {
            "type": "registration_confirmed",
            "agent_id": agent.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        await agent.websocket.send(json.dumps(confirmation))
    
    async def _route_message(self, sender: ConnectedAgent, message: AgentMessage) -> None:
        """
        Route a message to the appropriate recipient.
        
        Args:
            sender: Sending agent
            message: Message to route
        """
        if message.receiver_id == "broadcast":
            # Broadcast to all agents except sender
            await self._broadcast_message(sender, message)
        elif message.receiver_id in self.connected_agents:
            # Send to specific agent
            recipient = self.connected_agents[message.receiver_id]
            await self._send_to_agent(recipient, message)
        else:
            # Unknown recipient
            logger.warning(f"Unknown recipient: {message.receiver_id}")
            await self._send_error_response(sender, message, "Unknown recipient")
    
    async def _send_to_agent(self, agent: ConnectedAgent, message: AgentMessage) -> None:
        """
        Send a message to a specific agent.
        
        Args:
            agent: Recipient agent
            message: Message to send
        """
        try:
            message_data = {
                "id": message.id,
                "sender_id": message.sender_id,
                "receiver_id": message.receiver_id,
                "message_type": message.message_type,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "priority": message.priority,
                "requires_response": message.requires_response
            }
            
            await agent.websocket.send(json.dumps(message_data))
            logger.debug(f"Message routed to {agent.agent_id}")
            
        except Exception as e:
            logger.error(f"Error sending message to {agent.agent_id}: {e}")
    
    async def _broadcast_message(self, sender: ConnectedAgent, message: AgentMessage) -> None:
        """
        Broadcast a message to all agents except sender.
        
        Args:
            sender: Broadcasting agent
            message: Message to broadcast
        """
        recipients = [
            agent for agent_id, agent in self.connected_agents.items()
            if agent_id != sender.agent_id
        ]
        
        for recipient in recipients:
            await self._send_to_agent(recipient, message)
        
        logger.debug(f"Message broadcast to {len(recipients)} agents")
    
    async def _send_error_response(self, agent: ConnectedAgent, original_message: AgentMessage, error: str) -> None:
        """
        Send an error response to an agent.
        
        Args:
            agent: Agent to send error to
            original_message: Original message that caused error
            error: Error description
        """
        error_message = AgentMessage(
            sender_id="server",
            receiver_id=agent.agent_id,
            message_type="error",
            content={"error": error, "original_message_id": original_message.id},
            timestamp=datetime.now()
        )
        
        await self._send_to_agent(agent, error_message)
    
    async def _message_processor(self) -> None:
        """Background task for processing queued messages."""
        while self.is_running:
            try:
                # Process message queue
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                # Message processing is now handled directly in _process_message
                self.message_queue.task_done()
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error in message processor: {e}")
    
    async def _connection_monitor(self) -> None:
        """Background task for monitoring connections."""
        while self.is_running:
            try:
                await asyncio.sleep(30)  # Check every 30 seconds
                
                # Check for stale connections
                current_time = datetime.now()
                stale_agents = []
                
                for agent_id, agent in self.connected_agents.items():
                    if (current_time - agent.last_ping).seconds > 120:  # 2 minutes timeout
                        stale_agents.append(agent)
                
                # Close stale connections
                for agent in stale_agents:
                    logger.warning(f"Closing stale connection: {agent.agent_id}")
                    await agent.websocket.close()
                    self.connected_agents.pop(agent.agent_id, None)
                
            except Exception as e:
                logger.error(f"Error in connection monitor: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get server statistics."""
        return {
            "host": self.host,
            "port": self.port,
            "is_running": self.is_running,
            "connected_agents": len(self.connected_agents),
            "total_connections": self.total_connections,
            "total_messages": self.total_messages,
            "server_start_time": self.server_start_time.isoformat() if self.server_start_time else None,
            "uptime_seconds": (
                (datetime.now() - self.server_start_time).total_seconds()
                if self.server_start_time else 0
            ),
            "agents": {
                agent_id: agent.get_info()
                for agent_id, agent in self.connected_agents.items()
            }
        }
    
    def get_agent_list(self) -> List[Dict[str, Any]]:
        """Get list of connected agents."""
        return [
            {
                "agent_id": agent.agent_id,
                "agent_type": agent.agent_type,
                "connected_at": agent.connected_at.isoformat(),
                "message_count": agent.message_count
            }
            for agent in self.connected_agents.values()
        ]


# Global server instances
_red_team_server: Optional[MCPServer] = None
_blue_team_server: Optional[MCPServer] = None
_main_server: Optional[MCPServer] = None


async def start_main_server(host: str = "localhost", port: int = 8080) -> MCPServer:
    """Start the main MCP server."""
    global _main_server
    _main_server = MCPServer(host, port)
    await _main_server.start()
    return _main_server


async def start_red_team_server(host: str = "localhost", port: int = 8081) -> MCPServer:
    """Start the red team MCP server."""
    global _red_team_server
    _red_team_server = MCPServer(host, port)
    await _red_team_server.start()
    return _red_team_server


async def start_blue_team_server(host: str = "localhost", port: int = 8082) -> MCPServer:
    """Start the blue team MCP server."""
    global _blue_team_server
    _blue_team_server = MCPServer(host, port)
    await _blue_team_server.start()
    return _blue_team_server


async def stop_all_servers() -> None:
    """Stop all MCP servers."""
    for server in [_main_server, _red_team_server, _blue_team_server]:
        if server:
            await server.stop()
