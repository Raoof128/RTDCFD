"""
Red Team Reconnaissance Agent

This agent specializes in OSINT gathering, network mapping, and vulnerability
scanning simulation for security testing under the Australian SOCI Act framework.
"""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.base_agent import AgentMessage, BaseAgent
from config import AgentConfig
from utils.logging_handler import get_agent_logger, get_narrative_logger
from utils.prompt_templates import RECON_AGENT_PROMPT


class ReconAgent(BaseAgent):
    """
    Red Team Reconnaissance Agent

    Capabilities:
    - OSINT gathering simulation
    - Network topology mapping
    - Vulnerability scanning simulation
    - Asset enumeration
    - Attack surface identification

    MITRE ATT&CK Techniques:
    - T1592: Gather Victim Org Information
    - T1595: Active Scanning
    - T1596: Search Open Websites/Domains
    - T1598: Phishing for Information
    """

    def __init__(self, agent_id: str = None):
        """Initialize the reconnaissance agent."""
        agent_id = agent_id or f"recon_agent_{uuid.uuid4().hex[:8]}"

        # Initialize with reconnaissance-specific tools
        tools = self._create_recon_tools()

        super().__init__(
            agent_id=agent_id,
            agent_type="red_team_recon",
            system_prompt=RECON_AGENT_PROMPT,
            tools=tools,
            enable_mcp=True,
        )

        self.logger = get_agent_logger(agent_id, "red_team_recon")
        self.narrative_logger = get_narrative_logger()

        # Reconnaissance state
        self.discovered_assets = {}
        self.network_map = {}
        self.vulnerability_findings = []
        self.osint_data = {}

        self.logger.info(f"Reconnaissance Agent {agent_id} initialized")

    def _create_recon_tools(self) -> List:
        """Create reconnaissance-specific tools."""
        from langchain.tools import BaseTool
        from pydantic import BaseModel, Field

        class OSINTGatherInput(BaseModel):
            query: str = Field(description="OSINT search query or target")
            information_type: str = Field(
                description="Type of information to gather (company, person, technology)"
            )

        class OSINTGatherTool(BaseTool):
            name = "osint_gather"
            description = "Simulate OSINT gathering about targets"
            args_schema = OSINTGatherInput

            def _run(self, query: str, information_type: str) -> str:
                # Simulate OSINT gathering
                return f"Simulated OSINT results for {query} ({information_type}): Found public information, social media profiles, technical details, and organizational structure."

        class NetworkScanInput(BaseModel):
            target_range: str = Field(description="Target network range or hostname")
            scan_type: str = Field(description="Type of scan (port, service, version)")

        class NetworkScanTool(BaseTool):
            name = "network_scan"
            description = "Simulate network scanning to discover assets"
            args_schema = NetworkScanInput

            def _run(self, target_range: str, scan_type: str) -> str:
                # Simulate network scanning
                return f"Simulated {scan_type} scan results for {target_range}: Discovered hosts, open ports, services, and potential vulnerabilities."

        class VulnerabilityScanInput(BaseModel):
            target: str = Field(description="Target system or application")
            scan_level: str = Field(
                description="Scan intensity (light, medium, comprehensive)"
            )

        class VulnerabilityScanTool(BaseTool):
            name = "vulnerability_scan"
            description = "Simulate vulnerability scanning"
            args_schema = VulnerabilityScanInput

            def _run(self, target: str, scan_level: str) -> str:
                # Simulate vulnerability scanning
                return f"Simulated {scan_level} vulnerability scan for {target}: Found potential vulnerabilities, misconfigurations, and security gaps."

        class AssetEnumerationInput(BaseModel):
            domain: str = Field(description="Target domain or organization")
            enumeration_type: str = Field(
                description="Type of enumeration (subdomains, technologies, employees)"
            )

        class AssetEnumerationTool(BaseTool):
            name = "asset_enumeration"
            description = "Simulate asset enumeration"
            args_schema = AssetEnumerationInput

            def _run(self, domain: str, enumeration_type: str) -> str:
                # Simulate asset enumeration
                return f"Simulated {enumeration_type} enumeration for {domain}: Discovered assets, technologies, and potential attack vectors."

        return [
            OSINTGatherTool(),
            NetworkScanTool(),
            VulnerabilityScanTool(),
            AssetEnumerationTool(),
        ]

    async def process_command(self, command: Dict[str, Any]) -> None:
        """Process reconnaissance command from coordinator."""
        self.logger.info(f"Processing recon command: {command}")

        command_type = command.get("type", "unknown")

        if command_type == "osint_gathering":
            await self._handle_osint_command(command)
        elif command_type == "network_mapping":
            await self._handle_network_mapping_command(command)
        elif command_type == "vulnerability_scan":
            await self._handle_vulnerability_scan_command(command)
        elif command_type == "asset_enumeration":
            await self._handle_asset_enumeration_command(command)
        else:
            self.logger.warning(f"Unknown command type: {command_type}")

    async def _handle_osint_command(self, command: Dict[str, Any]) -> None:
        """Handle OSINT gathering command."""
        target = command.get("target")
        information_type = command.get("information_type", "organization")

        self.logger.info(f"Starting OSINT gathering for: {target}")

        # Execute OSINT task
        task = f"Gather OSINT about {target} focusing on {information_type}"
        result = await self.execute_task(task)

        if result["success"]:
            # Store OSINT data
            self.osint_data[target] = {
                "information_type": information_type,
                "data": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "T1592",  # Gather Victim Org Information
            }

            # Log narrative event
            self.narrative_logger.log_attack_event(
                agent_id=self.agent_id,
                attack_stage="reconnaissance",
                mitre_technique="T1592",
                description=f"OSINT gathering completed for {target}",
                target=target,
                success=True,
                details={
                    "information_type": information_type,
                    "findings": result["result"],
                },
            )

            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "osint_gathering",
                    "target": target,
                    "results": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"OSINT gathering failed: {result.get('error')}")

    async def _handle_network_mapping_command(self, command: Dict[str, Any]) -> None:
        """Handle network mapping command."""
        target_range = command.get("target_range")
        scan_type = command.get("scan_type", "port")

        self.logger.info(f"Starting network mapping for: {target_range}")

        # Execute network mapping task
        task = f"Perform {scan_type} scan on {target_range} to map network topology"
        result = await self.execute_task(task)

        if result["success"]:
            # Store network map data
            self.network_map[target_range] = {
                "scan_type": scan_type,
                "data": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "T1595",  # Active Scanning
            }

            # Log narrative event
            self.narrative_logger.log_attack_event(
                agent_id=self.agent_id,
                attack_stage="reconnaissance",
                mitre_technique="T1595",
                description=f"Network mapping completed for {target_range}",
                target=target_range,
                success=True,
                details={"scan_type": scan_type, "findings": result["result"]},
            )

            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "network_mapping",
                    "target_range": target_range,
                    "results": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"Network mapping failed: {result.get('error')}")

    async def _handle_vulnerability_scan_command(self, command: Dict[str, Any]) -> None:
        """Handle vulnerability scanning command."""
        target = command.get("target")
        scan_level = command.get("scan_level", "medium")

        self.logger.info(f"Starting vulnerability scan for: {target}")

        # Execute vulnerability scan task
        task = f"Perform {scan_level} vulnerability scan on {target}"
        result = await self.execute_task(task)

        if result["success"]:
            # Store vulnerability findings
            vulnerability_finding = {
                "target": target,
                "scan_level": scan_level,
                "findings": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "T1595",  # Active Scanning
            }
            self.vulnerability_findings.append(vulnerability_finding)

            # Log narrative event
            self.narrative_logger.log_attack_event(
                agent_id=self.agent_id,
                attack_stage="reconnaissance",
                mitre_technique="T1595",
                description=f"Vulnerability scan completed for {target}",
                target=target,
                success=True,
                details={"scan_level": scan_level, "findings": result["result"]},
            )

            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "vulnerability_scan",
                    "target": target,
                    "results": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"Vulnerability scan failed: {result.get('error')}")

    async def _handle_asset_enumeration_command(self, command: Dict[str, Any]) -> None:
        """Handle asset enumeration command."""
        domain = command.get("domain")
        enumeration_type = command.get("enumeration_type", "subdomains")

        self.logger.info(f"Starting asset enumeration for: {domain}")

        # Execute asset enumeration task
        task = f"Perform {enumeration_type} enumeration for {domain}"
        result = await self.execute_task(task)

        if result["success"]:
            # Store discovered assets
            self.discovered_assets[domain] = {
                "enumeration_type": enumeration_type,
                "assets": result["result"],
                "timestamp": datetime.now().isoformat(),
                "mitre_technique": "T1596",  # Search Open Websites/Domains
            }

            # Log narrative event
            self.narrative_logger.log_attack_event(
                agent_id=self.agent_id,
                attack_stage="reconnaissance",
                mitre_technique="T1596",
                description=f"Asset enumeration completed for {domain}",
                target=domain,
                success=True,
                details={
                    "enumeration_type": enumeration_type,
                    "assets": result["result"],
                },
            )

            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "asset_enumeration",
                    "domain": domain,
                    "results": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"Asset enumeration failed: {result.get('error')}")

    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Get reconnaissance agent capabilities."""
        return {
            "agent_type": "red_team_recon",
            "capabilities": [
                "OSINT gathering",
                "Network mapping",
                "Vulnerability scanning",
                "Asset enumeration",
                "Attack surface identification",
            ],
            "mitre_techniques": [
                "T1592 - Gather Victim Org Information",
                "T1595 - Active Scanning",
                "T1596 - Search Open Websites/Domains",
                "T1598 - Phishing for Information",
            ],
            "tools": [tool.name for tool in self.tools],
            "current_state": {
                "discovered_assets_count": len(self.discovered_assets),
                "network_maps_count": len(self.network_map),
                "vulnerability_findings_count": len(self.vulnerability_findings),
                "osint_data_count": len(self.osint_data),
            },
        }

    def get_reconnaissance_summary(self) -> Dict[str, Any]:
        """Get comprehensive reconnaissance summary."""
        return {
            "agent_id": self.agent_id,
            "summary": {
                "discovered_assets": self.discovered_assets,
                "network_maps": self.network_map,
                "vulnerability_findings": self.vulnerability_findings,
                "osint_data": self.osint_data,
            },
            "statistics": {
                "total_assets_discovered": len(self.discovered_assets),
                "total_networks_mapped": len(self.network_map),
                "total_vulnerabilities_found": len(self.vulnerability_findings),
                "total_osint_gathered": len(self.osint_data),
            },
            "mitre_techniques_used": list(
                set(
                    [
                        data.get("mitre_technique")
                        for data in list(self.discovered_assets.values())
                        + list(self.network_map.values())
                        + self.vulnerability_findings
                        + list(self.osint_data.values())
                        if data.get("mitre_technique")
                    ]
                )
            ),
        }
