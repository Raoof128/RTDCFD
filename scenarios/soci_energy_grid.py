"""
SOCI Act Energy Grid Critical Infrastructure Scenario

This module defines a comprehensive simulation scenario for testing
cyber attacks against Australian energy grid infrastructure under the SOCI Act.
"""

from datetime import datetime
from typing import Any, Dict, List


class SOCEnergyGridScenario:
    """
    Australian Energy Grid Critical Infrastructure Scenario

    This scenario simulates cyber attacks against energy grid infrastructure,
    including SCADA systems, power distribution networks, and control systems.
    Aligned with Australian SOCI Act requirements and ASD Essential Eight.
    """

    def __init__(self):
        """Initialize the energy grid scenario."""
        self.scenario_name = "soci_energy_grid"
        self.scenario_version = "1.0"
        self.created_date = datetime.now()

        # Scenario configuration
        self.critical_assets = self._define_critical_assets()
        self.attack_vectors = self._define_attack_vectors()
        self.defensive_measures = self._define_defensive_measures()
        self.success_criteria = self._define_success_criteria()
        self.compliance_requirements = self._define_compliance_requirements()

    def _define_critical_assets(self) -> Dict[str, Any]:
        """Define critical energy grid assets."""
        return {
            "scada_master_system": {
                "type": "industrial_control_system",
                "criticality": "critical",
                "location": "control_center",
                "function": "grid_monitoring_and_control",
                "protocols": ["Modbus", "DNP3", "IEC_61850"],
                "access_methods": ["vpn", "dedicated_lines"],
                "vulnerabilities": ["weak_authentication", "legacy_protocols"],
                "impact_if_compromised": "grid_instability_blackout",
            },
            "power_distribution_management": {
                "type": "management_system",
                "criticality": "critical",
                "location": "distribution_center",
                "function": "load_balancing_distribution",
                "protocols": ["HTTP", "HTTPS", "proprietary"],
                "access_methods": ["web_interface", "api"],
                "vulnerabilities": ["web_vulnerabilities", "api_exposure"],
                "impact_if_compromised": "localized_outages_cascading",
            },
            "substation_automation": {
                "type": "automation_system",
                "criticality": "high",
                "location": "multiple_substations",
                "function": "automated_switching_protection",
                "protocols": ["IEC_61850", "IEC_60870-5-104"],
                "access_methods": ["remote_access", "local_hmi"],
                "vulnerabilities": ["default_credentials", "insecure_remote_access"],
                "impact_if_compromised": "equipment_damage_safety_risks",
            },
            "energy_market_system": {
                "type": "business_system",
                "criticality": "medium",
                "location": "corporate_office",
                "function": "energy_trading_billing",
                "protocols": ["HTTPS", "MQTT"],
                "access_methods": ["web_portal", "api"],
                "vulnerabilities": ["business_logic_flaws", "data_exposure"],
                "impact_if_compromised": "financial_losses_market_disruption",
            },
            "customer_billing_portal": {
                "type": "customer_system",
                "criticality": "low",
                "location": "cloud_hosted",
                "function": "customer_management_billing",
                "protocols": ["HTTPS", "REST_API"],
                "access_methods": ["public_internet"],
                "vulnerabilities": ["web_attacks", "authentication_bypass"],
                "impact_if_compromised": "customer_discomfort_privacy_breach",
            },
            "grid_monitoring_sensors": {
                "type": "iot_system",
                "criticality": "medium",
                "location": "grid_wide",
                "function": "real_time_monitoring_telemetry",
                "protocols": ["MQTT", "CoAP", "LoRaWAN"],
                "access_methods": ["wireless_networks"],
                "vulnerabilities": ["weak_encryption", "device_compromise"],
                "impact_if_compromised": "blind_spots_incorrect_data",
            },
        }

    def _define_attack_vectors(self) -> List[Dict[str, Any]]:
        """Define potential attack vectors for energy grid."""
        return [
            {
                "vector_id": "av001",
                "name": "SCADA System Intrusion",
                "attack_stage": "initial_access",
                "mitre_techniques": ["T1190", "T1133"],
                "description": "Exploit vulnerabilities in SCADA master system through VPN access or direct network connection",
                "prerequisites": ["network_access", "vulnerability_knowledge"],
                "indicators": ["unusual_scada_traffic", "authentication_failures"],
                "mitigation": ["network_segmentation", "multi_factor_authentication"],
                "likelihood": "medium",
                "impact": "critical",
            },
            {
                "vector_id": "av002",
                "name": "Supply Chain Compromise",
                "attack_stage": "initial_access",
                "mitre_techniques": ["T1195", "T1199"],
                "description": "Compromise third-party vendor systems to gain access to energy grid networks",
                "prerequisites": ["vendor_relationship", "trusted_access"],
                "indicators": ["vendor_system_anomalies", "lateral_movement"],
                "mitigation": ["vendor_security_assessments", "access_controls"],
                "likelihood": "high",
                "impact": "high",
            },
            {
                "vector_id": "av003",
                "name": "Protocol Manipulation",
                "attack_stage": "execution",
                "mitre_techniques": ["T1203", "T1068"],
                "description": "Manipulate industrial control protocols to send unauthorized commands",
                "prerequisites": ["protocol_access", "knowledge_base"],
                "indicators": ["unusual_command_sequences", "parameter_changes"],
                "mitigation": ["protocol_monitoring", "command_whitelisting"],
                "likelihood": "medium",
                "impact": "critical",
            },
            {
                "vector_id": "av004",
                "name": "DDoS Against Control Systems",
                "attack_stage": "impact",
                "mitre_techniques": ["T1498", "T1499"],
                "description": "Overwhelm control system communications to disrupt grid operations",
                "prerequisites": ["bandwidth", "botnet"],
                "indicators": ["communication_failures", "response_time_delays"],
                "mitigation": ["traffic_filtering", "redundant_communications"],
                "likelihood": "high",
                "impact": "high",
            },
            {
                "vector_id": "av005",
                "name": "Insider Threat",
                "attack_stage": "privilege_escalation",
                "mitre_techniques": ["T1078", "T1548"],
                "description": "Malicious insider abuses legitimate access to compromise systems",
                "prerequisites": ["legitimate_access", "malicious_intent"],
                "indicators": ["unusual_access_patterns", "privilege_abuse"],
                "mitigation": ["access_controls", "behavioral_monitoring"],
                "likelihood": "medium",
                "impact": "critical",
            },
        ]

    def _define_defensive_measures(self) -> List[Dict[str, Any]]:
        """Define defensive measures aligned with ASD Essential Eight."""
        return [
            {
                "measure_id": "dm001",
                "name": "Network Segmentation",
                "essential_eight": "network_segmentation",
                "description": "Implement proper network segmentation between IT and OT networks",
                "implementation": ["firewalls", "vlans", "air_gaps"],
                "effectiveness": "high",
                "coverage": ["scada_systems", "control_networks"],
                "monitoring": ["traffic_analysis", "connection_logging"],
            },
            {
                "measure_id": "dm002",
                "name": "Multi-Factor Authentication",
                "essential_eight": "multi_factor_authentication",
                "description": "Enforce MFA for all remote access and privileged accounts",
                "implementation": ["hardware_tokens", "biometric_factors"],
                "effectiveness": "high",
                "coverage": ["remote_access", "administrative_accounts"],
                "monitoring": ["authentication_logs", "access_attempts"],
            },
            {
                "measure_id": "dm003",
                "name": "Application Control",
                "essential_eight": "application_control",
                "description": "Implement application whitelisting on critical systems",
                "implementation": ["whitelisting_policies", "code_signing"],
                "effectiveness": "medium",
                "coverage": ["control_systems", "workstations"],
                "monitoring": ["execution_logs", "policy_violations"],
            },
            {
                "measure_id": "dm004",
                "name": "Security Monitoring",
                "essential_eight": "security_monitoring",
                "description": "Deploy comprehensive security monitoring across all systems",
                "implementation": ["siem", "intrusion_detection", "log_analysis"],
                "effectiveness": "high",
                "coverage": ["all_systems", "network_traffic"],
                "monitoring": ["real_time_alerts", "threat_intelligence"],
            },
            {
                "measure_id": "dm005",
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
                    "compromise_scada_master_system",
                    "demonstrate_grid_impact_capability",
                    "maintain_persistence_for_30_days",
                ],
                "secondary_objectives": [
                    "exfiltrate_operational_data",
                    "compromise_substation_automation",
                    "disrupt_energy_market_operations",
                ],
                "scoring_weights": {
                    "critical_asset_compromise": 40,
                    "persistence_maintenance": 25,
                    "data_exfiltration": 20,
                    "defense_evasion": 15,
                },
            },
            "blue_team_success": {
                "primary_objectives": [
                    "detect_initial_compromise_within_24h",
                    "prevent_critical_system_compromise",
                    "maintain_grid_stability",
                ],
                "secondary_objectives": [
                    "identify_all_attack_vectors",
                    "contain_incident_within_72h",
                    "preserve_forensic_evidence",
                ],
                "scoring_weights": {
                    "detection_speed": 35,
                    "prevention_effectiveness": 35,
                    "incident_response": 20,
                    "recovery_time": 10,
                },
            },
        }

    def _define_compliance_requirements(self) -> Dict[str, Any]:
        """Define SOCI Act and Australian compliance requirements."""
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
            "reporting_obligations": {
                "acsc_reporting": "within_72_hours",
                "soci_act_reporting": "within_12_hours_critical",
                "privacy_act_reporting": "within_30_days",
            },
        }

    def get_scenario_config(self) -> Dict[str, Any]:
        """Get complete scenario configuration."""
        return {
            "scenario_metadata": {
                "name": self.scenario_name,
                "version": self.scenario_version,
                "created_date": self.created_date.isoformat(),
                "sector": "energy",
                "soci_act_applicable": True,
                "critical_infrastructure": True,
            },
            "critical_assets": self.critical_assets,
            "attack_vectors": self.attack_vectors,
            "defensive_measures": self.defensive_measures,
            "success_criteria": self.success_criteria,
            "compliance_requirements": self.compliance_requirements,
            "simulation_parameters": {
                "duration_hours": 72,
                "red_team_agents": 4,
                "blue_team_agents": 3,
                "real_time_monitoring": True,
                "forensic_collection": True,
                "compliance_validation": True,
            },
        }

    def validate_scenario(self) -> Dict[str, Any]:
        """Validate scenario configuration and requirements."""
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
            mitre_techniques.update(vector.get("mitre_techniques", []))

        if len(mitre_techniques) < 5:
            validation_results["warnings"].append("Limited MITRE technique coverage")

        # Check ASD Essential Eight alignment
        essential_eight_coverage = set()
        for measure in self.defensive_measures:
            essential_eight_coverage.add(measure.get("essential_eight"))

        if len(essential_eight_coverage) < 4:
            validation_results["recommendations"].append(
                "Expand ASD Essential Eight coverage"
            )

        return validation_results


# Scenario factory function
def create_scenario() -> SOCEnergyGridScenario:
    """Create and return the energy grid scenario."""
    return SOCEnergyGridScenario()


# Scenario metadata for registration
SCENARIO_METADATA = {
    "name": "soci_energy_grid",
    "display_name": "SOCI Act Energy Grid Critical Infrastructure",
    "description": "Comprehensive cyber attack simulation against Australian energy grid infrastructure",
    "sector": "energy",
    "difficulty": "advanced",
    "duration_hours": 72,
    "red_team_agents": 4,
    "blue_team_agents": 3,
    "compliance_frameworks": ["SOCI_Act", "ASD_Essential_Eight", "Privacy_Act"],
    "created_by": "Autonomous Multi-Agent System",
    "version": "1.0",
}
