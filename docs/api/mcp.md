# MCP API Documentation

## 🔄 MCP Overview

The MCP (Model Context Protocol) API provides endpoints for managing inter-agent communication within the autonomous multi-agent simulation system. The MCP API enables real-time messaging, coordination, and data exchange between agents, ensuring seamless collaboration and information sharing.

## 🔗 Base URLs
```
Main MCP Server: http://localhost:8080/api/v1/mcp
Red Team MCP: http://localhost:8081/api/v1/mcp
Blue Team MCP: http://localhost:8082/api/v1/mcp
```

## 🏗️ MCP Architecture

### Server Types
- **Main MCP Server**: Central coordination and cross-team communication
- **Red Team MCP Server**: Red team internal communication
- **Blue Team MCP Server**: Blue team internal communication

### Message Types
- **Command**: Agent commands and task assignments
- **Alert**: Security alerts and notifications
- **Data**: Information sharing and data exchange
- **Status**: Agent status updates and heartbeats
- **Coordination**: Cross-team coordination messages

## 🚀 API Endpoints

### Get Server Status
```http
GET /api/v1/mcp/status
```

**Response:**
```json
{
  "success": true,
  "data": {
    "server_type": "main",
    "status": "running",
    "host": "localhost",
    "port": 8080,
    "uptime": 7200,
    "connections": {
      "total": 7,
      "active": 7,
      "red_team": 4,
      "blue_team": 3
    },
    "messaging": {
      "messages_sent": 1234,
      "messages_received": 1156,
      "messages_queued": 0,
      "average_throughput": 0.17
    },
    "performance": {
      "cpu_usage": 15.2,
      "memory_usage": 256,
      "network_io": 1024,
      "error_rate": 0.01
    },
    "version": "1.0.0",
    "start_time": "2023-12-31T10:30:00Z"
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

### Get Connected Agents
```http
GET /api/v1/mcp/agents
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
        "team": "red_team",
        "status": "connected",
        "connection_time": "2023-12-31T10:35:00Z",
        "last_heartbeat": "2023-12-31T12:34:56Z",
        "messages_sent": 234,
        "messages_received": 198,
        "capabilities": ["osint_gathering", "network_mapping"]
      },
      {
        "agent_id": "detection_agent_001",
        "agent_type": "blue_team_detection",
        "team": "blue_team",
        "status": "connected",
        "connection_time": "2023-12-31T10:35:15Z",
        "last_heartbeat": "2023-12-31T12:34:58Z",
        "messages_sent": 156,
        "messages_received": 178,
        "capabilities": ["anomaly_detection", "ioc_generation"]
      }
    ],
    "total": 7,
    "red_team": 4,
    "blue_team": 3,
    "connected": 7
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

### Send Message
```http
POST /api/v1/mcp/message
Content-Type: application/json
```

**Request Body:**
```json
{
  "sender_id": "recon_agent_001",
  "receiver_id": "detection_agent_001",
  "message_type": "alert",
  "priority": "normal",
  "content": {
    "alert_type": "suspicious_activity",
    "description": "Unusual network traffic detected",
    "severity": "medium",
    "data": {
      "source_ip": "192.168.1.100",
      "destination": "10.0.0.50",
      "protocol": "HTTP",
      "port": 80,
      "timestamp": "2023-12-31T12:34:56Z",
      "packet_count": 1250,
      "bytes_transferred": 2048576
    },
    "mitre_technique": "T1071",
    "recommendations": [
      "Investigate source IP",
      "Monitor for similar traffic patterns",
      "Check for data exfiltration"
    ]
  },
  "metadata": {
    "simulation_id": "sim_20231231_123456",
    "phase": "execution",
    "correlation_id": "correl_20231231_123456"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message_id": "msg_20231231_123456",
    "sender_id": "recon_agent_001",
    "receiver_id": "detection_agent_001",
    "message_type": "alert",
    "status": "sent",
    "timestamp": "2023-12-31T12:34:56Z",
    "delivery_confirmed": true,
    "delivery_time": "2023-12-31T12:34:57Z"
  },
  "timestamp": "2023-12-31T12:34:57Z"
}
```

### Broadcast Message
```http
POST /api/v1/mcp/broadcast
Content-Type: application/json
```

