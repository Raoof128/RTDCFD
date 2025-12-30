"""
Blue Team MCP Server - Specialized for Blue Team Agent Communication

This module provides the MCP server specifically configured for
blue team agents in the autonomous multi-agent simulation system.
"""

import asyncio
from typing import Dict, Any, Optional, List

from mcp_servers.mcp_server import MCPServer
from config import settings
from utils.logging_handler import get_logger


logger = get_logger(__name__)


class BlueTeamMCPServer(MCPServer):
    """
    Specialized MCP server for blue team agent communication.
    
    Provides:
    - Blue team specific message routing
    - Defense coordination features
    - Alert management
    - Incident tracking
    """
    
    def __init__(
        self,
        host: str = None,
        port: int = None,
        max_connections: int = 20
    ):
        """
        Initialize blue team MCP server.
        
        Args:
            host: Server host (from config if None)
            port: Server port (from config if None)
            max_connections: Maximum connections
        """
        super().__init__(
            host=host or settings.mcp_server_host,
            port=port or settings.mcp_blue_team_port,
            max_connections=max_connections
        )
        
        # Blue team specific state
        self.defense_posture = "monitoring"  # monitoring, active, containment, recovery
        self.active_alerts: Dict[str, Any] = {}
        self.incident_log: List[Dict[str, Any]] = []
        self.detection_rules: Dict[str, Any] = {}
        self.mitigation_actions: List[Dict[str, Any]] = []
        
        logger.info("Blue Team MCP Server initialized")
    
    async def start(self) -> None:
        """Start the blue team MCP server."""
        await super().start()
        logger.info(f"Blue Team MCP Server started on port {self.port}")
    
    def get_defense_status(self) -> Dict[str, Any]:
        """
        Get current defense status.
        
        Returns:
            Dictionary containing defense status information
        """
        return {
            "defense_posture": self.defense_posture,
            "active_alerts_count": len(self.active_alerts),
            "incident_log_length": len(self.incident_log),
            "detection_rules_count": len(self.detection_rules),
            "mitigation_actions_count": len(self.mitigation_actions),
            "connected_agents": len(self.connected_agents),
            "agent_types": self.agent_types
        }
    
    def update_defense_posture(self, new_posture: str) -> None:
        """
        Update the current defense posture.
        
        Args:
            new_posture: New defense posture
        """
        old_posture = self.defense_posture
        self.defense_posture = new_posture
        
        logger.info(f"Defense posture updated: {old_posture} -> {new_posture}")
        
        # Add to incident log
        self.incident_log.append({
            "timestamp": str(asyncio.get_event_loop().time()),
            "event": "posture_change",
            "old_posture": old_posture,
            "new_posture": new_posture,
            "severity": "info"
        })
    
    def create_alert(
        self,
        alert_id: str,
        alert_type: str,
        severity: str,
        description: str,
        source_agent: str,
        details: Dict[str, Any] = None
    ) -> None:
        """
        Create a new security alert.
        
        Args:
            alert_id: Alert identifier
            alert_type: Type of alert
            severity: Alert severity (low, medium, high, critical)
            description: Alert description
            source_agent: Agent that generated the alert
            details: Additional alert details
        """
        self.active_alerts[alert_id] = {
            "type": alert_type,
            "severity": severity,
            "description": description,
            "source_agent": source_agent,
            "created_at": str(asyncio.get_event_loop().time()),
            "status": "open",
            "details": details or {}
        }
        
        logger.warning(f"Alert created: {alert_id} - {alert_type} ({severity})")
        
        # Add to incident log
        self.incident_log.append({
            "timestamp": str(asyncio.get_event_loop().time()),
            "event": "alert_created",
            "alert_id": alert_id,
            "alert_type": alert_type,
            "severity": severity,
            "source_agent": source_agent
        })
    
    def update_alert_status(self, alert_id: str, new_status: str, assigned_to: str = None) -> None:
        """
        Update alert status.
        
        Args:
            alert_id: Alert identifier
            new_status: New status (open, investigating, resolved, false_positive)
            assigned_to: Agent assigned to handle the alert
        """
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id]["status"] = new_status
            self.active_alerts[alert_id]["assigned_to"] = assigned_to
            self.active_alerts[alert_id]["updated_at"] = str(asyncio.get_event_loop().time())
            
            logger.info(f"Alert {alert_id} status updated to: {new_status}")
            
            # Add to incident log
            self.incident_log.append({
                "timestamp": str(asyncio.get_event_loop().time()),
                "event": "alert_status_change",
                "alert_id": alert_id,
                "new_status": new_status,
                "assigned_to": assigned_to
            })
    
    def add_detection_rule(self, rule_id: str, rule_config: Dict[str, Any]) -> None:
        """
        Add a detection rule.
        
        Args:
            rule_id: Rule identifier
            rule_config: Rule configuration
        """
        self.detection_rules[rule_id] = {
            "config": rule_config,
            "created_at": str(asyncio.get_event_loop().time()),
            "enabled": True,
            "trigger_count": 0
        }
        
        logger.info(f"Detection rule added: {rule_id}")
    
    def trigger_detection_rule(self, rule_id: str, trigger_data: Dict[str, Any]) -> None:
        """
        Trigger a detection rule.
        
        Args:
            rule_id: Rule identifier
            trigger_data: Data that triggered the rule
        """
        if rule_id in self.detection_rules:
            self.detection_rules[rule_id]["trigger_count"] += 1
            self.detection_rules[rule_id]["last_triggered"] = str(asyncio.get_event_loop().time())
            
            logger.info(f"Detection rule triggered: {rule_id}")
    
    def add_mitigation_action(
        self,
        action_id: str,
        action_type: str,
        description: str,
        source_agent: str,
        target_threat: str = None
    ) -> None:
        """
        Add a mitigation action.
        
        Args:
            action_id: Action identifier
            action_type: Type of mitigation action
            description: Action description
            source_agent: Agent that performed the action
            target_threat: Threat being mitigated
        """
        mitigation_action = {
            "action_id": action_id,
            "action_type": action_type,
            "description": description,
            "source_agent": source_agent,
            "target_threat": target_threat,
            "performed_at": str(asyncio.get_event_loop().time()),
            "status": "completed"
        }
        
        self.mitigation_actions.append(mitigation_action)
        
        logger.info(f"Mitigation action performed: {action_id} - {action_type}")
        
        # Add to incident log
        self.incident_log.append({
            "timestamp": str(asyncio.get_event_loop().time()),
            "event": "mitigation_performed",
            "action_id": action_id,
            "action_type": action_type,
            "source_agent": source_agent,
            "target_threat": target_threat
        })
    
    def get_blue_team_statistics(self) -> Dict[str, Any]:
        """
        Get blue team specific statistics.
        
        Returns:
            Dictionary containing blue team statistics
        """
        base_stats = super().get_statistics()
        
        # Count alerts by severity
        alert_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for alert in self.active_alerts.values():
            alert_counts[alert["severity"]] = alert_counts.get(alert["severity"], 0) + 1
        
        blue_team_stats = {
            "defense_posture": self.defense_posture,
            "active_alerts": len(self.active_alerts),
            "alert_counts_by_severity": alert_counts,
            "incident_log_length": len(self.incident_log),
            "detection_rules_count": len(self.detection_rules),
            "mitigation_actions_count": len(self.mitigation_actions),
            "recent_incidents": self.incident_log[-10:],  # Last 10 incidents
            "active_alerts_detail": self.active_alerts
        }
        
        base_stats.update(blue_team_stats)
        return base_team_stats
    
    def get_incident_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all incidents.
        
        Returns:
            Dictionary containing incident summary
        """
        if not self.incident_log:
            return {"total_incidents": 0}
        
        # Count incident types
        incident_types = {}
        for incident in self.incident_log:
            event_type = incident.get("event", "unknown")
            incident_types[event_type] = incident_types.get(event_type, 0) + 1
        
        # Get recent incidents
        recent_incidents = self.incident_log[-20:]  # Last 20 incidents
        
        return {
            "total_incidents": len(self.incident_log),
            "incident_types": incident_types,
            "recent_incidents": recent_incidents,
            "active_alerts_count": len(self.active_alerts),
            "defense_posture": self.defense_posture
        }


# Global blue team server instance
_blue_team_server_instance: Optional[BlueTeamMCPServer] = None


async def start_blue_team_server(
    host: str = None,
    port: int = None,
    max_connections: int = 20
) -> BlueTeamMCPServer:
    """
    Start the blue team MCP server.
    
    Args:
        host: Server host
        port: Server port
        max_connections: Maximum connections
        
    Returns:
        BlueTeamMCPServer instance
    """
    global _blue_team_server_instance
    
    _blue_team_server_instance = BlueTeamMCPServer(
        host=host or settings.mcp_server_host,
        port=port or settings.mcp_blue_team_port,
        max_connections=max_connections
    )
    
    await _blue_team_server_instance.start()
    return _blue_team_server_instance


def get_blue_team_server() -> Optional[BlueTeamMCPServer]:
    """
    Get the global blue team server instance.
    
    Returns:
        BlueTeamMCPServer instance or None
    """
    return _blue_team_server_instance


async def stop_blue_team_server() -> None:
    """Stop the blue team MCP server."""
    global _blue_team_server_instance
    
    if _blue_team_server_instance:
        await _blue_team_server_instance.stop()
        _blue_team_server_instance = None
        logger.info("Blue Team MCP Server stopped")
