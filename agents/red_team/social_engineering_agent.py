"""
Red Team Social Engineering Agent

This agent specializes in phishing content generation, pretexting scenarios,
and trust exploitation patterns for security testing under the Australian SOCI Act framework.
"""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.base_agent import AgentMessage, BaseAgent
from config import AgentConfig
from utils.logging_handler import get_agent_logger, get_narrative_logger
from utils.prompt_templates import SOCIAL_ENGINEERING_AGENT_PROMPT


class SocialEngineeringAgent(BaseAgent):
    """
    Red Team Social Engineering Agent

    Capabilities:
    - Phishing content generation (simulation only)
    - Pretexting scenario development
    - Trust exploitation pattern analysis
    - Human behavior manipulation tactics
    - Social engineering campaign planning

    MITRE ATT&CK Techniques:
    - T1566: Phishing
    - T1598: Phishing for Information
    - T1657: Financial Theft
    - T1656: Impersonation
    """

    def __init__(self, agent_id: str = None):
        """Initialize the social engineering agent."""
        agent_id = agent_id or f"social_engineering_agent_{uuid.uuid4().hex[:8]}"

        # Initialize with social engineering-specific tools
        tools = self._create_social_engineering_tools()

        super().__init__(
            agent_id=agent_id,
            agent_type="red_team_social_engineering",
            system_prompt=SOCIAL_ENGINEERING_AGENT_PROMPT,
            tools=tools,
            enable_mcp=True,
        )

        self.logger = get_agent_logger(agent_id, "red_team_social_engineering")
        self.narrative_logger = get_narrative_logger()

        # Social engineering state
        self.phishing_campaigns = {}
        self.pretexting_scenarios = {}
        self.target_profiles = {}
        self.psychological_tactics = {}

        self.logger.info(f"Social Engineering Agent {agent_id} initialized")

    def _create_social_engineering_tools(self) -> List:
        """Create social engineering-specific tools."""
        from langchain.tools import BaseTool
        from pydantic import BaseModel, Field

        class PhishingContentInput(BaseModel):
            target_role: str = Field(description="Target role or department")
            scenario_type: str = Field(
                description="Type of phishing scenario (credential, financial, malware)"
            )
            urgency_level: str = Field(description="Urgency level (low, medium, high)")

        class PhishingContentTool(BaseTool):
            name = "generate_phishing_content"
            description = "Generate simulated phishing content for security testing"
            args_schema = PhishingContentInput

            def _run(
                self, target_role: str, scenario_type: str, urgency_level: str
            ) -> str:
                # Simulate phishing content generation
                return f"Simulated phishing content for {target_role} - {scenario_type} scenario with {urgency_level} urgency. Includes email template, psychological tactics, and detection indicators."

        class PretextingInput(BaseModel):
            target_person: str = Field(description="Target person or role")
            pretext_type: str = Field(
                description="Type of pretext (IT support, executive, vendor)"
            )
            objective: str = Field(description="Objective of the pretext")

        class PretextingTool(BaseTool):
            name = "develop_pretext"
            description = "Develop pretexting scenarios for security testing"
            args_schema = PretextingInput

            def _run(
                self, target_person: str, pretext_type: str, objective: str
            ) -> str:
                # Simulate pretexting scenario development
                return f"Simulated pretexting scenario for {target_person} using {pretext_type} pretext to achieve {objective}. Includes dialogue, props, and backup story."

        class TargetProfilingInput(BaseModel):
            target_info: str = Field(description="Information about the target")
            profiling_depth: str = Field(
                description="Depth of profiling (basic, detailed, comprehensive)"
            )

        class TargetProfilingTool(BaseTool):
            name = "profile_target"
            description = "Create psychological profiles for social engineering targets"
            args_schema = TargetProfilingInput

            def _run(self, target_info: str, profiling_depth: str) -> str:
                # Simulate target profiling
                return f"Simulated {profiling_depth} psychological profile for target based on: {target_info}. Includes behavioral patterns, motivations, and vulnerabilities."

        class TacticAnalysisInput(BaseModel):
            tactic_type: str = Field(description="Type of psychological tactic")
            context: str = Field(description="Context or scenario for the tactic")

        class TacticAnalysisTool(BaseTool):
            name = "analyze_tactic"
            description = "Analyze psychological manipulation tactics"
            args_schema = TacticAnalysisInput

            def _run(self, tactic_type: str, context: str) -> str:
                # Simulate tactic analysis
                return f"Simulated analysis of {tactic_type} psychological tactic in context: {context}. Includes effectiveness, detection indicators, and countermeasures."

        return [
            PhishingContentTool(),
            PretextingTool(),
            TargetProfilingTool(),
            TacticAnalysisTool(),
        ]

    async def process_command(self, command: Dict[str, Any]) -> None:
        """Process social engineering command from coordinator."""
        self.logger.info(f"Processing social engineering command: {command}")

        command_type = command.get("type", "unknown")

        if command_type == "phishing_campaign":
            await self._handle_phishing_campaign_command(command)
        elif command_type == "pretexting_scenario":
            await self._handle_pretexting_scenario_command(command)
        elif command_type == "target_profiling":
            await self._handle_target_profiling_command(command)
        elif command_type == "tactic_analysis":
            await self._handle_tactic_analysis_command(command)
        else:
            self.logger.warning(f"Unknown command type: {command_type}")

    async def _handle_phishing_campaign_command(self, command: Dict[str, Any]) -> None:
        """Handle phishing campaign command."""
        target_role = command.get("target_role")
        scenario_type = command.get("scenario_type", "credential")
        urgency_level = command.get("urgency_level", "medium")
        campaign_id = command.get("campaign_id", f"campaign_{uuid.uuid4().hex[:8]}")

        self.logger.info(f"Starting phishing campaign development: {campaign_id}")

        # Execute phishing content generation task
        task = f"Generate phishing content for {target_role} targeting {scenario_type} with {urgency_level} urgency"
        result = await self.execute_task(task)

        if result["success"]:
            # Store phishing campaign data
            self.phishing_campaigns[campaign_id] = {
                "target_role": target_role,
                "scenario_type": scenario_type,
                "urgency_level": urgency_level,
                "content": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "T1566",  # Phishing
            }

            # Log narrative event
            self.narrative_logger.log_attack_event(
                agent_id=self.agent_id,
                attack_stage="initial_access",
                mitre_technique="T1566",
                description=f"Phishing campaign developed: {campaign_id}",
                target=target_role,
                success=True,
                details={
                    "campaign_id": campaign_id,
                    "scenario_type": scenario_type,
                    "urgency_level": urgency_level,
                    "content_summary": (
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
                    "command_type": "phishing_campaign",
                    "campaign_id": campaign_id,
                    "target_role": target_role,
                    "results": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(
                f"Phishing campaign development failed: {result.get('error')}"
            )

    async def _handle_pretexting_scenario_command(
        self, command: Dict[str, Any]
    ) -> None:
        """Handle pretexting scenario command."""
        target_person = command.get("target_person")
        pretext_type = command.get("pretext_type", "IT support")
        objective = command.get("objective", "information gathering")
        scenario_id = command.get("scenario_id", f"pretext_{uuid.uuid4().hex[:8]}")

        self.logger.info(f"Starting pretexting scenario development: {scenario_id}")

        # Execute pretexting development task
        task = f"Develop {pretext_type} pretexting scenario targeting {target_person} to achieve {objective}"
        result = await self.execute_task(task)

        if result["success"]:
            # Store pretexting scenario data
            self.pretexting_scenarios[scenario_id] = {
                "target_person": target_person,
                "pretext_type": pretext_type,
                "objective": objective,
                "scenario": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "T1656",  # Impersonation
            }

            # Log narrative event
            self.narrative_logger.log_attack_event(
                agent_id=self.agent_id,
                attack_stage="initial_access",
                mitre_technique="T1656",
                description=f"Pretexting scenario developed: {scenario_id}",
                target=target_person,
                success=True,
                details={
                    "scenario_id": scenario_id,
                    "pretext_type": pretext_type,
                    "objective": objective,
                    "scenario_summary": (
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
                    "command_type": "pretexting_scenario",
                    "scenario_id": scenario_id,
                    "target_person": target_person,
                    "results": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(
                f"Pretexting scenario development failed: {result.get('error')}"
            )

    async def _handle_target_profiling_command(self, command: Dict[str, Any]) -> None:
        """Handle target profiling command."""
        target_info = command.get("target_info")
        profiling_depth = command.get("profiling_depth", "basic")
        profile_id = command.get("profile_id", f"profile_{uuid.uuid4().hex[:8]}")

        self.logger.info(f"Starting target profiling: {profile_id}")

        # Execute target profiling task
        task = (
            f"Create {profiling_depth} psychological profile for target: {target_info}"
        )
        result = await self.execute_task(task)

        if result["success"]:
            # Store target profile data
            self.target_profiles[profile_id] = {
                "target_info": target_info,
                "profiling_depth": profiling_depth,
                "profile": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "T1598",  # Phishing for Information
            }

            # Log narrative event
            self.narrative_logger.log_attack_event(
                agent_id=self.agent_id,
                attack_stage="reconnaissance",
                mitre_technique="T1598",
                description=f"Target profile created: {profile_id}",
                target="target_profiling",
                success=True,
                details={
                    "profile_id": profile_id,
                    "profiling_depth": profiling_depth,
                    "profile_summary": (
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
                    "command_type": "target_profiling",
                    "profile_id": profile_id,
                    "profiling_depth": profiling_depth,
                    "results": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"Target profiling failed: {result.get('error')}")

    async def _handle_tactic_analysis_command(self, command: Dict[str, Any]) -> None:
        """Handle tactic analysis command."""
        tactic_type = command.get("tactic_type")
        context = command.get("context", "general")
        analysis_id = command.get("analysis_id", f"analysis_{uuid.uuid4().hex[:8]}")

        self.logger.info(f"Starting tactic analysis: {analysis_id}")

        # Execute tactic analysis task
        task = f"Analyze {tactic_type} psychological manipulation tactic in context: {context}"
        result = await self.execute_task(task)

        if result["success"]:
            # Store tactic analysis data
            self.psychological_tactics[analysis_id] = {
                "tactic_type": tactic_type,
                "context": context,
                "analysis": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "T1566",  # Phishing (primary)
            }

            # Log narrative event
            self.narrative_logger.log_attack_event(
                agent_id=self.agent_id,
                attack_stage="pre_attack",
                mitre_technique="T1566",
                description=f"Tactic analysis completed: {analysis_id}",
                target="tactic_analysis",
                success=True,
                details={
                    "analysis_id": analysis_id,
                    "tactic_type": tactic_type,
                    "context": context,
                    "analysis_summary": (
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
                    "command_type": "tactic_analysis",
                    "analysis_id": analysis_id,
                    "tactic_type": tactic_type,
                    "results": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"Tactic analysis failed: {result.get('error')}")

    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Get social engineering agent capabilities."""
        return {
            "agent_type": "red_team_social_engineering",
            "capabilities": [
                "Phishing content generation",
                "Pretexting scenario development",
                "Target psychological profiling",
                "Manipulation tactic analysis",
                "Social engineering campaign planning",
            ],
            "mitre_techniques": [
                "T1566 - Phishing",
                "T1598 - Phishing for Information",
                "T1657 - Financial Theft",
                "T1656 - Impersonation",
            ],
            "tools": [tool.name for tool in self.tools],
            "current_state": {
                "phishing_campaigns_count": len(self.phishing_campaigns),
                "pretexting_scenarios_count": len(self.pretexting_scenarios),
                "target_profiles_count": len(self.target_profiles),
                "tactic_analyses_count": len(self.psychological_tactics),
            },
        }

    def get_social_engineering_summary(self) -> Dict[str, Any]:
        """Get comprehensive social engineering summary."""
        return {
            "agent_id": self.agent_id,
            "summary": {
                "phishing_campaigns": self.phishing_campaigns,
                "pretexting_scenarios": self.pretexting_scenarios,
                "target_profiles": self.target_profiles,
                "psychological_tactics": self.psychological_tactics,
            },
            "statistics": {
                "total_campaigns": len(self.phishing_campaigns),
                "total_scenarios": len(self.pretexting_scenarios),
                "total_profiles": len(self.target_profiles),
                "total_analyses": len(self.psychological_tactics),
            },
            "mitre_techniques_used": list(
                set(
                    [
                        data.get("mitre_technique")
                        for data in list(self.phishing_campaigns.values())
                        + list(self.pretexting_scenarios.values())
                        + list(self.target_profiles.values())
                        + list(self.psychological_tactics.values())
                        if data.get("mitre_technique")
                    ]
                )
            ),
        }
