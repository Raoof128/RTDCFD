"""
Standalone validation utilities that don't require complex imports.
This module provides validation functions that can be tested independently.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List


def validate_python_version() -> bool:
    """Validate Python version compatibility."""
    version = sys.version_info

    if version.major < 3 or version.minor < 8:
        print(
            f"Python {version.major}.{version.minor} not supported. Requires Python 3.8+"
        )
        return False

    print(
        f"✅ Python version validation passed: {version.major}.{version.minor}.{version.micro}"
    )
    return True


def validate_directory_structure() -> bool:
    """Validate that required directories exist."""
    project_root = Path(".")
    required_dirs = [
        "agents",
        "agents/red_team",
        "agents/blue_team",
        "orchestration",
        "mcp_servers",
        "scenarios",
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
        full_path = project_root / dir_path
        if not full_path.exists():
            missing_dirs.append(dir_path)

    if missing_dirs:
        print(f"❌ Missing required directories: {', '.join(missing_dirs)}")
        return False

    print("✅ Directory structure validation passed")
    return True


def validate_required_files() -> bool:
    """Validate that required files exist."""
    project_root = Path(".")

    # Check for basic Python files
    python_files = ["config.py", "main.py"]

    # Check for documentation files
    doc_files = ["README.md", "AGENT.md", "CHANGELOG.md"]

    # Check for configuration files
    config_files = ["requirements.txt", ".env.example"]

    all_files = python_files + doc_files + config_files
    missing_files = []

    for file_path in all_files:
        full_path = project_root / file_path
        if not full_path.exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False

    print("✅ Required files validation passed")
    return True


def validate_scenario_files() -> bool:
    """Validate that scenario files exist."""
    scenarios_dir = Path("scenarios")

    if not scenarios_dir.exists():
        print("❌ Scenarios directory not found")
        return False

    required_scenarios = [
        "soci_energy_grid.py",
        "soci_telco_network.py",
        "soci_water_system.py",
    ]

    missing_scenarios = []

    for scenario_file in required_scenarios:
        full_path = scenarios_dir / scenario_file
        if not full_path.exists():
            missing_scenarios.append(scenario_file)

    if missing_scenarios:
        print(f"❌ Missing scenario files: {', '.join(missing_scenarios)}")
        return False

    print("✅ Scenario files validation passed")
    return True


def validate_agent_files() -> bool:
    """Validate that agent files exist."""
    project_root = Path(".")

    # Red team agents
    red_team_agents = [
        "agents/red_team/recon_agent.py",
        "agents/red_team/social_engineering_agent.py",
        "agents/red_team/exploitation_agent.py",
        "agents/red_team/lateral_movement_agent.py",
    ]

    # Blue team agents
    blue_team_agents = [
        "agents/blue_team/detection_agent.py",
        "agents/blue_team/response_agent.py",
        "agents/blue_team/threat_intel_agent.py",
    ]

    all_agents = red_team_agents + blue_team_agents
    missing_agents = []

    for agent_file in all_agents:
        full_path = project_root / agent_file
        if not full_path.exists():
            missing_agents.append(agent_file)

    if missing_agents:
        print(f"❌ Missing agent files: {', '.join(missing_agents)}")
        return False

    print("✅ Agent files validation passed")
    return True


def validate_mcp_server_files() -> bool:
    """Validate that MCP server files exist."""
    project_root = Path(".")

    mcp_files = [
        "mcp_servers/mcp_server.py",
        "mcp_servers/red_team_mcp.py",
        "mcp_servers/blue_team_mcp.py",
    ]

    missing_mcp = []

    for mcp_file in mcp_files:
        full_path = project_root / mcp_file
        if not full_path.exists():
            missing_mcp.append(mcp_file)

    if missing_mcp:
        print(f"❌ Missing MCP server files: {', '.join(missing_mcp)}")
        return False

    print("✅ MCP server files validation passed")
    return True


def validate_dashboard_files() -> bool:
    """Validate that dashboard files exist."""
    project_root = Path(".")

    dashboard_files = ["dashboard/streamlit_ui.py"]

    missing_dashboard = []

    for dashboard_file in dashboard_files:
        full_path = project_root / dashboard_file
        if not full_path.exists():
            missing_dashboard.append(dashboard_file)

    if missing_dashboard:
        print(f"❌ Missing dashboard files: {', '.join(missing_dashboard)}")
        return False

    print("✅ Dashboard files validation passed")
    return True


def validate_python_syntax() -> bool:
    """Validate Python file syntax."""
    project_root = Path(".")
    python_files = list(project_root.glob("**/*.py"))

    syntax_errors = []

    for py_file in python_files:
        # Skip __pycache__ directories
        if "__pycache__" in str(py_file):
            continue

        try:
            with open(py_file, "r") as f:
                content = f.read()
            compile(content, str(py_file), "exec")
        except SyntaxError as e:
            syntax_errors.append(f"{py_file}: {e}")

    if syntax_errors:
        print("❌ Python syntax errors found:")
        for error in syntax_errors:
            print(f"  {error}")
        return False

    print("✅ Python syntax validation passed")
    return True


def validate_documentation_quality() -> bool:
    """Validate documentation quality."""
    project_root = Path(".")

    doc_files = {
        "README.md": "Main documentation",
        "AGENT.md": "Development guidelines",
        "CHANGELOG.md": "Project changelog",
    }

    issues = []

    for doc_file, description in doc_files.items():
        full_path = project_root / doc_file
        if not full_path.exists():
            issues.append(f"Missing {description}: {doc_file}")
            continue

        try:
            with open(full_path, "r") as f:
                content = f.read()

            # Basic quality checks
            lines = len(content.split("\n"))
            words = len(content.split())

            if lines < 10:
                issues.append(f"{doc_file} too short: {lines} lines")

            if words < 50:
                issues.append(f"{doc_file} too brief: {words} words")

        except Exception as e:
            issues.append(f"Error reading {doc_file}: {e}")

    if issues:
        print("❌ Documentation quality issues:")
        for issue in issues:
            print(f"  {issue}")
        return False

    print("✅ Documentation quality validation passed")
    return True


def validate_configuration_files() -> bool:
    """Validate configuration files."""
    project_root = Path(".")

    config_files = {
        "requirements.txt": "Python dependencies",
        ".env.example": "Environment variables example",
    }

    issues = []

    for config_file, description in config_files.items():
        full_path = project_root / config_file
        if not full_path.exists():
            issues.append(f"Missing {description}: {config_file}")
            continue

        try:
            with open(full_path, "r") as f:
                content = f.read()

            lines = len(
                [
                    line
                    for line in content.split("\n")
                    if line.strip() and not line.startswith("#")
                ]
            )

            if lines < 3:
                issues.append(f"{config_file} has too few entries: {lines}")

        except Exception as e:
            issues.append(f"Error reading {config_file}: {e}")

    if issues:
        print("❌ Configuration file issues:")
        for issue in issues:
            print(f"  {issue}")
        return False

    print("✅ Configuration files validation passed")
    return True


def get_project_statistics() -> Dict[str, Any]:
    """Get comprehensive project statistics."""
    project_root = Path(".")

    # Count Python files
    python_files = list(project_root.glob("**/*.py"))
    python_files = [f for f in python_files if "__pycache__" not in str(f)]

    # Count lines of code
    total_lines = 0
    for py_file in python_files:
        try:
            with open(py_file, "r") as f:
                lines = len(f.readlines())
            total_lines += lines
        except:
            pass

    # Count directories
    dirs = [
        d for d in project_root.iterdir() if d.is_dir() and not d.name.startswith(".")
    ]

    # Component breakdown
    components = {
        "Red Team Agents": len(list(Path("agents/red_team").glob("*.py"))),
        "Blue Team Agents": len(list(Path("agents/blue_team").glob("*.py"))),
        "Scenarios": len(list(Path("scenarios").glob("*.py"))),
        "MCP Servers": len(list(Path("mcp_servers").glob("*.py"))),
        "Tests": len(list(Path("tests").glob("*.py"))),
    }

    return {
        "python_files": len(python_files),
        "total_lines": total_lines,
        "directories": len(dirs),
        "components": components,
    }


def check_system_health() -> Dict[str, Any]:
    """Perform comprehensive system health check."""
    print("🔍 Performing comprehensive system health check...")

    validations = [
        ("Python Version", validate_python_version),
        ("Directory Structure", validate_directory_structure),
        ("Required Files", validate_required_files),
        ("Scenario Files", validate_scenario_files),
        ("Agent Files", validate_agent_files),
        ("MCP Server Files", validate_mcp_server_files),
        ("Dashboard Files", validate_dashboard_files),
        ("Python Syntax", validate_python_syntax),
        ("Documentation Quality", validate_documentation_quality),
        ("Configuration Files", validate_configuration_files),
    ]

    results = {}
    all_passed = True

    for name, validator in validations:
        try:
            result = validator()
            results[name] = result
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ {name} validation failed with error: {e}")
            results[name] = False
            all_passed = False

    # Get project statistics
    stats = get_project_statistics()

    print(f"\n📊 Project Statistics:")
    print(f"  Python files: {stats['python_files']}")
    print(f"  Total lines: {stats['total_lines']:,}")
    print(f"  Directories: {stats['directories']}")

    print(f"\n📁 Component Breakdown:")
    for component, count in stats["components"].items():
        print(f"  {component}: {count}")

    print(f"\n🎯 Overall Health Status:")
    if all_passed:
        print("✅ ALL VALIDATIONS PASSED - System is healthy and ready!")
    else:
        print("⚠️  Some validations failed - review issues above")

    return {"all_passed": all_passed, "validations": results, "statistics": stats}


if __name__ == "__main__":
    check_system_health()
