"""
Simulation Coordinator for Autonomous Multi-Agent Red/Blue Team System

This module provides the main orchestration logic for coordinating
agents, managing simulation flow, and maintaining attack/defense narratives.
"""

import asyncio
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from agents import (
    BaseAgent,
    DetectionAgent,
    ExploitationAgent,
    LateralMovementAgent,
    ReconAgent,
    ResponseAgent,
    SocialEngineeringAgent,
    ThreatIntelAgent,
)
from config import ScenarioConfig, settings
from mcp_servers import (
    start_blue_team_server,
    start_main_server,
    start_red_team_server,
    stop_all_servers,
)
from utils.logging_handler import get_logger, get_narrative_logger
from utils.prompt_templates import COORDINATOR_PROMPT


class SimulationPhase(Enum):
    """Simulation phases."""

    INITIALIZATION = "initialization"
    RECONNAISSANCE = "reconnaissance"
    INITIAL_ACCESS = "initial_access"
    EXECUTION = "execution"
    PERSISTENCE = "persistence"
    DEFENSE_RESPONSE = "defense_response"
    LATERAL_MOVEMENT = "lateral_movement"
    EXFILTRATION = "exfiltration"
    POST_INCIDENT = "post_incident"
    COMPLETED = "completed"


@dataclass
class SimulationState:
    """Current state of the simulation."""

    simulation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    scenario_name: str = ""
    phase: SimulationPhase = SimulationPhase.INITIALIZATION
    start_time: datetime = field(default_factory=datetime.now)
    current_phase_start: datetime = field(default_factory=datetime.now)
    agents_active: Dict[str, BaseAgent] = field(default_factory=dict)
    red_team_score: int = 0
    blue_team_score: int = 0
    attack_timeline: List[Dict[str, Any]] = field(default_factory=list)
    defense_timeline: List[Dict[str, Any]] = field(default_factory=list)
    critical_assets: Dict[str, Any] = field(default_factory=dict)
    compromised_assets: List[str] = field(default_factory=list)
    detected_attacks: List[str] = field(default_factory=list)
    mitre_techniques_used: List[str] = field(default_factory=list)
    simulation_complete: bool = False


