# Contributing to Autonomous Multi-Agent Red/Blue Team Simulation System

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Anthropic API key (for testing)
- Git
- Familiarity with cybersecurity concepts and MITRE ATT&CK framework

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork the repository on GitHub, then clone your fork
   git clone https://github.com/your-username/autonomous-multi-agent-simulation.git
   cd autonomous-multi-agent-simulation
   ```

2. **Set Up Development Environment**
   ```bash
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Verify Setup**
   ```bash
   # Run system validation
   python main.py --validate-config
   
   # Run tests
   pytest
   ```

## 📋 Development Workflow

### 1. Create an Issue

Before starting work, please create an issue to discuss your proposed changes. This helps:
- Avoid duplicate work
- Get early feedback on your approach
- Ensure alignment with project goals

### 2. Create a Branch

```bash
# Create a feature branch from main
git checkout main
git pull origin main
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-number-description
```

### 3. Make Your Changes

Follow these guidelines:

#### Code Quality
- **Follow PEP 8** for Python code style
- **Add type hints** for all functions and methods
- **Write docstrings** for all classes and functions
- **Use meaningful variable and function names**
- **Keep functions small and focused**

#### Security Requirements
- **All attacks must be simulation-only**
- **No actual exploitation or malicious code**
- **Validate all inputs and outputs**
- **Follow security best practices**
- **Maintain Australian compliance requirements**

#### Testing
- **Add tests** for new functionality
- **Ensure existing tests pass**
- **Maintain test coverage above 80%**
- **Write integration tests for complex features**

#### Documentation
- **Update README.md** if adding user-facing features
- **Add inline documentation** for complex logic
- **Update API documentation** if applicable
- **Include examples** for new features

### 4. Run Tests and Validation

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov=orchestration --cov=utils --cov=scenarios

# Run linting
flake8 agents/ orchestration/ utils/ scenarios/
black --check agents/ orchestration/ utils/ scenarios/

# Run system validation
python main.py --validate-config

# Test scenarios
python -c "import scenarios; scenarios.validate_all_scenarios()"
```

### 5. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a clear message
git commit -m "feat: add new threat intelligence agent capability

- Implement threat attribution logic
- Add MITRE ATT&CK technique mapping
- Include comprehensive tests
- Update documentation"

# Push to your fork
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

1. **Open a Pull Request** from your feature branch to `main`
2. **Fill out the PR template** completely
3. **Link to any related issues**
4. **Request review from maintainers**
5. **Address feedback promptly**

## 🏗️ Architecture Guidelines

### Adding New Agents

When adding new agents:

1. **Inherit from BaseAgent**
   ```python
   from agents.base_agent import BaseAgent
   
   class NewAgent(BaseAgent):
       def __init__(self, agent_id: str = None):
           super().__init__(
               agent_id=agent_id,
               agent_type="new_agent_type",
               system_prompt=PROMPT_TEMPLATE,
               tools=self._create_tools(),
               enable_mcp=True
           )
   ```

2. **Define Tools**
   ```python
   def _create_tools(self) -> List[BaseTool]:
       # Implement agent-specific tools
       return [Tool1(), Tool2(), ...]
   ```

3. **Add Tests**
   ```python
   # tests/test_new_agent.py
   class TestNewAgent:
       def test_agent_initialization(self):
           agent = NewAgent()
           assert agent.agent_type == "new_agent_type"
   ```

### Adding New Scenarios

1. **Create Scenario Class**
   ```python
   class NewScenario:
       def __init__(self):
           self.scenario_name = "new_scenario"
           self.critical_assets = self._define_assets()
           self.attack_vectors = self._define_vectors()
   ```

2. **Implement Required Methods**
   - `_define_critical_assets()`
   - `_define_attack_vectors()`
   - `_define_defensive_measures()`
   - `validate_scenario()`

3. **Register Scenario**
   ```python
   # scenarios/__init__.py
   SCENARIOS["new_scenario"] = {
       "class": NewScenario,
       "factory": create_new_scenario,
       "metadata": {...}
   }
   ```

## 📝 Code Style Guide

### Python Style

- **Indentation**: 4 spaces
- **Line Length**: 88 characters maximum
- **Imports**: Group imports (standard library, third-party, local)
- **Docstrings**: Google style or NumPy style
- **Type Hints**: Use for all function parameters and return values

### Naming Conventions

- **Classes**: `PascalCase`
- **Functions/Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private Members**: `_leading_underscore`
- **Modules**: `lowercase_with_underscores`

### Documentation Standards

#### Function Docstrings
```python
def calculate_risk_score(vulnerability: str, asset_value: int) -> float:
    """Calculate risk score for a vulnerability.
    
    Args:
        vulnerability: Description of the vulnerability
        asset_value: Value of the affected asset (1-10)
    
    Returns:
        Risk score between 0.0 and 1.0
    
    Raises:
        ValueError: If asset_value is not between 1 and 10
    """
