#!/usr/bin/env python3
"""
Basic Simulation Example

This example demonstrates how to run a basic simulation using the
Autonomous Multi-Agent Red/Blue Team Simulation System.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestration import SimulationCoordinator
from utils.logging_handler import get_logger, setup_logging


async def run_basic_simulation():
    """Run a basic simulation example."""

    # Setup logging
    setup_logging()
    logger = get_logger(__name__)

    logger.info("Starting basic simulation example")

    # Create coordinator
    coordinator = SimulationCoordinator()

    try:
        # Initialize simulation
        logger.info("Initializing simulation with energy grid scenario")
        await coordinator.initialize_simulation("soci_energy_grid")

        # Run simulation for 5 minutes (300 seconds)
        logger.info("Running simulation for 5 minutes")
        await coordinator.run_simulation(timeout_minutes=5)

        # Generate report
        logger.info("Generating simulation report")
        report_path = await coordinator.generate_report()

        logger.info(f"Simulation completed! Report saved to: {report_path}")

        # Print summary
        status = coordinator.get_simulation_status()
        print(f"\n🎯 Simulation Summary:")
        print(f"  Scenario: {status['scenario_name']}")
        print(f"  Duration: {status['start_time']} to present")
        print(f"  Final Phase: {status['current_phase']}")
        print(f"  Red Team Score: {status['red_team_score']}")
        print(f"  Blue Team Score: {status['blue_team_score']}")
        print(f"  Attack Events: {len(status['attack_timeline'])}")
        print(f"  Defense Events: {len(status['defense_timeline'])}")
        print(f"  MITRE Techniques: {len(status['mitre_techniques_used'])}")

    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        raise
    finally:
        # Cleanup
        logger.info("Cleaning up simulation resources")
        await coordinator.cleanup()


async def run_custom_scenario():
    """Run a custom scenario with specific configuration."""

    logger = get_logger(__name__)
    logger.info("Running custom scenario example")

    # Create coordinator
    coordinator = SimulationCoordinator()

    try:
        # Initialize with telecom scenario
        await coordinator.initialize_simulation("soci_telco_network")

        # Run for 3 minutes
        await coordinator.run_simulation(timeout_minutes=3)

        # Generate report
        report_path = await coordinator.generate_report()
        logger.info(f"Custom scenario completed! Report: {report_path}")

    except Exception as e:
        logger.error(f"Custom scenario failed: {e}")
        raise
    finally:
        await coordinator.cleanup()


def main():
    """Main function for the basic simulation example."""

    print("🚀 Autonomous Multi-Agent Red/Blue Team Simulation System")
    print("=" * 60)
    print("Basic Simulation Example")
    print("=" * 60)

    # Choose simulation type
    import typer

    app = typer.Typer()

    @app.command()
    def basic():
        """Run basic energy grid simulation."""
        asyncio.run(run_basic_simulation())

    @app.command()
    def custom():
        """Run custom telecom scenario."""
        asyncio.run(run_custom_scenario())

    @app.command()
    def water():
        """Run water system scenario."""

        async def run_water_scenario():
            coordinator = SimulationCoordinator()
            try:
                await coordinator.initialize_simulation("soci_water_system")
                await coordinator.run_simulation(timeout_minutes=3)
                report_path = await coordinator.generate_report()
                print(f"Water scenario completed! Report: {report_path}")
            finally:
                await coordinator.cleanup()

        asyncio.run(run_water_scenario())

    @app.command()
    def validate():
        """Validate system configuration."""
        from utils.validation_standalone import check_system_health

        print("🔍 Validating system health...")
        result = check_system_health()

        if result["all_passed"]:
            print("✅ System is healthy and ready!")
        else:
            print("❌ System has issues that need to be addressed.")

        print(f"📊 Statistics: {result['statistics']}")

    if len(sys.argv) > 1:
        app()
    else:
        # Default to basic simulation
        asyncio.run(run_basic_simulation())


if __name__ == "__main__":
    main()
