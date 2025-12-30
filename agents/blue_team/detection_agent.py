"""
Blue Team Detection Agent

This agent specializes in anomaly pattern recognition, IOC generation,
and alert correlation for defending against attacks in the Australian SOCI Act framework.
"""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.base_agent import AgentMessage, BaseAgent
from config import AgentConfig
from utils.logging_handler import get_agent_logger, get_narrative_logger
from utils.prompt_templates import DETECTION_AGENT_PROMPT


class DetectionAgent(BaseAgent):
    """
    Blue Team Detection Agent

    Capabilities:
    - Anomaly pattern recognition and analysis
    - IOC (Indicators of Compromise) generation
    - Alert correlation and prioritization
    - Threat behavior pattern matching
    - Detection rule development

    MITRE ATT&CK Detection Focus:
    - TA0001: Initial Access detection
    - TA0002: Execution monitoring
    - TA0003: Persistence identification
    - TA0004: Privilege Escalation detection
    """

    def __init__(self, agent_id: str = None):
        """Initialize the detection agent."""
        agent_id = agent_id or f"detection_agent_{uuid.uuid4().hex[:8]}"

        # Initialize with detection-specific tools
        tools = self._create_detection_tools()

        super().__init__(
            agent_id=agent_id,
            agent_type="blue_team_detection",
            system_prompt=DETECTION_AGENT_PROMPT,
            tools=tools,
            enable_mcp=True,
        )

        self.logger = get_agent_logger(agent_id, "blue_team_detection")
        self.narrative_logger = get_narrative_logger()

        # Detection state
        self.active_alerts = {}
        self.detection_rules = {}
        self.ioc_database = {}
        self.pattern_matches = {}
        self.correlation_rules = {}

        self.logger.info(f"Detection Agent {agent_id} initialized")

    def _create_detection_tools(self) -> List:
        """Create detection-specific tools."""
        from langchain.tools import BaseTool
        from pydantic import BaseModel, Field

        class AnomalyDetectionInput(BaseModel):
            log_data: str = Field(description="Log data or event data to analyze")
            baseline_behavior: str = Field(
                description="Baseline normal behavior description"
            )
            analysis_type: str = Field(
                description="Type of analysis (statistical, behavioral, signature)"
            )

        class AnomalyDetectionTool(BaseTool):
            name = "detect_anomalies"
            description = "Detect anomalies in log or event data"
            args_schema = AnomalyDetectionInput

            def _run(
                self, log_data: str, baseline_behavior: str, analysis_type: str
            ) -> str:
                # Simulate anomaly detection
                return f"Simulated {analysis_type} anomaly detection for log data against baseline: {baseline_behavior}. Identified suspicious patterns, deviations, and potential indicators."

        class IOCGenerationInput(BaseModel):
            attack_data: str = Field(description="Attack data or indicators")
            ioc_type: str = Field(
                description="Type of IOC to generate (network, file, registry, behavioral)"
            )

        class IOCGenerationTool(BaseTool):
            name = "generate_iocs"
            description = "Generate Indicators of Compromise (IOCs)"
            args_schema = IOCGenerationInput

            def _run(self, attack_data: str, ioc_type: str) -> str:
                # Simulate IOC generation
                return f"Simulated {ioc_type} IOC generation from attack data: {attack_data}. Generated observable indicators, signatures, and detection patterns."

        class AlertCorrelationInput(BaseModel):
            alerts: str = Field(description="List of alerts to correlate")
            correlation_method: str = Field(
                description="Correlation method (temporal, causal, pattern)"
            )

        class AlertCorrelationTool(BaseTool):
            name = "correlate_alerts"
            description = "Correlate and prioritize security alerts"
            args_schema = AlertCorrelationInput

            def _run(self, alerts: str, correlation_method: str) -> str:
                # Simulate alert correlation
                return f"Simulated {correlation_method} alert correlation for: {alerts}. Identified relationships, attack chains, and priority levels."

        class DetectionRuleInput(BaseModel):
            threat_pattern: str = Field(
                description="Threat pattern or attack technique"
            )
            rule_type: str = Field(
                description="Type of detection rule (sigma, yara, snort)"
            )
            target_platform: str = Field(description="Target platform or system")

        class DetectionRuleTool(BaseTool):
            name = "create_detection_rule"
            description = "Create detection rules for threats"
            args_schema = DetectionRuleInput

            def _run(
                self, threat_pattern: str, rule_type: str, target_platform: str
            ) -> str:
                # Simulate detection rule creation
                return f"Simulated {rule_type} detection rule for {threat_pattern} on {target_platform}. Generated rule syntax, logic, and deployment guidance."

        return [
            AnomalyDetectionTool(),
            IOCGenerationTool(),
            AlertCorrelationTool(),
            DetectionRuleTool(),
        ]

    async def process_command(self, command: Dict[str, Any]) -> None:
        """Process detection command from coordinator."""
        self.logger.info(f"Processing detection command: {command}")

        command_type = command.get("type", "unknown")

        if command_type == "anomaly_detection":
            await self._handle_anomaly_detection_command(command)
        elif command_type == "ioc_generation":
            await self._handle_ioc_generation_command(command)
        elif command_type == "alert_correlation":
            await self._handle_alert_correlation_command(command)
        elif command_type == "detection_rule":
            await self._handle_detection_rule_command(command)
        else:
            self.logger.warning(f"Unknown command type: {command_type}")

    async def _handle_anomaly_detection_command(self, command: Dict[str, Any]) -> None:
        """Handle anomaly detection command."""
        log_data = command.get("log_data")
        baseline_behavior = command.get("baseline_behavior", "normal operations")
        analysis_type = command.get("analysis_type", "behavioral")
        detection_id = command.get("detection_id", f"detection_{uuid.uuid4().hex[:8]}")

        self.logger.info(f"Starting anomaly detection: {detection_id}")

        # Execute anomaly detection task
        task = f"Perform {analysis_type} anomaly detection on log data against baseline: {baseline_behavior}"
        result = await self.execute_task(task)

        if result["success"]:
            # Store anomaly detection data
            self.pattern_matches[detection_id] = {
                "log_data": log_data,
                "baseline_behavior": baseline_behavior,
                "analysis_type": analysis_type,
                "detection_results": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "TA0001",  # Initial Access detection
            }

            # Log narrative event
            self.narrative_logger.log_defense_event(
                agent_id=self.agent_id,
                defense_action="anomaly_detection",
                detection_type=analysis_type,
                description=f"Anomaly detection completed: {detection_id}",
                mitigated_threat="unknown_anomaly",
                details={
                    "detection_id": detection_id,
                    "analysis_type": analysis_type,
                    "detection_summary": (
                        result["result"][:200] + "..."
                        if len(result["result"]) > 200
                        else result["result"]
                    ),
                },
            )

            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "anomaly_detection",
                    "detection_id": detection_id,
                    "analysis_type": analysis_type,
                    "results": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"Anomaly detection failed: {result.get('error')}")

    async def _handle_ioc_generation_command(self, command: Dict[str, Any]) -> None:
        """Handle IOC generation command."""
        attack_data = command.get("attack_data")
        ioc_type = command.get("ioc_type", "network")
        ioc_id = command.get("ioc_id", f"ioc_{uuid.uuid4().hex[:8]}")

        self.logger.info(f"Starting IOC generation: {ioc_id}")

        # Execute IOC generation task
        task = f"Generate {ioc_type} IOCs from attack data: {attack_data}"
        result = await self.execute_task(task)

        if result["success"]:
            # Store IOC data
            self.ioc_database[ioc_id] = {
                "attack_data": attack_data,
                "ioc_type": ioc_type,
                "generated_iocs": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "TA0002",  # Execution monitoring
            }

            # Log narrative event
            self.narrative_logger.log_defense_event(
                agent_id=self.agent_id,
                defense_action="ioc_generation",
                detection_type="indicator_analysis",
                description=f"IOC generation completed: {ioc_id}",
                mitigated_threat="attack_indicators",
                details={
                    "ioc_id": ioc_id,
                    "ioc_type": ioc_type,
                    "ioc_summary": (
                        result["result"][:200] + "..."
                        if len(result["result"]) > 200
                        else result["result"]
                    ),
                },
            )

            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "ioc_generation",
                    "ioc_id": ioc_id,
                    "ioc_type": ioc_type,
                    "results": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"IOC generation failed: {result.get('error')}")

    async def _handle_alert_correlation_command(self, command: Dict[str, Any]) -> None:
        """Handle alert correlation command."""
        alerts = command.get("alerts")
        correlation_method = command.get("correlation_method", "temporal")
        correlation_id = command.get(
            "correlation_id", f"correlation_{uuid.uuid4().hex[:8]}"
        )

        self.logger.info(f"Starting alert correlation: {correlation_id}")

        # Execute alert correlation task
        task = f"Perform {correlation_method} alert correlation for alerts: {alerts}"
        result = await self.execute_task(task)

        if result["success"]:
            # Store alert correlation data
            self.correlation_rules[correlation_id] = {
                "alerts": alerts,
                "correlation_method": correlation_method,
                "correlation_results": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "TA0003",  # Persistence identification
            }

            # Log narrative event
            self.narrative_logger.log_defense_event(
                agent_id=self.agent_id,
                defense_action="alert_correlation",
                detection_type="pattern_analysis",
                description=f"Alert correlation completed: {correlation_id}",
                mitigated_threat="coordinated_attack",
                details={
                    "correlation_id": correlation_id,
                    "correlation_method": correlation_method,
                    "correlation_summary": (
                        result["result"][:200] + "..."
                        if len(result["result"]) > 200
                        else result["result"]
                    ),
                },
            )

            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "alert_correlation",
                    "correlation_id": correlation_id,
                    "correlation_method": correlation_method,
                    "results": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"Alert correlation failed: {result.get('error')}")

    async def _handle_detection_rule_command(self, command: Dict[str, Any]) -> None:
        """Handle detection rule creation command."""
        threat_pattern = command.get("threat_pattern")
        rule_type = command.get("rule_type", "sigma")
        target_platform = command.get("target_platform", "windows")
        rule_id = command.get("rule_id", f"rule_{uuid.uuid4().hex[:8]}")

        self.logger.info(f"Starting detection rule creation: {rule_id}")

        # Execute detection rule creation task
        task = f"Create {rule_type} detection rule for {threat_pattern} on {target_platform}"
        result = await self.execute_task(task)

        if result["success"]:
            # Store detection rule data
            self.detection_rules[rule_id] = {
                "threat_pattern": threat_pattern,
                "rule_type": rule_type,
                "target_platform": target_platform,
                "detection_rule": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "TA0004",  # Privilege Escalation detection
            }

            # Log narrative event
            self.narrative_logger.log_defense_event(
                agent_id=self.agent_id,
                defense_action="detection_rule_creation",
                detection_type="rule_development",
                description=f"Detection rule created: {rule_id}",
                mitigated_threat=threat_pattern,
                details={
                    "rule_id": rule_id,
                    "threat_pattern": threat_pattern,
                    "rule_type": rule_type,
                    "rule_summary": (
                        result["result"][:200] + "..."
                        if len(result["result"]) > 200
                        else result["result"]
                    ),
                },
            )

            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "detection_rule",
                    "rule_id": rule_id,
                    "threat_pattern": threat_pattern,
                    "results": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"Detection rule creation failed: {result.get('error')}")

    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Get detection agent capabilities."""
        return {
            "agent_type": "blue_team_detection",
            "capabilities": [
                "Anomaly pattern recognition",
                "IOC generation and analysis",
                "Alert correlation and prioritization",
                "Threat behavior pattern matching",
                "Detection rule development",
            ],
            "mitre_techniques": [
                "TA0001 - Initial Access detection",
                "TA0002 - Execution monitoring",
                "TA0003 - Persistence identification",
                "TA0004 - Privilege Escalation detection",
            ],
            "tools": [tool.name for tool in self.tools],
            "current_state": {
                "active_alerts_count": len(self.active_alerts),
                "detection_rules_count": len(self.detection_rules),
                "ioc_database_count": len(self.ioc_database),
                "pattern_matches_count": len(self.pattern_matches),
                "correlation_rules_count": len(self.correlation_rules),
            },
        }

    def get_detection_summary(self) -> Dict[str, Any]:
        """Get comprehensive detection summary."""
        return {
            "agent_id": self.agent_id,
            "summary": {
                "active_alerts": self.active_alerts,
                "detection_rules": self.detection_rules,
                "ioc_database": self.ioc_database,
                "pattern_matches": self.pattern_matches,
                "correlation_rules": self.correlation_rules,
            },
            "statistics": {
                "total_alerts": len(self.active_alerts),
                "total_rules": len(self.detection_rules),
                "total_iocs": len(self.ioc_database),
                "total_patterns": len(self.pattern_matches),
                "total_correlations": len(self.correlation_rules),
            },
            "mitre_techniques_covered": list(
                set(
                    [
                        data.get("mitre_technique")
                        for data in list(self.pattern_matches.values())
                        + list(self.ioc_database.values())
                        + list(self.correlation_rules.values())
                        + list(self.detection_rules.values())
                        if data.get("mitre_technique")
                    ]
                )
            ),
        }
