"""
Tests for standalone validation utilities
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.validation_standalone import (
    validate_python_version,
    validate_directory_structure,
    validate_required_files,
    validate_scenario_files,
    validate_agent_files,
    validate_mcp_server_files,
    validate_dashboard_files,
    validate_python_syntax,
    validate_documentation_quality,
    validate_configuration_files,
    check_system_health
)


class TestValidationStandalone:
    """Test suite for standalone validation utilities."""
    
    def test_validate_python_version(self):
        """Test Python version validation."""
        result = validate_python_version()
        assert isinstance(result, bool)
        assert result is True  # Should pass on current system
    
    def test_validate_directory_structure(self):
        """Test directory structure validation."""
        result = validate_directory_structure()
        assert isinstance(result, bool)
        assert result is True  # Should pass as we created all directories
    
    def test_validate_required_files(self):
        """Test required files validation."""
        result = validate_required_files()
        assert isinstance(result, bool)
        assert result is True  # Should pass as we created all files
    
    def test_validate_scenario_files(self):
        """Test scenario files validation."""
        result = validate_scenario_files()
        assert isinstance(result, bool)
        assert result is True  # Should pass as we created scenario files
    
    def test_validate_agent_files(self):
        """Test agent files validation."""
        result = validate_agent_files()
        assert isinstance(result, bool)
        assert result is True  # Should pass as we created agent files
    
    def test_validate_mcp_server_files(self):
        """Test MCP server files validation."""
        result = validate_mcp_server_files()
        assert isinstance(result, bool)
        assert result is True  # Should pass as we created MCP files
    
    def test_validate_dashboard_files(self):
        """Test dashboard files validation."""
        result = validate_dashboard_files()
        assert isinstance(result, bool)
        assert result is True  # Should pass as we created dashboard files
    
    def test_validate_python_syntax(self):
        """Test Python syntax validation."""
        result = validate_python_syntax()
        assert isinstance(result, bool)
        assert result is True  # Should pass as all files have valid syntax
    
    def test_validate_documentation_quality(self):
        """Test documentation quality validation."""
        result = validate_documentation_quality()
        assert isinstance(result, bool)
        assert result is True  # Should pass as we have good documentation
    
    def test_validate_configuration_files(self):
        """Test configuration files validation."""
        result = validate_configuration_files()
        assert isinstance(result, bool)
        assert result is True  # Should pass as we have proper config files
    
    def test_check_system_health(self):
        """Test comprehensive system health check."""
        result = check_system_health()
        assert isinstance(result, dict)
        assert "all_passed" in result
        assert "validations" in result
        assert "statistics" in result
        
        # Should pass all validations
        assert result["all_passed"] is True
    
    def test_project_statistics(self):
        """Test project statistics generation."""
        from utils.validation_standalone import get_project_statistics
        
        stats = get_project_statistics()
        assert isinstance(stats, dict)
        
        required_keys = ["python_files", "total_lines", "directories", "components"]
        for key in required_keys:
            assert key in stats
        
        # Check that we have substantial implementation
        assert stats["python_files"] >= 30
        assert stats["total_lines"] >= 5000
        assert stats["directories"] >= 10
    
    def test_validation_return_types(self):
        """Test that validation functions return correct types."""
        assert isinstance(validate_python_version(), bool)
        assert isinstance(validate_directory_structure(), bool)
        assert isinstance(validate_required_files(), bool)
        assert isinstance(validate_scenario_files(), bool)
        assert isinstance(validate_agent_files(), bool)
        assert isinstance(validate_mcp_server_files(), bool)
        assert isinstance(validate_dashboard_files(), bool)
        assert isinstance(validate_python_syntax(), bool)
        assert isinstance(validate_documentation_quality(), bool)
        assert isinstance(validate_configuration_files(), bool)
    
    def test_validation_error_handling(self):
        """Test that validation functions handle errors gracefully."""
        # All validation functions should handle errors gracefully
        # and return False rather than raising exceptions
        try:
            validate_python_version()
            validate_directory_structure()
            validate_required_files()
            validate_scenario_files()
            validate_agent_files()
            validate_mcp_server_files()
            validate_dashboard_files()
            validate_python_syntax()
            validate_documentation_quality()
            validate_configuration_files()
        except Exception as e:
            pytest.fail(f"Validation function raised unexpected exception: {e}")
    
    def test_validation_completeness(self):
        """Test that all expected validations are available."""
        expected_validations = [
            validate_python_version,
            validate_directory_structure,
            validate_required_files,
            validate_scenario_files,
            validate_agent_files,
            validate_mcp_server_files,
            validate_dashboard_files,
            validate_python_syntax,
            validate_documentation_quality,
            validate_configuration_files
        ]
        
        # All should be callable functions
        for validation in expected_validations:
            assert callable(validation), f"{validation.__name__} is not callable"
    
    def test_system_health_structure(self):
        """Test system health check structure."""
        health = check_system_health()
        
        assert isinstance(health, dict)
        assert "all_passed" in health
        assert "validations" in health
        assert "statistics" in health
        
        validations = health["validations"]
        assert isinstance(validations, dict)
        
        # Should have results for all validations
        expected_keys = [
            "Python Version",
            "Directory Structure", 
            "Required Files",
            "Scenario Files",
            "Agent Files",
            "MCP Server Files",
            "Dashboard Files",
            "Python Syntax",
            "Documentation Quality",
            "Configuration Files"
        ]
        
        for key in expected_keys:
            assert key in validations
            assert isinstance(validations[key], bool)


if __name__ == "__main__":
    pytest.main([__file__])
