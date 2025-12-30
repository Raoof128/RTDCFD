"""
Test scenarios for the Autonomous Multi-Agent Red/Blue Team Simulation System
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scenarios import (
    get_available_scenarios,
    get_scenario_metadata,
    create_scenario,
    validate_all_scenarios
)


class TestScenarios:
    """Test suite for scenario functionality."""
    
    def test_get_available_scenarios(self):
        """Test getting list of available scenarios."""
        scenarios = get_available_scenarios()
        
        assert isinstance(scenarios, list)
        assert len(scenarios) >= 3
        assert "soci_energy_grid" in scenarios
        assert "soci_telco_network" in scenarios
        assert "soci_water_system" in scenarios
    
    def test_get_scenario_metadata(self):
        """Test getting scenario metadata."""
        metadata = get_scenario_metadata("soci_energy_grid")
        
        assert isinstance(metadata, dict)
        assert "name" in metadata
        assert "display_name" in metadata
        assert "sector" in metadata
        assert "difficulty" in metadata
        assert metadata["sector"] == "energy"
        assert metadata["red_team_agents"] == 4
        assert metadata["blue_team_agents"] == 3
    
    def test_create_energy_scenario(self):
        """Test creating energy grid scenario."""
        scenario = create_scenario("soci_energy_grid")
        
        assert scenario is not None
        assert scenario.scenario_name == "soci_energy_grid"
        assert hasattr(scenario, 'critical_assets')
        assert hasattr(scenario, 'attack_vectors')
        assert hasattr(scenario, 'defensive_measures')
    
    def test_create_telco_scenario(self):
        """Test creating telecommunications scenario."""
        scenario = create_scenario("soci_telco_network")
        
        assert scenario is not None
        assert scenario.scenario_name == "soci_telco_network"
        assert scenario.scenario_version == "1.0"
        assert len(scenario.critical_assets) >= 5
    
    def test_create_water_scenario(self):
        """Test creating water system scenario."""
        scenario = create_scenario("soci_water_system")
        
        assert scenario is not None
        assert scenario.scenario_name == "soci_water_system"
        assert scenario.scenario_version == "1.0"
        assert len(scenario.attack_vectors) >= 5
    
    def test_validate_energy_scenario(self):
        """Test energy scenario validation."""
        scenario = create_scenario("soci_energy_grid")
        validation = scenario.validate_scenario()
        
        assert isinstance(validation, dict)
        assert "scenario_valid" in validation
        assert "validation_errors" in validation
        assert "warnings" in validation
        assert "recommendations" in validation
        assert validation["scenario_valid"] is True
    
    def test_validate_telco_scenario(self):
        """Test telecommunications scenario validation."""
        scenario = create_scenario("soci_telco_network")
        validation = scenario.validate_scenario()
        
        assert isinstance(validation, dict)
        assert validation["scenario_valid"] is True
        assert len(validation["validation_errors"]) == 0
    
    def test_validate_water_scenario(self):
        """Test water system scenario validation."""
        scenario = create_scenario("soci_water_system")
        validation = scenario.validate_scenario()
        
        assert isinstance(validation, dict)
        assert validation["scenario_valid"] is True
        assert len(validation["validation_errors"]) == 0
    
    def test_validate_all_scenarios(self):
        """Test validating all scenarios."""
        results = validate_all_scenarios()
        
        assert isinstance(results, dict)
        assert len(results) >= 3
        
        for scenario_name, validation in results.items():
            assert isinstance(validation, dict)
            assert "scenario_valid" in validation
            assert validation["scenario_valid"] is True
    
    def test_scenario_config_completeness(self):
        """Test scenario configuration completeness."""
        for scenario_name in get_available_scenarios():
            scenario = create_scenario(scenario_name)
            config = scenario.get_scenario_config()
            
            assert isinstance(config, dict)
            assert "scenario_metadata" in config
            assert "critical_assets" in config
            assert "attack_vectors" in config
            assert "defensive_measures" in config
            assert "success_criteria" in config
            assert "compliance_requirements" in config
            assert "simulation_parameters" in config
    
    def test_mitre_technique_coverage(self):
        """Test MITRE ATT&CK technique coverage in scenarios."""
        for scenario_name in get_available_scenarios():
            scenario = create_scenario(scenario_name)
            
            # Collect all MITRE techniques
            all_techniques = set()
            for vector in scenario.attack_vectors:
                techniques = vector.get("mitre_techniques", [])
                all_techniques.update(techniques)
            
            assert len(all_techniques) >= 5, f"Scenario {scenario_name} should have at least 5 MITRE techniques"
    
    def test_compliance_requirements(self):
        """Test compliance requirements presence."""
        for scenario_name in get_available_scenarios():
            scenario = create_scenario(scenario_name)
            compliance = scenario.compliance_requirements
            
            assert "soci_act_requirements" in compliance
            assert "asd_essential_eight" in compliance
            assert "reporting_obligations" in compliance
    
    def test_critical_assets_structure(self):
        """Test critical assets have required structure."""
        for scenario_name in get_available_scenarios():
            scenario = create_scenario(scenario_name)
            
            for asset_id, asset in scenario.critical_assets.items():
                assert "type" in asset
                assert "criticality" in asset
                assert "function" in asset
                assert "protocols" in asset
                assert "vulnerabilities" in asset
                assert "impact_if_compromised" in asset
    
    def test_attack_vectors_structure(self):
        """Test attack vectors have required structure."""
        for scenario_name in get_available_scenarios():
            scenario = create_scenario(scenario_name)
            
            for vector in scenario.attack_vectors:
                assert "vector_id" in vector
                assert "name" in vector
                assert "attack_stage" in vector
                assert "mitre_techniques" in vector
                assert "description" in vector
                assert "likelihood" in vector
                assert "impact" in vector
    
    def test_defensive_measures_structure(self):
        """Test defensive measures have required structure."""
        for scenario_name in get_available_scenarios():
            scenario = create_scenario(scenario_name)
            
            for measure in scenario.defensive_measures:
                assert "measure_id" in measure
                assert "name" in measure
                assert "essential_eight" in measure
                assert "description" in measure
                assert "effectiveness" in measure
                assert "coverage" in measure


if __name__ == "__main__":
    pytest.main([__file__])