class SimulationCoordinator:
    """
    Main coordinator for the autonomous multi-agent simulation system.

    Responsibilities:
    - Initialize and manage SOCI Act scenarios
    - Coordinate red team agent activities
    - Trigger blue team responses based on attack progression
    - Maintain attack/defense narrative consistency
    - Generate comprehensive simulation reports
    """

    def __init__(self):
        """Initialize the simulation coordinator."""
        self.logger = get_logger(__name__)
        self.narrative_logger = get_narrative_logger()

        # Simulation state
        self.state = SimulationState()

        # Agent instances
        self.red_team_agents = {}
        self.blue_team_agents = {}

        # MCP servers
        self.main_server = None
        self.red_team_server = None
        self.blue_team_server = None

        # Configuration
        self.max_simulation_time = timedelta(minutes=settings.scenario_timeout_minutes)
        self.phase_durations = {
            SimulationPhase.INITIALIZATION: timedelta(minutes=2),
            SimulationPhase.RECONNAISSANCE: timedelta(minutes=10),
            SimulationPhase.INITIAL_ACCESS: timedelta(minutes=8),
            SimulationPhase.EXECUTION: timedelta(minutes=12),
            SimulationPhase.PERSISTENCE: timedelta(minutes=6),
            SimulationPhase.DEFENSE_RESPONSE: timedelta(minutes=10),
            SimulationPhase.LATERAL_MOVEMENT: timedelta(minutes=8),
            SimulationPhase.EXFILTRATION: timedelta(minutes=6),
            SimulationPhase.POST_INCIDENT: timedelta(minutes=5),
        }

        self.logger.info("Simulation Coordinator initialized")

    async def initialize_simulation(self, scenario_name: str) -> None:
        """
        Initialize the simulation with a specific scenario.

        Args:
            scenario_name: Name of the SOCI Act scenario to run
        """
        self.logger.info(f"Initializing simulation for scenario: {scenario_name}")

        # Set scenario
        self.state.scenario_name = scenario_name

        # Load scenario configuration
        scenario_config = await self._load_scenario(scenario_name)

        # Initialize critical assets
        self.state.critical_assets = scenario_config.get("critical_assets", {})

        # Start MCP servers
        await self._start_mcp_servers()

        # Initialize agents
        await self._initialize_agents(scenario_config)

        # Start agent MCP clients
        await self._start_agent_communication()

        # Update state
        self.state.phase = SimulationPhase.INITIALIZATION
        self.state.current_phase_start = datetime.now()

        # Log initialization
        self.narrative_logger.log_scenario_event(
            scenario=scenario_name,
            event_type="simulation_initialized",
            description=f"Simulation initialized for {scenario_name}",
            details={
                "simulation_id": self.state.simulation_id,
                "critical_assets": list(self.state.critical_assets.keys()),
                "agents_initialized": len(self.state.agents_active),
            },
        )

        self.logger.info(f"Simulation initialization completed for {scenario_name}")

    async def _load_scenario(self, scenario_name: str) -> Dict[str, Any]:
        """Load scenario configuration."""
        # For now, return default scenario config
        # In future, this would load from scenario files
        default_scenarios = {
            "soci_energy_grid": {
                "critical_assets": {
                    "scada_system": {
                        "type": "industrial_control",
                        "criticality": "high",
                    },
                    "power_grid_monitoring": {
                        "type": "monitoring",
                        "criticality": "high",
                    },
                    "employee_portal": {
                        "type": "web_application",
                        "criticality": "medium",
                    },
                    "billing_system": {"type": "database", "criticality": "medium"},
                },
                "attack_surface": [
                    "public_web_servers",
                    "remote_access_points",
                    "third_party_integrations",
                    "employee_credentials",
                ],
                "defensive_measures": [
                    "network_segmentation",
                    "intrusion_detection",
                    "security_monitoring",
                    "incident_response_team",
                ],
            },
            "soci_telco_network": {
                "critical_assets": {
                    "core_network_switches": {
                        "type": "network_infrastructure",
                        "criticality": "high",
                    },
                    "customer_database": {"type": "database", "criticality": "high"},
                    "billing_platform": {
                        "type": "application",
                        "criticality": "medium",
                    },
                    "mobile_network_core": {
                        "type": "telecom_infrastructure",
                        "criticality": "high",
                    },
                },
                "attack_surface": [
                    "customer_facing_portals",
                    "network_management_interfaces",
                    "mobile_applications",
                    "partner_connections",
                ],
                "defensive_measures": [
                    "network_monitoring",
                    "access_control",
                    "encryption_protocols",
                    "security_operations_center",
                ],
            },
            "soci_water_system": {
                "critical_assets": {
                    "water_treatment_plant": {
                        "type": "industrial_control",
                        "criticality": "high",
                    },
                    "distribution_system": {
                        "type": "infrastructure",
                        "criticality": "high",
                    },
                    "quality_monitoring": {"type": "monitoring", "criticality": "high"},
                    "customer_billing": {"type": "application", "criticality": "low"},
                },
                "attack_surface": [
                    "remote_telemetry",
                    "control_system_interfaces",
                    "operator_workstations",
                    "maintenance_access",
                ],
                "defensive_measures": [
                    "physical_security",
                    "system_hardening",
                    "monitoring_alerts",
                    "backup_systems",
                ],
            },
        }

        return default_scenarios.get(
            scenario_name, default_scenarios["soci_energy_grid"]
        )

    async def _start_mcp_servers(self) -> None:
        """Start MCP servers for agent communication."""
        self.logger.info("Starting MCP servers...")

        # Start main server
        self.main_server = await start_main_server(
            host=settings.mcp_server_host, port=settings.mcp_server_port
        )

        # Start red team server
        self.red_team_server = await start_red_team_server(
            host=settings.mcp_server_host, port=settings.mcp_red_team_port
        )

        # Start blue team server
        self.blue_team_server = await start_blue_team_server(
            host=settings.mcp_server_host, port=settings.mcp_blue_team_port
        )

        # Give servers time to start
        await asyncio.sleep(2)

        self.logger.info("MCP servers started successfully")

    async def _initialize_agents(self, scenario_config: Dict[str, Any]) -> None:
        """Initialize all agents for the simulation."""
        self.logger.info("Initializing agents...")

        # Initialize red team agents
        self.red_team_agents = {
            "recon": ReconAgent(),
            "social_engineering": SocialEngineeringAgent(),
            "exploitation": ExploitationAgent(),
            "lateral_movement": LateralMovementAgent(),
        }

        # Initialize blue team agents
        self.blue_team_agents = {
            "detection": DetectionAgent(),
            "response": ResponseAgent(),
            "threat_intel": ThreatIntelAgent(),
        }

        # Combine all agents
        all_agents = {**self.red_team_agents, **self.blue_team_agents}
        self.state.agents_active = {
            agent_id: agent for agent_id, agent in all_agents.items()
        }

        self.logger.info(
            f"Initialized {len(self.red_team_agents)} red team and {len(self.blue_team_agents)} blue team agents"
        )

    async def _start_agent_communication(self) -> None:
        """Start MCP client communication for all agents."""
        self.logger.info("Starting agent communication...")

        # Start all agent MCP clients
        for agent_id, agent in self.state.agents_active.items():
            await agent.start_mcp_client()
            self.logger.debug(f"Started MCP client for agent: {agent_id}")

        self.logger.info("Agent communication started")

    async def run_simulation(self, timeout_minutes: int = 60) -> None:
        """
        Run the main simulation loop.

        Args:
            timeout_minutes: Maximum simulation time in minutes
        """
        self.logger.info(
            f"Starting simulation loop with timeout: {timeout_minutes} minutes"
        )

        simulation_end_time = datetime.now() + timedelta(minutes=timeout_minutes)

        # Main simulation loop
        while (
            datetime.now() < simulation_end_time
            and not self.state.simulation_complete
            and self.state.phase != SimulationPhase.COMPLETED
        ):

            try:
                # Execute current phase
                await self._execute_current_phase()

                # Check phase transition
                if await self._should_transition_phase():
                    await self._transition_to_next_phase()

                # Update scores
                self._update_scores()

                # Brief pause between phases
                await asyncio.sleep(1)

            except Exception as e:
                self.logger.error(f"Error in simulation loop: {e}")
                break

        # Complete simulation
        await self._complete_simulation()

        self.logger.info("Simulation loop completed")

    async def _execute_current_phase(self) -> None:
        """Execute the current simulation phase."""
        phase = self.state.phase

        self.logger.info(f"Executing phase: {phase.value}")

        if phase == SimulationPhase.INITIALIZATION:
            await self._execute_initialization_phase()
        elif phase == SimulationPhase.RECONNAISSANCE:
            await self._execute_reconnaissance_phase()
        elif phase == SimulationPhase.INITIAL_ACCESS:
            await self._execute_initial_access_phase()
        elif phase == SimulationPhase.EXECUTION:
            await self._execute_execution_phase()
        elif phase == SimulationPhase.PERSISTENCE:
            await self._execute_persistence_phase()
        elif phase == SimulationPhase.DEFENSE_RESPONSE:
            await self._execute_defense_response_phase()
        elif phase == SimulationPhase.LATERAL_MOVEMENT:
            await self._execute_lateral_movement_phase()
        elif phase == SimulationPhase.EXFILTRATION:
            await self._execute_exfiltration_phase()
        elif phase == SimulationPhase.POST_INCIDENT:
            await self._execute_post_incident_phase()

    async def _execute_initialization_phase(self) -> None:
        """Execute initialization phase."""
        # Send initial setup commands to all agents
        for agent_id, agent in self.state.agents_active.items():
            command = {
                "type": "initialize",
                "scenario": self.state.scenario_name,
                "critical_assets": self.state.critical_assets,
                "simulation_id": self.state.simulation_id,
            }
            await agent.send_message(
                receiver_id=agent_id, message_type="command", content=command
            )

    async def _execute_reconnaissance_phase(self) -> None:
        """Execute reconnaissance phase."""
        # Task recon agent to gather intelligence
        recon_agent = self.red_team_agents.get("recon")
        if recon_agent:
            command = {
                "type": "osint_gathering",
                "target": self.state.scenario_name,
                "information_type": "organization",
            }
            await recon_agent.send_message(
                receiver_id=recon_agent.agent_id,
                message_type="command",
                content=command,
            )

        # Task detection agent to monitor for reconnaissance
        detection_agent = self.blue_team_agents.get("detection")
        if detection_agent:
            command = {
                "type": "anomaly_detection",
                "log_data": "simulated_network_logs",
                "baseline_behavior": "normal_operations",
                "analysis_type": "statistical",
            }
            await detection_agent.send_message(
                receiver_id=detection_agent.agent_id,
                message_type="command",
                content=command,
            )

    async def _execute_initial_access_phase(self) -> None:
        """Execute initial access phase."""
        # Task social engineering agent
        se_agent = self.red_team_agents.get("social_engineering")
        if se_agent:
            command = {
                "type": "phishing_campaign",
                "target_role": "system_administrator",
                "scenario_type": "credential_theft",
                "urgency_level": "high",
            }
            await se_agent.send_message(
                receiver_id=se_agent.agent_id, message_type="command", content=command
            )

        # Task response agent to prepare for incidents
        response_agent = self.blue_team_agents.get("response")
        if response_agent:
            command = {
                "type": "incident_triage",
                "incident_data": "simulated_phishing_alerts",
                "severity_factors": "credential_compromise_risk",
                "business_impact": "critical",
            }
            await response_agent.send_message(
                receiver_id=response_agent.agent_id,
                message_type="command",
                content=command,
            )

    async def _execute_execution_phase(self) -> None:
        """Execute execution phase."""
        # Task exploitation agent
        exploit_agent = self.red_team_agents.get("exploitation")
        if exploit_agent:
            command = {
                "type": "vulnerability_chain",
                "vulnerabilities": "CVE-2023-1234, CVE-2023-5678",
                "target_system": "employee_portal",
                "chain_complexity": "moderate",
            }
            await exploit_agent.send_message(
                receiver_id=exploit_agent.agent_id,
                message_type="command",
                content=command,
            )

        # Task detection agent for active monitoring
        detection_agent = self.blue_team_agents.get("detection")
        if detection_agent:
            command = {
                "type": "alert_correlation",
                "alerts": "simulated_exploitation_alerts",
                "correlation_method": "temporal",
            }
            await detection_agent.send_message(
                receiver_id=detection_agent.agent_id,
                message_type="command",
                content=command,
            )

    async def _execute_persistence_phase(self) -> None:
        """Execute persistence phase."""
        # Task lateral movement agent
        lm_agent = self.red_team_agents.get("lateral_movement")
        if lm_agent:
            command = {
                "type": "persistence_mechanism",
                "mechanism_type": "scheduled_task",
                "target_system": "domain_controller",
                "stealth_level": "high",
            }
            await lm_agent.send_message(
                receiver_id=lm_agent.agent_id, message_type="command", content=command
            )

    async def _execute_defense_response_phase(self) -> None:
        """Execute defense response phase."""
        # Task response agent for containment
        response_agent = self.blue_team_agents.get("response")
        if response_agent:
            command = {
                "type": "containment_strategy",
                "threat_vector": "malware_execution",
                "affected_systems": "employee_portal, domain_controller",
                "containment_level": "segmented",
            }
            await response_agent.send_message(
                receiver_id=response_agent.agent_id,
                message_type="command",
                content=command,
            )

        # Task threat intel agent for analysis
        intel_agent = self.blue_team_agents.get("threat_intel")
        if intel_agent:
            command = {
                "type": "ttp_mapping",
                "attack_data": "simulated_attack_techniques",
                "mapping_granularity": "technique",
                "framework_version": "v13.1",
            }
            await intel_agent.send_message(
                receiver_id=intel_agent.agent_id,
                message_type="command",
                content=command,
            )

    async def _execute_lateral_movement_phase(self) -> None:
        """Execute lateral movement phase."""
        # Task lateral movement agent
        lm_agent = self.red_team_agents.get("lateral_movement")
        if lm_agent:
            command = {
                "type": "network_traversal",
                "starting_point": "employee_portal",
                "target_destination": "scada_system",
                "network_constraints": "network_segmentation",
            }
            await lm_agent.send_message(
                receiver_id=lm_agent.agent_id, message_type="command", content=command
            )

    async def _execute_exfiltration_phase(self) -> None:
        """Execute exfiltration phase."""
        # Task exploitation agent for data exfiltration simulation
        exploit_agent = self.red_team_agents.get("exploitation")
        if exploit_agent:
            command = {
                "type": "control_bypass",
                "security_control": "data_loss_prevention",
                "bypass_method": "encryption_steganography",
                "target_environment": "internal_network",
            }
            await exploit_agent.send_message(
                receiver_id=exploit_agent.agent_id,
                message_type="command",
                content=command,
            )

    async def _execute_post_incident_phase(self) -> None:
        """Execute post-incident phase."""
        # Task response agent for remediation
        response_agent = self.blue_team_agents.get("response")
        if response_agent:
            command = {
                "type": "remediation_procedure",
                "incident_type": "advanced_persistent_threat",
                "compromised_assets": "employee_portal, domain_controller",
                "recovery_priority": "critical",
            }
            await response_agent.send_message(
                receiver_id=response_agent.agent_id,
                message_type="command",
                content=command,
            )

        # Task threat intel for final report
        intel_agent = self.blue_team_agents.get("threat_intel")
        if intel_agent:
            command = {
                "type": "intelligence_report",
                "intelligence_data": "simulated_full_attack_chain",
                "report_type": "strategic",
                "audience": "executive_management",
            }
            await intel_agent.send_message(
                receiver_id=intel_agent.agent_id,
                message_type="command",
                content=command,
            )

    async def _should_transition_phase(self) -> bool:
        """Check if simulation should transition to next phase."""
        current_phase_duration = datetime.now() - self.state.current_phase_start
        max_duration = self.phase_durations.get(self.state.phase, timedelta(minutes=5))

        return current_phase_duration >= max_duration

    async def _transition_to_next_phase(self) -> None:
        """Transition to the next simulation phase."""
        current_phase = self.state.phase

        # Define phase order
        phase_order = [
            SimulationPhase.INITIALIZATION,
            SimulationPhase.RECONNAISSANCE,
            SimulationPhase.INITIAL_ACCESS,
            SimulationPhase.EXECUTION,
            SimulationPhase.PERSISTENCE,
            SimulationPhase.DEFENSE_RESPONSE,
            SimulationPhase.LATERAL_MOVEMENT,
            SimulationPhase.EXFILTRATION,
            SimulationPhase.POST_INCIDENT,
            SimulationPhase.COMPLETED,
        ]

        # Find current phase index
        current_index = phase_order.index(current_phase)

        # Move to next phase
        if current_index < len(phase_order) - 1:
            next_phase = phase_order[current_index + 1]

            self.logger.info(
                f"Transitioning from {current_phase.value} to {next_phase.value}"
            )

            # Update state
            self.state.phase = next_phase
            self.state.current_phase_start = datetime.now()

            # Log phase transition
            self.narrative_logger.log_scenario_event(
                scenario=self.state.scenario_name,
                event_type="phase_transition",
                description=f"Phase transition: {current_phase.value} -> {next_phase.value}",
                details={
                    "previous_phase": current_phase.value,
                    "new_phase": next_phase.value,
                    "simulation_time": str(datetime.now() - self.state.start_time),
                },
            )

    def _update_scores(self) -> None:
        """Update red team and blue team scores."""
        # Simple scoring logic for demonstration
        red_team_progress = len(self.state.attack_timeline)
        blue_team_progress = len(self.state.defense_timeline)

        self.state.red_team_score = red_team_progress * 10
        self.state.blue_team_score = blue_team_progress * 10

    async def _complete_simulation(self) -> None:
        """Complete the simulation and generate final report."""
        self.logger.info("Completing simulation...")

        # Update state
        self.state.simulation_complete = True
        self.state.phase = SimulationPhase.COMPLETED

        # Log completion
        self.narrative_logger.log_scenario_event(
            scenario=self.state.scenario_name,
            event_type="simulation_completed",
            description="Simulation completed successfully",
            details={
                "simulation_id": self.state.simulation_id,
                "total_duration": str(datetime.now() - self.state.start_time),
                "red_team_score": self.state.red_team_score,
                "blue_team_score": self.state.blue_team_score,
                "mitre_techniques_used": self.state.mitre_techniques_used,
            },
        )

        # Generate final report
        await self.generate_report()

    async def generate_report(self) -> str:
        """
        Generate comprehensive simulation report.

        Returns:
            Path to generated report file
        """
        self.logger.info("Generating simulation report...")

        # Compile report data
        report_data = {
            "simulation_id": self.state.simulation_id,
            "scenario_name": self.state.scenario_name,
            "execution_summary": {
                "start_time": self.state.start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "total_duration": str(datetime.now() - self.state.start_time),
                "phases_completed": [
                    phase.value
                    for phase in SimulationPhase
                    if phase != SimulationPhase.COMPLETED
                ],
            },
            "agent_performance": {
                "red_team_agents": {
                    agent_id: agent.get_agent_capabilities()
                    for agent_id, agent in self.red_team_agents.items()
                },
                "blue_team_agents": {
                    agent_id: agent.get_agent_capabilities()
                    for agent_id, agent in self.blue_team_agents.items()
                },
            },
            "attack_timeline": self.state.attack_timeline,
            "defense_timeline": self.state.defense_timeline,
            "scoring": {
                "red_team_score": self.state.red_team_score,
                "blue_team_score": self.state.blue_team_score,
                "winner": (
                    "red_team"
                    if self.state.red_team_score > self.state.blue_team_score
                    else "blue_team"
                ),
            },
            "mitre_techniques": self.state.mitre_techniques_used,
            "critical_assets": {
                "total": len(self.state.critical_assets),
                "compromised": len(self.state.compromised_assets),
                "protected": len(self.state.critical_assets)
                - len(self.state.compromised_assets),
            },
            "detection_effectiveness": {
                "attacks_detected": len(self.state.detected_attacks),
                "total_attacks": len(self.state.attack_timeline),
                "detection_rate": len(self.state.detected_attacks)
                / max(len(self.state.attack_timeline), 1),
            },
        }

        # Generate report file
        from pathlib import Path

        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)

        report_filename = f"simulation_report_{self.state.scenario_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = reports_dir / report_filename

        with open(report_path, "w") as f:
            json.dump(report_data, f, indent=2, default=str)

        self.logger.info(f"Report generated: {report_path}")
        return str(report_path)

    async def cleanup(self) -> None:
        """Clean up simulation resources."""
        self.logger.info("Cleaning up simulation resources...")

        # Stop all agent MCP clients
        for agent_id, agent in self.state.agents_active.items():
            await agent.cleanup()

        # Stop MCP servers
        await stop_all_servers()

        self.logger.info("Simulation cleanup completed")

    def get_simulation_status(self) -> Dict[str, Any]:
        """Get current simulation status."""
        return {
            "simulation_id": self.state.simulation_id,
            "scenario_name": self.state.scenario_name,
            "current_phase": self.state.phase.value,
            "start_time": self.state.start_time.isoformat(),
            "current_phase_start": self.state.current_phase_start.isoformat(),
            "agents_active": len(self.state.agents_active),
            "red_team_score": self.state.red_team_score,
            "blue_team_score": self.state.blue_team_score,
            "simulation_complete": self.state.simulation_complete,
            "attack_timeline_length": len(self.state.attack_timeline),
            "defense_timeline_length": len(self.state.defense_timeline),
        }
