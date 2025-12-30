# Installation Guide

This guide will help you install and set up the Autonomous Multi-Agent Red/Blue Team Simulation System on your system.

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 10GB available disk space
- **Network**: Internet connection for LLM API access

### Recommended Requirements
- **Python**: 3.10 or higher
- **Memory**: 8GB RAM or more
- **Storage**: 20GB available disk space
- **Network**: Stable internet connection
- **CPU**: Multi-core processor recommended

### Supported Operating Systems
- **Linux**: Ubuntu 20.04+, CentOS 8+, Debian 11+
- **macOS**: macOS 11+ (Intel/Apple Silicon)
- **Windows**: Windows 10+ (WSL2 recommended)

## 🚀 Installation Methods

### Method 1: Standard Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/your-org/autonomous-multi-agent-simulation.git
cd autonomous-multi-agent-simulation
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

#### 4. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit environment file
nano .env
```

Add your Anthropic API key:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

#### 5. Verify Installation
```bash
# Validate configuration
python main.py --validate-config

# Test basic functionality
python -c "import scenarios; print('Scenarios available:', scenarios.get_available_scenarios())"
```

### Method 2: Docker Installation

#### 1. Pull Docker Image
```bash
docker pull autonomous-multi-agent-simulation:latest
```

#### 2. Run with Docker
```bash
# Create data directory
mkdir -p data logs reports storage

# Run the container
docker run -d \
  --name simulation \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/storage:/app/storage \
  -e ANTHROPIC_API_KEY \
  autonomous-multi-agent-simulation
```

#### 3. Access Dashboard
Open your browser to `http://localhost:8501`

### Method 3: Development Installation

#### 1. Install Development Tools
```bash
# Install development dependencies
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install
```

#### 2. Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov=orchestration --cov=utils --cov=scenarios --cov=dashboard --cov=mcp_servers
```

#### 3. Run Quality Checks
```bash
# Run linting
make lint

# Run security checks
make security

# Run all quality checks
make quality
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional
LOG_LEVEL=INFO
ENABLE_CONSOLE_OUTPUT=true
SIMULATION_MODE_ONLY=true
ENABLE_SAFETY_CHECKS=true
AUDIT_LOGGING=true

# Database Configuration
SQLITE_DB_PATH=storage/simulation.db
CHROMA_DB_PATH=storage/vector_db

# Server Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8080
MCP_RED_TEAM_PORT=8081
MCP_BLUE_TEAM_PORT=8082

# Dashboard Configuration
DASHBOARD_HOST=localhost
DASHBOARD_PORT=8501
REFRESH_INTERVAL_SECONDS=2

# Agent Configuration
MAX_AGENTS_PER_TEAM=10
AGENT_TIMEOUT_SECONDS=300
CONVERSATION_MEMORY_LIMIT=50

# Scenario Configuration
SCENARIO_TIMEOUT_MINUTES=60
MAX_ATTACK_STAGES=10
```

### Configuration Files

#### Main Configuration (`config.py`)
The main configuration file contains system-wide settings. You can modify these values to customize the system behavior.

#### Agent Configuration
Agent-specific configurations are defined in the agent classes. Modify the agent classes to change behavior.

#### Scenario Configuration
Scenario configurations are defined in the scenario classes. Create new scenarios by extending the base scenario class.

## 🔧 Verification

### System Health Check
```bash
# Run comprehensive validation
python main.py --validate-config

# Run standalone validation
python -c "from utils.validation_standalone import check_system_health; check_system_health()"
```

### Test Suite
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_scenarios.py
pytest tests/test_basic_functionality.py
pytest tests/test_config.py

# Run with coverage
pytest --cov=agents --cov=orchestration --cov=utils --cov=scenarios --cov=dashboard --cov=mcp_servers --cov-report=html
```

### Quality Checks
```bash
# Run all quality checks
make quality

# Run individual checks
make lint
make format
make security
```

## 🚀 Quick Start

