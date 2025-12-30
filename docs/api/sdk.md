# SDK Documentation

## 📚 SDK Overview

The Autonomous Multi-Agent Red/Blue Team Simulation System provides official SDKs for Python and JavaScript, enabling developers to easily integrate simulation capabilities into their applications. The SDKs provide high-level abstractions for managing simulations, agents, scenarios, and real-time monitoring.

## 🐍 Python SDK

### Installation
```bash
pip install autonomous-multi-agent-sdk
```

### Quick Start
```python
from autonomous_multi_agent import SimulationClient, ScenarioClient, AgentClient

# Initialize clients
simulation_client = SimulationClient(
    base_url="http://localhost:8080",
    api_key="your-api-key"
)

# Start a simulation
simulation = simulation_client.start_simulation(
    scenario_name="soci_energy_grid",
    timeout_minutes=60,
    enable_dashboard=True
)

# Monitor progress
while simulation.is_running():
    status = simulation.get_status()
    print(f"Progress: {status['progress']}%")
    time.sleep(5)

# Generate report
report = simulation.generate_report()
print(f"Report: {report['file_path']}")
```

### Core Classes

#### SimulationClient
Main client for managing simulations.

```python
from autonomous_multi_agent import SimulationClient

client = SimulationClient(
    base_url="http://localhost:8080",
    api_key="your-api-key",
    timeout=30,
    retries=3
)

# Start simulation
simulation = client.start_simulation(
    scenario_name="soci_energy_grid",
    configuration={
        "simulation_mode_only": True,
        "enable_safety_checks": True
    },
    execution_options={
        "enable_dashboard": True,
        "generate_report": True
    }
)

# Get simulation status
status = simulation.get_status()
print(f"Status: {status['status']}")

# Stop simulation
simulation.stop()
```

#### ScenarioClient
Client for managing scenarios.

```python
from autonomous_multi_agent import ScenarioClient

client = ScenarioClient(
    base_url="http://localhost:8080",
    api_key="your-api-key"
)

# List scenarios
scenarios = client.list_scenarios()
for scenario in scenarios['data']['scenarios']:
    print(f"Scenario: {scenario['name']}")

# Validate scenario
validation = client.validate_scenario("soci_energy_grid", {
    "simulation_mode_only": True,
    "enable_safety_checks": True
})

if validation['data']['valid']:
    print("Scenario is valid")
```

#### AgentClient
Client for managing agents.

```python
from autonomous_multi_agent import AgentClient

client = AgentClient(
    base_url="http://localhost:8080",
    api_key="your-api-key"
)

# List agents
agents = client.list_agents()
for agent in agents['data']['agents']:
    print(f"Agent: {agent['agent_type']}")

# Send command to agent
command = client.send_command(
    agent_id="recon_agent_001",
    command_type="execute_task",
    task="Perform OSINT on target",
    parameters={"target": "example.com"}
)

# Wait for completion
while command.get_status()['data']['status'] == 'running':
    print(f"Status: {command.get_status()['data']['status']}")
    time.sleep(2)

result = command.get_result()
print(f"Result: {result['data']['result']['success']}")
```

#### WebSocketClient
Client for real-time updates.

```python
from autonomous_multi_agent import WebSocketClient
import asyncio

async def handle_message(message):
    print(f"Received: {message['type']}")

client = WebSocketClient(
    url="ws://localhost:8080/ws/simulation/sim_20231231_123456",
    token="your-auth-token"
)

# Register message handlers
client.on('simulation_status', handle_message)
client.on('agent_task_completed', handle_message)
client.on('security_alert', handle_message)

# Connect and listen
await client.connect()
```

### Advanced Usage

#### Custom Configuration
```python
from autonomous_multi_agent import SimulationClient

# Custom client configuration
client = SimulationClient(
    base_url="http://localhost:8080",
    api_key="your-api-key",
    timeout=60,
    retries=5,
    retry_delay=2,
    verify_ssl=True,
    custom_headers={
        "User-Agent": "MyApp/1.0",
        "X-Custom-Header": "value"
    }
)
```

