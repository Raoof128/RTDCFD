"""
Basic functionality tests that don't require complex imports
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestBasicFunctionality:
    """Test basic functionality without complex dependencies."""
    
    def test_project_structure(self):
        """Test that project structure exists."""
        project_root = Path(__file__).parent.parent
        
        required_dirs = [
            "agents",
            "agents/red_team",
            "agents/blue_team", 
            "orchestration",
            "mcp_servers",
            "scenarios",
            "utils",
            "dashboard",
            "tests",
            "storage",
            "logs",
            "reports"
        ]
        
        for dir_path in required_dirs:
            full_path = project_root / dir_path
            assert full_path.exists(), f"Missing directory: {dir_path}"
            assert full_path.is_dir(), f"Path is not a directory: {dir_path}"
    
    def test_required_files_exist(self):
        """Test that required files exist."""
        project_root = Path(__file__).parent.parent
        
        required_files = [
            "config.py",
            "main.py", 
            "requirements.txt",
            "README.md",
            "AGENT.md",
            "CHANGELOG.md",
            ".env.example"
        ]
        
        for file_path in required_files:
            full_path = project_root / file_path
            assert full_path.exists(), f"Missing file: {file_path}"
            assert full_path.is_file(), f"Path is not a file: {file_path}"
    
    def test_python_files_syntax(self):
        """Test that Python files have valid syntax."""
        project_root = Path(__file__).parent.parent
        
        python_files = list(project_root.glob("**/*.py"))
        
        for py_file in python_files:
            # Skip __pycache__ and test files that import complex modules
            if "__pycache__" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                compile(content, str(py_file), 'exec')
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {py_file}: {e}")
    
    def test_scenario_files_exist(self):
        """Test that scenario files exist."""
        project_root = Path(__file__).parent.parent
        scenarios_dir = project_root / "scenarios"
        
        required_scenarios = [
            "soci_energy_grid.py",
            "soci_telco_network.py",
            "soci_water_system.py"
        ]
        
        for scenario_file in required_scenarios:
            full_path = scenarios_dir / scenario_file
            assert full_path.exists(), f"Missing scenario file: {scenario_file}"
            assert full_path.is_file(), f"Path is not a file: {scenario_file}"
    
    def test_agent_files_exist(self):
        """Test that agent files exist."""
        project_root = Path(__file__).parent.parent
        
        # Red team agents
        red_team_agents = [
            "agents/red_team/recon_agent.py",
            "agents/red_team/social_engineering_agent.py", 
            "agents/red_team/exploitation_agent.py",
            "agents/red_team/lateral_movement_agent.py"
        ]
        
        # Blue team agents
        blue_team_agents = [
            "agents/blue_team/detection_agent.py",
            "agents/blue_team/response_agent.py",
            "agents/blue_team/threat_intel_agent.py"
        ]
        
        all_agents = red_team_agents + blue_team_agents
        
        for agent_file in all_agents:
            full_path = project_root / agent_file
            assert full_path.exists(), f"Missing agent file: {agent_file}"
            assert full_path.is_file(), f"Path is not a file: {agent_file}"
    
    def test_mcp_server_files_exist(self):
        """Test that MCP server files exist."""
        project_root = Path(__file__).parent.parent
        
        mcp_files = [
            "mcp_servers/mcp_server.py",
            "mcp_servers/red_team_mcp.py",
            "mcp_servers/blue_team_mcp.py"
        ]
        
        for mcp_file in mcp_files:
            full_path = project_root / mcp_file
            assert full_path.exists(), f"Missing MCP file: {mcp_file}"
            assert full_path.is_file(), f"Path is not a file: {mcp_file}"
    
    def test_dashboard_files_exist(self):
        """Test that dashboard files exist."""
        project_root = Path(__file__).parent.parent
        
        dashboard_files = [
            "dashboard/streamlit_ui.py"
        ]
        
        for dashboard_file in dashboard_files:
            full_path = project_root / dashboard_file
            assert full_path.exists(), f"Missing dashboard file: {dashboard_file}"
            assert full_path.is_file(), f"Path is not a file: {dashboard_file}"
    
    def test_init_files_exist(self):
        """Test that __init__.py files exist where needed."""
        project_root = Path(__file__).parent.parent
        
        init_files = [
            "agents/__init__.py",
            "agents/red_team/__init__.py",
            "agents/blue_team/__init__.py",
            "orchestration/__init__.py",
            "mcp_servers/__init__.py",
            "scenarios/__init__.py",
            "utils/__init__.py",
            "dashboard/__init__.py",
            "tests/__init__.py"
        ]
        
        for init_file in init_files:
            full_path = project_root / init_file
            assert full_path.exists(), f"Missing __init__.py file: {init_file}"
            assert full_path.is_file(), f"Path is not a file: {init_file}"
    
    def test_readme_content(self):
        """Test that README.md contains required sections."""
        project_root = Path(__file__).parent.parent
        readme_path = project_root / "README.md"
        
        with open(readme_path, 'r') as f:
            content = f.read()
        
        required_sections = [
            "# Autonomous Multi-Agent Red/Blue Team Simulation System",
            "## 🎯 Project Overview",
            "## 🏗️ Architecture",
            "## 🚀 Quick Start",
            "## 📋 Available Scenarios",
            "## 🤖 Agent Capabilities",
            "## 📊 Dashboard Features",
            "## 🛡️ Safety & Ethics",
            "## 📈 Compliance & Standards"
        ]
        
        for section in required_sections:
            assert section in content, f"Missing section in README: {section}"
    
    def test_agent_md_content(self):
        """Test that AGENT.md contains required sections."""
        project_root = Path(__file__).parent.parent
        agent_md_path = project_root / "AGENT.md"
        
        with open(agent_md_path, 'r') as f:
            content = f.read()
        
        required_sections = [
            "# Autonomous Multi-Agent Red/Blue Team Simulation System - Development Guidelines",
            "## Project Overview",
            "## Development Constraints",
            "## Safety & Ethics (CRITICAL)",
            "## Technical Standards",
            "## Architecture Constraints",
            "## Australian SOCI Act Integration"
        ]
        
        for section in required_sections:
            assert section in content, f"Missing section in AGENT.md: {section}"
    
    def test_changelog_content(self):
        """Test that CHANGELOG.md has proper structure."""
        project_root = Path(__file__).parent.parent
        changelog_path = project_root / "CHANGELOG.md"
        
        with open(changelog_path, 'r') as f:
            content = f.read()
        
        assert "# Changelog" in content
        assert "## Unreleased" in content
        assert "## [2025-12-31]" in content
    
    def test_requirements_content(self):
        """Test that requirements.txt contains required packages."""
        project_root = Path(__file__).parent.parent
        requirements_path = project_root / "requirements.txt"
        
        with open(requirements_path, 'r') as f:
            content = f.read()
        
        required_packages = [
            "langchain",
            "langchain-anthropic",
            "anthropic",
            "streamlit",
            "pydantic-settings",
            "pytest"
        ]
        
        for package in required_packages:
            assert package in content, f"Missing required package: {package}"
    
    def test_env_example_content(self):
        """Test that .env.example contains required variables."""
        project_root = Path(__file__).parent.parent
        env_example_path = project_root / ".env.example"
        
        with open(env_example_path, 'r') as f:
            content = f.read()
        
        required_vars = [
            "ANTHROPIC_API_KEY",
            "ENABLE_SAFETY_CHECKS",
            "SIMULATION_MODE_ONLY"
        ]
        
        for var in required_vars:
            assert var in content, f"Missing environment variable: {var}"
    
    def test_file_count(self):
        """Test that we have the expected number of Python files."""
        project_root = Path(__file__).parent.parent
        python_files = list(project_root.glob("**/*.py"))
        
        # Should have at least 25 Python files (excluding tests)
        non_test_files = [f for f in python_files if "tests" not in str(f)]
        
        assert len(non_test_files) >= 25, f"Expected at least 25 Python files, got {len(non_test_files)}"
    
    def test_code_line_count(self):
        """Test that we have substantial code implementation."""
        project_root = Path(__file__).parent.parent
        
        total_lines = 0
        python_files = list(project_root.glob("**/*.py"))
        
        for py_file in python_files:
            if "__pycache__" in str(py_file):
                continue
            try:
                with open(py_file, 'r') as f:
                    lines = len(f.readlines())
                total_lines += lines
            except:
                pass
        
        # Should have at least 5000 lines of code
        assert total_lines >= 5000, f"Expected at least 5000 lines of code, got {total_lines}"
    
    def test_project_name_consistency(self):
        """Test that project name is consistent across files."""
        project_root = Path(__file__).parent.parent
        
        # Check README
        with open(project_root / "README.md", 'r') as f:
            readme_content = f.read()
        
        # Check AGENT.md
        with open(project_root / "AGENT.md", 'r') as f:
            agent_content = f.read()
        
        project_name = "Autonomous Multi-Agent Red/Blue Team Simulation System"
        
        assert project_name in readme_content
        assert project_name in agent_content


if __name__ == "__main__":
    pytest.main([__file__])
