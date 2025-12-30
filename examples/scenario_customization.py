#!/usr/bin/env python3
"""
Scenario Customization Example

This example demonstrates how to create custom scenarios for the
Autonomous Multi-Agent Red/Blue Team Simulation System.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scenarios import create_scenario, validate_all_scenarios
from utils.logging_handler import get_logger


class CustomCriticalInfrastructureScenario:
    """
    Custom scenario for a fictional critical infrastructure scenario.

    This demonstrates how to create a new scenario class that follows
    the established patterns and integrates with the simulation system.
    """

    def __init__(self):
        """Initialize the custom scenario."""
        self.scenario_name = "custom_critical_infrastructure"
        self.scenario_version = "1.0"
        self.created_date = datetime.now()

        # Scenario configuration
        self.critical_assets = self._define_critical_assets()
        self.attack_vectors = self._define_attack_vectors()
        self.defensive_measures = self._define_defensive_measures()
        self.success_criteria = self._define_success_criteria()
        self.compliance_requirements = self._define_compliance_requirements()

    def _define_critical_assets(self) -> Dict[str, Any]:
        """Define critical assets for the custom scenario."""
        return {
            "industrial_control_system": {
                "type": "industrial_control",
                "criticality": "critical",
                "location": "control_center",
                "function": "process_control_monitoring",
                "protocols": ["Modbus", "OPC_UA", "DNP3"],
                "access_methods": ["hmi_stations", "remote_access"],
                "vulnerabilities": ["legacy_protocols", "weak_authentication"],
                "impact_if_compromised": "process_disruption_safety_risks",
            },
            "data_center": {
                "type": "it_infrastructure",
                "criticality": "high",
                "location": "main_facility",
                "function": "data_processing_storage",
                "protocols": ["HTTPS", "SSH", "RDP"],
                "access_methods": ["vpn", "direct_access"],
                "vulnerabilities": ["misconfiguration", "weak_credentials"],
                "impact_if_compromised": "data_breach_service_disruption",
            },
            "communication_system": {
                "type": "communication_infrastructure",
                "criticality": "medium",
                "location": "distributed_locations",
                "function": "internal_communications",
                "protocols": ["VoIP", "email", "messaging"],
                "access_methods": ["web_interface", "mobile_apps"],
                "vulnerabilities": ["social_engineering", "malware"],
                "impact_if_compromised": "communication_disruption",
            },
            "physical_security_system": {
                "type": "security_infrastructure",
                "criticality": "medium",
                "location": "facility_perimeter",
                "function": "access_control_monitoring",
                "protocols": ["proprietary", "HTTP"],
                "access_methods": ["control_panel", "mobile_app"],
                "vulnerabilities": ["default_credentials", "physical_bypass"],
                "impact_if_compromised": "unauthorized_access",
            },
        }

    def _define_attack_vectors(self) -> List[Dict[str, Any]]:
        """Define attack vectors for the custom scenario."""
        return [
            {
                "vector_id": "custom_001",
                "name": "Industrial Control System Intrusion",
                "attack_stage": "initial_access",
                "mitre_techniques": ["T1190", "T1133"],
                "description": "Compromise industrial control system through vulnerable protocols",
                "prerequisites": ["network_access", "protocol_knowledge"],
                "indicators": ["unusual_ics_traffic", "protocol_anomalies"],
                "mitigation": ["protocol_monitoring", "network_segmentation"],
                "likelihood": "medium",
                "impact": "critical",
            },
            {
                "vector_id": "custom_002",
                "name": "Supply Chain Compromise",
                "attack_stage": "initial_access",
                "mitre_techniques": ["T1195", "T1199"],
                "description": "Compromise third-party vendor systems to gain access",
                "prerequisites": ["vendor_relationship", "trusted_access"],
                "indicators": ["vendor_system_anomalies", "lateral_movement"],
                "mitigation": ["vendor_security_assessments", "access_controls"],
                "likelihood": "high",
                "impact": "high",
            },
            {
                "vector_id": "custom_003",
                "name": "Data Center Breach",
                "attack_stage": "execution",
                "mitre_techniques": ["T1078", "T1083"],
                "description": "Compromise data center through credential theft",
                "prerequisites": ["credential_access", "privilege_escalation"],
                "indicators": ["unusual_access_patterns", "data_exfiltration"],
                "mitigation": ["multi_factor_authentication", "access_monitoring"],
                "likelihood": "medium",
                "impact": "high",
            },
            {
                "vector_id": "custom_004",
                "name": "Communication System Disruption",
                "attack_stage": "impact",
                "mitre_techniques": ["T1565", "T1499"],
                "description": "Disrupt communication systems through targeted attacks",
                "prerequisites": ["system_access", "communication_knowledge"],
                "indicators": ["service_outages", "communication_anomalies"],
                "mitigation": ["redundant_systems", "backup_communications"],
                "likelihood": "medium",
                "impact": "medium",
            },
            {
                "vector_id": "custom_005",
                "name": "Physical Security Bypass",
                "attack_stage": "persistence",
                "mitre_techniques": ["T1091", "T1200"],
                "description": "Bypass physical security controls for persistence",
                "prerequisites": ["physical_access", "security_knowledge"],
                "indicators": ["unauthorized_physical_access", "security_bypass"],
                "mitigation": ["enhanced_physical_security", "access_logging"],
                "likelihood": "low",
                "impact": "medium",
            },
        ]

    def _define_defensive_measures(self) -> List[Dict[str, Any]]:
        """Define defensive measures for the custom scenario."""
        return [
            {
                "measure_id": "custom_dm001",
                "name": "Network Segmentation",
                "essential_eight": "network_segmentation",
                "description": "Implement strict network segmentation between IT and OT systems",
                "implementation": ["firewalls", "vlans", "air_gaps"],
                "effectiveness": "high",
                "coverage": ["control_systems", "data_center"],
                "monitoring": ["traffic_monitoring", "access_logging"],
            },
            {
                "measure_id": "custom_dm002",
                "name": "Multi-Factor Authentication",
                "essential_eight": "multi_factor_authentication",
                "description": "Enforce MFA for all remote access and privileged accounts",
                "implementation": ["hardware_tokens", "biometric_factors"],
                "effectiveness": "high",
                "coverage": ["remote_access", "administrative_accounts"],
                "monitoring": ["authentication_logs", "access_attempts"],
            },
            {
                "measure_id": "custom_dm003",
                "name": "Application Control",
                "essential_eight": "application_control",
                "description": "Implement application whitelisting on critical systems",
                "implementation": ["whitelisting_policies", "code_signing"],
                "effectiveness": "medium",
                "coverage": ["control_systems", "workstations"],
                "monitoring": ["execution_monitoring", "policy_violations"],
            },
            {
                "measure_id": "custom_dm004",
                "name": "Security Monitoring",
                "essential_eight": "security_monitoring",
                "description": "Deploy comprehensive security monitoring across all systems",
                "implementation": ["siem", "intrusion_detection", "log_analysis"],
                "effectiveness": "high",
                "coverage": ["all_systems", "network_traffic"],
                "monitoring": ["real_time_alerts", "threat_intelligence"],
            },
            {
                "measure_id": "custom_dm005",
                "name": "Patch Management",
                "essential_eight": "patch_management",
                "description": "Maintain rigorous patch management for all systems",
                "implementation": ["automated_patching", "vulnerability_scanning"],
                "effectiveness": "medium",
                "coverage": ["it_systems", "accessible_ot_systems"],
                "monitoring": ["patch_status", "vulnerability_reports"],
            },
        ]

    def _define_success_criteria(self) -> Dict[str, Any]:
        """Define success criteria for red and blue teams."""
        return {
            "red_team_success": {
                "primary_objectives": [
                    "compromise_industrial_control_system",
                    "exfiltrate_critical_data",
                    "disrupt_communication_systems",
                ],
                "secondary_objectives": [
                    "establish_persistence",
                    "bypass_physical_security",
                    "demonstrate_lateral_movement",
                ],
                "scoring_weights": {
                    "critical_asset_compromise": 40,
                    "data_exfiltration": 25,
                    "service_disruption": 20,
                    "persistence": 15,
                },
            },
            "blue_team_success": {
                "primary_objectives": [
                    "prevent_control_system_compromise",
                    "detect_data_breach_attempts",
                    "maintain_service_availability",
                ],
                "secondary_objectives": [
                    "identify_supply_chain_compromise",
                    "contain_incident_within_72h",
                    "preserve_forensic_evidence",
                ],
                "scoring_weights": {
                    "prevention_effectiveness": 35,
                    "detection_speed": 35,
                    "incident_response": 20,
                    "evidence_preservation": 10,
                },
            },
        }

    def _define_compliance_requirements(self) -> Dict[str, Any]:
        """Define compliance requirements."""
        return {
            "soci_act_requirements": {
                "critical_infrastructure_registration": True,
                "cyber_security_incident_reporting": True,
                "risk_management_program": True,
                "cyber_security_reviews": True,
                "information_sharing_requirements": True,
            },
            "asd_essential_eight": {
                "application_control": "implemented",
                "patch_management": "implemented",
                "multi_factor_authentication": "implemented",
                "restrict_administrative_privileges": "implemented",
                "macro_execution": "implemented",
                "hardening_user_applications": "implemented",
                "microsoft_office_macro_settings": "implemented",
                "security_monitoring": "implemented",
            },
            "privacy_act_requirements": {
                "personal_information_protection": True,
                "data_breach_notification": True,
                "cross_border_data_transfers": True,
            },
            "industry_regulations": {
                "industrial_security": True,
                "data_protection": True,
                "physical_security": True,
            },
            "reporting_obligations": {
                "acsc_reporting": "within_72_hours",
                "soci_act_reporting": "within_12_hours_critical",
                "privacy_act_reporting": "within_30_days",
                "industry_authority": "within_48_hours",
            },
        }

    def get_scenario_config(self) -> Dict[str, Any]:
        """Get complete scenario configuration."""
        return {
            "scenario_metadata": {
                "name": self.scenario_name,
                "version": self.scenario_version,
                "created_date": self.created_date.isoformat(),
                "sector": "critical_infrastructure",
                "soci_act_applicable": True,
                "critical_infrastructure": True,
                "custom_scenario": True,
            },
            "critical_assets": self.critical_assets,
            "attack_vectors": self.attack_vectors,
            "defensive_measures": self.defensive_measures,
            "success_criteria": self.success_criteria,
            "compliance_requirements": self.compliance_requirements,
            "simulation_parameters": {
                "duration_hours": 48,
                "red_team_agents": 4,
                "blue_team_agents": 3,
                "real_time_monitoring": True,
                "forensic_collection": True,
                "compliance_validation": True,
                "custom_features": [
                    "industrial_control_simulation",
                    "supply_chain_modeling",
                    "physical_security_integration",
                ],
            },
        }

    def validate_scenario(self) -> Dict[str, Any]:
        """Validate scenario configuration."""
        validation_results = {
            "scenario_valid": True,
            "validation_errors": [],
            "warnings": [],
            "recommendations": [],
        }

        # Check critical assets
        if not self.critical_assets:
            validation_results["scenario_valid"] = False
            validation_results["validation_errors"].append("No critical assets defined")

        # Check attack vectors
        if not self.attack_vectors:
            validation_results["scenario_valid"] = False
            validation_results["validation_errors"].append("No attack vectors defined")

        # Check defensive measures
        if not self.defensive_measures:
            validation_results["warnings"].append("No defensive measures defined")

        # Validate MITRE technique coverage
        mitre_techniques = set()
        for vector in self.attack_vectors:
            techniques = vector.get("mitre_techniques", [])
            mitre_techniques.update(techniques)

        if len(mitre_techniques) < 5:
            validation_results["warnings"].append("Limited MITRE technique coverage")

        # Validate compliance requirements
        if not self.compliance_requirements.get("soci_act_requirements"):
            validation_results["warnings"].append(
                "Missing SOCI Act compliance requirements"
            )

        # Validate custom features
        if self.scenario_name.startswith("custom_"):
            validation_results["recommendations"].append(
                "Consider registering custom scenario in scenarios/__init__.py"
            )

        return validation_results


def create_custom_scenario():
    """Create and return the custom scenario."""
    return CustomCriticalInfrastructureScenario()


def main():
    """Main function for scenario customization example."""

    print("🎛 Custom Scenario Example")
    print("=" * 50)

    # Create custom scenario
    scenario = create_custom_scenario()

    print(f"Scenario Name: {scenario.scenario_name}")
    print(f"Scenario Version: {scenario.scenario_version}")
    print(f"Critical Assets: {len(scenario.critical_assets)}")
    print(f"Attack Vectors: {len(scenario.attack_vectors)}")
    print(f"Defensive Measures: {len(scenario.defensive_measures)}")

    # Validate scenario
    validation = scenario.validate_scenario()
    print(f"\n🔍 Validation Results:")
    print(f"  Valid: {validation['scenario_valid']}")
    print(f"  Errors: {len(validation['validation_errors'])}")
    print(f"  Warnings: {len(validation['warnings'])}")
    print(f"  Recommendations: {len(validation['recommendations'])}")

    if validation["validation_errors"]:
        print("\n❌ Validation Errors:")
        for error in validation["validation_errors"]:
            print(f"  - {error}")

    if validation["warnings"]:
        print("\n⚠️ Warnings:")
        for warning in validation["warnings"]:
            print(f"  - {warning}")

    if validation["recommendations"]:
        print("\n💡 Recommendations:")
        for recommendation in validation["recommendations"]:
            print(f"  - {recommendation}")

    # Get scenario configuration
    config = scenario.get_scenario_config()
    print(f"\n📋 Scenario Configuration:")
    print(f"  Sector: {config['scenario_metadata']['sector']}")
    print(f"  Duration: {config['simulation_parameters']['duration_hours']} hours")
    print(f"  Red Team Agents: {config['simulation_parameters']['red_team_agents']}")
    print(f"  Blue Team Agents: {config['simulation_parameters']['blue_team_agents']}")
    print(f"  Custom Features: {config['simulation_parameters']['custom_features']}")

    # Show critical assets
    print(f"\n🏭️ Critical Assets:")
    for asset_id, asset in scenario.critical_assets.items():
        print(f"  - {asset_id}: {asset['type']} ({asset['criticality']})")

    # Show attack vectors
    print(f"\n⚔️ Attack Vectors:")
    for vector in scenario.attack_vectors:
        print(
            f"  - {vector['name']} (Stage: {vector['attack_stage']}, Impact: {vector['impact']})"
        )

    # Show defensive measures
    print(f"\n🛡️ Defensive Measures:")
    for measure in scenario.defensive_measures:
        print(f"  - {measure['name']} (Essential Eight: {measure['essential_eight']})")

    print(f"\n✅ Custom scenario created and validated successfully!")

    # Show how to integrate with the system
    print(f"\n🔗 Integration Instructions:")
    print(f"  1. Add scenario to scenarios/__init__.py:")
    print(f"     SCENARIOS['{scenario.scenario_name}'] = {{")
    print(f"         'class': CustomCriticalInfrastructureScenario,")
    print(f"         'factory': create_custom_scenario,")
    print(f"         'metadata': {{...}}")
    print(f"     }}")
    print(f"  2. Import and use in main.py:")
    print(f"     from scenarios import create_scenario")
    print(f"     scenario = create_scenario('{scenario.scenario_name}')")
    print(f"  3. Run simulation:")
    print(f"     python main.py --scenario {scenario.scenario_name}")


if __name__ == "__main__":
    main()
