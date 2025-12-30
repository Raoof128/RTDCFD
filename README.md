# Autonomous Multi-Agent Red/Blue Team Simulation System

🛡️ A production-ready agentic AI security testing framework for Australian critical infrastructure scenarios under the SOCI Act.

## 🎯 Project Overview

This system simulates coordinated cyber attacks with autonomous AI red team agents and defensive blue team counter-agents, specifically designed for Australian critical infrastructure sectors (energy, telecommunications, water, transport). Built with LangChain, Claude 3.5 Sonnet, and custom MCP servers for inter-agent communication.

## 🏗️ Architecture

### Core Components

- **Agent Orchestration Layer**: Primary coordinator using LangChain with custom MCP server integration
- **Red Team Agent Squad** (4 agents): Recon, Social Engineering, Exploitation, Lateral Movement
- **Blue Team Defense Squad** (3 agents): Detection, Response, Threat Intelligence
- **MCP Communication**: Custom servers for inter-agent messaging and state synchronization
- **MITRE ATT&CK Integration**: Complete framework mapping and TTP analysis
- **Real-time Dashboard**: Streamlit-based visualization and monitoring interface

### Technology Stack

- **Primary Framework**: LangChain with custom chains and agents
- **LLM Provider**: Claude 3.5 Sonnet via Anthropic API
- **Agent Communication**: Custom MCP servers for inter-agent messaging
- **Knowledge Base**: MITRE ATT&CK framework (programmatically accessible)
- **Logging**: Structured JSON logging with attack/defense narrative generation
- **Storage**: SQLite for session persistence, vector DB for knowledge retrieval
- **Dashboard**: Streamlit for real-time monitoring and visualization

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Anthropic API key
- Git

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd autonomous-multi-agent-simulation

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Verify installation
python main.py --validate-config
```

### Running the System

```bash
# List available scenarios
python main.py --list-scenarios

# Run simulation with dashboard
python main.py --scenario soci_energy_grid --dashboard

# Run headless simulation
python main.py --scenario soci_telco_network --headless

