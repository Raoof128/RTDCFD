"""
SOCI Act Water Treatment System Critical Infrastructure Scenario

This module defines a comprehensive simulation scenario for testing
cyber attacks against Australian water treatment infrastructure under the SOCI Act.
"""

from datetime import datetime
from typing import Any, Dict, List


class SOCIWaterSystemScenario:
    """
    Australian Water Treatment System Critical Infrastructure Scenario

    This scenario simulates cyber attacks against water treatment infrastructure,
    including treatment plants, distribution systems, and control systems.
    Aligned with Australian SOCI Act requirements and ASD Essential Eight.
    """

    def __init__(self):
        """Initialize the water treatment system scenario."""
        self.scenario_name = "soci_water_system"
        self.scenario_version = "1.0"
        self.created_date = datetime.now()

        # Scenario configuration
        self.critical_assets = self._define_critical_assets()
        self.attack_vectors = self._define_attack_vectors()
        self.defensive_measures = self._define_defensive_measures()
        self.success_criteria = self._define_success_criteria()
        self.compliance_requirements = self._define_compliance_requirements()

    def _define_critical_assets(self) -> Dict[str, Any]:
        """Define critical water treatment assets."""
        return {
            "water_treatment_plant_scada": {
                "type": "industrial_control_system",
                "criticality": "critical",
                "location": "treatment_facility",
                "function": "water_treatment_process_control",
                "protocols": ["Modbus", "DNP3", "OPC_UA"],
                "access_methods": ["hmi_stations", "remote_access"],
                "vulnerabilities": ["legacy_protocols", "weak_authentication"],
                "impact_if_compromised": "water_safety_public_health_crisis",
            },
            "chemical_dosing_system": {
                "type": "control_system",
                "criticality": "critical",
                "location": "treatment_plant",
                "function": "chemical_treatment_dosing",
                "protocols": ["Modbus", "proprietary"],
                "access_methods": ["local_hmi", "remote_monitoring"],
                "vulnerabilities": ["insecure_remote_access", "logic_vulnerabilities"],
                "impact_if_compromised": "water_contamination_health_risks",
            },
            "distribution_control_system": {
                "type": "control_system",
                "criticality": "high",
                "location": "pumping_stations",
                "function": "water_pressure_flow_control",
                "protocols": ["DNP3", "IEC_60870-5-104"],
                "access_methods": ["control_center", "remote_terminals"],
                "vulnerabilities": [
                    "communication_vulnerabilities",
                    "access_control_issues",
                ],
                "impact_if_compromised": "service_disruption_pressure_issues",
            },
            "water_quality_monitoring": {
                "type": "monitoring_system",
                "criticality": "high",
                "location": "distribution_network",
                "function": "real_time_quality_assessment",
                "protocols": ["MQTT", "HTTP", "proprietary"],
                "access_methods": ["web_interface", "api"],
                "vulnerabilities": ["web_vulnerabilities", "data_manipulation"],
                "impact_if_compromised": "undetected_contamination_false_readings",
            },
            "customer_billing_system": {
                "type": "business_system",
                "criticality": "medium",
                "location": "corporate_office",
                "function": "customer_billing_usage_tracking",
                "protocols": ["HTTPS", "SQL"],
                "access_methods": ["web_portal", "internal_network"],
                "vulnerabilities": [
                    "web_application_vulnerabilities",
                    "database_issues",
                ],
                "impact_if_compromised": "financial_losses_customer_data_breach",
            },
            "reservoir_level_control": {
                "type": "control_system",
                "criticality": "medium",
                "location": "reservoir_sites",
                "function": "water_storage_level_management",
                "protocols": ["Modbus", "SCADA"],
                "access_methods": ["remote_terminal_units", "control_center"],
                "vulnerabilities": [
                    "remote_access_vulnerabilities",
                    "protocol_weaknesses",
                ],
                "impact_if_compromised": "water_shortages_overflow_risks",
            },
            "emergency_shutdown_system": {
                "type": "safety_system",
                "criticality": "critical",
                "location": "treatment_facility",
                "function": "emergency_response_safety",
                "protocols": ["hardwired", "redundant_systems"],
                "access_methods": ["physical_access", "safety_panels"],
                "vulnerabilities": ["physical_access", "bypass_attempts"],
                "impact_if_compromised": "inability_respond_emergencies",
            },
        }

    def _define_attack_vectors(self) -> List[Dict[str, Any]]:
        """Define potential attack vectors for water treatment systems."""
        return [
            {
                "vector_id": "wv001",
                "name": "SCADA System Compromise",
                "attack_stage": "initial_access",
                "mitre_techniques": ["T1190", "T1133"],
                "description": "Compromise SCADA systems through VPN access or direct network intrusion",
                "prerequisites": ["network_access", "scada_knowledge"],
                "indicators": ["unauthorized_scada_access", "unusual_control_commands"],
                "mitigation": ["network_segmentation", "access_controls"],
                "likelihood": "medium",
                "impact": "critical",
            },
            {
                "vector_id": "wv002",
                "name": "Chemical Dosing Manipulation",
                "attack_stage": "execution",
                "mitre_techniques": ["T1203", "T1068"],
                "description": "Manipulate chemical dosing systems to alter water treatment processes",
                "prerequisites": ["system_access", "process_knowledge"],
                "indicators": ["abnormal_chemical_levels", "unusual_dosing_patterns"],
                "mitigation": ["process_monitoring", "safety_interlocks"],
                "likelihood": "medium",
                "impact": "critical",
            },
            {
                "vector_id": "wv003",
                "name": "Data Integrity Attack",
                "attack_stage": "impact",
                "mitre_techniques": ["T1565", "T1491"],
                "description": "Manipulate water quality monitoring data to hide contamination",
                "prerequisites": ["monitoring_system_access", "data_manipulation"],
                "indicators": [
                    "sensor_data_anomalies",
                    "quality_reading_inconsistencies",
                ],
                "mitigation": ["data_validation", "redundant_monitoring"],
                "likelihood": "high",
                "impact": "high",
            },
            {
                "vector_id": "wv004",
                "name": "Operational Technology Ransomware",
                "attack_stage": "impact",
                "mitre_techniques": ["T1486", "T1490"],
                "description": "Deploy ransomware against operational technology systems",
                "prerequisites": ["system_access", "malware_deployment"],
                "indicators": ["system_encryption", "ransom_notes"],
                "mitigation": ["system_backups", "air_gapping"],
                "likelihood": "medium",
                "impact": "critical",
            },
            {
                "vector_id": "wv005",
                "name": "Supply Chain Compromise",
                "attack_stage": "initial_access",
                "mitre_techniques": ["T1195", "T1199"],
                "description": "Compromise third-party equipment vendors or maintenance contractors",
                "prerequisites": ["vendor_relationship", "trusted_access"],
                "indicators": ["vendor_system_anomalies", "maintenance_irregularities"],
                "mitigation": ["vendor_security", "access_monitoring"],
                "likelihood": "high",
                "impact": "high",
            },
            {
                "vector_id": "wv006",
                "name": "Physical System Sabotage",
                "attack_stage": "impact",
                "mitre_techniques": ["T0856", "T0857"],
                "description": "Combine cyber attacks with physical sabotage for maximum impact",
                "prerequisites": ["physical_access", "cyber_compromise"],
                "indicators": ["physical_tampering", "cyber_physical_coordination"],
                "mitigation": ["physical_security", "cyber_physical_monitoring"],
                "likelihood": "low",
                "impact": "critical",
            },
        ]

    def _define_defensive_measures(self) -> List[Dict[str, Any]]:
        """Define defensive measures aligned with ASD Essential Eight."""
        return [
            {
                "measure_id": "wm001",
                "name": "OT Network Segmentation",
                "essential_eight": "network_segmentation",
                "description": "Implement strict network segmentation between IT and OT systems",
                "implementation": ["firewalls", "demilitarized_zones", "air_gaps"],
                "effectiveness": "high",
                "coverage": ["scada_systems", "control_networks"],
                "monitoring": ["traffic_monitoring", "access_logging"],
            },
            {
                "measure_id": "wm002",
                "name": "Process Safety Controls",
                "essential_eight": "security_monitoring",
                "description": "Implement independent process safety controls and monitoring",
                "implementation": [
                    "safety_instrumented_systems",
                    "redundant_sensors",
                    "emergency_stops",
                ],
                "effectiveness": "high",
                "coverage": ["chemical_dosing", "treatment_processes"],
                "monitoring": ["real_time_monitoring", "safety_interlocks"],
            },
            {
                "measure_id": "wm003",
                "name": "Remote Access Security",
                "essential_eight": "multi_factor_authentication",
                "description": "Secure all remote access to critical systems",
                "implementation": ["mfa", "vpn_security", "session_monitoring"],
                "effectiveness": "high",
                "coverage": ["remote_access_points", "vendor_connections"],
                "monitoring": ["access_monitoring", "session_logging"],
            },
            {
                "measure_id": "wm004",
                "name": "System Backup and Recovery",
                "essential_eight": "patch_management",
                "description": "Implement comprehensive backup and recovery systems",
                "implementation": [
                    "system_backups",
                    "recovery_procedures",
                    "failover_systems",
                ],
                "effectiveness": "medium",
                "coverage": ["control_systems", "monitoring_systems"],
                "monitoring": ["backup_validation", "recovery_testing"],
            },
            {
                "measure_id": "wm005",
                "name": "Physical Security Integration",
                "essential_eight": "restrict_administrative_privileges",
                "description": "Integrate cybersecurity with physical security measures",
                "implementation": [
                    "access_control",
                    "surveillance",
                    "intrusion_detection",
                ],
                "effectiveness": "high",
                "coverage": ["facility_access", "equipment_protection"],
                "monitoring": ["physical_monitoring", "cyber_physical_correlation"],
            },
        ]

    def _define_success_criteria(self) -> Dict[str, Any]:
        """Define success criteria for red and blue teams."""
        return {
            "red_team_success": {
                "primary_objectives": [
                    "compromise_water_treatment_process",
                    "manipulate_water_quality_data",
                    "demonstrate_operational_disruption",
                ],
                "secondary_objectives": [
                    "deploy_ransomware_against_ot_systems",
                    "maintain_persistence_for_30_days",
                    "exfiltrate_operational_data",
                ],
                "scoring_weights": {
                    "process_compromise": 40,
                    "data_manipulation": 25,
                    "service_disruption": 20,
                    "persistence": 15,
                },
            },
            "blue_team_success": {
                "primary_objectives": [
                    "maintain_water_safety_standards",
                    "detect_process_anomalies",
                    "preserve_system_availability",
                ],
                "secondary_objectives": [
                    "prevent_data_manipulation",
                    "identify_supply_chain_compromise",
                    "coordinate_emergency_response",
                ],
                "scoring_weights": {
                    "safety_maintenance": 40,
                    "threat_detection": 30,
                    "service_continuity": 20,
                    "incident_response": 10,
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
            "water_regulations": {
                "drinking_water_standards": True,
                "water_quality_monitoring": True,
                "environmental_protection": True,
                "public_health_obligations": True,
            },
            "reporting_obligations": {
                "acsc_reporting": "within_72_hours",
                "soci_act_reporting": "within_12_hours_critical",
                "privacy_act_reporting": "within_30_days",
                "health_authority_reporting": "immediate_public_health_risk",
            },
        }

    def get_scenario_config(self) -> Dict[str, Any]:
        """Get complete scenario configuration."""
        return {
            "scenario_metadata": {
                "name": self.scenario_name,
                "version": self.scenario_version,
                "created_date": self.created_date.isoformat(),
                "sector": "water",
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

        # Check for water-specific critical assets
        water_assets = [
            asset
            for asset in self.critical_assets.values()
            if asset.get("type")
            in ["industrial_control_system", "control_system", "monitoring_system"]
        ]

        if len(water_assets) < 4:
            validation_results["warnings"].append(
                "Limited water treatment-specific assets"
            )

        # Check attack vectors
        if not self.attack_vectors:
            validation_results["scenario_valid"] = False
            validation_results["validation_errors"].append("No attack vectors defined")

        # Validate safety-critical focus
        safety_critical_assets = [
            asset
            for asset in self.critical_assets.values()
            if asset.get("criticality") == "critical"
        ]

        if len(safety_critical_assets) < 3:
            validation_results["recommendations"].append(
                "Expand safety-critical asset coverage"
            )

        # Check for process safety controls
        process_safety_measures = [
            measure
            for measure in self.defensive_measures
            if "safety" in measure.get("name", "").lower()
        ]

        if len(process_safety_measures) < 2:
            validation_results["recommendations"].append(
                "Add more process safety controls"
            )

        # Validate MITRE technique coverage
        mitre_techniques = set()
        for vector in self.attack_vectors:
            mitre_techniques.update(vector.get("mitre_techniques", []))

        if len(mitre_techniques) < 5:
            validation_results["warnings"].append("Limited MITRE technique coverage")

        return validation_results


# Scenario factory function
def create_scenario() -> SOCIWaterSystemScenario:
    """Create and return the water treatment system scenario."""
    return SOCIWaterSystemScenario()


# Scenario metadata for registration
SCENARIO_METADATA = {
    "name": "soci_water_system",
    "display_name": "SOCI Act Water Treatment System Critical Infrastructure",
    "description": "Comprehensive cyber attack simulation against Australian water treatment infrastructure",
    "sector": "water",
    "difficulty": "advanced",
    "duration_hours": 72,
    "red_team_agents": 4,
    "blue_team_agents": 3,
    "compliance_frameworks": [
        "SOCI_Act",
        "ASD_Essential_Eight",
        "Privacy_Act",
        "Water_Regulations",
    ],
    "created_by": "Autonomous Multi-Agent System",
    "version": "1.0",
}
