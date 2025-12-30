"""
Configuration management for the Autonomous Multi-Agent Red/Blue Team Simulation System.

This module handles all configuration settings including:
- API keys and credentials
- Database connections
- Agent settings
- Scenario configurations
- Logging preferences
"""

import os
from typing import Dict, List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """Main application settings."""
    
    # API Configuration
    anthropic_api_key: str = Field(default="")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022")
    
    # Database Configuration
    sqlite_db_path: str = Field(default="storage/simulation.db")
    chroma_db_path: str = Field(default="storage/vector_db")
    
    # Agent Configuration
    max_agents_per_team: int = Field(default=10)
    agent_timeout_seconds: int = Field(default=300)
    conversation_memory_limit: int = Field(default=50)
    
    # MCP Server Configuration
    mcp_server_host: str = Field(default="localhost")
    mcp_server_port: int = Field(default=8080)
    mcp_red_team_port: int = Field(default=8081)
    mcp_blue_team_port: int = Field(default=8082)
    
    # Scenario Configuration
    scenario_timeout_minutes: int = Field(default=60)
    max_attack_stages: int = Field(default=10)
    
    # Logging Configuration
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="logs/simulation.log")
    enable_console_output: bool = Field(default=True)
    
    # Dashboard Configuration
    dashboard_host: str = Field(default="localhost")
    dashboard_port: int = Field(default=8501)
    refresh_interval_seconds: int = Field(default=2)
    
    # Safety and Security
    enable_safety_checks: bool = Field(default=True)
    simulation_mode_only: bool = Field(default=True)
    audit_logging: bool = Field(default=True)
    
    # Australian SOCI Act Settings
    soci_critical_sectors: List[str] = Field(
        default=["energy", "telecommunications", "water", "transport"]
    )
    asd_essential_eight_enabled: bool = Field(default=True)
    privacy_act_compliance: bool = Field(default=True)
    
    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class AgentConfig:
    """Configuration for individual agents."""
    
    # Red Team Agent Types
    RED_TEAM_RECON = "recon_agent"
    RED_TEAM_SOCIAL_ENGINEERING = "social_engineering_agent"
    RED_TEAM_EXPLOITATION = "exploitation_agent"
    RED_TEAM_LATERAL_MOVEMENT = "lateral_movement_agent"
    
    # Blue Team Agent Types
    BLUE_TEAM_DETECTION = "detection_agent"
    BLUE_TEAM_RESPONSE = "response_agent"
    BLUE_TEAM_THREAT_INTEL = "threat_intel_agent"
    
    # Common Agent Settings
    MAX_MEMORY_TURNS = 20
    TOOL_EXECUTION_TIMEOUT = 30
    RESPONSE_MAX_TOKENS = 2000


class ScenarioConfig:
    """Configuration for attack scenarios."""
    
    # SOCI Act Scenarios
    ENERGY_GRID_DISRUPTION = "soci_energy_grid"
    TELECOM_NETWORK_COMPROMISE = "soci_telco_network"
    WATER_SYSTEM_INTRUSION = "soci_water_system"
    
    # Attack Stages
    RECONNAISSANCE = "reconnaissance"
    INITIAL_ACCESS = "initial_access"
    EXECUTION = "execution"
    PERSISTENCE = "persistence"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    DEFENSE_EVASION = "defense_evasion"
    CREDENTIAL_ACCESS = "credential_access"
    DISCOVERY = "discovery"
    LATERAL_MOVEMENT = "lateral_movement"
    COLLECTION = "collection"
    COMMAND_CONTROL = "command_control"
    EXFILTRATION = "exfiltration"
    IMPACT = "impact"


class MITREConfig:
    """MITRE ATT&CK framework integration settings."""
    
    ATTACK_DATA_URL = "https://attack.mitre.org/techniques/enterprise/"
    LOCAL_ATTACK_DATA_PATH = "data/mitre_attack_data.json"
    TECHNIQUE_MAPPING_CACHE_PATH = "data/technique_mapping_cache.json"
    
    # TTP Categories
    RECONNAISSANCE_TACTICS = ["TA0043"]
    RESOURCE_DEVELOPMENT_TACTICS = ["TA0042"]
    INITIAL_ACCESS_TACTICS = ["TA0001"]
    EXECUTION_TACTICS = ["TA0002"]
    PERSISTENCE_TACTICS = ["TA0003"]
    PRIVILEGE_ESCALATION_TACTICS = ["TA0004"]
    DEFENSE_EVASION_TACTICS = ["TA0005"]
    CREDENTIAL_ACCESS_TACTICS = ["TA0006"]
    DISCOVERY_TACTICS = ["TA0007"]
    LATERAL_MOVEMENT_TACTICS = ["TA0008"]
    COLLECTION_TACTICS = ["TA0009"]
    COMMAND_CONTROL_TACTICS = ["TA0011"]
    EXFILTRATION_TACTICS = ["TA0010"]
    IMPACT_TACTICS = ["TA0040"]


# Global settings instance
settings = Settings()

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"
STORAGE_DIR = PROJECT_ROOT / "storage"

# Ensure directories exist
for directory in [DATA_DIR, LOGS_DIR, REPORTS_DIR, STORAGE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
