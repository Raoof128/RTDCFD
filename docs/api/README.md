# API Documentation

This section provides comprehensive API documentation for the Autonomous Multi-Agent Red/Blue Team Simulation System.

## 📚 API Overview

The system provides several APIs for different use cases:

- **Simulation API**: Core simulation management
- **Agent API**: Agent interaction and control
- **Scenario API**: Scenario management and configuration
- **MCP API**: Inter-agent communication
- **Dashboard API**: Real-time monitoring and visualization

## 🔗 API Endpoints

### Simulation API

#### Base URL: `http://localhost:8080/api/v1`

#### Simulation Management

##### Start Simulation
```http
POST /api/v1/simulation/start
Content-Type: application/json

{
  "scenario_name": "soci_energy_grid",
  "timeout_minutes": 60,
  "enable_dashboard": true,
  "config": {
    "log_level": "INFO",
    "simulation_mode_only": true
  }
}
```

**Response:**
```json
{
  "simulation_id": "sim_20231231_123456",
  "status": "started",
  "scenario_name": "soci_energy_grid",
  "start_time": "2023-12-31T12:34:56Z",
  "agents": {
    "red_team": ["recon_agent", "social_engineering_agent", "exploitation_agent", "lateral_movement_agent"],
    "blue_team": ["detection_agent", "response_agent", "threat_intel_agent"]
  }
}
```

##### Stop Simulation
```http
POST /api/v1/simulation/stop
Content-Type: application/json

{
  "simulation_id": "sim_20231231_123456"
}
```

##### Get Simulation Status
```http
GET /api/v1/simulation/{simulation_id}/status
```

**Response:**
```json
{
  "simulation_id": "sim_20231231_123456",
  "status": "running",
  "current_phase": "initial_access",
  "progress": 45,
  "start_time": "2023-12-31T12:34:56Z",
  "elapsed_time": 1800,
  "agents": {
    "active": 7,
    "completed_tasks": 23,
    "failed_tasks": 2
  },
  "scores": {
    "red_team": 65,
    "blue_team": 35
  }
}
```

##### Generate Report
```http
POST /api/v1/simulation/{simulation_id}/report
Content-Type: application/json

{
  "format": "json",
  "include_timeline": true,
  "include_mitre_analysis": true,
  "include_compliance": true
}
```

### Agent API

#### Base URL: `http://localhost:8080/api/v1/agents`

#### Agent Management

##### List All Agents
```http
GET /api/v1/agents
```

**Response:**
```json
{
  "agents": [
    {
      "agent_id": "recon_agent_001",
      "agent_type": "red_team_recon",
      "status": "active",
      "capabilities": ["osint", "network_mapping", "vulnerability_scanning"],
      "current_task": "OSINT gathering on target infrastructure"
    },
    {
      "agent_id": "detection_agent_001",
      "agent_type": "blue_team_detection",
      "status": "active",
      "capabilities": ["anomaly_detection", "ioc_generation", "alert_correlation"],
      "current_task": "Monitoring network traffic for anomalies"
    }
  ]
}
```

##### Get Agent Details
```http
GET /api/v1/agents/{agent_id}
```

##### Send Command to Agent
```http
POST /api/v1/agents/{agent_id}/command
Content-Type: application/json

{
  "type": "execute_task",
  "task": "Perform OSINT on target infrastructure",
  "parameters": {
    "target": "energy-grid.example.com",
    "techniques": ["T1595", "T1596"]
  },
  "timeout": 300
}
```

**Response:**
```json
{
  "command_id": "cmd_20231231_123456",
  "status": "queued",
  "agent_id": "recon_agent_001",
  "timestamp": "2023-12-31T12:34:56Z"
}
```

##### Get Agent Capabilities
```http
GET /api/v1/agents/{agent_id}/capabilities
```

### Scenario API

#### Base URL: `http://localhost:8080/api/v1/scenarios`

#### Scenario Management

##### List Available Scenarios
```http
GET /api/v1/scenarios
```

