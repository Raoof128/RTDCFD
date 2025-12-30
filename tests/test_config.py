"""
Test configuration for the Autonomous Multi-Agent Red/Blue Team Simulation System
"""

import pytest
import sys
from pathlib import Path
import os

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings, AgentConfig, ScenarioConfig, MITREConfig


class TestConfig:
    """Test suite for configuration settings."""
    
    def test_settings_initialization(self):
        """Test settings initialization."""
        assert settings is not None
        assert hasattr(settings, 'anthropic_model')
        assert hasattr(settings, 'sqlite_db_path')
        assert hasattr(settings, 'mcp_server_host')
        assert hasattr(settings, 'dashboard_port')
    
    def test_default_values(self):
        """Test default configuration values."""
        assert settings.anthropic_model == "claude-3-5-sonnet-20241022"
        assert settings.sqlite_db_path == "storage/simulation.db"
        assert settings.chroma_db_path == "storage/vector_db"
        assert settings.mcp_server_host == "localhost"
        assert settings.mcp_server_port == 8080
        assert settings.mcp_red_team_port == 8081
        assert settings.mcp_blue_team_port == 8082
        assert settings.dashboard_host == "localhost"
        assert settings.dashboard_port == 8501
    
    def test_agent_config_constants(self):
        """Test agent configuration constants."""
        assert AgentConfig.RED_TEAM_RECON == "recon_agent"
        assert AgentConfig.RED_TEAM_SOCIAL_ENGINEERING == "social_engineering_agent"
        assert AgentConfig.RED_TEAM_EXPLOITATION == "exploitation_agent"
        assert AgentConfig.RED_TEAM_LATERAL_MOVEMENT == "lateral_movement_agent"
        
        assert AgentConfig.BLUE_TEAM_DETECTION == "detection_agent"
        assert AgentConfig.BLUE_TEAM_RESPONSE == "response_agent"
        assert AgentConfig.BLUE_TEAM_THREAT_INTEL == "threat_intel_agent"
        
        assert AgentConfig.MAX_MEMORY_TURNS == 20
        assert AgentConfig.TOOL_EXECUTION_TIMEOUT == 30
        assert AgentConfig.RESPONSE_MAX_TOKENS == 2000
    
    def test_scenario_config_constants(self):
        """Test scenario configuration constants."""
        assert ScenarioConfig.ENERGY_GRID_DISRUPTION == "soci_energy_grid"
        assert ScenarioConfig.TELECOM_NETWORK_COMPROMISE == "soci_telco_network"
        assert ScenarioConfig.WATER_SYSTEM_INTRUSION == "soci_water_system"
        
        # Attack stages
        assert ScenarioConfig.RECONNAISSANCE == "reconnaissance"
        assert ScenarioConfig.INITIAL_ACCESS == "initial_access"
        assert ScenarioConfig.EXECUTION == "execution"
        assert ScenarioConfig.PERSISTENCE == "persistence"
        assert ScenarioConfig.PRIVILEGE_ESCALATION == "privilege_escalation"
        assert ScenarioConfig.DEFENSE_EVASION == "defense_evasion"
        assert ScenarioConfig.CREDENTIAL_ACCESS == "credential_access"
        assert ScenarioConfig.DISCOVERY == "discovery"
        assert ScenarioConfig.LATERAL_MOVEMENT == "lateral_movement"
        assert ScenarioConfig.COLLECTION == "collection"
        assert ScenarioConfig.COMMAND_CONTROL == "command_control"
        assert ScenarioConfig.EXFILTRATION == "exfiltration"
        assert ScenarioConfig.IMPACT == "impact"
    
    def test_mitre_config_constants(self):
        """Test MITRE configuration constants."""
        assert MITREConfig.ATTACK_DATA_URL == "https://attack.mitre.org/techniques/enterprise/"
        assert MITREConfig.LOCAL_ATTACK_DATA_PATH == "data/mitre_attack_data.json"
        assert MITREConfig.TECHNIQUE_MAPPING_CACHE_PATH == "data/technique_mapping_cache.json"
        
        # Tactic lists
        assert len(MITREConfig.RECONNAISSANCE_TACTICS) > 0
        assert "TA0043" in MITREConfig.RECONNAISSANCE_TACTICS
        assert len(MITREConfig.INITIAL_ACCESS_TACTICS) > 0
        assert "TA0001" in MITREConfig.INITIAL_ACCESS_TACTICS
        assert len(MITREConfig.EXECUTION_TACTICS) > 0
        assert "TA0002" in MITREConfig.EXECUTION_TACTICS
    
    def test_soci_sectors(self):
        """Test SOCI critical sectors configuration."""
        expected_sectors = ["energy", "telecommunications", "water", "transport"]
        assert settings.soci_critical_sectors == expected_sectors
    
    def test_safety_settings(self):
        """Test safety and security settings."""
        assert settings.enable_safety_checks is True
        assert settings.simulation_mode_only is True
        assert settings.audit_logging is True
    
    def test_agent_limits(self):
        """Test agent configuration limits."""
        assert settings.max_agents_per_team == 10
        assert settings.agent_timeout_seconds == 300
        assert settings.conversation_memory_limit == 50
    
    def test_scenario_settings(self):
        """Test scenario configuration settings."""
        assert settings.scenario_timeout_minutes == 60
        assert settings.max_attack_stages == 10
    
    def test_logging_settings(self):
        """Test logging configuration."""
        assert settings.log_level == "INFO"
        assert settings.log_file == "logs/simulation.log"
        assert settings.enable_console_output is True
    
    def test_dashboard_settings(self):
        """Test dashboard configuration."""
        assert settings.refresh_interval_seconds == 2
        assert isinstance(settings.dashboard_port, int)
        assert settings.dashboard_port > 0
    
    def test_project_paths_exist(self):
        """Test that project paths are properly configured."""
        from config import PROJECT_ROOT, DATA_DIR, LOGS_DIR, REPORTS_DIR, STORAGE_DIR
        
        assert PROJECT_ROOT.exists()
        assert DATA_DIR.exists()
        assert LOGS_DIR.exists()
        assert REPORTS_DIR.exists()
        assert STORAGE_DIR.exists()
    
    def test_environment_variable_handling(self):
        """Test environment variable handling."""
        # Test that environment variables can be loaded
        # This is a basic test - in practice, you'd set env vars and test loading
        assert hasattr(settings, 'model_config')
        assert 'env_file' in settings.model_config
        assert 'env_file_encoding' in settings.model_config
    
    def test_configuration_completeness(self):
        """Test that all required configuration sections are present."""
        required_attrs = [
            'anthropic_api_key', 'anthropic_model', 'sqlite_db_path', 'chroma_db_path',
            'max_agents_per_team', 'agent_timeout_seconds', 'conversation_memory_limit',
            'mcp_server_host', 'mcp_server_port', 'mcp_red_team_port', 'mcp_blue_team_port',
            'scenario_timeout_minutes', 'max_attack_stages', 'log_level', 'log_file',
            'dashboard_host', 'dashboard_port', 'refresh_interval_seconds',
            'enable_safety_checks', 'simulation_mode_only', 'audit_logging',
            'soci_critical_sectors', 'asd_essential_eight_enabled', 'privacy_act_compliance'
        ]
        
        for attr in required_attrs:
            assert hasattr(settings, attr), f"Missing required configuration: {attr}"
    
    def test_configuration_types(self):
        """Test configuration value types."""
        assert isinstance(settings.anthropic_model, str)
        assert isinstance(settings.sqlite_db_path, str)
        assert isinstance(settings.max_agents_per_team, int)
        assert isinstance(settings.agent_timeout_seconds, int)
        assert isinstance(settings.mcp_server_port, int)
        assert isinstance(settings.scenario_timeout_minutes, int)
        assert isinstance(settings.enable_safety_checks, bool)
        assert isinstance(settings.simulation_mode_only, bool)
        assert isinstance(settings.audit_logging, bool)
        assert isinstance(settings.soci_critical_sectors, list)
    
    def test_port_ranges(self):
        """Test that port numbers are in valid ranges."""
        assert 1024 <= settings.mcp_server_port <= 65535
        assert 1024 <= settings.mcp_red_team_port <= 65535
        assert 1024 <= settings.mcp_blue_team_port <= 65535
        assert 1024 <= settings.dashboard_port <= 65535
        
        # Ensure ports are different
        assert settings.mcp_server_port != settings.mcp_red_team_port
        assert settings.mcp_server_port != settings.mcp_blue_team_port
        assert settings.mcp_red_team_port != settings.mcp_blue_team_port


if __name__ == "__main__":
    pytest.main([__file__])
