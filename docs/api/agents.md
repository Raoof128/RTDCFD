# Agents API Documentation

## 🤖 Agent Overview

The Agents API provides endpoints for managing and interacting with autonomous AI agents in the simulation system. The API allows you to control agent behavior, monitor their status, and retrieve detailed information about their capabilities and activities.

## 🔗 Base URL
```
http://localhost:8080/api/v1/agents
```

## 📋 Agent Types

### Red Team Agents
- **Recon Agent** (`red_team_recon`): OSINT gathering and network mapping
- **Social Engineering Agent** (`red_team_social`): Phishing and social engineering simulation
- **Exploitation Agent** (`red_team_exploit`): Vulnerability exploitation and attack path analysis
- **Lateral Movement Agent** (`red_team_lateral`): Network traversal and persistence

### Blue Team Agents
- **Detection Agent** (`blue_team_detection`): Anomaly detection and IOC generation
- **Response Agent** (`blue_team_response`): Incident response and containment
- **Threat Intelligence Agent** (`blue_team_threat_intel`): Threat attribution and TTP analysis

## 🚀 API Endpoints

### List All Agents
```http
GET /api/v1/agents
```

**Response:**
```json
{
  "success": true,
  "data": {
    "agents": [
      {
        "agent_id": "recon_agent_001",
        "agent_type": "red_team_recon",
        "status": "active",
        "team": "red_team",
        "capabilities": [
          "osint_gathering",
          "network_mapping",
          "vulnerability_scanning",
          "attack_surface_analysis"
        ],
        "current_task": "OSINT gathering on target infrastructure",
        "tasks_completed": 15,
        "tasks_failed": 2,
        "last_activity": "2023-12-31T12:34:56Z",
        "created_at": "2023-12-31T12:30:00Z"
      }
    ],
    "total": 7,
    "active": 7,
    "red_team": 4,
    "blue_team": 3
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

### Get Agent Details
```http
GET /api/v1/agents/{agent_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "agent_id": "recon_agent_001",
    "agent_type": "red_team_recon",
    "status": "active",
    "team": "red_team",
    "capabilities": [
      {
        "name": "osint_gathering",
        "description": "Open-source intelligence gathering",
        "mitre_techniques": ["T1592", "T1595", "T1596", "T1598"],
        "tools": ["nmap", "shodan", "whois", "dns_enumeration"]
      },
      {
        "name": "network_mapping",
        "description": "Network topology mapping",
        "mitre_techniques": ["T1018", "T1046", "T1049"],
        "tools": ["network_scanner", "port_scanner", "topology_mapper"]
      }
    ],
    "configuration": {
      "max_tasks": 100,
      "timeout_seconds": 300,
      "memory_limit": "1GB",
      "enable_mcp": true
    },
    "current_task": "OSINT gathering on target infrastructure",
    "tasks_completed": 15,
    "tasks_failed": 2,
    "success_rate": 88.2,
    "average_response_time": 45.5,
    "last_activity": "2023-12-31T12:34:56Z",
    "created_at": "2023-12-31T12:30:00Z",
    "updated_at": "2023-12-31T12:34:56Z"
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

### Get Agent Capabilities
```http
GET /api/v1/agents/{agent_id}/capabilities
```

**Response:**
```json
{
  "success": true,
  "data": {
    "agent_id": "recon_agent_001",
    "agent_type": "red_team_recon",
    "capabilities": [
      {
        "name": "osint_gathering",
        "description": "Open-source intelligence gathering",
        "mitre_techniques": ["T1592", "T1595", "T1596", "T1598"],
        "tools": [
          {
            "name": "nmap",
            "description": "Network scanning tool",
            "parameters": {
              "target": "string (required)",
              "ports": "array of integers (optional)",
              "scan_type": "string (optional)"
            }
          },
          {
            "name": "shodan",
            "description": "Internet scanning tool",
            "parameters": {
              "query": "string (required)",
              "limit": "integer (optional)"
            }
          }
        ],
        "examples": [
          "Perform OSINT on target infrastructure",
          "Gather information about target organization",
          "Map network topology of target"
        ]
      }
    ],
    "tools_count": 8,
    "mitre_coverage": 12
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

### Send Command to Agent
```http
POST /api/v1/agents/{agent_id}/command
Content-Type: application/json
```

**Request Body:**
```json
{
  "type": "execute_task",
  "task": "Perform OSINT on target infrastructure",
  "parameters": {
    "target": "energy-grid.example.com",
    "techniques": ["T1595", "T1596"],
    "tools": ["nmap", "shodan"],
    "priority": "normal",
    "timeout": 300
  },
  "metadata": {
    "simulation_id": "sim_20231231_123456",
    "phase": "initial_access"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "command_id": "cmd_20231231_123456",
    "agent_id": "recon_agent_001",
    "status": "queued",
    "command_type": "execute_task",
    "timestamp": "2023-12-31T12:34:56Z",
    "estimated_duration": 300
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

### Get Command Status
```http
GET /api/v1/agents/{agent_id}/commands/{command_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "command_id": "cmd_20231231_123456",
    "agent_id": "recon_agent_001",
    "status": "completed",
    "command_type": "execute_task",
    "result": {
      "success": true,
      "output": "OSINT gathering completed successfully",
      "findings": {
        "target": "energy-grid.example.com",
        "open_ports": [80, 443, 22, 8080],
        "technologies": ["Apache", "nginx", "OpenSSH"],
        "vulnerabilities": [
          {
            "cve": "CVE-2023-1234",
            "severity": "medium",
            "description": "Apache vulnerability"
          }
        ]
      },
      "metrics": {
        "duration": 245,
        "tools_used": ["nmap", "shodan"],
        "data_collected": "2.3MB"
      }
    },
    "started_at": "2023-12-31T12:34:56Z",
    "completed_at": "2023-12-31T12:38:41Z",
    "duration": 245
  },
  "timestamp": "2023-12-31T12:39:00Z"
}
```

### Get Agent Activity
```http
GET /api/v1/agents/{agent_id}/activity
```

**Query Parameters:**
- `limit` (integer, optional): Number of recent activities to return (default: 50)
- `since` (string, optional): Return activities since this timestamp
- `status` (string, optional): Filter by status (completed, failed, running)

**Response:**
```json
{
  "success": true,
  "data": {
    "activities": [
      {
        "activity_id": "act_20231231_123456",
        "agent_id": "recon_agent_001",
        "type": "command_completed",
        "description": "OSINT gathering on target infrastructure",
        "status": "completed",
        "timestamp": "2023-12-31T12:38:41Z",
        "duration": 245,
        "success": true
      },
      {
        "activity_id": "act_20231231_123457",
        "agent_id": "recon_agent_001",
        "type": "message_sent",
        "description": "Alert sent to blue team",
        "timestamp": "2023-12-31T12:38:45Z",
        "recipient": "detection_agent_001",
        "message_type": "alert"
      }
    ],
    "total": 25,
    "limit": 50
  },
  "timestamp": "2023-12-31T12:39:00Z"
}
```

### Get Agent Metrics
```http
GET /api/v1/agents/{agent_id}/metrics
```

**Response:**
```json
{
  "success": true,
  "data": {
    "agent_id": "recon_agent_001",
    "metrics": {
      "tasks_completed": 15,
      "tasks_failed": 2,
      "success_rate": 88.2,
      "average_response_time": 45.5,
      "total_duration": 7200,
      "commands_processed": 17,
      "messages_sent": 23,
      "messages_received": 19,
      "cpu_usage": 45.2,
      "memory_usage": 512,
      "tools_used": ["nmap", "shodan", "whois", "dns_enumeration"],
      "mitre_techniques_used": ["T1592", "T1595", "T1596", "T1598"]
    },
    "performance": {
      "tasks_per_hour": 7.5,
      "commands_per_hour": 8.5,
      "messages_per_hour": 19.2,
      "average_task_duration": 45.5
    }
  },
  "timestamp": "2023-12-31T12:39:00Z"
}
```

## 🔧 Agent Configuration

### Update Agent Configuration
```http
PUT /api/v1/agents/{agent_id}/config
Content-Type: application/json
```

**Request Body:**
```json
{
  "max_tasks": 150,
  "timeout_seconds": 600,
  "memory_limit": "2GB",
  "enable_mcp": true,
  "logging_level": "INFO",
  "custom_settings": {
    "preferred_tools": ["nmap", "shodan"],
    "mitre_focus": ["reconnaissance", "resource_development"]
  }
}
```

### Reset Agent
```http
POST /api/v1/agents/{agent_id}/reset
```

**Response:**
```json
{
  "success": true,
  "data": {
    "agent_id": "recon_agent_001",
    "status": "reset",
    "message": "Agent has been reset to initial state",
    "timestamp": "2023-12-31T12:39:00Z"
  },
  "timestamp": "2023-12-31T12:39:00Z"
}
```

## 📊 Agent Types Reference

### Red Team Agent Types

#### Recon Agent (`red_team_recon`)
**Purpose**: Open-source intelligence gathering and reconnaissance

**Capabilities**:
- OSINT gathering
- Network mapping
- Vulnerability scanning
- Attack surface analysis
- Asset identification

**MITRE Techniques**: T1592, T1595, T1596, T1598

**Tools**: nmap, shodan, whois, dns_enumeration

**Example Commands**:
```json
{
  "type": "execute_task",
  "task": "Perform comprehensive OSINT on target",
  "parameters": {
    "target": "target.example.com",
    "techniques": ["T1595", "T1596"]
  }
}
```

#### Social Engineering Agent (`red_team_social`)
**Purpose**: Social engineering and phishing simulation

**Capabilities**:
- Phishing content generation
- Pretexting scenario development
- Trust exploitation patterns
- Social network analysis

**MITRE Techniques**: T1566, T1598, T1657, T1656

**Tools**: email_generator, social_media_analyzer, pretext_generator

#### Exploitation Agent (`red_team_exploit`)
**Purpose**: Vulnerability exploitation and attack path analysis

**Capabilities**:
- Vulnerability chaining analysis
- Attack path generation
- Security control bypass
- Exploit development

**MITRE Techniques**: T1203, T1210, T1190, T1068

**Tools**: exploit_framework, vulnerability_scanner, payload_generator

#### Lateral Movement Agent (`red_team_lateral`)
**Purpose**: Network traversal and persistence

**Capabilities**:
- Network traversal simulation
- Privilege escalation
- Persistence mechanism analysis
- Lateral movement paths

**MITRE Techniques**: T1021, T1028, T1547, T1574

**Tools**: network_traversal, privilege_escalation, persistence_kits

### Blue Team Agent Types

#### Detection Agent (`blue_team_detection`)
**Purpose**: Anomaly detection and IOC generation

**Capabilities**:
- Anomaly pattern recognition
- IOC generation and analysis
- Alert correlation
- Threat hunting

**MITRE Techniques**: TA0001, TA0002, TA0003, TA0004

**Tools**: siem, anomaly_detector, ioc_analyzer

#### Response Agent (`blue_team_response`)
**Purpose**: Incident response and containment

**Capabilities**:
- Incident triage and prioritization
- Containment strategy development
- Remediation procedures
- Incident coordination

**Tools**: incident_response, containment_tools, remediation_framework

#### Threat Intelligence Agent (`blue_team_threat_intel`)
**Purpose**: Threat attribution and TTP analysis

**Capabilities**:
- Attack attribution
- TTP mapping
- Threat landscape analysis
- Intelligence reporting

**MITRE Techniques**: All ATT&CK techniques

**Tools**: mitre_analyzer, threat_intelligence_feeds, attribution_engine

## 🧪 Error Handling

### Common Agent Errors

#### Agent Not Found
```json
{
  "success": false,
  "error": {
    "code": "AGENT_NOT_FOUND",
    "message": "Agent 'invalid_agent_id' does not exist"
  }
}
```

#### Agent Not Active
```json
{
  "success": false,
  "error": {
    "code": "AGENT_NOT_ACTIVE",
    "message": "Agent 'recon_agent_001' is not currently active"
  }
}
```

#### Invalid Command
```json
{
  "success": false,
  "error": {
    "code": "INVALID_COMMAND",
    "message": "Invalid command type provided",
    "details": "Command 'invalid_command' is not supported"
  }
}
```

#### Command Timeout
```json
{
  "success": false,
  "error": {
    "code": "COMMAND_TIMEOUT",
    "message": "Command execution timed out",
    "details": "Command exceeded timeout of 300 seconds"
  }
}
```

## 📚 SDK Examples

### Python SDK
```python
from simulation_client import AgentClient

# Initialize agent client
agent_client = AgentClient(
    base_url="http://localhost:8080",
    api_key="your-api-key"
)

# List all agents
agents = agent_client.list_agents()
print(f"Found {len(agents['data']['agents'])} agents")

# Get specific agent
agent = agent_client.get_agent("recon_agent_001")
print(f"Agent: {agent['data']['agent_type']}")

# Send command to agent
command = agent_client.send_command(
    agent_id="recon_agent_001",
    command_type="execute_task",
    task="Perform OSINT on target",
    parameters={"target": "example.com"}
)

# Monitor command progress
while command.get_status()["data"]["status"] == "running":
    print(f"Command status: {command.get_status()['data']['status']}")
    time.sleep(5)

# Get command result
result = agent_client.get_command_result(command["data"]["command_id"])
print(f"Command result: {result['data']['result']['success']}")
```

### JavaScript SDK
```javascript
import { AgentClient } from '@autonomous-multi-agent/sdk';

// Initialize agent client
const agentClient = new AgentClient({
    baseUrl: 'http://localhost:8080',
    apiKey: 'your-api-key'
});

// List all agents
const agents = await agentClient.listAgents();
console.log(`Found ${agents.data.agents.length} agents`);

// Get specific agent
const agent = await agentClient.getAgent('recon_agent_001');
console.log(`Agent: ${agent.data.agentType}`);

// Send command to agent
const command = await agentClient.sendCommand('recon_agent_001', {
    type: 'execute_task',
    task: 'Perform OSINT on target',
    parameters: { target: 'example.com' }
});

// Monitor command progress
command.on('completed', (result) => {
    console.log('Command completed:', result.data.result.success);
});

// Wait for completion
await command.waitForCompletion();
```

## 📖 Additional Resources

- [Main API Documentation](README.md)
- [Scenario API Documentation](scenarios.md)
- [MCP API Documentation](mcp.md)
- [Dashboard API Documentation](dashboard.md)
- [Examples](../../examples/)

## 🆘 Support

For agent API support:
- Create an issue on GitHub
- Check the [examples](../../examples/)
- Review the [testing guide](../../tests/)
- Contact the development team