#### Error Handling
```python
from autonomous_multi_agent import SimulationClient, SimulationError, AuthenticationError

client = SimulationClient(
    base_url="http://localhost:8080",
    api_key="your-api-key"
)

try:
    simulation = client.start_simulation("soci_energy_grid")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except SimulationError as e:
    print(f"Simulation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

#### Batch Operations
```python
from autonomous_multi_agent import AgentClient

client = AgentClient(
    base_url="http://localhost:8080",
    api_key="your-api-key"
)

# Batch agent commands
commands = []
for agent_id in ["recon_agent_001", "recon_agent_002"]:
    command = client.send_command(
        agent_id=agent_id,
        command_type="execute_task",
        task="Perform OSINT",
        parameters={"target": "example.com"}
    )
    commands.append(command)

# Wait for all commands to complete
results = []
for command in commands:
    result = command.wait_for_completion()
    results.append(result)

print(f"Completed {len(results)} commands")
```

## 📜 JavaScript SDK

### Installation
```bash
npm install @autonomous-multi-agent/sdk
```

### Quick Start
```javascript
import { SimulationClient, ScenarioClient, AgentClient } from '@autonomous-multi-agent/sdk';

// Initialize clients
const simulationClient = new SimulationClient({
    baseUrl: 'http://localhost:8080',
    apiKey: 'your-api-key'
});

// Start a simulation
const simulation = await simulationClient.startSimulation({
    scenarioName: 'soci_energy_grid',
    timeoutMinutes: 60,
    enableDashboard: true
});

// Monitor progress
simulation.on('progress', (progress) => {
    console.log(`Progress: ${progress.percentage}%`);
});

// Wait for completion
await simulation.waitForCompletion();

// Generate report
const report = await simulation.generateReport();
console.log(`Report: ${report.filePath}`);
```

### Core Classes

#### SimulationClient
Main client for managing simulations.

```javascript
import { SimulationClient } from '@autonomous-multi-agent/sdk';

const client = new SimulationClient({
    baseUrl: 'http://localhost:8080',
    apiKey: 'your-api-key',
    timeout: 30000,
    retries: 3
});

// Start simulation
const simulation = await client.startSimulation({
    scenarioName: 'soci_energy_grid',
    configuration: {
        simulationModeOnly: true,
        enableSafetyChecks: true
    },
    executionOptions: {
        enableDashboard: true,
        generateReport: true
    }
});

// Get simulation status
const status = await simulation.getStatus();
console.log(`Status: ${status.status}`);

// Stop simulation
await simulation.stop();
```

#### ScenarioClient
Client for managing scenarios.

```javascript
import { ScenarioClient } from '@autonomous-multi-agent/sdk';

const client = new ScenarioClient({
    baseUrl: 'http://localhost:8080',
    apiKey: 'your-api-key'
});

// List scenarios
const scenarios = await client.listScenarios();
scenarios.data.scenarios.forEach(scenario => {
    console.log(`Scenario: ${scenario.name}`);
});

// Validate scenario
const validation = await client.validateScenario('soci_energy_grid', {
    simulationModeOnly: true,
    enableSafetyChecks: true
});

if (validation.data.valid) {
    console.log('Scenario is valid');
}
```

#### AgentClient
Client for managing agents.

```javascript
import { AgentClient } from '@autonomous-multi-agent/sdk';

const client = new AgentClient({
    baseUrl: 'http://localhost:8080',
    apiKey: 'your-api-key'
});

// List agents
const agents = await client.listAgents();
agents.data.agents.forEach(agent => {
    console.log(`Agent: ${agent.agentType}`);
});

// Send command to agent
const command = await client.sendCommand('recon_agent_001', {
    commandType: 'execute_task',
    task: 'Perform OSINT on target',
    parameters: { target: 'example.com' }
});

// Wait for completion
command.on('completed', (result) => {
    console.log(`Result: ${result.data.result.success}`);
});

await command.waitForCompletion();
```

#### WebSocketClient
Client for real-time updates.

```javascript
import { WebSocketClient } from '@autonomous-multi-agent/sdk';

const client = new WebSocketClient({
    url: 'ws://localhost:8080/ws/simulation/sim_20231231_123456',
    token: 'your-auth-token'
});

