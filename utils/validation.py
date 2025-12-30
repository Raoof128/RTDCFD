"""
Validation utilities for the Autonomous Multi-Agent Red/Blue Team Simulation System.

Provides configuration validation, scenario validation, and system health checks.
"""

import os
import sys
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import PROJECT_ROOT, settings
from utils.logging_handler import get_logger

logger = get_logger(__name__)


def validate_anthropic_api_key() -> bool:
    """Validate that Anthropic API key is available."""
    api_key = settings.anthropic_api_key

    if not api_key:
        logger.error("ANTHROPIC_API_KEY not found in environment variables")
        return False

    if not api_key.startswith("sk-ant-"):
        logger.error("ANTHROPIC_API_KEY format appears invalid")
        return False

    logger.info("✅ Anthropic API key validation passed")
    return True


def validate_python_version() -> bool:
    """Validate Python version compatibility."""
    version = sys.version_info

    if version.major < 3 or version.minor < 8:
        logger.error(
            f"Python {version.major}.{version.minor} not supported. Requires Python 3.8+"
        )
        return False

    logger.info(
        f"✅ Python version validation passed: {version.major}.{version.minor}.{version.micro}"
    )
    return True


def validate_required_packages() -> bool:
    """Validate that required packages are installed."""
    required_packages = [
        "langchain",
        "langchain_anthropic",
        "anthropic",
        "streamlit",
        "pydantic",
        "requests",
        "numpy",
        "pandas",
    ]

    missing_packages = []

    for package in required_packages:
        try:
            spec = find_spec(package.replace("-", "_"))
            if spec is None:
                missing_packages.append(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        logger.error(f"Missing required packages: {', '.join(missing_packages)}")
        logger.info("Install with: pip install -r requirements.txt")
        return False

    logger.info("✅ Required packages validation passed")
    return True


def validate_directory_structure() -> bool:
    """Validate that required directories exist."""
    required_dirs = [
        "agents",
        "agents/red_team",
        "agents/blue_team",
        "orchestration",
        "mcp_servers",
        "scenarios",
        "mitre_integration",
        "utils",
        "dashboard",
        "storage",
        "logs",
        "reports",
        "tests",
        "data",
        "scripts",
    ]

    missing_dirs = []

    for dir_path in required_dirs:
        full_path = PROJECT_ROOT / dir_path
        if not full_path.exists():
            missing_dirs.append(dir_path)

    if missing_dirs:
        logger.error(f"Missing required directories: {', '.join(missing_dirs)}")
        return False

    logger.info("✅ Directory structure validation passed")
    return True


def validate_configuration() -> bool:
    """
    Validate the complete system configuration.

    Returns:
        True if all validations pass, False otherwise
    """
    logger.info("Starting configuration validation...")

    validations = [
        ("Python Version", validate_python_version),
        ("Required Packages", validate_required_packages),
        ("Anthropic API Key", validate_anthropic_api_key),
        ("Directory Structure", validate_directory_structure),
    ]

    all_passed = True

    for name, validator in validations:
        logger.info(f"Validating {name}...")
        try:
            if not validator():
                all_passed = False
        except Exception as e:
            logger.error(f"Validation failed for {name}: {e}")
            all_passed = False

    if all_passed:
        logger.info("🎉 All configuration validations passed!")
    else:
        logger.error("❌ Configuration validation failed!")

    return all_passed


def list_available_scenarios() -> List[str]:
    """
    List all available SOCI Act scenarios.

    Returns:
        List of scenario names
    """
    scenarios_dir = PROJECT_ROOT / "scenarios"

    if not scenarios_dir.exists():
        logger.warning(f"Scenarios directory not found: {scenarios_dir}")
        return []

    scenario_files = list(scenarios_dir.glob("*.py"))
    scenarios = []

    for file_path in scenario_files:
        if file_path.name != "__init__.py":
            scenario_name = file_path.stem
            scenarios.append(scenario_name)

    logger.info(f"Found {len(scenarios)} scenarios: {', '.join(scenarios)}")
    return scenarios


def validate_scenario(scenario_name: str) -> bool:
    """
    Validate a specific scenario.

    Args:
        scenario_name: Name of the scenario to validate

    Returns:
        True if scenario is valid, False otherwise
    """
    scenario_path = PROJECT_ROOT / "scenarios" / f"{scenario_name}.py"

    if not scenario_path.exists():
        logger.error(f"Scenario file not found: {scenario_path}")
        return False

    try:
        # Try to import the scenario module
        spec = find_spec(f"scenarios.{scenario_name}")
        if spec is None:
            logger.error(f"Could not import scenario module: scenarios.{scenario_name}")
            return False

        logger.info(f"✅ Scenario validation passed: {scenario_name}")
        return True

    except Exception as e:
        logger.error(f"Scenario validation failed for {scenario_name}: {e}")
        return False


def check_system_health() -> Dict[str, Any]:
    """
    Perform a comprehensive system health check.

    Returns:
        Dictionary containing health status information
    """
    health_status = {
        "timestamp": str(Path(__file__).stat().st_mtime),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "project_root": str(PROJECT_ROOT),
        "checks": {},
    }

    # Configuration validation
    health_status["checks"]["configuration"] = validate_configuration()

    # Available scenarios
    health_status["checks"]["scenarios"] = {
        "available": list_available_scenarios(),
        "count": len(list_available_scenarios()),
    }

    # Directory permissions
    health_status["checks"]["directories"] = {}
    for dir_name in ["storage", "logs", "reports"]:
        dir_path = PROJECT_ROOT / dir_name
        health_status["checks"]["directories"][dir_name] = {
            "exists": dir_path.exists(),
            "writable": os.access(dir_path, os.W_OK) if dir_path.exists() else False,
        }

    # Environment variables
    health_status["checks"]["environment"] = {
        "anthropic_api_key_set": bool(settings.anthropic_api_key),
        "simulation_mode_only": settings.simulation_mode_only,
        "safety_checks_enabled": settings.enable_safety_checks,
    }

    return health_status


def print_system_health() -> None:
    """Print a formatted system health report."""
    health = check_system_health()

    print("\n" + "=" * 60)
    print("SYSTEM HEALTH REPORT")
    print("=" * 60)

    print(f"Python Version: {health['python_version']}")
    print(f"Project Root: {health['project_root']}")
    print(
        f"Configuration: {'✅ OK' if health['checks']['configuration'] else '❌ FAILED'}"
    )

    scenarios = health["checks"]["scenarios"]
    print(
        f"Scenarios: {scenarios['count']} available ({', '.join(scenarios['available'])})"
    )

    print("\nDirectory Status:")
    for dir_name, status in health["checks"]["directories"].items():
        status_str = "✅" if status["exists"] and status["writable"] else "❌"
        print(f"  {dir_name}/: {status_str}")

    print("\nEnvironment:")
    env = health["checks"]["environment"]
    print(f"  API Key Set: {'✅' if env['anthropic_api_key_set'] else '❌'}")
    print(f"  Simulation Mode: {'✅' if env['simulation_mode_only'] else '❌'}")
    print(f"  Safety Checks: {'✅' if env['safety_checks_enabled'] else '❌'}")

    print("=" * 60)


def validate_mitre_attack_data() -> bool:
    """
    Validate MITRE ATT&CK data availability.

    Returns:
        True if ATT&CK data is available, False otherwise
    """
    attack_data_path = PROJECT_ROOT / "data" / "mitre_attack_data.json"

    if not attack_data_path.exists():
        logger.warning("MITRE ATT&CK data file not found. Will download on first run.")
        return True  # Not an error, will be downloaded

    try:
        import json

        with open(attack_data_path, "r") as f:
            data = json.load(f)

        # Basic validation of data structure
        if not isinstance(data, dict) or "objects" not in data:
            logger.error("MITRE ATT&CK data file appears corrupted")
            return False

        techniques = [
            obj for obj in data["objects"] if obj.get("type") == "attack-pattern"
        ]
        logger.info(
            f"✅ MITRE ATT&CK data validated: {len(techniques)} techniques loaded"
        )
        return True

    except Exception as e:
        logger.error(f"Error validating MITRE ATT&CK data: {e}")
        return False