**Request Body:**
```json
{
  "sender_id": "coordinator_001",
  "message_type": "coordination",
  "priority": "high",
  "target_teams": ["red_team", "blue_team"],
  "target_agent_types": ["red_team_recon", "blue_team_detection"],
  "content": {
    "coordination_type": "phase_change",
    "description": "Simulation phase changing to execution",
    "new_phase": "execution",
    "start_time": "2023-12-31T12:35:00Z",
    "instructions": {
      "red_team": "Begin execution phase activities",
      "blue_team": "Enhance monitoring for execution phase"
    },
    "constraints": {
      "max_duration": 3600,
      "safety_checks": true,
      "compliance_monitoring": true
    }
  },
  "metadata": {
    "simulation_id": "sim_20231231_123456",
    "correlation_id": "phase_change_123456"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "broadcast_id": "bc_20231231_123456",
    "sender_id": "coordinator_001",
    "message_type": "coordination",
    "status": "sent",
    "timestamp": "2023-12-31T12:34:56Z",
    "recipients": {
      "targeted": 7,
      "delivered": 7,
      "failed": 0
    },
    "delivery_details": [
      {
        "agent_id": "recon_agent_001",
        "status": "delivered",
        "delivery_time": "2023-12-31T12:34:57Z"
      },
      {
        "agent_id": "detection_agent_001",
        "status": "delivered",
        "delivery_time": "2023-12-31T12:34:57Z"
      }
    ]
  },
  "timestamp": "2023-12-31T12:34:57Z"
}
```

### Get Message History
```http
GET /api/v1/mcp/messages
```

**Query Parameters:**
- `sender_id` (string, optional): Filter by sender
- `receiver_id` (string, optional): Filter by receiver
- `message_type` (string, optional): Filter by message type
- `priority` (string, optional): Filter by priority
- `since` (string, optional): Return messages since this timestamp
- `limit` (integer, optional): Number of messages to return (default: 100)

