# Autonomous Multi-Agent Red/Blue Team Simulation System - Development Guidelines

## Project Overview
Production-ready agentic AI security testing framework for Australian critical infrastructure scenarios under the SOCI Act. Simulates coordinated cyber attacks with autonomous AI red team agents and defensive blue team counter-agents.

## Development Constraints

### Safety & Ethics (CRITICAL)
- **ALL ATTACKS ARE SIMULATED** - No actual exploitation, network scanning, or malicious payloads
- Generate descriptions, strategies, and documentation only
- Include prominent disclaimers about simulation-only nature
- Comply with Australian Computer Crimes Act 1989
- Focus on educational and defensive value

### Technical Standards
- Use LangChain with custom chains and agents
- Claude 3.5 Sonnet via Anthropic API for LLM provider
- Custom MCP servers for inter-agent communication
- MITRE ATT&CK framework integration
- Structured JSON logging with attack/defense narrative generation
- SQLite for session persistence, vector DB for knowledge retrieval

### Code Quality Requirements
- Clean naming conventions and modular functions
- Type hinting throughout codebase
- Comprehensive error handling (try/except blocks)
- Clear comments explaining complex logic
- PEP 8 formatting compliance
- Unit tests for all core components

### Architecture Constraints
- Base agent class with LangChain ReAct implementation
- Memory management (conversation + episodic)
- Tool calling interface with MCP client integration
- Message passing between agents via MCP servers
- Shared state synchronization and event broadcasting

### Australian SOCI Act Integration
- Model attacks against Australian critical infrastructure sectors
- Reference SOCI Act reporting requirements
- Include ASD Essential Eight mitigation strategies
- Consider Australian Privacy Act 1988 compliance
- Focus on energy, telecommunications, water, transport sectors

## Agent Development Guidelines

### Red Team Agents (4 minimum)
1. **Recon Agent**: OSINT gathering, network mapping, vulnerability scanning simulation
2. **Social Engineering Agent**: Phishing content generation, pretexting scenarios
3. **Exploitation Agent**: Vulnerability chaining, payload simulation, attack path generation
4. **Lateral Movement Agent**: Network traversal simulation, privilege escalation tactics

### Blue Team Agents (3 minimum)
1. **Detection Agent**: Anomaly pattern recognition, IOC generation, alert correlation
2. **Response Agent**: Incident triage, containment strategies, remediation steps
3. **Threat Intelligence Agent**: Attack attribution, TTP mapping to MITRE ATT&CK

### System Prompts Requirements
- Detailed role definition with capabilities and constraints
- MITRE ATT&CK technique references
- Australian context and SOCI Act alignment
- Clear output formatting requirements
- Safety constraints and simulation disclaimers

## Output Requirements
- Real-time console logging of agent actions
- Streamlit dashboard with active agents, attack progression, MITRE ATT&CK heatmap
- Final JSON report with complete engagement narrative
- Markdown summary suitable for portfolio presentation
- Executive summary for compliance documentation

## Success Criteria
- Minimum 4 red team agents operating autonomously
- Minimum 3 blue team agents providing defense
- Complete MITRE ATT&CK technique mapping
- All 3 SOCI scenarios functional
- Clean, documented codebase ready for GitHub
- Impressive visual dashboard for demos

## Security Considerations
- No functional malicious code generation
- No actual vulnerability exploitation
- All network operations simulated
- Biometric data handling per Privacy Act 1988
- Secure API key management
- Audit logging for all agent activities

## Raouf: Implementation Summary
- Date: 2025-12-31 (Australia/Sydney)
- Scope: Complete system implementation
- Status: ✅ COMPLETED
- Files implemented: Full codebase with all agents, scenarios, dashboard, and infrastructure
- Verification: System ready for validation and demonstration
- Follow-ups: Run system validation, create demo scenarios, prepare portfolio presentation

## Change Log
- Raouf: 2025-12-31 (Australia/Sydney) | scope: repo-split | summary: split parent repo and initialize standalone git repo | files: .git (new), AGENT.md, CHANGELOG.md | verification: not run | follow-ups: rename default branch if desired
