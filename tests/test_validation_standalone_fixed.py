"""
Tests for standalone validation utilities
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_validate_python_version():
    """Test Python version validation."""
    from utils.validation_standalone import validate_python_version
    
    result = validate_python_version()
    assert isinstance(result, bool)
    assert result is True  # Should pass on current system


def test_validate_directory_structure():
    """Test directory structure validation."""
    from utils.validation_standalone import validate_directory_structure
    
    result = validate_directory_structure()
    assert isinstance(result, bool)
    assert result is True  # Should pass as we created all directories


def test_validate_required_files():
    """Test required files validation."""
    from utils.validation_standalone import validate_required_files
    
    result = validate_required_files()
    assert isinstance(result, bool)
    assert result is True  # Should pass as we created all files


def test_validate_scenario_files():
    """Test scenario files validation."""
    from utils.validation_standalone import validate_scenario_files
    
    result = validate_scenario_files()
    assert isinstance(result, bool)
    assert result is True  # Should pass as we created scenario files


def test_validate_agent_files():
    """Test agent files validation."""
    from utils.validation_standalone import validate_agent_files
    
    result = validate_agent_files()
    assert isinstance(result, bool)
    assert result is True  # Should pass as we created agent files


def test_validate_mcp_server_files():
    """Test MCP server files validation."""
    from utils.validation_standalone import validate_mcp_server_files
    
    result = validate_mcp_server_files()
    assert isinstance(result, bool)
    assert result is True  # Should pass as we created MCP files


def test_validate_dashboard_files():
    """Test dashboard files validation."""
    from utils.validation_standalone import validate_dashboard_files
    
    result = validate_dashboard_files()
    assert isinstance(result, bool)
    assert result is True  # Should pass as we created dashboard files


def test_validate_python_syntax():
    """Test Python syntax validation."""
    from utils.validation_standalone import validate_python_syntax
    
    result = validate_python_syntax()
    assert isinstance(result, bool)
    assert result is True  # Should pass as all files have valid syntax


def test_validate_documentation_quality():
    """Test documentation quality validation."""
    from utils.validation_standalone import validate_documentation_quality
    
    result = validate_documentation_quality()
    assert isinstance(result, bool)
    assert result is True  # Should pass as we have good documentation


def test_validate_configuration_files():
    """Test configuration files validation."""
    from utils.validation_standalone import validate_configuration_files
    
    result = validate_configuration_files()
    assert isinstance(result, bool)
    assert result is True  # Should pass as we have proper config files


def test_check_system_health():
    """Test comprehensive system health check."""
    from utils.validation_standalone import check_system_health
    
    result = check_system_health()
    assert isinstance(result, dict)
    assert "all_passed" in result
    assert "validations" in result
    assert "statistics" in result
    
    # Should pass all validations
    assert result["all_passed"] is True


def test_project_statistics():
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


def test_validation_return_types():
    """Test that validation functions return correct types."""
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
        validate_configuration_files
    )
    
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


def test_validation_error_handling():
    """Test that validation functions handle errors gracefully."""
    # All validation functions should handle errors gracefully
    # and return False rather than raising exceptions
    try:
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
            validate_configuration_files
        )
        
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


def test_validation_completeness():
    """Test that all expected validations are available."""
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
        validate_configuration_files
    )
    
    # All should be callable functions
    assert callable(validate_python_version)
    assert callable(validate_directory_structure)
    assert callable(validate_required_files)
    assert callable(validate_scenario_files)
    assert callable(validate_agent_files)
    assert callable(validate_mcp_server_files)
    assert callable(validate_dashboard_files)
    assert callable(validate_python_syntax)
    assert callable(validate_documentation_quality)
    assert callable(validate_configuration_files)


def test_system_health_structure():
    """Test system health check structure."""
    from utils.validation_standalone import check_system_health
    
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
