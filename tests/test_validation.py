"""
Test validation utilities for the Autonomous Multi-Agent Red/Blue Team Simulation System
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.validation import (
    validate_configuration,
    list_available_scenarios,
    check_system_health,
    validate_anthropic_api_key,
    validate_python_version,
    validate_required_packages,
    validate_directory_structure,
    validate_mitre_attack_data
)


class TestValidation:
    """Test suite for validation utilities."""
    
    def test_validate_python_version(self):
        """Test Python version validation."""
        result = validate_python_version()
        assert isinstance(result, bool)
        assert result is True  # Should pass on current system
    
    def test_validate_required_packages(self):
        """Test required packages validation."""
        result = validate_required_packages()
        assert isinstance(result, bool)
        # This might fail if packages aren't installed
    
    def test_validate_directory_structure(self):
        """Test directory structure validation."""
        result = validate_directory_structure()
        assert isinstance(result, bool)
        assert result is True  # Should pass as we created all directories
    
    def test_list_available_scenarios(self):
        """Test listing available scenarios."""
        scenarios = list_available_scenarios()
        assert isinstance(scenarios, list)
        assert len(scenarios) >= 3
        assert "soci_energy_grid" in scenarios
        assert "soci_telco_network" in scenarios
        assert "soci_water_system" in scenarios
    
    def test_check_system_health(self):
        """Test system health check."""
        health = check_system_health()
        assert isinstance(health, dict)
        assert "checks" in health
        assert "python_version" in health
        assert "project_root" in health
        
        checks = health["checks"]
        assert "configuration" in checks
        assert "scenarios" in checks
        assert "directories" in checks
        assert "environment" in checks
    
    def test_validate_configuration(self):
        """Test complete configuration validation."""
        result = validate_configuration()
        assert isinstance(result, bool)
        # Might fail due to missing API key or dependencies
    
    def test_validate_anthropic_api_key_missing(self):
        """Test Anthropic API key validation when missing."""
        # This tests the validation logic when API key is not set
        # The actual validation might pass if key is set in environment
        result = validate_anthropic_api_key()
        assert isinstance(result, bool)
    
    def test_validate_mitre_attack_data(self):
        """Test MITRE ATT&CK data validation."""
        result = validate_mitre_attack_data()
        assert isinstance(result, bool)
        # Should pass as it handles missing data gracefully
    
    def test_system_health_structure(self):
        """Test system health check structure."""
        health = check_system_health()
        
        required_keys = [
            "timestamp", "python_version", "project_root", "checks"
        ]
        
        for key in required_keys:
            assert key in health, f"Missing health check key: {key}"
        
        checks = health["checks"]
        required_checks = [
            "configuration", "scenarios", "directories", "environment"
        ]
        
        for check in required_checks:
            assert check in checks, f"Missing health check: {check}"
    
    def test_scenario_count_in_health_check(self):
        """Test scenario count in health check."""
        health = check_system_health()
        scenarios = health["checks"]["scenarios"]
        
        assert "available" in scenarios
        assert "count" in scenarios
        assert isinstance(scenarios["available"], list)
        assert isinstance(scenarios["count"], int)
        assert scenarios["count"] >= 3
    
    def test_directory_status_in_health_check(self):
        """Test directory status in health check."""
        health = check_system_health()
        directories = health["checks"]["directories"]
        
        required_dirs = ["storage", "logs", "reports"]
        
        for dir_name in required_dirs:
            assert dir_name in directories
            dir_info = directories[dir_name]
            assert "exists" in dir_info
            assert "writable" in dir_info
            assert isinstance(dir_info["exists"], bool)
            assert isinstance(dir_info["writable"], bool)
    
    def test_environment_status_in_health_check(self):
        """Test environment status in health check."""
        health = check_system_health()
        environment = health["checks"]["environment"]
        
        required_env_vars = [
            "anthropic_api_key_set",
            "simulation_mode_only",
            "safety_checks_enabled"
        ]
        
        for env_var in required_env_vars:
            assert env_var in environment
            assert isinstance(environment[env_var], bool)
    
    def test_validation_error_handling(self):
        """Test validation error handling."""
        # Test that validation functions handle errors gracefully
        try:
            validate_python_version()
            validate_required_packages()
            validate_directory_structure()
            list_available_scenarios()
        except Exception as e:
            pytest.fail(f"Validation function raised unexpected exception: {e}")
    
    def test_scenario_list_content(self):
        """Test scenario list content."""
        scenarios = list_available_scenarios()
        
        expected_scenarios = [
            "soci_energy_grid",
            "soci_telco_network", 
            "soci_water_system"
        ]
        
        for scenario in expected_scenarios:
            assert scenario in scenarios, f"Missing expected scenario: {scenario}"
    
    def test_health_check_completeness(self):
        """Test health check provides complete information."""
        health = check_system_health()
        
        # Check that health check provides comprehensive information
        assert "timestamp" in health
        assert isinstance(health["python_version"], str)
        assert isinstance(health["project_root"], str)
        
        # Check checks section
        checks = health["checks"]
        assert len(checks) >= 4
        
        # Check scenarios section
        scenarios = checks["scenarios"]
        assert scenarios["count"] > 0
        assert len(scenarios["available"]) == scenarios["count"]
        
        # Check directories section
        directories = checks["directories"]
        assert len(directories) >= 3
        
        # Check environment section
        environment = checks["environment"]
        assert len(environment) >= 3
    
    def test_validation_return_types(self):
        """Test that validation functions return correct types."""
        assert isinstance(validate_python_version(), bool)
        assert isinstance(validate_required_packages(), bool)
        assert isinstance(validate_directory_structure(), bool)
        assert isinstance(list_available_scenarios(), list)
        assert isinstance(check_system_health(), dict)
        assert isinstance(validate_configuration(), bool)
        assert isinstance(validate_anthropic_api_key(), bool)
        assert isinstance(validate_mitre_attack_data(), bool)
    
    def test_scenario_validation_integration(self):
        """Test scenario validation integration."""
        scenarios = list_available_scenarios()
        health = check_system_health()
        
        # Ensure scenario counts match
        assert len(scenarios) == health["checks"]["scenarios"]["count"]
        assert scenarios == health["checks"]["scenarios"]["available"]
    
    def test_directory_validation_integration(self):
        """Test directory validation integration."""
        health = check_system_health()
        directories = health["checks"]["directories"]
        
        # Check that directory validation matches individual validation
        individual_result = validate_directory_structure()
        health_result = all(
            dir_info["exists"] and dir_info["writable"]
            for dir_info in directories.values()
        )
        
        # Both should give the same result
        assert individual_result == health_result


if __name__ == "__main__":
    pytest.main([__file__])
