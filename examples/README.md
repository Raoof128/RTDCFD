# Examples Directory

This directory contains examples demonstrating how to use and extend the Autonomous Multi-Agent Red/Blue Team Simulation System.

## 📁 Available Examples

### 1. Basic Simulation (`basic_simulation.py`)
**Purpose**: Demonstrates how to run a basic simulation with the system.

**Features**:
- Energy grid scenario execution
- Telecom scenario execution
- Water system scenario execution
- System validation
- Report generation

**Usage**:
```bash
# Run basic energy grid simulation
python examples/basic_simulation.py basic

# Run custom telecom scenario
python examples/basic_simulation.py custom

# Run water system scenario
python examples/basic_simulation.py water

# Validate system configuration
python examples/basic_simulation.py validate
```

### 2. Custom Agent (`custom_agent.py`)
**Purpose**: Shows how to create and integrate custom agents.

**Features**:
- Custom agent implementation
- Specialized tools (pattern recognition, report generation, data transformation)
- Command handling and processing
- MCP communication integration
- Agent capabilities and summary

**Usage**:
```bash
# Run custom agent example
python examples/custom_agent.py
```

### 3. Scenario Customization (`scenario_customization.py`)
**Purpose**: Demonstrates how to create custom scenarios.

**Features**:
- Custom scenario class implementation
- Critical assets definition
- Attack vectors configuration
- Defensive measures setup
- Compliance requirements
- Validation and integration

**Usage**:
```bash
# Run scenario customization example
python examples/scenario_customization.py
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- All project dependencies installed
- Anthropic API key configured

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Validate installation
python main.py --validate-config
```

## 📋 Example Structure

Each example follows this structure:
- **Header**: Example description and purpose
- **Features**: List of demonstrated features
- **Usage**: Command-line usage examples
- **Code**: Complete, runnable code
- **Comments**: Detailed inline documentation

## 🎯 Learning Path

### 1. Start with Basic Simulation
```bash
python examples/basic_simulation.py
```
This will show you:
- How to initialize the simulation coordinator
- How to run different scenarios
- How to generate reports
- How to monitor simulation progress

### 2. Create Custom Agents
```bash
python examples/custom_agent.py
```
This will teach you:
- How to extend the base agent class
- How to create custom tools
- How to handle agent commands
- How to integrate with MCP communication

### 3. Design Custom Scenarios
```bash
python examples/scenario_customization.py
```
This will demonstrate:
- How to structure scenario classes
- How to define critical assets
- How to configure attack vectors
- How to set up defensive measures
- How to validate scenarios

## 🔧 Advanced Examples

### Creating Multi-Agent Workflows
```python
# Example: Multi-agent coordination
from orchestration import SimulationCoordinator

async def multi_agent_workflow():
    coordinator = SimulationCoordinator()
    
    # Initialize with custom scenario
    await coordinator.initialize_simulation("custom_critical_infrastructure")
    
    # Run with extended timeout
    await coordinator.run_simulation(timeout_minutes=120)
    
    # Generate comprehensive report
    report_path = await coordinator.generate_report()
    return report_path
```

### Custom Tool Development
```python
# Example: Custom tool implementation
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class CustomTool(BaseTool):
    name = "custom_tool"
    description = "Custom tool for specific tasks"
    
    def _run(self, input_data: str) -> str:
        # Custom logic here
        return f"Processed: {input_data}"
```

### Scenario Integration
```python
# Example: Register custom scenario
from scenarios import SCENARIOS

SCENARIOS["custom_scenario"] = {
    "class": CustomScenario,
    "factory": create_custom_scenario,
    "metadata": {
        "name": "custom_scenario",
        "display_name": "Custom Critical Infrastructure",
        "description": "Custom scenario demonstration",
        "sector": "critical_infrastructure",
        "difficulty": "advanced"
    }
}
```

## 📊 Monitoring and Debugging

### Logging Configuration
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use structured logging
from utils.logging_handler import get_logger
logger = get_logger(__name__)
logger.info("Example message")
```

### Performance Monitoring
```python
# Monitor agent performance
import time

start_time = time.time()
# ... agent execution ...
end_time = time.time()
logger.info(f"Execution time: {end_time - start_time:.2f}s")
```

### Error Handling
```python
try:
    # Simulation code
    await coordinator.run_simulation()
except Exception as e:
    logger.error(f"Simulation failed: {e}")
    raise
```

## 🔒 Security Considerations

### Simulation-Only Policy
All examples follow the simulation-only policy:
- No real network scanning
- No actual exploitation
- No functional malicious code
- Educational focus only

### Input Validation
```python
# Validate user input
def validate_input(user_input: str) -> bool:
    """Validate user input for safety."""
    # Add validation logic here
    return len(user_input) > 0 and len(user_input) < 1000
```

### Output Sanitization
```python
# Sanitize agent output
def sanitize_output(output: str) -> str:
    """Sanitize agent output for safety."""
    # Remove potentially harmful content
    return output.replace("rm -rf", "[COMMAND_REMOVED]")
```

## 📚 Best Practices

### Code Quality
- Follow PEP 8 for Python code
- Use type hints for all functions
- Add comprehensive docstrings
- Include error handling
- Write unit tests

### Security
- Validate all inputs
- Sanitize all outputs
- Use secure communication protocols
- Follow Australian compliance requirements

### Performance
- Use async/await for I/O operations
- Implement proper error handling
- Monitor resource usage
- Optimize database queries

### Documentation
- Provide clear usage examples
- Include inline comments
- Document custom components
- Update README files

## 🤝 Contributing

### Adding New Examples
1. Create a new Python file in `examples/`
2. Follow the established structure
3. Include comprehensive documentation
4. Add usage examples
5. Test the example thoroughly
6. Update this README

### Example Template
```python
#!/usr/bin/env python3
"""
Example Title

Brief description of what this example demonstrates.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import required modules
# ... your imports here ...

def main():
    """Main function for the example."""
    # ... your code here ...
    print("Example completed successfully!")

if __name__ == "__main__":
    main()
```

## 🔗 Integration with Main System

### Running Examples with Main System
```bash
# Run example with main system
python examples/basic_simulation.py

# Then use main system
python main.py --scenario soci_energy_grid
```

### Extending Main System
```python
# Import examples in main.py
from examples.custom_agent import CustomAgent
from examples.scenario_customization import create_custom_scenario

# Use in main system
coordinator.agents["custom"] = CustomAgent()
```

## 📞 Support

### Getting Help
- Check the main README.md for general information
- Review the API documentation for technical details
- Look at the source code for implementation details
- Run `python main.py --help` for command options

### Reporting Issues
- Create an issue on GitHub
- Include error messages and stack traces
- Provide steps to reproduce
- Suggest potential solutions

---

These examples are designed to help you understand and extend the Autonomous Multi-Agent Red/Blue Team Simulation System. Start with the basic simulation example and gradually explore more advanced features as you become more familiar with the system.
