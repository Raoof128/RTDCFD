"""
Red Team MCP Server - Specialized for Red Team Agent Communication

This module provides the MCP server specifically configured for
red team agents in the autonomous multi-agent simulation system.
"""

import asyncio
from typing import Dict, Any, Optional

from mcp_servers.mcp_server import MCPServer
from config import settings
from utils.logging_handler import get_logger


logger = get_logger(__name__)


class RedTeamMCPServer(MCPServer):
    """
    Specialized MCP server for red team agent communication.
    
    Provides:
    - Red team specific message routing
    - Attack coordination features
    - Progress tracking
    - Security constraints enforcement
    """
    
    def __init__(
        self,
        host: str = None,
        port: int = None,
        max_connections: int = 20
    ):
        """
        Initialize red team MCP server.
        
        Args:
            host: Server host (from config if None)
            port: Server port (from config if None)
            max_connections: Maximum connections
        """
        super().__init__(
            host=host or settings.mcp_red_team_port,
            port=port or settings.mcp_red_team_port,
            max_connections=max_connections
        )
        
        # Red team specific state
        self.attack_phase = "reconnaissance"
        self.active_targets: Dict[str, Any] = {}
        self.attack_timeline: list = []
        
        logger.info("Red Team MCP Server initialized")
    
    async def start(self) -> None:
        """Start the red team MCP server."""
        await super().start()
        logger.info(f"Red Team MCP Server started on port {self.port}")
    
    def get_attack_status(self) -> Dict[str, Any]:
        """
        Get current attack status.
        
        Returns:
            Dictionary containing attack status information
        """
        return {
            "attack_phase": self.attack_phase,
            "active_targets": self.active_targets,
            "attack_timeline": self.attack_timeline,
            "connected_agents": len(self.connected_agents),
            "agent_types": self.agent_types
        }
    
    def update_attack_phase(self, new_phase: str) -> None:
        """
        Update the current attack phase.
        
        Args:
            new_phase: New attack phase
        """
        old_phase = self.attack_phase
        self.attack_phase = new_phase
        
        logger.info(f"Attack phase updated: {old_phase} -> {new_phase}")
        
        # Add to timeline
        self.attack_timeline.append({
            "timestamp": str(asyncio.get_event_loop().time()),
            "event": "phase_change",
            "old_phase": old_phase,
            "new_phase": new_phase
        })
    
    def add_target(self, target_id: str, target_info: Dict[str, Any]) -> None:
        """
        Add a target to the active targets list.
        
        Args:
            target_id: Target identifier
            target_info: Target information
        """
        self.active_targets[target_id] = {
            "info": target_info,
            "status": "identified",
            "discovered_at": str(asyncio.get_event_loop().time())
        }
        
        logger.info(f"Target added: {target_id}")
        
        # Add to timeline
        self.attack_timeline.append({
            "timestamp": str(asyncio.get_event_loop().time()),
            "event": "target_identified",
            "target_id": target_id,
            "target_info": target_info
        })
    
    def update_target_status(self, target_id: str, new_status: str, details: Dict[str, Any] = None) -> None:
        """
        Update target status.
        
        Args:
            target_id: Target identifier
            new_status: New status
            details: Additional details
        """
        if target_id in self.active_targets:
            self.active_targets[target_id]["status"] = new_status
            if details:
                self.active_targets[target_id]["details"] = details
            
            logger.info(f"Target {target_id} status updated to: {new_status}")
            
            # Add to timeline
            self.attack_timeline.append({
                "timestamp": str(asyncio.get_event_loop().time()),
                "event": "target_status_change",
                "target_id": target_id,
                "new_status": new_status,
                "details": details or {}
            })
    
    def get_red_team_statistics(self) -> Dict[str, Any]:
        """
        Get red team specific statistics.
        
        Returns:
            Dictionary containing red team statistics
        """
        base_stats = super().get_statistics()
        
        red_team_stats = {
            "attack_phase": self.attack_phase,
            "active_targets_count": len(self.active_targets),
            "attack_timeline_length": len(self.attack_timeline),
            "active_targets": self.active_targets,
            "recent_timeline": self.attack_timeline[-10:]  # Last 10 events
        }
        
        base_stats.update(red_team_stats)
        return base_team_stats


# Global red team server instance
_red_team_server_instance: Optional[RedTeamMCPServer] = None


async def start_red_team_server(
    host: str = None,
    port: int = None,
    max_connections: int = 20
) -> RedTeamMCPServer:
    """
    Start the red team MCP server.
    
    Args:
        host: Server host
        port: Server port
        max_connections: Maximum connections
        
    Returns:
        RedTeamMCPServer instance
    """
    global _red_team_server_instance
    
    _red_team_server_instance = RedTeamMCPServer(
        host=host or settings.mcp_server_host,
        port=port or settings.mcp_red_team_port,
        max_connections=max_connections
    )
    
    await _red_team_server_instance.start()
    return _red_team_server_instance


def get_red_team_server() -> Optional[RedTeamMCPServer]:
    """
    Get the global red team server instance.
    
    Returns:
        RedTeamMCPServer instance or None
    """
    return _red_team_server_instance


async def stop_red_team_server() -> None:
    """Stop the red team MCP server."""
    global _red_team_server_instance
    
    if _red_team_server_instance:
        await _red_team_server_instance.stop()
        _red_team_server_instance = None
        logger.info("Red Team MCP Server stopped")
