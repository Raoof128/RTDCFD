#!/usr/bin/env python3
"""
Autonomous Multi-Agent Red/Blue Team Simulation System

Main entry point for the agentic AI security testing framework.
This system simulates coordinated cyber attacks against Australian critical infrastructure
under the SOCI Act, with autonomous AI red team agents and defensive blue team agents.

Usage:
    python main.py --scenario soci_energy_grid --dashboard
    python main.py --list-scenarios
    python main.py --validate-config
"""

import asyncio
import argparse
import sys
from pathlib import Path
from typing import Optional

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import settings, PROJECT_ROOT
from utils.logging_handler import setup_logging, get_logger
from orchestration.coordinator import SimulationCoordinator
from utils.validation import validate_configuration, list_available_scenarios


logger = get_logger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Autonomous Multi-Agent Red/Blue Team Simulation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --scenario soci_energy_grid --dashboard
  %(prog)s --scenario soci_telco_network --headless
  %(prog)s --list-scenarios
  %(prog)s --validate-config
        """
    )
    
    parser.add_argument(
        "--scenario",
        type=str,
        help="SOCI Act scenario to run (energy_grid, telco_network, water_system)"
    )
    
    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Launch Streamlit dashboard for real-time monitoring"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run simulation without dashboard (console output only)"
    )
    
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="List all available SOCI Act scenarios"
    )
    
    parser.add_argument(
        "--validate-config",
        action="store_true",
        help="Validate configuration and environment"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=settings.log_level,
        help="Set logging level"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=settings.scenario_timeout_minutes,
        help="Scenario timeout in minutes"
    )
    
    return parser.parse_args()


async def run_simulation(scenario_name: str, dashboard: bool = False, timeout: int = 60) -> None:
    """
    Run the main simulation with specified scenario.
    
    Args:
        scenario_name: Name of the SOCI Act scenario to run
        dashboard: Whether to launch the dashboard
        timeout: Simulation timeout in minutes
    """
    logger.info(f"Starting simulation: {scenario_name}")
    logger.info(f"Dashboard enabled: {dashboard}")
    logger.info(f"Timeout: {timeout} minutes")
    
    # Initialize the simulation coordinator
    coordinator = SimulationCoordinator()
    
    try:
        # Initialize the simulation environment
        await coordinator.initialize_simulation(scenario_name)
        
        # Launch dashboard if requested
        if dashboard:
            logger.info("Launching Streamlit dashboard...")
            # Note: Dashboard runs in separate process
            import subprocess
            dashboard_cmd = [
                "streamlit", "run", 
                str(PROJECT_ROOT / "dashboard" / "streamlit_ui.py"),
                "--server.port", str(settings.dashboard_port),
                "--server.address", settings.dashboard_host
            ]
            subprocess.Popen(dashboard_cmd)
        
        # Run the simulation
        logger.info("Starting agent coordination...")
        await coordinator.run_simulation(timeout_minutes=timeout)
        
        # Generate final report
        logger.info("Generating final report...")
        report_path = await coordinator.generate_report()
        logger.info(f"Report generated: {report_path}")
        
    except KeyboardInterrupt:
        logger.info("Simulation interrupted by user")
    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        raise
    finally:
        # Cleanup
        await coordinator.cleanup()


def main() -> None:
    """Main entry point."""
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    setup_logging(
        log_level=args.log_level,
        log_file=settings.log_file,
        enable_console=settings.enable_console_output
    )
    
    logger.info("=" * 80)
    logger.info("Autonomous Multi-Agent Red/Blue Team Simulation System")
    logger.info("Australian SOCI Act Critical Infrastructure Security Testing")
    logger.info("=" * 80)
    
    try:
        # Handle utility commands
        if args.list_scenarios:
            scenarios = list_available_scenarios()
            print("\nAvailable SOCI Act Scenarios:")
            print("-" * 40)
            for scenario in scenarios:
                print(f"  • {scenario}")
            print("\nUsage: python main.py --scenario <scenario_name>")
            return
        
        if args.validate_config:
            validate_configuration()
            print("\n✅ Configuration validation passed")
            return
        
        # Validate required arguments
        if not args.scenario:
            print("Error: --scenario is required")
            print("Use --list-scenarios to see available options")
            sys.exit(1)
        
        # Validate scenario
        available_scenarios = list_available_scenarios()
        if args.scenario not in available_scenarios:
            print(f"Error: Unknown scenario '{args.scenario}'")
            print(f"Available scenarios: {', '.join(available_scenarios)}")
            sys.exit(1)
        
        # Check if dashboard or headless mode is specified
        if not args.dashboard and not args.headless:
            print("Error: Please specify either --dashboard or --headless")
            sys.exit(1)
        
        # Run the simulation
        asyncio.run(run_simulation(
            scenario_name=args.scenario,
            dashboard=args.dashboard,
            timeout=args.timeout
        ))
        
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
