# Autonomous Multi-Agent Red/Blue Team Simulation System Documentation

Welcome to the comprehensive documentation for the Autonomous Multi-Agent Red/Blue Team Simulation System. This documentation provides detailed information about the system architecture, usage, and development.

## 📚 Table of Contents

- [Installation Guide](installation.md) - Getting started with the system
- [User Guide](user-guide/) - Using the simulation system
- [Developer Guide](developer-guide/) - Development and customization
- [API Reference](api-reference/) - Complete API documentation
- [Architecture](architecture.md) - System architecture and design
- [Scenarios](scenarios/) - Available simulation scenarios
- [Agents](agents/) - Agent documentation
- [Examples](examples/) - Usage examples
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

## 🚀 Quick Start

### For Users

1. **Installation**: Follow the [Installation Guide](installation.md)
2. **Basic Usage**: Check the [User Guide](user-guide/)
3. **Run Simulation**: See [Quick Start](user-guide/quick-start.md)
4. **Dashboard**: Learn about the [Dashboard](user-guide/dashboard.md)

### For Developers

1. **Development Setup**: Follow the [Developer Guide](developer-guide/)
2. **Code Structure**: Review the [Architecture](architecture.md)
3. **API Reference**: Check the [API Reference](api-reference/)
4. **Examples**: See the [Examples](examples/) directory

### For Security Professionals

1. **Safety Guidelines**: Review [Security Policy](../SECURITY.md)
2. **Compliance**: Check [Compliance](compliance/)
3. **Incident Response**: Review [Incident Response](security/incident-response.md)

## 🏗️ System Overview

The Autonomous Multi-Agent Red/Blue Team Simulation System is a production-ready agentic AI security testing framework designed for Australian critical infrastructure scenarios under the SOCI Act. The system simulates coordinated cyber attacks with autonomous AI red team agents and defensive blue team counter-agents.

### Key Features

- **Multi-Agent Architecture**: 7 specialized agents (4 red team, 3 blue team)
- **Real-time Simulation**: Live attack/defense scenarios
- **MITRE ATT&CK Integration**: Complete framework mapping
- **Australian Compliance**: SOCI Act and ASD Essential Eight alignment
- **Interactive Dashboard**: Real-time monitoring and visualization
- **Extensible Framework**: Easy to add custom agents and scenarios

### Technology Stack

- **Python 3.8+**: Primary programming language
- **LangChain**: Agent framework and LLM integration
- **Claude 3.5 Sonnet**: Large Language Model provider
- **Streamlit**: Interactive dashboard
- **FastAPI**: API framework
- **SQLite**: Database storage
- **WebSockets**: Real-time communication

## 🎯 Target Audience

### Security Professionals
- Red Team operators and penetration testers
- Blue Team analysts and incident responders
- Security architects and engineers
- Compliance officers and auditors

### Researchers and Educators
- Cybersecurity researchers
- Academic institutions
- Training organizations
- Security awareness programs

### Developers
- Python developers
- AI/ML engineers
- Security software developers
- System integrators

## 🛡️ Safety and Ethics

**CRITICAL**: This system is designed for simulation and education ONLY.

- ✅ **No Real Attacks**: All cyber attacks are simulated
- ✅ **No Exploitation**: No actual vulnerability exploitation
- ✅ **No Malicious Code**: No functional malicious code generation
- ✅ **Educational Focus**: Educational and defensive purposes only
- ✅ **Legal Compliance**: Complies with Australian laws and regulations

## 📋 Documentation Structure

```
docs/
├── index.md                    # This file
├── installation.md              # Installation guide
├── user-guide/                 # User documentation
│   ├── quick-start.md
│   ├── dashboard.md
│   ├── scenarios.md
│   └── troubleshooting.md
├── developer-guide/             # Developer documentation
│   ├── setup.md
│   ├── architecture.md
│   ├── extending-agents.md
│   ├── custom-scenarios.md
│   ├── testing.md
│   └── deployment.md
├── api-reference/              # API documentation
│   ├── coordinator.md
│   ├── agents.md
│   ├── scenarios.md
│   ├── mcp-servers.md
│   └── utils.md
├── scenarios/                  # Scenario documentation
│   ├── soci-energy-grid.md
│   ├── soci-telco-network.md
│   ├── soci-water-system.md
│   └── custom-scenarios.md
├── agents/                    # Agent documentation
│   ├── base-agent.md
│   ├── red-team/
│   │   ├── recon-agent.md
│   │   ├── social-engineering-agent.md
│   │   ├── exploitation-agent.md
│   │   └── lateral-movement-agent.md
│   └── blue-team/
│       ├── detection-agent.md
│       ├── response-agent.md
│       └── threat-intel-agent.md
├── security/                   # Security documentation
│   ├── overview.md
│   ├── incident-response.md
│   ├── compliance/
│   │   ├── soci-act.md
│   ├── asd-essential-eight.md
│   └── privacy-act.md
│   └── best-practices.md
├── troubleshooting/             # Troubleshooting guide
│   ├── common-issues.md
│   ├── configuration.md
│   ├── performance.md
│   └── integration.md
└── examples/                   # Examples documentation
    ├── basic-simulation.md
    ├── custom-agent.md
    └── scenario-customization.md
```

## 🔍 Navigation

### Getting Started
- [Installation Guide](installation.md) - Set up the system
- [User Guide](user-guide/quick-start.md) - Quick start guide
- [Examples](examples/) - Usage examples

### Understanding the System
- [Architecture](architecture.md) - System architecture
- [Scenarios](scenarios/) - Available scenarios
- [Agents](agents/) - Agent documentation

### Development
- [Developer Guide](developer-guide/) - Development setup
- [API Reference](api-reference/) - API documentation
- [Examples](examples/) - Code examples

### Reference
- [Security Policy](../SECURITY.md) - Security information
- [Contributing](../CONTRIBUTING.md) - Contributing guidelines
- [License](../LICENSE) - License information

## 📞 Getting Help

### Questions and Support

- **Documentation**: Browse the documentation sections above
- **Examples**: Check the [Examples](examples/) directory
- **Community**: Create an issue on GitHub
- **Security**: Report security issues privately

### Reporting Issues

- **Bug Reports**: Use GitHub issues with detailed information
- **Security Issues**: Email security@example.com
- **Documentation Issues**: Create an issue or submit a pull request

### Contributing

- See [Contributing](../CONTRIBUTING.md) for guidelines
- Follow the [Code of Conduct](../CODE_OF_CONDUCT.md)
- Review the [Development Guide](developer-guide/setup.md)

---

This documentation is designed to help you understand and effectively use the Autonomous Multi-Agent Red/Blue Team Simulation System. Start with the installation guide and explore the sections most relevant to your needs.
