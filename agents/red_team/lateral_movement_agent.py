"""
Red Team Lateral Movement Agent

This agent specializes in network traversal simulation, privilege escalation tactics,
and persistence mechanisms for security testing under the Australian SOCI Act framework.
"""

import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

from agents.base_agent import BaseAgent, AgentMessage
from config import AgentConfig
from utils.logging_handler import get_agent_logger, get_narrative_logger
from utils.prompt_templates import LATERAL_MOVEMENT_AGENT_PROMPT


class LateralMovementAgent(BaseAgent):
    """
    Red Team Lateral Movement Agent
    
    Capabilities:
    - Network traversal path analysis
    - Privilege escalation scenario simulation
    - Persistence mechanism documentation
    - Defense evasion tactic analysis
    - Detection strategy development
    
    MITRE ATT&CK Techniques:
    - T1021: Remote Services
    - T1028: Windows Remote Management
    - T1547: Boot or Logon Autostart Execution
    - T1574: Hijack Execution Flow
    """
    
    def __init__(self, agent_id: str = None):
        """Initialize the lateral movement agent."""
        agent_id = agent_id or f"lateral_movement_agent_{uuid.uuid4().hex[:8]}"
        
        # Initialize with lateral movement-specific tools
        tools = self._create_lateral_movement_tools()
        
        super().__init__(
            agent_id=agent_id,
            agent_type="red_team_lateral_movement",
            system_prompt=LATERAL_MOVEMENT_AGENT_PROMPT,
            tools=tools,
            enable_mcp=True
        )
        
        self.logger = get_agent_logger(agent_id, "red_team_lateral_movement")
        self.narrative_logger = get_narrative_logger()
        
        # Lateral movement state
        self.network_traversals = {}
        self.privilege_escalations = {}
        self.persistence_mechanisms = {}
        self.defense_evasions = {}
        
        self.logger.info(f"Lateral Movement Agent {agent_id} initialized")
    
    def _create_lateral_movement_tools(self) -> List:
        """Create lateral movement-specific tools."""
        from langchain.tools import BaseTool
        from pydantic import BaseModel, Field
        
        class NetworkTraversalInput(BaseModel):
            starting_point: str = Field(description="Starting point in network")
            target_destination: str = Field(description="Target destination")
            network_constraints: str = Field(description="Network constraints or segmentation")
        
        class NetworkTraversalTool(BaseTool):
            name = "analyze_network_traversal"
            description = "Analyze network traversal paths and possibilities"
            args_schema = NetworkTraversalInput
            
            def _run(self, starting_point: str, target_destination: str, network_constraints: str) -> str:
                # Simulate network traversal analysis
                return f"Simulated network traversal analysis from {starting_point} to {target_destination} with constraints: {network_constraints}. Includes possible paths, required credentials, and detection points."
        
        class PrivilegeEscalationInput(BaseModel):
            current_privilege: str = Field(description="Current privilege level")
            target_privilege: str = Field(description="Target privilege level")
            system_type: str = Field(description="System type or OS")
        
        class PrivilegeEscalationTool(BaseTool):
            name = "simulate_privilege_escalation"
            description = "Simulate privilege escalation scenarios"
            args_schema = PrivilegeEscalationInput
            
            def _run(self, current_privilege: str, target_privilege: str, system_type: str) -> str:
                # Simulate privilege escalation
                return f"Simulated privilege escalation from {current_privilege} to {target_privilege} on {system_type}. Includes escalation vectors, required conditions, and detection methods."
        
        class PersistenceMechanismInput(BaseModel):
            mechanism_type: str = Field(description="Type of persistence mechanism")
            target_system: str = Field(description="Target system or environment")
            stealth_level: str = Field(description="Stealth level (low, medium, high)")
        
        class PersistenceMechanismTool(BaseTool):
            name = "analyze_persistence_mechanism"
            description = "Analyze persistence mechanisms"
            args_schema = PersistenceMechanismInput
            
            def _run(self, mechanism_type: str, target_system: str, stealth_level: str) -> str:
                # Simulate persistence mechanism analysis
                return f"Simulated {stealth_level} stealth {mechanism_type} persistence for {target_system}. Includes implementation details, detection challenges, and removal methods."
        
        class DefenseEvasionInput(BaseModel):
            defense_type: str = Field(description="Type of defense to evade")
            evasion_method: str = Field(description="Method of evasion")
            target_environment: str = Field(description="Target environment")
        
        class DefenseEvasionTool(BaseTool):
            name = "analyze_defense_evasion"
            description = "Analyze defense evasion techniques"
            args_schema = DefenseEvasionInput
            
            def _run(self, defense_type: str, evasion_method: str, target_environment: str) -> str:
                # Simulate defense evasion analysis
                return f"Simulated analysis of {evasion_method} evasion for {defense_type} in {target_environment}. Includes evasion steps, effectiveness, and countermeasures."
        
        return [
            NetworkTraversalTool(),
            PrivilegeEscalationTool(),
            PersistenceMechanismTool(),
            DefenseEvasionTool()
        ]
    
    async def process_command(self, command: Dict[str, Any]) -> None:
        """Process lateral movement command from coordinator."""
        self.logger.info(f"Processing lateral movement command: {command}")
        
        command_type = command.get("type", "unknown")
        
        if command_type == "network_traversal":
            await self._handle_network_traversal_command(command)
        elif command_type == "privilege_escalation":
            await self._handle_privilege_escalation_command(command)
        elif command_type == "persistence_mechanism":
            await self._handle_persistence_mechanism_command(command)
        elif command_type == "defense_evasion":
            await self._handle_defense_evasion_command(command)
        else:
            self.logger.warning(f"Unknown command type: {command_type}")
    
    async def _handle_network_traversal_command(self, command: Dict[str, Any]) -> None:
        """Handle network traversal command."""
        starting_point = command.get("starting_point")
        target_destination = command.get("target_destination")
        network_constraints = command.get("network_constraints", "standard")
        traversal_id = command.get("traversal_id", f"traversal_{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting network traversal analysis: {traversal_id}")
        
        # Execute network traversal task
        task = f"Analyze network traversal from {starting_point} to {target_destination} with constraints: {network_constraints}"
        result = await self.execute_task(task)
        
        if result["success"]:
            # Store network traversal data
            self.network_traversals[traversal_id] = {
                "starting_point": starting_point,
                "target_destination": target_destination,
                "network_constraints": network_constraints,
                "traversal_analysis": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "T1021"  # Remote Services
            }
            
            # Log narrative event
            self.narrative_logger.log_attack_event(
                agent_id=self.agent_id,
                attack_stage="lateral_movement",
                mitre_technique="T1021",
                description=f"Network traversal analyzed: {traversal_id}",
                target=target_destination,
                success=True,
                details={
                    "traversal_id": traversal_id,
                    "starting_point": starting_point,
                    "target_destination": target_destination,
                    "traversal_summary": result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"]
                }
            )
            
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "network_traversal",
                    "traversal_id": traversal_id,
                    "target_destination": target_destination,
                    "results": result["result"],
                    "success": True
                }
            )
        else:
            self.logger.error(f"Network traversal analysis failed: {result.get('error')}")
    
    async def _handle_privilege_escalation_command(self, command: Dict[str, Any]) -> None:
        """Handle privilege escalation command."""
        current_privilege = command.get("current_privilege")
        target_privilege = command.get("target_privilege")
        system_type = command.get("system_type", "Windows")
        escalation_id = command.get("escalation_id", f"escalation_{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting privilege escalation simulation: {escalation_id}")
        
        # Execute privilege escalation task
        task = f"Simulate privilege escalation from {current_privilege} to {target_privilege} on {system_type}"
        result = await self.execute_task(task)
        
        if result["success"]:
            # Store privilege escalation data
            self.privilege_escalations[escalation_id] = {
                "current_privilege": current_privilege,
                "target_privilege": target_privilege,
                "system_type": system_type,
                "escalation_scenario": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "T1574"  # Hijack Execution Flow
            }
            
            # Log narrative event
            self.narrative_logger.log_attack_event(
                agent_id=self.agent_id,
                attack_stage="privilege_escalation",
                mitre_technique="T1574",
                description=f"Privilege escalation simulated: {escalation_id}",
                target=target_privilege,
                success=True,
                details={
                    "escalation_id": escalation_id,
                    "current_privilege": current_privilege,
                    "target_privilege": target_privilege,
                    "system_type": system_type,
                    "escalation_summary": result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"]
                }
            )
            
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "privilege_escalation",
                    "escalation_id": escalation_id,
                    "target_privilege": target_privilege,
                    "results": result["result"],
                    "success": True
                }
            )
        else:
            self.logger.error(f"Privilege escalation simulation failed: {result.get('error')}")
    
    async def _handle_persistence_mechanism_command(self, command: Dict[str, Any]) -> None:
        """Handle persistence mechanism command."""
        mechanism_type = command.get("mechanism_type")
        target_system = command.get("target_system")
        stealth_level = command.get("stealth_level", "medium")
        persistence_id = command.get("persistence_id", f"persistence_{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting persistence mechanism analysis: {persistence_id}")
        
        # Execute persistence mechanism task
        task = f"Analyze {stealth_level} stealth {mechanism_type} persistence for {target_system}"
        result = await self.execute_task(task)
        
        if result["success"]:
            # Store persistence mechanism data
            self.persistence_mechanisms[persistence_id] = {
                "mechanism_type": mechanism_type,
                "target_system": target_system,
                "stealth_level": stealth_level,
                "persistence_analysis": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "T1547"  # Boot or Logon Autostart Execution
            }
            
            # Log narrative event
            self.narrative_logger.log_attack_event(
                agent_id=self.agent_id,
                attack_stage="persistence",
                mitre_technique="T1547",
                description=f"Persistence mechanism analyzed: {persistence_id}",
                target=target_system,
                success=True,
                details={
                    "persistence_id": persistence_id,
                    "mechanism_type": mechanism_type,
                    "target_system": target_system,
                    "stealth_level": stealth_level,
                    "persistence_summary": result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"]
                }
            )
            
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "persistence_mechanism",
                    "persistence_id": persistence_id,
                    "mechanism_type": mechanism_type,
                    "results": result["result"],
                    "success": True
                }
            )
        else:
            self.logger.error(f"Persistence mechanism analysis failed: {result.get('error')}")
    
    async def _handle_defense_evasion_command(self, command: Dict[str, Any]) -> None:
        """Handle defense evasion command."""
        defense_type = command.get("defense_type")
        evasion_method = command.get("evasion_method")
        target_environment = command.get("target_environment")
        evasion_id = command.get("evasion_id", f"evasion_{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting defense evasion analysis: {evasion_id}")
        
        # Execute defense evasion task
        task = f"Analyze {evasion_method} evasion for {defense_type} in {target_environment}"
        result = await self.execute_task(task)
        
        if result["success"]:
            # Store defense evasion data
            self.defense_evasions[evasion_id] = {
                "defense_type": defense_type,
                "evasion_method": evasion_method,
                "target_environment": target_environment,
                "evasion_analysis": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "T1028"  # Windows Remote Management
            }
            
            # Log narrative event
            self.narrative_logger.log_attack_event(
                agent_id=self.agent_id,
                attack_stage="defense_evasion",
                mitre_technique="T1028",
                description=f"Defense evasion analyzed: {evasion_id}",
                target=defense_type,
                success=True,
                details={
                    "evasion_id": evasion_id,
                    "defense_type": defense_type,
                    "evasion_method": evasion_method,
                    "target_environment": target_environment,
                    "evasion_summary": result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"]
                }
            )
            
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "defense_evasion",
                    "evasion_id": evasion_id,
                    "defense_type": defense_type,
                    "results": result["result"],
                    "success": True
                }
            )
        else:
            self.logger.error(f"Defense evasion analysis failed: {result.get('error')}")
    
    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Get lateral movement agent capabilities."""
        return {
            "agent_type": "red_team_lateral_movement",
            "capabilities": [
                "Network traversal analysis",
                "Privilege escalation simulation",
                "Persistence mechanism analysis",
                "Defense evasion technique analysis",
                "Detection strategy development"
            ],
            "mitre_techniques": [
                "T1021 - Remote Services",
                "T1028 - Windows Remote Management",
                "T1547 - Boot or Logon Autostart Execution",
                "T1574 - Hijack Execution Flow"
            ],
            "tools": [tool.name for tool in self.tools],
            "current_state": {
                "network_traversals_count": len(self.network_traversals),
                "privilege_escalations_count": len(self.privilege_escalations),
                "persistence_mechanisms_count": len(self.persistence_mechanisms),
                "defense_evasions_count": len(self.defense_evasions)
            }
        }
    
    def get_lateral_movement_summary(self) -> Dict[str, Any]:
        """Get comprehensive lateral movement summary."""
        return {
            "agent_id": self.agent_id,
            "summary": {
                "network_traversals": self.network_traversals,
                "privilege_escalations": self.privilege_escalations,
                "persistence_mechanisms": self.persistence_mechanisms,
                "defense_evasions": self.defense_evasions
            },
            "statistics": {
                "total_traversals": len(self.network_traversals),
                "total_escalations": len(self.privilege_escalations),
                "total_persistence": len(self.persistence_mechanisms),
                "total_evasions": len(self.defense_evasions)
            },
            "mitre_techniques_used": list(set([
                data.get("mitre_technique")
                for data in list(self.network_traversals.values()) +
                list(self.privilege_escalations.values()) +
                list(self.persistence_mechanisms.values()) +
                list(self.defense_evasions.values())
                if data.get("mitre_technique")
            ]))
        }