// Register message handlers
client.on('simulationStatus', (message) => {
    console.log(`Status: ${message.data.status}`);
});

client.on('agentTaskCompleted', (message) => {
    console.log(`Task completed: ${message.data.description}`);
});

client.on('securityAlert', (message) => {
    console.log(`Alert: ${message.data.description}`);
});

// Connect and listen
client.connect();
```

### Advanced Usage

#### Custom Configuration
```javascript
import { SimulationClient } from '@autonomous-multi-agent/sdk';

// Custom client configuration
const client = new SimulationClient({
    baseUrl: 'http://localhost:8080',
    apiKey: 'your-api-key',
    timeout: 60000,
    retries: 5,
    retryDelay: 2000,
    verifySsl: true,
    customHeaders: {
        'User-Agent': 'MyApp/1.0',
        'X-Custom-Header': 'value'
    }
});
```

#### Error Handling
```javascript
import { SimulationClient, SimulationError, AuthenticationError } from '@autonomous-multi-agent/sdk';

const client = new SimulationClient({
    baseUrl: 'http://localhost:8080',
    apiKey: 'your-api-key'
});

try {
    const simulation = await client.startSimulation('soci_energy_grid');
} catch (error) {
    if (error instanceof AuthenticationError) {
        console.error('Authentication failed:', error.message);
    } else if (error instanceof SimulationError) {
        console.error('Simulation error:', error.message);
    } else {
        console.error('Unexpected error:', error.message);
    }
}
```

#### Batch Operations
```javascript
import { AgentClient } from '@autonomous-multi-agent/sdk';

const client = new AgentClient({
    baseUrl: 'http://localhost:8080',
    apiKey: 'your-api-key'
});

// Batch agent commands
const commands = [];
const agentIds = ['recon_agent_001', 'recon_agent_002'];

for (const agentId of agentIds) {
    const command = await client.sendCommand(agentId, {
        commandType: 'execute_task',
        task: 'Perform OSINT',
        parameters: { target: 'example.com' }
    });
    commands.push(command);
}

// Wait for all commands to complete
const results = await Promise.all(
    commands.map(command => command.waitForCompletion())
);

console.log(`Completed ${results.length} commands`);
```

## 🔧 Configuration

### Environment Variables
```bash
# API Configuration
AUTONOMOUS_API_BASE_URL=http://localhost:8080
AUTONOMOUS_API_KEY=your-api-key
AUTONOMOUS_API_TIMEOUT=30
AUTONOMOUS_API_RETRIES=3

# WebSocket Configuration
AUTONOMOUS_WS_URL=ws://localhost:8080/ws
AUTONOMOUS_WS_TOKEN=your-auth-token

# Logging
AUTONOMOUS_LOG_LEVEL=INFO
AUTONOMOUS_LOG_FORMAT=json
```

### Configuration Files

#### Python (config.yaml)
```yaml
autonomous_multi_agent:
  api:
    base_url: http://localhost:8080
    api_key: your-api-key
    timeout: 30
    retries: 3
    verify_ssl: true
    custom_headers:
      User-Agent: MyApp/1.0
  
  websocket:
    url: ws://localhost:8080/ws
    token: your-auth-token
    reconnect_attempts: 5
    reconnect_delay: 1000
  
  logging:
    level: INFO
    format: json
    file: autonomous_sdk.log
```

#### JavaScript (config.json)
```json
{
  "autonomousMultiAgent": {
    "api": {
      "baseUrl": "http://localhost:8080",
      "apiKey": "your-api-key",
      "timeout": 30000,
      "retries": 3,
      "verifySsl": true,
      "customHeaders": {
        "User-Agent": "MyApp/1.0"
      }
    },
    "websocket": {
      "url": "ws://localhost:8080/ws",
      "token": "your-auth-token",
      "reconnectAttempts": 5,
      "reconnectDelay": 1000
    },
    "logging": {
      "level": "info",
      "format": "json"
    }
  }
}
```

## 📚 Examples

### Python Examples

#### Basic Simulation
```python
from autonomous_multi_agent import SimulationClient