**Response:**
```json
{
  "success": true,
  "data": {
    "messages": [
      {
        "message_id": "msg_20231231_123456",
        "sender_id": "recon_agent_001",
        "receiver_id": "detection_agent_001",
        "message_type": "alert",
        "priority": "normal",
        "status": "delivered",
        "content": {
          "alert_type": "suspicious_activity",
          "description": "Unusual network traffic detected",
          "severity": "medium"
        },
        "timestamp": "2023-12-31T12:34:56Z",
        "delivery_time": "2023-12-31T12:34:57Z",
        "metadata": {
          "simulation_id": "sim_20231231_123456",
          "phase": "execution"
        }
      }
    ],
    "total": 1234,
    "limit": 100,
    "filters": {
      "message_type": "alert",
      "priority": "normal"
    }
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

### Get Message Details
```http
GET /api/v1/mcp/messages/{message_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message_id": "msg_20231231_123456",
    "sender_id": "recon_agent_001",
    "receiver_id": "detection_agent_001",
    "message_type": "alert",
    "priority": "normal",
    "status": "delivered",
    "content": {
      "alert_type": "suspicious_activity",
      "description": "Unusual network traffic detected",
      "severity": "medium",
      "data": {
        "source_ip": "192.168.1.100",
        "destination": "10.0.0.50",
        "protocol": "HTTP",
        "port": 80,
        "timestamp": "2023-12-31T12:34:56Z",
        "packet_count": 1250,
        "bytes_transferred": 2048576
      },
      "mitre_technique": "T1071",
      "recommendations": [
        "Investigate source IP",
        "Monitor for similar traffic patterns",
        "Check for data exfiltration"
      ]
    },
    "metadata": {
      "simulation_id": "sim_20231231_123456",
      "phase": "execution",
      "correlation_id": "correl_20231231_123456"
    },
    "timestamp": "2023-12-31T12:34:56Z",
    "delivery_time": "2023-12-31T12:34:57Z",
    "read_time": "2023-12-31T12:35:02Z",
    "processing_time": 5
  },
  "timestamp": "2023-12-31T12:35:02Z"
}
```

### Get Server Metrics
```http
GET /api/v1/mcp/metrics
```

**Response:**
```json
{
  "success": true,
  "data": {
    "server_metrics": {
      "uptime": 7200,
      "connections": {
        "total": 7,
        "active": 7,
        "peak": 7,
        "average_duration": 7200
      },
      "messaging": {
        "messages_sent": 1234,
        "messages_received": 1156,
        "messages_queued": 0,
        "average_throughput": 0.17,
        "peak_throughput": 0.25,
        "message_size_average": 1024,
        "message_size_peak": 8192
      },
      "performance": {
        "cpu_usage": 15.2,
        "memory_usage": 256,
        "network_io": 1024,
        "disk_io": 512,
        "error_rate": 0.01,
        "latency_average": 5,
        "latency_p95": 15
      },
      "errors": {
        "total_errors": 12,
        "connection_errors": 2,
        "message_errors": 8,
        "system_errors": 2,
        "error_rate_trend": "decreasing"
      }
    },
    "agent_metrics": [
      {
        "agent_id": "recon_agent_001",
        "messages_sent": 234,
        "messages_received": 198,
        "average_response_time": 45,
        "success_rate": 98.5,
        "last_activity": "2023-12-31T12:34:56Z"
      }
    ]
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

## 📡 WebSocket Connections

### Connect to MCP WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8080/ws/mcp');

ws.onopen = function(event) {
    console.log('Connected to MCP WebSocket');
    
    // Authenticate
    ws.send(JSON.stringify({
        type: 'auth',
        agent_id: 'recon_agent_001',
        token: 'your-auth-token'
    }));
};

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    console.log('Received message:', message);
    
    // Handle different message types
    switch(message.type) {
        case 'message':
            handleIncomingMessage(message.data);
            break;
        case 'broadcast':
            handleBroadcast(message.data);
            break;
        case 'status':
            handleStatusUpdate(message.data);
            break;
    }
};
```

### WebSocket Message Types

#### Authentication
```json
{
  "type": "auth",
  "agent_id": "recon_agent_001",
  "token": "your-auth-token"
}
```

#### Incoming Message
```json
{
  "type": "message",
  "data": {
    "message_id": "msg_20231231_123456",
    "sender_id": "detection_agent_001",
    "receiver_id": "recon_agent_001",
    "message_type": "alert",
    "priority": "normal",
    "content": {
      "alert_type": "suspicious_activity",
      "description": "Unusual network traffic detected"
    },
    "timestamp": "2023-12-31T12:34:56Z"
  }
}
```

#### Broadcast Message
```json
{
  "type": "broadcast",
  "data": {
    "broadcast_id": "bc_20231231_123456",
    "sender_id": "coordinator_001",
    "message_type": "coordination",
    "content": {
      "coordination_type": "phase_change",
      "new_phase": "execution"
    },
    "timestamp": "2023-12-31T12:34:56Z"
  }
}
```

#### Status Update
```json
{
  "type": "status",
  "data": {
    "server_status": "running",
    "connected_agents": 7,
    "messages_sent": 1234,
    "messages_received": 1156
  }
}
```

## 🔧 Message Types Reference

### Command Messages
Used for agent commands and task assignments.

**Structure:**
```json
{
  "message_type": "command",
  "content": {
    "command_type": "execute_task",
    "task": "Perform OSINT on target",
    "parameters": {
      "target": "example.com",
      "techniques": ["T1595", "T1596"]
    },
    "timeout": 300,
    "priority": "normal"
  }
}
```

### Alert Messages
Used for security alerts and notifications.

**Structure:**
```json
{
  "message_type": "alert",
  "content": {
    "alert_type": "suspicious_activity",
    "description": "Unusual network traffic detected",
    "severity": "medium",
    "data": {
      "source_ip": "192.168.1.100",
      "destination": "10.0.0.50"
    },
    "mitre_technique": "T1071"
  }
}
```

### Data Messages
Used for information sharing and data exchange.

**Structure:**
```json
{
  "message_type": "data",
  "content": {
    "data_type": "osint_results",
    "description": "OSINT gathering results",
    "data": {
      "target": "example.com",
      "findings": [
        {
          "type": "open_port",
          "value": 80,
          "service": "HTTP"
        }
      ]
    }
  }
}
```

### Status Messages
Used for agent status updates and heartbeats.

**Structure:**
```json
{
  "message_type": "status",
  "content": {
    "status_type": "heartbeat",
    "agent_status": "active",
    "current_task": "OSINT gathering",
    "progress": 75,
    "metrics": {
      "cpu_usage": 45,
      "memory_usage": 512
    }
  }
}
```

### Coordination Messages
Used for cross-team coordination and phase changes.

**Structure:**
```json
{
  "message_type": "coordination",
  "content": {
    "coordination_type": "phase_change",
    "new_phase": "execution",
    "instructions": {
      "red_team": "Begin execution activities",
      "blue_team": "Enhance monitoring"
    }
  }
}
```

## 🧪 Error Handling

### Common MCP Errors

#### Server Not Available
```json
{
  "success": false,
  "error": {
    "code": "SERVER_UNAVAILABLE",
    "message": "MCP server is not available",
    "details": "Server status: stopped"
  }
}
```

#### Agent Not Connected
```json
{
  "success": false,
  "error": {
    "code": "AGENT_NOT_CONNECTED",
    "message": "Agent is not connected to MCP server",
    "details": "Agent 'recon_agent_001' not found in active connections"
  }
}
```

#### Message Delivery Failed
```json
{
  "success": false,
  "error": {
    "code": "MESSAGE_DELIVERY_FAILED",
    "message": "Failed to deliver message",
    "details": "Receiver 'detection_agent_001' not reachable"
  }
}
```

#### Invalid Message Format
```json
{
  "success": false,
  "error": {
    "code": "INVALID_MESSAGE_FORMAT",
    "message": "Message format is invalid",
    "details": "Missing required field: message_type"
  }
}
```

#### Authentication Failed
```json
{
  "success": false,
  "error": {
    "code": "AUTHENTICATION_FAILED",
    "message": "Authentication failed",
    "details": "Invalid or expired token"
  }
}
```

## 📚 SDK Examples

### Python SDK
```python
from simulation_client import MCPClient

# Initialize MCP client
mcp_client = MCPClient(
    base_url="http://localhost:8080",
    api_key="your-api-key"
)

# Get server status
status = mcp_client.get_status()
print(f"Server status: {status['data']['status']}")

# Send message to agent
message = mcp_client.send_message(
    sender_id="recon_agent_001",
    receiver_id="detection_agent_001",
    message_type="alert",
    content={
        "alert_type": "suspicious_activity",
        "description": "Unusual network traffic detected",
        "severity": "medium"
    }
)

# Broadcast message to all agents
broadcast = mcp_client.broadcast_message(
    sender_id="coordinator_001",
    message_type="coordination",
    content={
        "coordination_type": "phase_change",
        "new_phase": "execution"
    },
    target_teams=["red_team", "blue_team"]
)

# Get message history
history = mcp_client.get_message_history(
    message_type="alert",
    since="2023-12-31T12:00:00Z",
    limit=50
)

# WebSocket connection
def handle_message(message_data):
    print(f"Received message: {message_data['content']['description']}")

mcp_client.connect_websocket(
    agent_id="recon_agent_001",
    message_handlers={
        "message": handle_message,
        "broadcast": handle_message
    }
)
```

### JavaScript SDK
```javascript
import { MCPClient } from '@autonomous-multi-agent/sdk';

// Initialize MCP client
const mcpClient = new MCPClient({
    baseUrl: 'http://localhost:8080',
    apiKey: 'your-api-key'
});

// Get server status
const status = await mcpClient.getStatus();
console.log(`Server status: ${status.data.status}`);

// Send message to agent
const message = await mcpClient.sendMessage('recon_agent_001', 'detection_agent_001', {
    messageType: 'alert',
    content: {
        alertType: 'suspicious_activity',
        description: 'Unusual network traffic detected',
        severity: 'medium'
    }
});

// Broadcast message to all agents
const broadcast = await mcpClient.broadcastMessage('coordinator_001', {
    messageType: 'coordination',
    content: {
        coordinationType: 'phase_change',
        newPhase: 'execution'
    },
    targetTeams: ['red_team', 'blue_team']
});

// Get message history
const history = await mcpClient.getMessageHistory({
    messageType: 'alert',
    since: '2023-12-31T12:00:00Z',
    limit: 50
});

// WebSocket connection
mcpClient.connectWebSocket('recon_agent_001', {
    message: (messageData) => {
        console.log(`Received message: ${messageData.content.description}`);
    },
    broadcast: (broadcastData) => {
        console.log(`Received broadcast: ${broadcastData.content.description}`);
    }
});
```

## 📖 Additional Resources

- [Main API Documentation](README.md)
- [Agents API Documentation](agents.md)
- [Scenarios API Documentation](scenarios.md)
- [Dashboard API Documentation](dashboard.md)
- [WebSocket Documentation](../websockets/)
- [Examples](../../examples/)

## 🆘 Support

For MCP API support:
- Create an issue on GitHub
- Check the [examples](../../examples/)
- Review the [testing guide](../../tests/)
- Contact the development team