**Response:**
```json
{
  "scenarios": [
    {
      "id": "soci_energy_grid",
      "name": "SOCI Act Energy Grid Scenario",
      "description": "Critical infrastructure simulation for energy grid",
      "sector": "energy",
      "difficulty": "advanced",
      "estimated_duration": 60,
      "critical_assets": 4,
      "attack_vectors": 5,
      "defensive_measures": 5
    },
    {
      "id": "soci_telco_network",
      "name": "SOCI Act Telecommunications Network Scenario",
      "description": "Critical infrastructure simulation for telecommunications",
      "sector": "telecommunications",
      "difficulty": "advanced",
      "estimated_duration": 45,
      "critical_assets": 3,
      "attack_vectors": 5,
      "defensive_measures": 5
    }
  ]
}
```

##### Get Scenario Details
```http
GET /api/v1/scenarios/{scenario_id}
```

##### Validate Scenario
```http
POST /api/v1/scenarios/{scenario_id}/validate
```

### MCP API

#### Base URL: `http://localhost:8080/api/v1/mcp`

#### MCP Server Management

##### Get Server Status
```http
GET /api/v1/mcp/status
```

**Response:**
```json
{
  "servers": {
    "main": {
      "status": "running",
      "host": "localhost",
      "port": 8080,
      "connections": 7,
      "messages_sent": 1234,
      "messages_received": 1156
    },
    "red_team": {
      "status": "running",
      "host": "localhost",
      "port": 8081,
      "connections": 4,
      "messages_sent": 567,
      "messages_received": 523
    },
    "blue_team": {
      "status": "running",
      "host": "localhost",
      "port": 8082,
      "connections": 3,
      "messages_sent": 234,
      "messages_received": 198
    }
  }
}
```

##### Send Message
```http
POST /api/v1/mcp/message
Content-Type: application/json

{
  "sender_id": "recon_agent_001",
  "receiver_id": "detection_agent_001",
  "message_type": "alert",
  "content": {
    "alert_type": "suspicious_activity",
    "description": "Unusual network traffic detected",
    "severity": "medium",
    "data": {
      "source_ip": "192.168.1.100",
      "destination": "10.0.0.50",
      "protocol": "HTTP",
      "timestamp": "2023-12-31T12:34:56Z"
    }
  },
  "priority": "normal"
}
```

### Dashboard API

#### Base URL: `http://localhost:8501/api`

#### Real-time Data

##### Get Real-time Metrics
```http
GET /api/metrics
```

**Response:**
```json
{
  "simulation": {
    "status": "running",
    "phase": "execution",
    "progress": 45,
    "elapsed_time": 1800,
    "estimated_remaining": 1200
  },
  "agents": {
    "total": 7,
    "active": 7,
    "red_team": {
      "active": 4,
      "tasks_completed": 23,
      "tasks_failed": 2
    },
    "blue_team": {
      "active": 3,
      "tasks_completed": 18,
      "tasks_failed": 1
    }
  },
  "scores": {
    "red_team": 65,
    "blue_team": 35,
    "trend": "red_team_up"
  },
  "events": [
    {
      "timestamp": "2023-12-31T12:34:56Z",
      "type": "agent_task_completed",
      "agent_id": "recon_agent_001",
      "description": "OSINT gathering completed"
    }
  ]
}
```

##### Get MITRE ATT&CK Analysis
```http
GET /api/mitre/analysis
```

##### Get Compliance Status
```http
GET /api/compliance/status
```

## 🔐 Authentication

### API Key Authentication
All API endpoints require authentication using an API key:

```http
Authorization: Bearer your-api-key-here
```

### Getting an API Key
1. Set `ANTHROPIC_API_KEY` in your environment
2. Use the `/api/v1/auth/token` endpoint to generate a temporary token
3. Include the token in the `Authorization` header

### Token Generation
```http
POST /api/v1/auth/token
Content-Type: application/json

{
  "username": "your-username",
  "password": "your-password"
}
```

## 📊 Response Formats

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "Invalid scenario ID provided",
    "details": "Scenario 'invalid_scenario' does not exist"
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

### HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created
- `400 Bad Request`: Invalid parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service temporarily unavailable

## 🔄 WebSockets