def run_basic_simulation():
    client = SimulationClient(
        base_url="http://localhost:8080",
        api_key="your-api-key"
    )
    
    # Start simulation
    simulation = client.start_simulation(
        scenario_name="soci_energy_grid",
        timeout_minutes=60
    )
    
    print(f"Simulation started: {simulation.id}")
    
    # Monitor progress
    while simulation.is_running():
        status = simulation.get_status()
        print(f"Progress: {status['progress']}%")
        time.sleep(10)
    
    # Get results
    report = simulation.generate_report()
    print(f"Report generated: {report['file_path']}")
    
    return simulation

if __name__ == "__main__":
    run_basic_simulation()
```

#### Multi-Agent Coordination
```python
from autonomous_multi_agent import AgentClient, SimulationClient

def coordinate_agents():
    # Initialize clients
    sim_client = SimulationClient(
        base_url="http://localhost:8080",
        api_key="your-api-key"
    )
    
    agent_client = AgentClient(
        base_url="http://localhost:8080",
        api_key="your-api-key"
    )
    
    # Start simulation
    simulation = sim_client.start_simulation("soci_energy_grid")
    
    # Get available agents
    agents = agent_client.list_agents()
    red_team_agents = [a for a in agents['data']['agents'] if a['team'] == 'red_team']
    
    # Coordinate red team agents
    commands = []
    for agent in red_team_agents:
        command = agent_client.send_command(
            agent_id=agent['agent_id'],
            command_type="execute_task",
            task=f"Execute {agent['agent_type']} activities",
            parameters={"target": "example.com"}
        )
        commands.append(command)
    
    # Monitor all commands
    completed = 0
    while completed < len(commands):
        for command in commands:
            status = command.get_status()
            if status['data']['status'] == 'completed':
                completed += 1
        time.sleep(5)
    
    print(f"All {len(commands)} commands completed")
    
    # Stop simulation
    simulation.stop()
    
    return simulation

if __name__ == "__main__":
    coordinate_agents()
```

### JavaScript Examples

#### Basic Simulation
```javascript
import { SimulationClient } from '@autonomous-multi-agent/sdk';

async function runBasicSimulation() {
    const client = new SimulationClient({
        baseUrl: 'http://localhost:8080',
        apiKey: 'your-api-key'
    });
    
    try {
        // Start simulation
        const simulation = await client.startSimulation({
            scenarioName: 'soci_energy_grid',
            timeoutMinutes: 60
        });
        
        console.log(`Simulation started: ${simulation.id}`);
        
        // Monitor progress
        simulation.on('progress', (progress) => {
            console.log(`Progress: ${progress.percentage}%`);
        });
        
        // Wait for completion
        await simulation.waitForCompletion();
        
        // Generate report
        const report = await simulation.generateReport();
        console.log(`Report generated: ${report.filePath}`);
        
        return simulation;
        
    } catch (error) {
        console.error('Simulation failed:', error.message);
        throw error;
    }
}

// Run the simulation
runBasicSimulation().catch(console.error);
```

#### Real-time Dashboard
```javascript
import { SimulationClient, WebSocketClient } from '@autonomous-multi-agent/sdk';

class RealTimeDashboard {
    constructor() {
        this.simulationClient = new SimulationClient({
            baseUrl: 'http://localhost:8080',
            apiKey: 'your-api-key'
        });
        
        this.wsClient = new WebSocketClient({
            url: 'ws://localhost:8080/ws/simulation/sim_20231231_123456',
            token: 'your-auth-token'
        });
        
        this.setupWebSocketHandlers();
    }
    
    setupWebSocketHandlers() {
        this.wsClient.on('simulationStatus', (message) => {
            this.updateSimulationStatus(message.data);
        });
        
        this.wsClient.on('agentTaskCompleted', (message) => {
            this.updateAgentStatus(message.data);
        });
        
        this.wsClient.on('securityAlert', (message) => {
            this.showAlert(message.data);
        });
    }
    
    updateSimulationStatus(status) {
        console.log('Simulation status updated:', status);
        // Update UI elements
        document.getElementById('progress').textContent = `${status.progress}%`;
        document.getElementById('phase').textContent = status.phase;
    }
    
