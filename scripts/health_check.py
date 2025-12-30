#!/usr/bin/env python3
"""
Health Check Script for Autonomous Multi-Agent Red/Blue Team Simulation System

This script performs comprehensive health checks on the system to ensure
all components are functioning correctly.
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import argparse


class HealthChecker:
    """Health checker for the simulation system."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.issues = []
        self.warnings = []
        self.success_count = 0
        self.error_count = 0
        self.warning_count = 0
    
    def log_success(self, message: str):
        """Log a success message."""
        print(f"✅ {message}")
        self.success_count += 1
    
    def log_warning(self, message: str):
        """Log a warning message."""
        print(f"⚠️  {message}")
        self.warnings.append(message)
        self.warning_count += 1
    
    def log_error(self, message: str):
        """Log an error message."""
        print(f"❌ {message}")
        self.issues.append(message)
        self.error_count += 1
    
    def check_python_version(self) -> bool:
        """Check Python version compatibility."""
        print("\n🐍 Checking Python Version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.log_error(f"Python {version.major}.{version.minor} not supported. Requires Python 3.8+")
            return False
        
        self.log_success(f"Python {version.major}.{version.minor}.{version.micro} is supported")
        return True
    
    def check_project_structure(self) -> bool:
        """Check project structure."""
        print("\n📁 Checking Project Structure...")
        
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
            "examples",
            "docs",
            "scripts"
        ]
        
        all_good = True
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.log_success(f"Directory exists: {dir_name}")
            else:
                self.log_error(f"Missing directory: {dir_name}")
                all_good = False
        
        return all_good
    
    def check_required_files(self) -> bool:
        """Check required files."""
        print("\n📄 Checking Required Files...")
        
        required_files = [
            "main.py",
            "config.py",
            "requirements.txt",
            "README.md",
            "LICENSE",
            "CHANGELOG.md",
            "AGENT.md",
            "SECURITY.md",
            "ARCHITECTURE.md",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            ".env.example",
            "pyproject.toml",
            "Makefile"
        ]
        
        all_good = True
        for file_name in required_files:
            file_path = self.project_root / file_name
            if file_path.exists() and file_path.is_file():
                self.log_success(f"File exists: {file_name}")
            else:
                self.log_error(f"Missing file: {file_name}")
                all_good = False
        
        return all_good
    
    def check_python_syntax(self) -> bool:
        """Check Python syntax."""
        print("\n🐍 Checking Python Syntax...")
        
        python_files = list(self.project_root.glob("**/*.py"))
        python_files = [f for f in python_files if "__pycache__" not in str(f)]
        
        syntax_errors = []
        for py_file in python_files:
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                compile(content, str(py_file), 'exec')
            except SyntaxError as e:
                syntax_errors.append(f"{py_file}: {e}")
        
        if syntax_errors:
            self.log_error(f"Found {len(syntax_errors)} syntax errors:")
            for error in syntax_errors[:5]:  # Show first 5 errors
                self.log_error(f"  {error}")
            if len(syntax_errors) > 5:
                self.log_error(f"  ... and {len(syntax_errors) - 5} more")
            return False
        else:
            self.log_success(f"All {len(python_files)} Python files have valid syntax")
            return True
    
    def check_imports(self) -> bool:
        """Check Python imports."""
        print("\n📦 Checking Python Imports...")
        
        try:
            # Test core imports
            import config
            import scenarios
            from orchestration import SimulationCoordinator
            from agents.base_agent import BaseAgent
            
            self.log_success("Core imports successful")
            
            # Test scenario imports
            available_scenarios = scenarios.get_available_scenarios()
            self.log_success(f"Scenarios available: {len(available_scenarios)}")
            
            return True
        except ImportError as e:
            self.log_error(f"Import error: {e}")
            return False
        except Exception as e:
            self.log_error(f"Unexpected error during imports: {e}")
            return False
    
    def test_scenarios(self) -> bool:
        """Test scenario functionality."""
        print("\n🎭 Testing Scenarios...")
        
        try:
            import scenarios
            
            # Test scenario availability
            available_scenarios = scenarios.get_available_scenarios()
            if len(available_scenarios) < 3:
                self.log_error(f"Insufficient scenarios: {len(available_scenarios)} (minimum 3)")
                return False
            
            self.log_success(f"Scenarios available: {len(available_scenarios)}")
            
            # Test scenario validation
            all_validations = scenarios.validate_all_scenarios()
            invalid_scenarios = [name for name, validation in all_validations.items() 
                                if not validation["scenario_valid"]]
            
            if invalid_scenarios:
                self.log_error(f"Invalid scenarios: {invalid_scenarios}")
                return False
            
            self.log_success("All scenarios are valid")
            return True
            
        except Exception as e:
            self.log_error(f"Scenario test failed: {e}")
            return False
    
    def test_configuration(self) -> bool:
        """Test configuration."""
        print("\n⚙️ Testing Configuration...")
        
        try:
            from config import settings
            
            # Test key configuration values
            required_attrs = [
                "anthropic_api_key",
                "anthropic_model",
                "sqlite_db_path",
                "chroma_db_path",
                "enable_safety_checks",
                "simulation_mode_only"
            ]
            
            for attr in required_attrs:
                if not hasattr(settings, attr):
                    self.log_error(f"Missing configuration attribute: {attr}")
                    return False
                else:
                    value = getattr(settings, attr)
                    if attr == "anthropic_api_key" and not value:
                        self.log_warning(f"API key not set: {attr}")
                    else:
                        self.log_success(f"Configuration attribute {attr}: {value}")
            
            return True
            
        except Exception as e:
            self.log_error(f"Configuration test failed: {e}")
            return False
    
    def test_database_connectivity(self) -> bool:
        """Test database connectivity."""
        print("\n🗄️ Testing Database Connectivity...")
        
        try:
            from config import settings
            db_path = self.project_root / settings.sqlite_db_path
            
            # Test if database directory exists
            db_dir = db_path.parent
            if not db_dir.exists():
                self.log_warning(f"Database directory does not exist: {db_dir}")
                # Create directory for test
                db_dir.mkdir(parents=True, exist_ok=True)
            
            # Test database file creation
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            conn.execute("SELECT 1")
            conn.close()
            
            self.log_success(f"Database connectivity test passed: {db_path}")
            return True
            
        except Exception as e:
            self.log_error(f"Database connectivity test failed: {e}")
            return False
    
    def test_agent_creation(self) -> bool:
        """Test agent creation."""
        print("\n🤖 Testing Agent Creation...")
        
        try:
            from agents.base_agent import BaseAgent
            
            # Test base agent creation
            agent = BaseAgent(
                agent_id="test_agent",
                agent_type="test",
                system_prompt="Test prompt",
                tools=[],
                enable_mcp=False
            )
            
            if agent.agent_id != "test_agent":
                self.log_error("Agent ID not set correctly")
                return False
            
            if agent.agent_type != "test":
                self.log_error("Agent type not set correctly")
                return False
            
            self.log_success("Base agent creation test passed")
            return True
            
        except Exception as e:
            self.log_error(f"Agent creation test failed: {e}")
            return False
    
    def test_mcp_servers(self) -> bool:
        """Test MCP server functionality."""
        print("\n🔄 Testing MCP Servers...")
        
        try:
            from mcp_servers.mcp_server import MCPServer
            
            # Test server instantiation
            server = MCPServer(host="localhost", port=8080)
            
            if server.host != "localhost":
                self.log_error("MCP server host not set correctly")
                return False
            
            if server.port != 8080:
                self.log_error("MCP server port not set correctly")
                return False
            
            self.log_success("MCP server instantiation test passed")
            return True
            
        except Exception as e:
            self.log_error(f"MCP server test failed: {e}")
            return False
    
    def run_system_validation(self) -> bool:
        """Run standalone system validation."""
        print("\n🔍 Running System Validation...")
        
        try:
            from utils.validation_standalone import check_system_health
            
            result = check_system_health()
            
            if result["all_passed"]:
                self.log_success("System validation passed")
                return True
            else:
                self.log_error("System validation failed")
                return False
                
        except Exception as e:
            self.log_error(f"System validation failed: {e}")
            return False
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate health check report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy" if self.error_count == 0 else "unhealthy",
            "summary": {
                "success_count": self.success_count,
                "warning_count": self.warning_count,
                "error_count": self.error_count
            },
            "issues": self.issues,
            "warnings": self.warnings,
            "checks_performed": [
                "python_version",
                "project_structure",
                "required_files",
                "python_syntax",
                "imports",
                "scenarios",
                "configuration",
                "database_connectivity",
                "agent_creation",
                "mcp_servers",
                "system_validation"
            ]
        }
        
        return report
    
    def save_report(self, report: Dict[str, Any]) -> None:
        """Save health check report to file."""
        report_path = self.project_root / "health_check_report.json"
        
        try:
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            self.log_success(f"Health check report saved to: {report_path}")
        except Exception as e:
            self.log_error(f"Failed to save report: {e}")
    
    def print_summary(self) -> None:
        """Print health check summary."""
        print("\n" + "="*60)
        print("🏥 HEALTH CHECK SUMMARY")
        print("="*60)
        
        print(f"✅ Successful checks: {self.success_count}")
        print(f"⚠️  Warnings: {self.warning_count}")
        print(f"❌ Errors: {self.error_count}")
        
        if self.error_count == 0:
            print("\n🎉 SYSTEM IS HEALTHY AND READY FOR USE!")
        else:
            print(f"\n⚠️  SYSTEM HAS {self.error_count} ISSUES THAT NEED ATTENTION")
        
        if self.warnings > 0:
            print(f"\n⚠️  {self.warning_count} warnings were found - review recommended")
        
        print("\n" + "="*60)


