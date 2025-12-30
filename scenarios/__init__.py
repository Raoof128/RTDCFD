"""
Scenarios Package

This package contains SOCI Act critical infrastructure scenarios for the
autonomous multi-agent simulation system.
"""

from .soci_energy_grid import SOCEnergyGridScenario, create_scenario as create_energy_scenario
from .soci_telco_network import SOCTelcoNetworkScenario, create_scenario as create_telco_scenario
from .soci_water_system import SOCIWaterSystemScenario, create_scenario as create_water_scenario

# Scenario registry
SCENARIOS = {
    "soci_energy_grid": {
        "class": SOCEnergyGridScenario,
        "factory": create_energy_scenario,
        "metadata": {
            "name": "soci_energy_grid",
            "display_name": "SOCI Act Energy Grid Critical Infrastructure",
            "description": "Comprehensive cyber attack simulation against Australian energy grid infrastructure",
            "sector": "energy",
            "difficulty": "advanced",
            "duration_hours": 72,
            "red_team_agents": 4,
            "blue_team_agents": 3,
            "compliance_frameworks": ["SOCI_Act", "ASD_Essential_Eight", "Privacy_Act"]
        }
    },
    "soci_telco_network": {
        "class": SOCTelcoNetworkScenario,
        "factory": create_telco_scenario,
        "metadata": {
            "name": "soci_telco_network",
            "display_name": "SOCI Act Telecommunications Network Critical Infrastructure",
            "description": "Comprehensive cyber attack simulation against Australian telecommunications infrastructure",
            "sector": "telecommunications",
            "difficulty": "advanced",
            "duration_hours": 72,
            "red_team_agents": 4,
            "blue_team_agents": 3,
            "compliance_frameworks": ["SOCI_Act", "ASD_Essential_Eight", "Privacy_Act", "Telecommunications_Act"]
        }
    },
    "soci_water_system": {
        "class": SOCIWaterSystemScenario,
        "factory": create_water_scenario,
        "metadata": {
            "name": "soci_water_system",
            "display_name": "SOCI Act Water Treatment System Critical Infrastructure",
            "description": "Comprehensive cyber attack simulation against Australian water treatment infrastructure",
            "sector": "water",
            "difficulty": "advanced",
            "duration_hours": 72,
            "red_team_agents": 4,
            "blue_team_agents": 3,
            "compliance_frameworks": ["SOCI_Act", "ASD_Essential_Eight", "Privacy_Act", "Water_Regulations"]
        }
    }
}


def get_available_scenarios() -> list:
    """Get list of available scenario names."""
    return list(SCENARIOS.keys())


def get_scenario_metadata(scenario_name: str) -> dict:
    """Get metadata for a specific scenario."""
    if scenario_name in SCENARIOS:
        return SCENARIOS[scenario_name]["metadata"]
    else:
        raise ValueError(f"Unknown scenario: {scenario_name}")


def create_scenario(scenario_name: str):
    """Create a scenario instance."""
    if scenario_name in SCENARIOS:
        return SCENARIOS[scenario_name]["factory"]()
    else:
        raise ValueError(f"Unknown scenario: {scenario_name}")


def validate_all_scenarios() -> dict:
    """Validate all scenarios and return results."""
    validation_results = {}
    
    for scenario_name in SCENARIOS:
        try:
            scenario = create_scenario(scenario_name)
            validation_results[scenario_name] = scenario.validate_scenario()
        except Exception as e:
            validation_results[scenario_name] = {
                "scenario_valid": False,
                "validation_errors": [f"Scenario creation failed: {str(e)}"],
                "warnings": [],
                "recommendations": []
            }
    
    return validation_results


__all__ = [
    "SOCEnergyGridScenario",
    "SOCTelcoNetworkScenario", 
    "SOCIWaterSystemScenario",
    "create_energy_scenario",
    "create_telco_scenario",
    "create_water_scenario",
    "get_available_scenarios",
    "get_scenario_metadata",
    "create_scenario",
    "validate_all_scenarios",
    "SCENARIOS"
]
