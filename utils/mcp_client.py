"""
MCP (Model Context Protocol) Client for Agent Communication

This module provides the MCP client implementation for inter-agent
communication in the autonomous multi-agent simulation system.
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import websockets

from utils.logging_handler import get_logger


# Define AgentMessage locally to avoid circular imports
class AgentMessage:
    """Agent message for inter-agent communication"""

    def __init__(
        self,
        sender_id: str,
        receiver_id: str,
        message_type: str,
        content: Dict[str, Any],
    ):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message_type = message_type
        self.content = content
        self.timestamp = datetime.now()
        self.message_id = str(uuid.uuid4())


logger = get_logger(__name__)


class MCPClient:
    """
    MCP client for inter-agent communication.

    Provides:
    - WebSocket-based message passing
    - Message routing and filtering
    - Automatic reconnection
    - Message acknowledgment
    """

    def __init__(
        self,
        agent_id: str,
        server_host: str = "localhost",
        server_port: int = 8080,
        reconnect_interval: float = 5.0,
        max_reconnect_attempts: int = 10,
    ):
        """
        Initialize MCP client.

        Args:
            agent_id: ID of this agent
            server_host: MCP server host
            server_port: MCP server port
            reconnect_interval: Reconnection interval in seconds
            max_reconnect_attempts: Maximum reconnection attempts
        """
        self.agent_id = agent_id
        self.server_host = server_host
        self.server_port = server_port
        self.reconnect_interval = reconnect_interval
        self.max_reconnect_attempts = max_reconnect_attempts

        # WebSocket connection
        self.websocket: Optional[websockets.WebSocketServerProtocol] = None
        self.is_running = False
        self.reconnect_count = 0

        # Message handling
        self.message_handlers: Dict[str, Callable] = {}
        self.pending_responses: Dict[str, asyncio.Future] = {}

        # Statistics
        self.messages_sent = 0
        self.messages_received = 0
        self.connection_time: Optional[datetime] = None

        # URI for WebSocket connection
        self.uri = f"ws://{server_host}:{server_port}/ws/{agent_id}"

    async def start(self) -> None:
        """Start the MCP client and connect to the server."""
        self.is_running = True
        await self._connect()

        # Start message processing task
        asyncio.create_task(self._message_loop())

        logger.info(f"MCP client started for agent {self.agent_id}")

    async def stop(self) -> None:
        """Stop the MCP client."""
        self.is_running = False

        if self.websocket:
            await self.websocket.close()
            self.websocket = None

        logger.info(f"MCP client stopped for agent {self.agent_id}")

    async def _connect(self) -> None:
        """Connect to the MCP server with reconnection logic."""
        while self.is_running and self.reconnect_count < self.max_reconnect_attempts:
            try:
                logger.info(f"Connecting to MCP server at {self.uri}")
                self.websocket = await websockets.connect(self.uri)
                self.connection_time = datetime.now()
                self.reconnect_count = 0

                # Send registration message
                await self._register()

                logger.info(f"Connected to MCP server as {self.agent_id}")
                break

            except Exception as e:
                self.reconnect_count += 1
                logger.warning(f"Connection attempt {self.reconnect_count} failed: {e}")

                if self.reconnect_count < self.max_reconnect_attempts:
                    await asyncio.sleep(self.reconnect_interval)
                else:
                    logger.error(
                        f"Failed to connect after {self.max_reconnect_attempts} attempts"
                    )
                    raise

    async def _register(self) -> None:
        """Register with the MCP server."""
        registration_message = {
            "type": "register",
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
        }

        await self.websocket.send(json.dumps(registration_message))

    async def _message_loop(self) -> None:
        """Main message processing loop."""
        while self.is_running and self.websocket:
            try:
                message = await self.websocket.recv()
                await self._handle_received_message(message)

            except websockets.exceptions.ConnectionClosed:
                logger.warning(
                    "WebSocket connection closed, attempting reconnection..."
                )
                await self._connect()

            except Exception as e:
                logger.error(f"Error in message loop: {e}")
                await asyncio.sleep(1)

    async def _handle_received_message(self, raw_message: str) -> None:
        """Handle a received message."""
        try:
            message_data = json.loads(raw_message)

            # Convert to AgentMessage
            message = AgentMessage(
                id=message_data.get("id", str(uuid.uuid4())),
                sender_id=message_data.get("sender_id", ""),
                receiver_id=message_data.get("receiver_id", self.agent_id),
                message_type=message_data.get("message_type", "command"),
                content=message_data.get("content", {}),
                timestamp=datetime.fromisoformat(
                    message_data.get("timestamp", datetime.now().isoformat())
                ),
                priority=message_data.get("priority", "normal"),
                requires_response=message_data.get("requires_response", False),
            )

            self.messages_received += 1

            # Check if this is a response to a pending request
            if (
                message.message_type == "response"
                and message.id in self.pending_responses
            ):
                future = self.pending_responses.pop(message.id)
                future.set_result(message)
            else:
                # Handle regular message
                await self._process_message(message)

        except Exception as e:
            logger.error(f"Error handling received message: {e}")

    async def _process_message(self, message: AgentMessage) -> None:
        """Process a received message."""
        # Call registered handler if available
        handler = self.message_handlers.get(message.message_type)
        if handler:
            try:
                await handler(message)
            except Exception as e:
                logger.error(f"Error in message handler: {e}")
        else:
            logger.warning(f"No handler for message type: {message.message_type}")

    async def send_message(self, message: AgentMessage) -> None:
        """
        Send a message to another agent.

        Args:
            message: Message to send
        """
        if not self.websocket:
            logger.warning("Cannot send message: not connected to MCP server")
            return

        try:
            message_data = {
                "id": message.id,
                "sender_id": message.sender_id,
                "receiver_id": message.receiver_id,
                "message_type": message.message_type,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "priority": message.priority,
                "requires_response": message.requires_response,
            }

            await self.websocket.send(json.dumps(message_data))
            self.messages_sent += 1

            logger.debug(
                f"Sent {message.message_type} message to {message.receiver_id}"
            )

        except Exception as e:
            logger.error(f"Error sending message: {e}")

    async def send_command(
        self,
        receiver_id: str,
        command: Dict[str, Any],
        priority: str = "normal",
        timeout: float = 30.0,
    ) -> Optional[AgentMessage]:
        """
        Send a command and wait for response.

        Args:
            receiver_id: ID of the receiving agent
            command: Command content
            priority: Message priority
            timeout: Response timeout in seconds

        Returns:
            Response message or None if timeout
        """
        message = AgentMessage(
            sender_id=self.agent_id,
            receiver_id=receiver_id,
            message_type="command",
            content=command,
            priority=priority,
            requires_response=True,
        )

        # Create future for response
        response_future = asyncio.Future()
        self.pending_responses[message.id] = response_future

        # Send message
        await self.send_message(message)

        # Wait for response
        try:
            response = await asyncio.wait_for(response_future, timeout=timeout)
            return response
        except asyncio.TimeoutError:
            logger.warning(f"Command to {receiver_id} timed out")
            self.pending_responses.pop(message.id, None)
            return None

    def register_handler(self, message_type: str, handler: Callable) -> None:
        """
        Register a message handler.

        Args:
            message_type: Message type to handle
            handler: Handler function
        """
        self.message_handlers[message_type] = handler
        logger.debug(f"Registered handler for message type: {message_type}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get client statistics."""
        return {
            "agent_id": self.agent_id,
            "is_connected": self.websocket is not None,
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "reconnect_count": self.reconnect_count,
            "connection_time": (
                self.connection_time.isoformat() if self.connection_time else None
            ),
            "registered_handlers": list(self.message_handlers.keys()),
        }

    async def ping(self) -> bool:
        """Ping the server to check connection."""
        if not self.websocket:
            return False

        try:
            ping_message = {
                "type": "ping",
                "agent_id": self.agent_id,
                "timestamp": datetime.now().isoformat(),
            }

            await self.websocket.send(json.dumps(ping_message))
            return True

        except Exception as e:
            logger.error(f"Ping failed: {e}")
            return False