def main():
    """Main function for health check script."""
    parser = argparse.ArgumentParser(
        description="Health Check Script for Autonomous Multi-Agent Red/Blue Team Simulation System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate health check report"
    )
    
    parser.add_argument(
        "--output",
        default="health_check_report.json",
        help="Output file for health check report"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    print("🏥 AUTONOMOUS MULTI-AGENT RED/BLUE TEAM SIMULATION SYSTEM")
    print("🔍 HEALTH CHECK")
    print("="*60)
    
    # Create health checker
    checker = HealthChecker()
    
    # Run all health checks
    checks = [
        ("Python Version", checker.check_python_version),
        ("Project Structure", checker.check_project_structure),
        ("Required Files", checker.check_required_files),
        ("Python Syntax", checker.check_python_syntax),
        ("Imports", checker.check_imports),
        ("Scenarios", checker.test_scenarios),
        ("Configuration", checker.test_configuration),
        ("Database Connectivity", checker.test_database_connectivity),
        ("Agent Creation", checker.test_agent_creation),
        ("MCP Servers", checker.test_mcp_servers),
        ("System Validation", checker.run_system_validation)
    ]
    
    # Execute checks
    for check_name, check_func in checks:
        if args.verbose:
            print(f"\n🔍 Running {check_name}...")
        check_func()
    
    # Generate and save report if requested
    if args.report:
        report = checker.generate_report()
        checker.save_report(report)
        print(f"\n📊 Report saved to: {args.output}")
    
    # Print summary
    checker.print_summary()


if __name__ == "__main__":
    main()