# Start dashboard only
streamlit run dashboard/streamlit_ui.py
```

## 📋 Available Scenarios

### SOCI Act Critical Infrastructure Scenarios

1. **Energy Grid Disruption** (`soci_energy_grid`)
   - SCADA system compromise
   - Power distribution attacks
   - OT/IT convergence scenarios

2. **Telecommunications Network** (`soci_telco_network`)
   - SS7 network exploitation
   - Customer database breaches
   - Mobile network infrastructure attacks

3. **Water Treatment System** (`soci_water_system`)
   - Chemical dosing manipulation
   - Water quality data integrity attacks
   - Industrial control system compromise

## 🤖 Agent Capabilities

### Red Team Agents

#### Reconnaissance Agent
- OSINT gathering and network mapping
- Vulnerability scanning simulation
- Attack surface identification
- MITRE ATT&CK: T1592, T1595, T1596, T1598

#### Social Engineering Agent
- Phishing content generation
- Pretexting scenario development
- Trust exploitation patterns
- MITRE ATT&CK: T1566, T1598, T1657, T1656

#### Exploitation Agent
- Vulnerability chaining analysis
- Attack path generation
- Security control bypass analysis
- MITRE ATT&CK: T1203, T1210, T1190, T1068

#### Lateral Movement Agent
- Network traversal simulation
- Privilege escalation tactics
- Persistence mechanism analysis
- MITRE ATT&CK: T1021, T1028, T1547, T1574

### Blue Team Agents

#### Detection Agent
- Anomaly pattern recognition
- IOC generation and analysis
- Alert correlation and prioritization
- MITRE ATT&CK: TA0001, TA0002, TA0003, TA0004

#### Response Agent
- Incident triage and prioritization
- Containment strategy development
- Remediation procedure guidance
- Comprehensive incident response

#### Threat Intelligence Agent
- Attack attribution and TTP mapping
- Threat landscape analysis
- Intelligence report generation
- Predictive defense insights

## 📊 Dashboard Features

- **Real-time Agent Monitoring**: Live status of all agents and their activities
- **Attack/Defense Timeline**: Visual timeline of simulation events
- **MITRE ATT&CK Analysis**: Technique mapping and frequency analysis
- **Score Tracking**: Red team vs blue team performance metrics
- **Phase Progression**: Simulation phase tracking and transitions
- **System Logs**: Real-time logging and event monitoring

## 🔧 Configuration

### Environment Variables

```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
SQLITE_DB_PATH=storage/simulation.db
CHROMA_DB_PATH=storage/vector_db
LOG_LEVEL=INFO
ENABLE_CONSOLE_OUTPUT=true
```

### System Configuration

Edit `config.py` to customize:
- Agent timeouts and memory limits
- MCP server ports and hosts
- Scenario durations and phases
- Logging preferences
- Dashboard settings

## 🛡️ Safety & Ethics

**CRITICAL**: This is a simulation-only system. All attacks are SIMULATED.

- ✅ No actual vulnerability exploitation
- ✅ No functional malicious code generation
- ✅ No real network scanning or probing
- ✅ Educational and defensive focus only
- ✅ Complies with Australian Computer Crimes Act 1989
- ✅ Respects Australian Privacy Act 1988

## 📈 Compliance & Standards

### Australian SOCI Act
- Critical infrastructure registration compliance
- Cyber security incident reporting
- Risk management program alignment
- Information sharing requirements

### ASD Essential Eight
- Application control implementation
- Patch management procedures
- Multi-factor authentication
- Security monitoring integration

### MITRE ATT&CK Framework
- Complete technique mapping
- TTP analysis and documentation
- Adversary emulation scenarios
- Defensive countermeasure development

## 📁 Project Structure

```
project_root/
├── agents/                    # Agent implementations
│   ├── red_team/             # Red team agents
│   ├── blue_team/            # Blue team agents
│   └── base_agent.py         # Base agent class
├── orchestration/             # Coordination logic
│   └── coordinator.py        # Main simulation coordinator
├── mcp_servers/              # Inter-agent communication
│   ├── mcp_server.py         # Base MCP server
│   ├── red_team_mcp.py       # Red team MCP server
│   └── blue_team_mcp.py      # Blue team MCP server
├── scenarios/                # SOCI Act scenarios
│   ├── soci_energy_grid.py   # Energy grid scenario
│   ├── soci_telco_network.py # Telecom scenario
│   └── soci_water_system.py  # Water system scenario
├── utils/                     # Utility modules
│   ├── logging_handler.py    # Structured logging
│   ├── mcp_client.py         # MCP client implementation
│   ├── validation.py         # System validation
│   └── prompt_templates.py   # Agent system prompts
├── dashboard/                 # Streamlit dashboard
│   └── streamlit_ui.py       # Main dashboard interface
├── mitre_integration/         # MITRE ATT&CK integration
├── storage/                   # Data storage
├── logs/                      # Log files
├── reports/                   # Generated reports
├── config.py                  # System configuration
├── main.py                    # Application entry point
└── requirements.txt           # Dependencies
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_agents/
pytest tests/test_scenarios/
pytest tests/test_mcp/

# Run with coverage
pytest --cov=agents --cov=orchestration --cov=utils
```

## 📊 Usage Examples

### Basic Simulation

```python
from orchestration import SimulationCoordinator

# Initialize coordinator
coordinator = SimulationCoordinator()

# Initialize scenario
await coordinator.initialize_simulation("soci_energy_grid")

# Run simulation
await coordinator.run_simulation(timeout_minutes=60)

# Generate report
report_path = await coordinator.generate_report()
```

### Custom Agent

```python
from agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="custom_agent",
            agent_type="custom",
            system_prompt="Your custom prompt here",
            tools=[],
            enable_mcp=True
        )
    
    def get_agent_capabilities(self):
        return {
            "agent_type": "custom",
            "capabilities": ["custom_capability"],
            "tools": [tool.name for tool in self.tools]
        }
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Add comprehensive tests for new features
- Update documentation for API changes
- Ensure all security constraints are maintained
- Validate against Australian compliance requirements

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Australian Signals Directorate (ASD) for Essential Eight framework
- MITRE ATT&CK® framework for threat intelligence
- Anthropic for Claude 3.5 Sonnet API
- LangChain for agent framework
- Streamlit for dashboard technology

## 📞 Support

For questions, issues, or contributions:

- 📧 Create an Issue on GitHub
- 📖 Check the [Documentation](docs/)
- 🧪 Run `python main.py --validate-config` for system checks

## 🔮 Future Roadmap

- [ ] Integration with real threat intelligence feeds
- [ ] LLM-powered attack narrative generation
- [ ] Export to STIX/TAXII formats
- [ ] Integration with SIEM log formats
- [ ] Additional SOCI Act scenarios (transport, finance, health)
- [ ] Multi-cloud deployment support
- [ ] Advanced analytics and reporting

---

**⚠️ IMPORTANT**: This system is for authorized security testing and educational purposes only. All activities are simulated and no actual attacks are performed.