    updateAgentStatus(data) {
        console.log('Agent task completed:', data);
        // Update agent status in UI
        const agentElement = document.getElementById(`agent-${data.agent_id}`);
        if (agentElement) {
            agentElement.classList.add('task-completed');
        }
    }
    
    showAlert(alert) {
        console.log('Security alert:', alert);
        // Show alert in UI
        const alertElement = document.createElement('div');
        alertElement.className = 'alert alert-warning';
        alertElement.textContent = alert.description;
        document.getElementById('alerts').appendChild(alertElement);
    }
    
    async startSimulation() {
        try {
            const simulation = await this.simulationClient.startSimulation({
                scenarioName: 'soci_energy_grid',
                enableDashboard: true
            });
            
            // Connect WebSocket for real-time updates
            this.wsClient.url = `ws://localhost:8080/ws/simulation/${simulation.id}`;
            this.wsClient.connect();
            
            return simulation;
            
        } catch (error) {
            console.error('Failed to start simulation:', error.message);
            throw error;
        }
    }
}

// Initialize dashboard
const dashboard = new RealTimeDashboard();
dashboard.startSimulation().catch(console.error);
```

## 🧪 Testing

### Python Testing
```python
import pytest
from autonomous_multi_agent import SimulationClient, AgentClient

class TestSimulationSDK:
    def setup_method(self):
        self.sim_client = SimulationClient(
            base_url="http://localhost:8080",
            api_key="test-api-key"
        )
        self.agent_client = AgentClient(
            base_url="http://localhost:8080",
            api_key="test-api-key"
        )
    
    def test_start_simulation(self):
        simulation = self.sim_client.start_simulation(
            scenario_name="soci_energy_grid",
            timeout_minutes=30
        )
        
        assert simulation.id is not None
        assert simulation.status == "started"
        
        simulation.stop()
    
    def test_agent_command(self):
        command = self.agent_client.send_command(
            agent_id="test_agent_001",
            command_type="execute_task",
            task="Test task",
            parameters={"test": True}
        )
        
        assert command.id is not None
        assert command.status == "queued"
        
        result = command.wait_for_completion(timeout=10)
        assert result['data']['result']['success'] is True

if __name__ == "__main__":
    pytest.main([__file__])
```

### JavaScript Testing
```javascript
import { SimulationClient, AgentClient } from '@autonomous-multi-agent/sdk';
import { jest } from '@jest/globals';

describe('Simulation SDK', () => {
    let simClient;
    let agentClient;
    
    beforeEach(() => {
        simClient = new SimulationClient({
            baseUrl: 'http://localhost:8080',
            apiKey: 'test-api-key'
        });
        
        agentClient = new AgentClient({
            baseUrl: 'http://localhost:8080',
            apiKey: 'test-api-key'
        });
    });
    
    test('should start simulation', async () => {
        const simulation = await simClient.startSimulation({
            scenarioName: 'soci_energy_grid',
            timeoutMinutes: 30
        });
        
        expect(simulation.id).toBeDefined();
        expect(simulation.status).toBe('started');
        
        await simulation.stop();
    });
    
    test('should send agent command', async () => {
        const command = await agentClient.sendCommand('test_agent_001', {
            commandType: 'execute_task',
            task: 'Test task',
            parameters: { test: true }
        });
        
        expect(command.id).toBeDefined();
        expect(command.status).toBe('queued');
        
        const result = await command.waitForCompletion(10000);
        expect(result.data.result.success).toBe(true);
    });
});
```

## 📖 Additional Resources

- [Main API Documentation](README.md)
- [Agents API Documentation](agents.md)
- [Scenarios API Documentation](scenarios.md)
- [MCP API Documentation](mcp.md)
- [Dashboard API Documentation](dashboard.md)
- [WebSocket Documentation](websockets.md)
- [Examples](../../examples/)

## 🆘 Support

For SDK support:
- Create an issue on GitHub
- Check the [examples](../../examples/)
- Review the [testing guide](../../tests/)
- Contact the development team