### Real-time Updates
Connect to WebSocket endpoints for real-time updates:

```javascript
const ws = new WebSocket('ws://localhost:8080/ws/simulation/{simulation_id}');

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Real-time update:', data);
};
```

### WebSocket Events
- `simulation_started`: Simulation has started
- `phase_changed`: Simulation phase changed
- `agent_task_completed`: Agent completed a task
- `score_updated`: Team scores updated
- `alert_generated`: Security alert generated
- `simulation_completed`: Simulation completed

## 🧪 Testing

### API Testing Examples

#### Using curl
```bash
# Start simulation
curl -X POST http://localhost:8080/api/v1/simulation/start \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "scenario_name": "soci_energy_grid",
    "timeout_minutes": 60
  }'

# Get simulation status
curl -X GET http://localhost:8080/api/v1/simulation/sim_20231231_123456/status \
  -H "Authorization: Bearer your-api-key"

# Send agent command
curl -X POST http://localhost:8080/api/v1/agents/recon_agent_001/command \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "type": "execute_task",
    "task": "Perform OSINT on target"
  }'
```

#### Using Python
```python
import requests
import json

# API configuration
BASE_URL = "http://localhost:8080/api/v1"
API_KEY = "your-api-key"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Start simulation
response = requests.post(
    f"{BASE_URL}/simulation/start",
    headers=HEADERS,
    json={
        "scenario_name": "soci_energy_grid",
        "timeout_minutes": 60
    }
)

simulation_data = response.json()
print(f"Simulation started: {simulation_data['simulation_id']}")
```

## 📚 SDK Examples

### Python SDK
```python
from simulation_client import SimulationClient

# Initialize client
client = SimulationClient(
    base_url="http://localhost:8080",
    api_key="your-api-key"
)

# Start simulation
simulation = client.start_simulation(
    scenario_name="soci_energy_grid",
    timeout_minutes=60
)

# Monitor progress
while simulation.is_running():
    status = simulation.get_status()
    print(f"Progress: {status['progress']}%")
    time.sleep(5)

# Generate report
report = simulation.generate_report()
print(f"Report generated: {report['file_path']}")
```

### JavaScript SDK
```javascript
import { SimulationClient } from '@autonomous-multi-agent/sdk';

// Initialize client
const client = new SimulationClient({
    baseUrl: 'http://localhost:8080',
    apiKey: 'your-api-key'
});

// Start simulation
const simulation = await client.startSimulation({
    scenarioName: 'soci_energy_grid',
    timeoutMinutes: 60
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

## 🔍 Error Handling

### Common Errors

#### Authentication Errors
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or missing API key"
  }
}
```

#### Validation Errors
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid parameters provided",
    "details": {
      "field": "scenario_name",
      "error": "Required field missing"
    }
  }
}
```

#### Simulation Errors
```json
{
  "success": false,
  "error": {
    "code": "SIMULATION_ERROR",
    "message": "Simulation failed to start",
    "details": "Scenario configuration is invalid"
  }
}
```

## 📝 Rate Limiting

### Rate Limits
- **Simulation API**: 100 requests per minute
- **Agent API**: 200 requests per minute
- **Scenario API**: 50 requests per minute
- **MCP API**: 500 requests per minute
- **Dashboard API**: 1000 requests per minute

### Rate Limit Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 60
```

## 🚀 Deployment

### Production Deployment
```bash
# Production API server
python -m uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4

# With SSL
python -m uvicorn main:app --host 0.0.0.0 --port 8443 --ssl-keyfile key.pem --ssl-certfile cert.pem
```

### Docker Deployment
```bash
# Build image
docker build -t simulation-api .

# Run container
docker run -p 8080:8080 -e ANTHROPIC_API_KEY=your-key simulation-api
```

## 📖 Additional Resources

- [Architecture Documentation](../ARCHITERCURE.md)
- [Security Policy](../SECURITY.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Examples](../examples/)
- [Testing Guide](../tests/)

## 🆘 Support

For API support and questions:
- Create an issue on GitHub
- Check the [documentation](../docs/)
- Review the [examples](../examples/)
- Contact the development team
