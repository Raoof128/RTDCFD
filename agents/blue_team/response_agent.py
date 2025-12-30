"""
Blue Team Response Agent

This agent specializes in incident triage, containment strategies,
and remediation procedures for defending against attacks in the Australian SOCI Act framework.
"""

import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

from agents.base_agent import BaseAgent, AgentMessage
from config import AgentConfig
from utils.logging_handler import get_agent_logger, get_narrative_logger
from utils.prompt_templates import RESPONSE_AGENT_PROMPT


class ResponseAgent(BaseAgent):
    """
    Blue Team Response Agent
    
    Capabilities:
    - Incident triage and prioritization
    - Containment strategy development
    - Remediation procedure guidance
    - Incident coordination and communication
    - Post-incident analysis and reporting
    
    MITRE ATT&CK Response Focus:
    - All tactic areas for comprehensive response
    - Focus on containment and eradication
    - Recovery and restoration procedures
    - Lessons learned and improvement
    """
    
    def __init__(self, agent_id: str = None):
        """Initialize the response agent."""
        agent_id = agent_id or f"response_agent_{uuid.uuid4().hex[:8]}"
        
        # Initialize with response-specific tools
        tools = self._create_response_tools()
        
        super().__init__(
            agent_id=agent_id,
            agent_type="blue_team_response",
            system_prompt=RESPONSE_AGENT_PROMPT,
            tools=tools,
            enable_mcp=True
        )
        
        self.logger = get_agent_logger(agent_id, "blue_team_response")
        self.narrative_logger = get_narrative_logger()
        
        # Response state
        self.active_incidents = {}
        self.containment_strategies = {}
        self.remediation_procedures = {}
        self.communication_plans = {}
        self.lessons_learned = {}
        
        self.logger.info(f"Response Agent {agent_id} initialized")
    
    def _create_response_tools(self) -> List:
        """Create response-specific tools."""
        from langchain.tools import BaseTool
        from pydantic import BaseModel, Field
        
        class IncidentTriageInput(BaseModel):
            incident_data: str = Field(description="Incident data and indicators")
            severity_factors: str = Field(description="Factors affecting severity assessment")
            business_impact: str = Field(description="Business impact considerations")
        
        class IncidentTriageTool(BaseTool):
            name = "triage_incident"
            description = "Perform incident triage and prioritization"
            args_schema = IncidentTriageInput
            
            def _run(self, incident_data: str, severity_factors: str, business_impact: str) -> str:
                # Simulate incident triage
                return f"Simulated incident triage for data: {incident_data}. Assessed severity: {severity_factors}, business impact: {business_impact}. Generated priority level and response requirements."
        
        class ContainmentStrategyInput(BaseModel):
            threat_vector: str = Field(description="Threat vector or attack method")
            affected_systems: str = Field(description="Affected systems or assets")
            containment_level: str = Field(description="Level of containment (isolated, segmented, network-wide)")
        
        class ContainmentStrategyTool(BaseTool):
            name = "develop_containment_strategy"
            description = "Develop containment strategies for incidents"
            args_schema = ContainmentStrategyInput
            
            def _run(self, threat_vector: str, affected_systems: str, containment_level: str) -> str:
                # Simulate containment strategy development
                return f"Simulated {containment_level} containment strategy for {threat_vector} affecting {affected_systems}. Includes immediate actions, isolation procedures, and monitoring requirements."
        
        class RemediationProcedureInput(BaseModel):
            incident_type: str = Field(description="Type of security incident")
            compromised_assets: str = Field(description="Compromised assets or systems")
            recovery_priority: str = Field(description="Recovery priority (critical, high, medium, low)")
        
        class RemediationProcedureTool(BaseTool):
            name = "guide_remediation"
            description = "Guide remediation procedures"
            args_schema = RemediationProcedureInput
            
            def _run(self, incident_type: str, compromised_assets: str, recovery_priority: str) -> str:
                # Simulate remediation guidance
                return f"Simulated {recovery_priority} remediation guidance for {incident_type} affecting {compromised_assets}. Includes recovery steps, validation procedures, and restoration timeline."
        
        class CommunicationPlanInput(BaseModel):
            incident_severity: str = Field(description="Incident severity level")
            stakeholders: str = Field(description="Stakeholders to notify")
            communication_requirements: str = Field(description="Communication requirements and constraints")
        
        class CommunicationPlanTool(BaseTool):
            name = "create_communication_plan"
            description = "Create incident communication plans"
            args_schema = CommunicationPlanInput
            
            def _run(self, incident_severity: str, stakeholders: str, communication_requirements: str) -> str:
                # Simulate communication plan creation
                return f"Simulated communication plan for {incident_severity} incident. Stakeholders: {stakeholders}, requirements: {communication_requirements}. Includes notification timeline, messaging templates, and reporting procedures."
        
        return [
            IncidentTriageTool(),
            ContainmentStrategyTool(),
            RemediationProcedureTool(),
            CommunicationPlanTool()
        ]
    
    async def process_command(self, command: Dict[str, Any]) -> None:
        """Process response command from coordinator."""
        self.logger.info(f"Processing response command: {command}")
        
        command_type = command.get("type", "unknown")
        
        if command_type == "incident_triage":
            await self._handle_incident_triage_command(command)
        elif command_type == "containment_strategy":
            await self._handle_containment_strategy_command(command)
        elif command_type == "remediation_procedure":
            await self._handle_remediation_procedure_command(command)
        elif command_type == "communication_plan":
            await self._handle_communication_plan_command(command)
        else:
            self.logger.warning(f"Unknown command type: {command_type}")
    
    async def _handle_incident_triage_command(self, command: Dict[str, Any]) -> None:
        """Handle incident triage command."""
        incident_data = command.get("incident_data")
        severity_factors = command.get("severity_factors", "standard")
        business_impact = command.get("business_impact", "medium")
        triage_id = command.get("triage_id", f"triage_{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting incident triage: {triage_id}")
        
        # Execute incident triage task
        task = f"Perform incident triage for data: {incident_data} with severity factors: {severity_factors} and business impact: {business_impact}"
        result = await self.execute_task(task)
        
        if result["success"]:
            # Store incident triage data
            self.active_incidents[triage_id] = {
                "incident_data": incident_data,
                "severity_factors": severity_factors,
                "business_impact": business_impact,
                "triage_results": result["result"],
                "timestamp": datetime.now().isoformat(),
                "status": "triaged",
                "mitre_technique": "comprehensive_response"
            }
            
            # Log narrative event
            self.narrative_logger.log_defense_event(
                agent_id=self.agent_id,
                defense_action="incident_triage",
                detection_type="severity_assessment",
                description=f"Incident triage completed: {triage_id}",
                mitigated_threat="security_incident",
                details={
                    "triage_id": triage_id,
                    "severity_factors": severity_factors,
                    "business_impact": business_impact,
                    "triage_summary": result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"]
                }
            )
            
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "incident_triage",
                    "triage_id": triage_id,
                    "severity_factors": severity_factors,
                    "results": result["result"],
                    "success": True
                }
            )
        else:
            self.logger.error(f"Incident triage failed: {result.get('error')}")
    
    async def _handle_containment_strategy_command(self, command: Dict[str, Any]) -> None:
        """Handle containment strategy command."""
        threat_vector = command.get("threat_vector")
        affected_systems = command.get("affected_systems")
        containment_level = command.get("containment_level", "segmented")
        strategy_id = command.get("strategy_id", f"strategy_{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting containment strategy development: {strategy_id}")
        
        # Execute containment strategy task
        task = f"Develop {containment_level} containment strategy for {threat_vector} affecting {affected_systems}"
        result = await self.execute_task(task)
        
        if result["success"]:
            # Store containment strategy data
            self.containment_strategies[strategy_id] = {
                "threat_vector": threat_vector,
                "affected_systems": affected_systems,
                "containment_level": containment_level,
                "strategy": result["result"],
                "timestamp": datetime.now().isoformat(),
                "status": "developed",
                "mitre_technique": "containment_response"
            }
            
            # Log narrative event
            self.narrative_logger.log_defense_event(
                agent_id=self.agent_id,
                defense_action="containment_strategy",
                detection_type="isolation_planning",
                description=f"Containment strategy developed: {strategy_id}",
                mitigated_threat=threat_vector,
                details={
                    "strategy_id": strategy_id,
                    "threat_vector": threat_vector,
                    "containment_level": containment_level,
                    "strategy_summary": result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"]
                }
            )
            
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "containment_strategy",
                    "strategy_id": strategy_id,
                    "threat_vector": threat_vector,
                    "results": result["result"],
                    "success": True
                }
            )
        else:
            self.logger.error(f"Containment strategy development failed: {result.get('error')}")
    
    async def _handle_remediation_procedure_command(self, command: Dict[str, Any]) -> None:
        """Handle remediation procedure command."""
        incident_type = command.get("incident_type")
        compromised_assets = command.get("compromised_assets")
        recovery_priority = command.get("recovery_priority", "high")
        remediation_id = command.get("remediation_id", f"remediation_{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting remediation procedure guidance: {remediation_id}")
        
        # Execute remediation procedure task
        task = f"Guide {recovery_priority} remediation for {incident_type} affecting {compromised_assets}"
        result = await self.execute_task(task)
        
        if result["success"]:
            # Store remediation procedure data
            self.remediation_procedures[remediation_id] = {
                "incident_type": incident_type,
                "compromised_assets": compromised_assets,
                "recovery_priority": recovery_priority,
                "procedure": result["result"],
                "timestamp": datetime.now().isoformat(),
                "status": "developed",
                "mitre_technique": "remediation_response"
            }
            
            # Log narrative event
            self.narrative_logger.log_defense_event(
                agent_id=self.agent_id,
                defense_action="remediation_procedure",
                detection_type="recovery_planning",
                description=f"Remediation procedure developed: {remediation_id}",
                mitigated_threat=incident_type,
                details={
                    "remediation_id": remediation_id,
                    "incident_type": incident_type,
                    "recovery_priority": recovery_priority,
                    "procedure_summary": result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"]
                }
            )
            
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "remediation_procedure",
                    "remediation_id": remediation_id,
                    "incident_type": incident_type,
                    "results": result["result"],
                    "success": True
                }
            )
        else:
            self.logger.error(f"Remediation procedure guidance failed: {result.get('error')}")
    
    async def _handle_communication_plan_command(self, command: Dict[str, Any]) -> None:
        """Handle communication plan command."""
        incident_severity = command.get("incident_severity")
        stakeholders = command.get("stakeholders")
        communication_requirements = command.get("communication_requirements", "standard")
        plan_id = command.get("plan_id", f"plan_{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting communication plan creation: {plan_id}")
        
        # Execute communication plan task
        task = f"Create communication plan for {incident_severity} incident with stakeholders: {stakeholders} and requirements: {communication_requirements}"
        result = await self.execute_task(task)
        
        if result["success"]:
            # Store communication plan data
            self.communication_plans[plan_id] = {
                "incident_severity": incident_severity,
                "stakeholders": stakeholders,
                "communication_requirements": communication_requirements,
                "communication_plan": result["result"],
                "timestamp": datetime.now().isoformat(),
                "status": "developed",
                "mitre_technique": "communication_response"
            }
            
            # Log narrative event
            self.narrative_logger.log_defense_event(
                agent_id=self.agent_id,
                defense_action="communication_plan",
                detection_type="stakeholder_coordination",
                description=f"Communication plan created: {plan_id}",
                mitigated_threat="communication_gaps",
                details={
                    "plan_id": plan_id,
                    "incident_severity": incident_severity,
                    "stakeholders": stakeholders,
                    "plan_summary": result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"]
                }
            )
            
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "communication_plan",
                    "plan_id": plan_id,
                    "incident_severity": incident_severity,
                    "results": result["result"],
                    "success": True
                }
            )
        else:
            self.logger.error(f"Communication plan creation failed: {result.get('error')}")
    
    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Get response agent capabilities."""
        return {
            "agent_type": "blue_team_response",
            "capabilities": [
                "Incident triage and prioritization",
                "Containment strategy development",
                "Remediation procedure guidance",
                "Incident coordination and communication",
                "Post-incident analysis and reporting"
            ],
            "mitre_techniques": [
                "Comprehensive response across all MITRE ATT&CK tactics",
                "Containment and eradication procedures",
                "Recovery and restoration processes",
                "Lessons learned and improvement cycles"
            ],
            "tools": [tool.name for tool in self.tools],
            "current_state": {
                "active_incidents_count": len(self.active_incidents),
                "containment_strategies_count": len(self.containment_strategies),
                "remediation_procedures_count": len(self.remediation_procedures),
                "communication_plans_count": len(self.communication_plans),
                "lessons_learned_count": len(self.lessons_learned)
            }
        }
    
    def get_response_summary(self) -> Dict[str, Any]:
        """Get comprehensive response summary."""
        return {
            "agent_id": self.agent_id,
            "summary": {
                "active_incidents": self.active_incidents,
                "containment_strategies": self.containment_strategies,
                "remediation_procedures": self.remediation_procedures,
                "communication_plans": self.communication_plans,
                "lessons_learned": self.lessons_learned
            },
            "statistics": {
                "total_incidents": len(self.active_incidents),
                "total_strategies": len(self.containment_strategies),
                "total_procedures": len(self.remediation_procedures),
                "total_plans": len(self.communication_plans),
                "total_lessons": len(self.lessons_learned)
            },
            "response_capabilities": {
                "triage_accuracy": "simulated_high",
                "containment_effectiveness": "simulated_robust",
                "remediation_completeness": "simulated_comprehensive",
                "communication_clarity": "simulated_clear"
            }
        }
