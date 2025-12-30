"""
Blue Team Threat Intelligence Agent

This agent specializes in attack attribution, TTP mapping to MITRE ATT&CK,
and predictive defense insights for the Australian SOCI Act framework.
"""

import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

from agents.base_agent import BaseAgent, AgentMessage
from config import AgentConfig
from utils.logging_handler import get_agent_logger, get_narrative_logger
from utils.prompt_templates import THREAT_INTEL_AGENT_PROMPT


class ThreatIntelAgent(BaseAgent):
    """
    Blue Team Threat Intelligence Agent
    
    Capabilities:
    - Attack attribution and threat group analysis
    - TTP (Tactics, Techniques, Procedures) mapping
    - Threat landscape analysis and prediction
    - Intelligence report generation
    - Defense strategy recommendations
    
    MITRE ATT&CK Integration:
    - Complete framework mapping and analysis
    - Threat group behavior pattern analysis
    - Emerging technique identification
    - Defensive countermeasure development
    """
    
    def __init__(self, agent_id: str = None):
        """Initialize the threat intelligence agent."""
        agent_id = agent_id or f"threat_intel_agent_{uuid.uuid4().hex[:8]}"
        
        # Initialize with threat intelligence-specific tools
        tools = self._create_threat_intel_tools()
        
        super().__init__(
            agent_id=agent_id,
            agent_type="blue_team_threat_intel",
            system_prompt=THREAT_INTEL_AGENT_PROMPT,
            tools=tools,
            enable_mcp=True
        )
        
        self.logger = get_agent_logger(agent_id, "blue_team_threat_intel")
        self.narrative_logger = get_narrative_logger()
        
        # Threat intelligence state
        self.threat_groups = {}
        self.ttp_mappings = {}
        self.intelligence_reports = {}
        self.threat_predictions = {}
        self.defense_recommendations = {}
        
        self.logger.info(f"Threat Intelligence Agent {agent_id} initialized")
    
    def _create_threat_intel_tools(self) -> List:
        """Create threat intelligence-specific tools."""
        from langchain.tools import BaseTool
        from pydantic import BaseModel, Field
        
        class ThreatAttributionInput(BaseModel):
            attack_indicators: str = Field(description="Attack indicators and artifacts")
            attack_patterns: str = Field(description="Observed attack patterns and behaviors")
            geographic_context: str = Field(description="Geographic or regional context")
        
        class ThreatAttributionTool(BaseTool):
            name = "attribute_threat"
            description = "Attribute attacks to threat groups or actors"
            args_schema = ThreatAttributionInput
            
            def _run(self, attack_indicators: str, attack_patterns: str, geographic_context: str) -> str:
                # Simulate threat attribution
                return f"Simulated threat attribution for indicators: {attack_indicators}, patterns: {attack_patterns}, context: {geographic_context}. Identified potential threat actors, confidence levels, and supporting evidence."
        
        class TTPMappingInput(BaseModel):
            attack_data: str = Field(description="Attack data and techniques observed")
            mapping_granularity: str = Field(description="Mapping granularity (technique, sub-technique, procedure)")
            framework_version: str = Field(description="MITRE ATT&CK framework version")
        
        class TTPMappingTool(BaseTool):
            name = "map_ttp"
            description = "Map attacks to MITRE ATT&CK TTPs"
            args_schema = TTPMappingInput
            
            def _run(self, attack_data: str, mapping_granularity: str, framework_version: str) -> str:
                # Simulate TTP mapping
                return f"Simulated {mapping_granularity} TTP mapping for attack data: {attack_data} using ATT&CK {framework_version}. Mapped techniques, tactics, and procedures with confidence scores."
        
        class ThreatLandscapeInput(BaseModel):
            sector_focus: str = Field(description="Sector or industry focus")
            time_horizon: str = Field(description="Analysis time horizon (current, near-term, long-term)")
            geographic_scope: str = Field(description="Geographic scope of analysis")
        
        class ThreatLandscapeTool(BaseTool):
            name = "analyze_threat_landscape"
            description = "Analyze threat landscape and trends"
            args_schema = ThreatLandscapeInput
            
            def _run(self, sector_focus: str, time_horizon: str, geographic_scope: str) -> str:
                # Simulate threat landscape analysis
                return f"Simulated {time_horizon} threat landscape analysis for {sector_focus} sector in {geographic_scope}. Identified emerging threats, trend patterns, and risk assessments."
        
        class IntelligenceReportInput(BaseModel):
            intelligence_data: str = Field(description="Raw intelligence data and findings")
            report_type: str = Field(description="Type of intelligence report (strategic, tactical, operational)")
            audience: str = Field(description="Target audience for the report")
        
        class IntelligenceReportTool(BaseTool):
            name = "generate_intelligence_report"
            description = "Generate threat intelligence reports"
            args_schema = IntelligenceReportInput
            
            def _run(self, intelligence_data: str, report_type: str, audience: str) -> str:
                # Simulate intelligence report generation
                return f"Simulated {report_type} intelligence report for {audience}. Data: {intelligence_data}. Generated executive summary, technical details, and actionable recommendations."
        
        class DefenseStrategyInput(BaseModel):
            threat_assessment: str = Field(description="Threat assessment and analysis")
            organization_context: str = Field(description="Organization context and constraints")
            priority_level: str = Field(description="Defense priority level (critical, high, medium, low)")
        
        class DefenseStrategyTool(BaseTool):
            name = "recommend_defense_strategy"
            description = "Recommend defense strategies and countermeasures"
            args_schema = DefenseStrategyInput
            
            def _run(self, threat_assessment: str, organization_context: str, priority_level: str) -> str:
                # Simulate defense strategy recommendation
                return f"Simulated {priority_level} defense strategy for threat: {threat_assessment} in context: {organization_context}. Recommended controls, prioritizations, and implementation roadmap."
        
        return [
            ThreatAttributionTool(),
            TTPMappingTool(),
            ThreatLandscapeTool(),
            IntelligenceReportTool(),
            DefenseStrategyTool()
        ]
    
    async def process_command(self, command: Dict[str, Any]) -> None:
        """Process threat intelligence command from coordinator."""
        self.logger.info(f"Processing threat intelligence command: {command}")
        
        command_type = command.get("type", "unknown")
        
        if command_type == "threat_attribution":
            await self._handle_threat_attribution_command(command)
        elif command_type == "ttp_mapping":
            await self._handle_ttp_mapping_command(command)
        elif command_type == "threat_landscape":
            await self._handle_threat_landscape_command(command)
        elif command_type == "intelligence_report":
            await self._handle_intelligence_report_command(command)
        elif command_type == "defense_strategy":
            await self._handle_defense_strategy_command(command)
        else:
            self.logger.warning(f"Unknown command type: {command_type}")
    
    async def _handle_threat_attribution_command(self, command: Dict[str, Any]) -> None:
        """Handle threat attribution command."""
        attack_indicators = command.get("attack_indicators")
        attack_patterns = command.get("attack_patterns")
        geographic_context = command.get("geographic_context", "global")
        attribution_id = command.get("attribution_id", f"attribution_{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting threat attribution: {attribution_id}")
        
        # Execute threat attribution task
        task = f"Attribute threat based on indicators: {attack_indicators}, patterns: {attack_patterns}, context: {geographic_context}"
        result = await self.execute_task(task)
        
        if result["success"]:
            # Store threat attribution data
            self.threat_groups[attribution_id] = {
                "attack_indicators": attack_indicators,
                "attack_patterns": attack_patterns,
                "geographic_context": geographic_context,
                "attribution_results": result["result"],
                "timestamp": datetime.now().isoformat(),
                "confidence_level": "simulated_high",
                "mitre_technique": "threat_attribution"
            }
            
            # Log narrative event
            self.narrative_logger.log_defense_event(
                agent_id=self.agent_id,
                defense_action="threat_attribution",
                detection_type="actor_identification",
                description=f"Threat attribution completed: {attribution_id}",
                mitigated_threat="unknown_threat_actor",
                details={
                    "attribution_id": attribution_id,
                    "geographic_context": geographic_context,
                    "attribution_summary": result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"]
                }
            )
            
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "threat_attribution",
                    "attribution_id": attribution_id,
                    "geographic_context": geographic_context,
                    "results": result["result"],
                    "success": True
                }
            )
        else:
            self.logger.error(f"Threat attribution failed: {result.get('error')}")
    
    async def _handle_ttp_mapping_command(self, command: Dict[str, Any]) -> None:
        """Handle TTP mapping command."""
        attack_data = command.get("attack_data")
        mapping_granularity = command.get("mapping_granularity", "technique")
        framework_version = command.get("framework_version", "v13.1")
        mapping_id = command.get("mapping_id", f"mapping_{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting TTP mapping: {mapping_id}")
        
        # Execute TTP mapping task
        task = f"Map {mapping_granularity} TTPs for attack data: {attack_data} using ATT&CK {framework_version}"
        result = await self.execute_task(task)
        
        if result["success"]:
            # Store TTP mapping data
            self.ttp_mappings[mapping_id] = {
                "attack_data": attack_data,
                "mapping_granularity": mapping_granularity,
                "framework_version": framework_version,
                "ttp_mapping": result["result"],
                "timestamp": datetime.now().isoformat(),
                "coverage_percentage": "simulated_85",
                "mitre_technique": "ttp_analysis"
            }
            
            # Log narrative event
            self.narrative_logger.log_defense_event(
                agent_id=self.agent_id,
                defense_action="ttp_mapping",
                detection_type="technique_analysis",
                description=f"TTP mapping completed: {mapping_id}",
                mitigated_threat="attack_techniques",
                details={
                    "mapping_id": mapping_id,
                    "framework_version": framework_version,
                    "mapping_summary": result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"]
                }
            )
            
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "ttp_mapping",
                    "mapping_id": mapping_id,
                    "framework_version": framework_version,
                    "results": result["result"],
                    "success": True
                }
            )
        else:
            self.logger.error(f"TTP mapping failed: {result.get('error')}")
    
    async def _handle_threat_landscape_command(self, command: Dict[str, Any]) -> None:
        """Handle threat landscape analysis command."""
        sector_focus = command.get("sector_focus", "critical_infrastructure")
        time_horizon = command.get("time_horizon", "near-term")
        geographic_scope = command.get("geographic_scope", "Australia")
        landscape_id = command.get("landscape_id", f"landscape_{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting threat landscape analysis: {landscape_id}")
        
        # Execute threat landscape analysis task
        task = f"Analyze {time_horizon} threat landscape for {sector_focus} sector in {geographic_scope}"
        result = await self.execute_task(task)
        
        if result["success"]:
            # Store threat landscape data
            self.threat_predictions[landscape_id] = {
                "sector_focus": sector_focus,
                "time_horizon": time_horizon,
                "geographic_scope": geographic_scope,
                "landscape_analysis": result["result"],
                "timestamp": datetime.now().isoformat(),
                "risk_level": "simulated_elevated",
                "mitre_technique": "threat_prediction"
            }
            
            # Log narrative event
            self.narrative_logger.log_defense_event(
                agent_id=self.agent_id,
                defense_action="threat_landscape_analysis",
                detection_type="trend_analysis",
                description=f"Threat landscape analysis completed: {landscape_id}",
                mitigated_threat="emerging_threats",
                details={
                    "landscape_id": landscape_id,
                    "sector_focus": sector_focus,
                    "time_horizon": time_horizon,
                    "analysis_summary": result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"]
                }
            )
            
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "threat_landscape",
                    "landscape_id": landscape_id,
                    "sector_focus": sector_focus,
                    "results": result["result"],
                    "success": True
                }
            )
        else:
            self.logger.error(f"Threat landscape analysis failed: {result.get('error')}")
    
    async def _handle_intelligence_report_command(self, command: Dict[str, Any]) -> None:
        """Handle intelligence report generation command."""
        intelligence_data = command.get("intelligence_data")
        report_type = command.get("report_type", "tactical")
        audience = command.get("audience", "security_team")
        report_id = command.get("report_id", f"report_{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting intelligence report generation: {report_id}")
        
        # Execute intelligence report generation task
        task = f"Generate {report_type} intelligence report for {audience} from data: {intelligence_data}"
        result = await self.execute_task(task)
        
        if result["success"]:
            # Store intelligence report data
            self.intelligence_reports[report_id] = {
                "intelligence_data": intelligence_data,
                "report_type": report_type,
                "audience": audience,
                "report_content": result["result"],
                "timestamp": datetime.now().isoformat(),
                "classification": "simulated_internal",
                "mitre_technique": "intelligence_synthesis"
            }
            
            # Log narrative event
            self.narrative_logger.log_defense_event(
                agent_id=self.agent_id,
                defense_action="intelligence_report_generation",
                detection_type="knowledge_synthesis",
                description=f"Intelligence report generated: {report_id}",
                mitigated_threat="intelligence_gaps",
                details={
                    "report_id": report_id,
                    "report_type": report_type,
                    "audience": audience,
                    "report_summary": result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"]
                }
            )
            
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "intelligence_report",
                    "report_id": report_id,
                    "report_type": report_type,
                    "results": result["result"],
                    "success": True
                }
            )
        else:
            self.logger.error(f"Intelligence report generation failed: {result.get('error')}")
    
    async def _handle_defense_strategy_command(self, command: Dict[str, Any]) -> None:
        """Handle defense strategy recommendation command."""
        threat_assessment = command.get("threat_assessment")
        organization_context = command.get("organization_context", "enterprise")
        priority_level = command.get("priority_level", "high")
        strategy_id = command.get("strategy_id", f"strategy_{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting defense strategy recommendation: {strategy_id}")
        
        # Execute defense strategy recommendation task
        task = f"Recommend {priority_level} defense strategy for threat: {threat_assessment} in context: {organization_context}"
        result = await self.execute_task(task)
        
        if result["success"]:
            # Store defense strategy data
            self.defense_recommendations[strategy_id] = {
                "threat_assessment": threat_assessment,
                "organization_context": organization_context,
                "priority_level": priority_level,
                "defense_strategy": result["result"],
                "timestamp": datetime.now().isoformat(),
                "implementation_timeline": "simulated_90_days",
                "mitre_technique": "defense_planning"
            }
            
            # Log narrative event
            self.narrative_logger.log_defense_event(
                agent_id=self.agent_id,
                defense_action="defense_strategy_recommendation",
                detection_type="strategic_planning",
                description=f"Defense strategy recommended: {strategy_id}",
                mitigated_threat=threat_assessment,
                details={
                    "strategy_id": strategy_id,
                    "priority_level": priority_level,
                    "organization_context": organization_context,
                    "strategy_summary": result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"]
                }
            )
            
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "defense_strategy",
                    "strategy_id": strategy_id,
                    "priority_level": priority_level,
                    "results": result["result"],
                    "success": True
                }
            )
        else:
            self.logger.error(f"Defense strategy recommendation failed: {result.get('error')}")
    
    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Get threat intelligence agent capabilities."""
        return {
            "agent_type": "blue_team_threat_intel",
            "capabilities": [
                "Threat attribution and profiling",
                "MITRE ATT&CK TTP mapping",
                "Threat landscape analysis",
                "Intelligence report generation",
                "Defense strategy recommendations"
            ],
            "mitre_techniques": [
                "Complete MITRE ATT&CK framework integration",
                "Threat group behavior pattern analysis",
                "Emerging technique identification",
                "Defensive countermeasure development"
            ],
            "tools": [tool.name for tool in self.tools],
            "current_state": {
                "threat_groups_count": len(self.threat_groups),
                "ttp_mappings_count": len(self.ttp_mappings),
                "intelligence_reports_count": len(self.intelligence_reports),
                "threat_predictions_count": len(self.threat_predictions),
                "defense_recommendations_count": len(self.defense_recommendations)
            }
        }
    
    def get_threat_intelligence_summary(self) -> Dict[str, Any]:
        """Get comprehensive threat intelligence summary."""
        return {
            "agent_id": self.agent_id,
            "summary": {
                "threat_groups": self.threat_groups,
                "ttp_mappings": self.ttp_mappings,
                "intelligence_reports": self.intelligence_reports,
                "threat_predictions": self.threat_predictions,
                "defense_recommendations": self.defense_recommendations
            },
            "statistics": {
                "total_groups": len(self.threat_groups),
                "total_mappings": len(self.ttp_mappings),
                "total_reports": len(self.intelligence_reports),
                "total_predictions": len(self.threat_predictions),
                "total_recommendations": len(self.defense_recommendations)
            },
            "intelligence_capabilities": {
                "attribution_accuracy": "simulated_high",
                "ttp_coverage": "simulated_comprehensive",
                "prediction_confidence": "simulated_moderate",
                "strategic_value": "simulated_high"
            }
        }