```

#### Class Docstrings
```python
class ThreatIntelligenceAgent(BaseAgent):
    """Blue Team Threat Intelligence Agent.
    
    This agent specializes in attack attribution, TTP mapping to MITRE ATT&CK,
    and predictive defense insights for the Australian SOCI Act framework.
    
    Attributes:
        threat_groups: Dictionary of identified threat groups
        ttp_mappings: Dictionary of technique mappings
    """
```

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for component interactions
├── scenarios/      # Scenario-specific tests
├── fixtures/       # Test data and fixtures
└── conftest.py     # Pytest configuration
```

### Writing Tests

1. **Use Descriptive Names**
   ```python
   def test_threat_intelligence_agent_attributes_attack_successfully():
       # Test implementation
   ```

2. **Follow AAA Pattern** (Arrange, Act, Assert)
   ```python
   def test_agent_initialization():
       # Arrange
       agent_id = "test_agent"
       
       # Act
       agent = ThreatIntelligenceAgent(agent_id)
       
       # Assert
       assert agent.agent_id == agent_id
       assert agent.agent_type == "blue_team_threat_intel"
   ```

3. **Mock External Dependencies**
   ```python
   from unittest.mock import Mock, patch
   
   @patch('agents.blue_team.threat_intel_agent.ChatAnthropic')
   def test_agent_with_mock_llm(mock_anthropic):
       # Test with mocked LLM
   ```

### Test Coverage

- **Aim for 80%+ coverage**
- **Test all public methods**
- **Test error conditions**
- **Test edge cases**

## 🔒 Security Guidelines

### Simulation-Only Requirements

1. **No Real Attacks**
   - All attack simulations must be clearly marked as simulated
   - No actual network scanning or exploitation
   - No functional malicious code generation

2. **Input Validation**
   ```python
   def validate_scenario_input(scenario_data: Dict) -> bool:
       """Validate scenario input for safety."""
       required_fields = ["critical_assets", "attack_vectors"]
       return all(field in scenario_data for field in required_fields)
   ```

3. **Output Sanitization**
   ```python
   def sanitize_agent_output(output: str) -> str:
       """Remove any potentially harmful content from agent output."""
       # Remove actual commands, URLs, etc.
       return output
   ```

### Australian Compliance

- **SOCI Act**: Ensure scenarios align with critical infrastructure requirements
- **Privacy Act**: Handle any personal data according to Australian law
- **ASD Essential Eight**: Implement appropriate security controls

## 📚 Documentation Guidelines

### README Updates

When adding user-facing features:
1. Update the "Available Scenarios" section
2. Add new configuration options
3. Update usage examples
4. Update architecture diagram if needed

### API Documentation

For new APIs or significant changes:
1. Update docstrings
2. Add examples in docstrings
3. Update any external documentation
4. Consider adding a new section to README

### Code Comments

- **Explain complex logic**
- **Document assumptions**
- **Add TODO comments for future work**
- **Reference external standards or frameworks**

## 🐛 Bug Reports

### Reporting Bugs

1. **Use the Bug Report Template**
2. **Include system information**
3. **Provide steps to reproduce**
4. **Include logs and error messages**
5. **Suggest expected behavior**

### Bug Fix Process

1. **Create issue** to track the bug
2. **Create branch** with descriptive name
3. **Write failing test** that reproduces the bug
4. **Fix the bug**
5. **Ensure test passes**
6. **Add additional tests** if needed
7. **Update documentation** if behavior changed

## 🤝 Code Review Process

### Reviewer Guidelines

1. **Check for security compliance**
2. **Verify test coverage**
3. **Ensure code quality standards**
4. **Check documentation updates**
5. **Validate Australian compliance**

### Author Guidelines

1. **Address all feedback**
2. **Update tests as requested**
3. **Fix any identified issues**
4. **Keep PR size reasonable**
5. **Be responsive to comments**

## 🏆 Recognition

Contributors will be recognized in:
- **README.md** acknowledgments section
- **CHANGELOG.md** for significant contributions
- **Release notes** for new features
- **Community communications**

## 📞 Getting Help

### Resources

- **Documentation**: Check the `docs/` directory
- **Examples**: Look in `examples/` directory
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions

### Contact

- **Maintainers**: Tag maintainers in issues for urgent questions
- **Community**: Use GitHub Discussions for general questions
- **Security**: Report security issues privately

## 📋 Release Process

### Version Management

- **Semantic Versioning**: Use MAJOR.MINOR.PATCH
- **Release Notes**: Update CHANGELOG.md for each release
- **Tagging**: Create Git tags for releases
- **Documentation**: Update version numbers in documentation

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers updated
- [ ] Security review completed
- [ ] Performance tests passed
- [ ] Compatibility tested

---

Thank you for contributing to the Autonomous Multi-Agent Red/Blue Team Simulation System! Your contributions help make cybersecurity education and research more accessible and effective.