### Run Your First Simulation
```bash
# List available scenarios
python main.py --list-scenarios

# Run energy grid simulation
python main.py --scenario soci_energy_grid

# Run with dashboard
python main.py --scenario soci_energy_grid --dashboard
```

### Start Dashboard Only
```bash
# Start Streamlit dashboard
streamlit run dashboard/streamlit_ui.py
```

### Run Custom Examples
```bash
# Run basic simulation example
python examples/basic_simulation.py

# Run custom agent example
python examples/custom_agent.py

# Run scenario customization example
python examples/scenario_customization.py
```

## 🐛 Troubleshooting

### Common Issues

#### Installation Issues

**Problem**: `ModuleNotFoundError: No module named 'langchain'`
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
```

**Problem**: `ImportError: cannot import name 'ModelProfile'`
```bash
# Solution: Update langchain packages
pip install --upgrade langchain langchain-anthropic langchain-community
```

**Problem**: `Permission denied` when accessing files
```bash
# Solution: Check file permissions
ls -la .env
chmod 600 .env
```

#### Configuration Issues

**Problem**: `ValidationError: ANTHROPIC_API_KEY is required`
```bash
# Solution: Set environment variable
export ANTHROPIC_API_KEY="your_key_here"
# Or add to .env file
```

**Problem**: Database connection errors
```bash
# Solution: Create storage directory
mkdir -p storage logs reports
```

#### Runtime Issues

**Problem**: Simulation hangs or crashes
```bash
# Check logs
tail -f logs/simulation.log

# Check system resources
python main.py --validate-config
```

**Problem**: Dashboard not accessible
```bash
# Check port availability
lsof -i :8501

# Kill existing processes
pkill -f streamlit
```

**Problem**: Agent communication failures
```bash
# Check MCP server status
python -c "from mcp_servers import check_servers; check_servers()"
```

### Performance Issues

**Problem**: Slow simulation performance
```bash
# Check system resources
python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%, Memory: {psutil.virtual_memory().percent}%')"
```

**Problem**: High memory usage
```bash
# Clear cache and temporary files
python -c "import gc; gc.collect()"
```

**Problem**: Database errors
```bash
# Check database integrity
python -c "from utils.validation_standalone import check_system_health; check_system_health()"
```

## 🔧 Advanced Configuration

### Custom Agent Development
1. Create a new agent class extending `BaseAgent`
2. Implement required methods (`process_command`, `get_agent_capabilities`)
3. Add custom tools using LangChain
4. Register agent in coordinator
5. Test thoroughly

### Custom Scenario Development
1. Create a new scenario class
2. Define critical assets and attack vectors
3. Implement validation methods
4. Register scenario in scenarios module
5. Test with coordinator

### Database Configuration
1. Configure SQLite database path in config.py
2. Set up vector database for agent memory
3. Configure backup procedures
4. Test database connectivity

### Network Configuration
1. Configure MCP server ports
2. Set up WebSocket connections
3. Configure firewall rules
4. Test network connectivity

## 📚 Documentation

### Additional Documentation
- [Architecture](architecture.md) - System architecture
- [API Reference](api-reference/) - Complete API documentation
- [Security Policy](../SECURITY.md) - Security information
- [Contributing](../CONTRIBUTING.md) - Contributing guidelines

### External Resources
- [LangChain Documentation](https://python.langchain.com/)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Australian SOCI Act](https://www.cyber.gov.au/soci-act)

## 🆘 Getting Help

### Documentation
- Browse this documentation
- Check the [User Guide](user-guide/) for usage instructions
- Review the [API Reference](api-reference/) for technical details

### Community
- Create an issue on GitHub
- Join discussions on GitHub
- Check the [Contributing](../CONTRIBUTING.md) for guidelines

### Support
- Review the [Troubleshooting](troubleshooting/) guide
- Check the [Security Policy](../SECURITY.md) for security issues
- Email support@example.com for assistance

---

This installation guide should help you get the Autonomous Multi-Agent Red/Blue Team Simulation System up and running. If you encounter any issues, check the troubleshooting guide or create an issue on GitHub.
