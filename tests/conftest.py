"""
Pytest configuration and fixtures for the Autonomous Multi-Agent Red/Blue Team Simulation System
"""

import pytest
import sys
from pathlib import Path

# Add project root to Python path for all tests
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root():
    """Fixture providing the project root path."""
    return project_root


@pytest.fixture(scope="session")
def test_scenarios():
    """Fixture providing test scenario names."""
    return [
        "soci_energy_grid",
        "soci_telco_network", 
        "soci_water_system"
    ]


@pytest.fixture(scope="session")
def mock_api_key():
    """Fixture providing a mock API key for testing."""
    return "test-api-key-123456789"


@pytest.fixture
def sample_scenario_config():
    """Fixture providing sample scenario configuration."""
    return {
        "scenario_metadata": {
            "name": "test_scenario",
            "version": "1.0",
            "sector": "test",
            "soci_act_applicable": True
        },
        "critical_assets": {
            "test_asset": {
                "type": "test_system",
                "criticality": "high",
                "function": "test_function",
                "protocols": ["test_protocol"],
                "vulnerabilities": ["test_vulnerability"],
                "impact_if_compromised": "test_impact"
            }
        },
        "attack_vectors": [
            {
                "vector_id": "test_001",
                "name": "Test Attack",
                "attack_stage": "initial_access",
                "mitre_techniques": ["T0001"],
                "description": "Test attack description",
                "likelihood": "medium",
                "impact": "high"
            }
        ],
        "defensive_measures": [
            {
                "measure_id": "test_dm001",
                "name": "Test Defense",
                "essential_eight": "application_control",
                "description": "Test defense description",
                "effectiveness": "high",
                "coverage": ["test_system"]
            }
        ]
    }


@pytest.fixture
def mock_agent_state():
    """Fixture providing mock agent state."""
    return {
        "agent_id": "test_agent_001",
        "agent_type": "test_agent",
        "status": "active",
        "current_task": "test_task",
        "memory_count": 5,
        "last_activity": "2025-12-31T07:00:00",
        "tools_available": ["test_tool"],
        "metrics": {"tasks_completed": 3}
    }


@pytest.fixture
def mock_simulation_state():
    """Fixture providing mock simulation state."""
    return {
        "simulation_id": "test_sim_001",
        "scenario_name": "test_scenario",
        "phase": "initialization",
        "start_time": "2025-12-31T07:00:00",
        "agents_active": {"agent1": {}, "agent2": {}},
        "red_team_score": 10,
        "blue_team_score": 5,
        "attack_timeline": [],
        "defense_timeline": [],
        "simulation_complete": False
    }


@pytest.fixture
def mock_mitre_techniques():
    """Fixture providing mock MITRE ATT&CK techniques."""
    return [
        "T1592",  # Gather Victim Org Information
        "T1566",  # Phishing
        "T1203",  # Exploitation for Client Execution
        "T1021",  # Remote Services
        "T1059",  # Command and Scripting Interpreter
        "T1078",  # Valid Accounts
        "T1133",  # Valid Accounts
        "T1190",  # Exploit Public-Facing Application
        "T1210",  # Exploitation of Remote Services
        "T1547",  # Boot or Logon Autostart Execution
    ]


@pytest.fixture
def sample_agent_message():
    """Fixture providing sample agent message."""
    return {
        "id": "test_msg_001",
        "sender_id": "test_agent_001",
        "receiver_id": "test_agent_002",
        "message_type": "command",
        "content": {"task": "test_task", "parameters": {}},
        "timestamp": "2025-12-31T07:00:00",
        "priority": "normal",
        "requires_response": False
    }


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Setup test environment for all tests."""
    # Mock environment variables
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-for-testing")
    monkeypatch.setenv("SIMULATION_MODE_ONLY", "true")
    monkeypatch.setenv("ENABLE_SAFETY_CHECKS", "true")
    
    # Mock logging to reduce test output
    import logging
    logging.getLogger().setLevel(logging.CRITICAL)


@pytest.fixture
def temp_config_file(tmp_path, mock_api_key):
    """Create a temporary configuration file for testing."""
    config_file = tmp_path / "test_config.py"
    config_content = f'''
import os
from pathlib import Path

# Test configuration
ANTHROPIC_API_KEY = "{mock_api_key}"
SQLITE_DB_PATH = "test_simulation.db"
CHROMA_DB_PATH = "test_vector_db"

# Test paths
PROJECT_ROOT = Path("{project_root}")
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"
STORAGE_DIR = PROJECT_ROOT / "storage"

# Ensure directories exist
for directory in [DATA_DIR, LOGS_DIR, REPORTS_DIR, STORAGE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
'''
    
    config_file.write_text(config_content)
    return config_file


# Custom markers for different test categories
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual components"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests for component interactions"
    )
    config.addinivalue_line(
        "markers", "scenario: Tests for scenario functionality"
    )
    config.addinivalue_line(
        "markers", "validation: Tests for validation utilities"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer to run"
    )
    config.addinivalue_line(
        "markers", "network: Tests that require network access"
    )


# Test collection hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on file location
        if "test_scenarios.py" in str(item.fspath):
            item.add_marker(pytest.mark.scenario)
        elif "test_config.py" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "test_validation.py" in str(item.fspath):
            item.add_marker(pytest.mark.validation)
        
        # Add slow marker for tests that might take longer
        if "validate_all_scenarios" in str(item.name):
            item.add_marker(pytest.mark.slow)


# Test session configuration
def pytest_sessionstart(session):
    """Configure test session."""
    # Set up any global test configuration
    pass


def pytest_sessionfinish(session, exitstatus):
    """Clean up after test session."""
    # Clean up any global test state
    pass
