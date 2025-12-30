# WebSocket API Documentation

## 🔄 WebSocket Overview

The WebSocket API provides real-time, bidirectional communication between the simulation system and client applications. WebSockets enable instant updates, live monitoring, and interactive dashboard functionality without the overhead of HTTP polling.

## 🔗 WebSocket Endpoints

### Main WebSocket Server
```
ws://localhost:8080/ws/simulation/{simulation_id}
```

### MCP WebSocket Servers
```
Main MCP: ws://localhost:8080/ws/mcp
Red Team MCP: ws://localhost:8081/ws/mcp
Blue Team MCP: ws://localhost:8082/ws/mcp
```

### Dashboard WebSocket
```
ws://localhost:8501/ws/dashboard
```

## 📡 Connection Protocol

### Authentication
WebSocket connections require authentication using a token or API key:

```javascript
const ws = new WebSocket('ws://localhost:8080/ws/simulation/sim_20231231_123456');

ws.onopen = function(event) {
    // Authenticate connection
    ws.send(JSON.stringify({
        type: 'auth',
        token: 'your-auth-token',
        client_id: 'client_001'
    }));
};
```

### Message Format
All WebSocket messages follow a consistent JSON format:

```json
{
  "type": "message_type",
  "data": { ... },
  "timestamp": "2023-12-31T12:34:56Z",
  "message_id": "msg_20231231_123456"
}
```

## 🚀 Message Types

### Authentication Messages

#### Authentication Request
```json
{
  "type": "auth",
  "token": "your-auth-token",
  "client_id": "client_001",
  "capabilities": ["receive_events", "send_commands"]
}
```

#### Authentication Response
```json
{
  "type": "auth_response",
  "status": "success",
  "client_id": "client_001",
  "session_id": "session_20231231_123456",
  "capabilities": ["receive_events", "send_commands"]
}
```

### Simulation Messages

#### Simulation Status Update
```json
{
  "type": "simulation_status",
  "data": {
    "simulation_id": "sim_20231231_123456",
    "status": "running",
    "phase": "execution",
    "progress": 45,
    "elapsed_time": 1800,
    "estimated_remaining": 1200
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

#### Phase Change Notification
```json
{
  "type": "phase_change",
  "data": {
    "simulation_id": "sim_20231231_123456",
    "old_phase": "initial_access",
    "new_phase": "execution",
    "start_time": "2023-12-31T12:35:00Z",
    "description": "Simulation phase changed to execution"
  },
  "timestamp": "2023-12-31T12:35:00Z"
}
```

#### Simulation Completed
```json
{
  "type": "simulation_completed",
  "data": {
    "simulation_id": "sim_20231231_123456",
    "status": "completed",
    "end_time": "2023-12-31T13:30:00Z",
    "total_duration": 3600,
    "final_scores": {
      "red_team": 65,
      "blue_team": 35,
      "winner": "red_team"
    },
    "report_generated": true
  },
  "timestamp": "2023-12-31T13:30:00Z"
}
```

### Agent Messages

#### Agent Status Update
```json
{
  "type": "agent_status",
  "data": {
    "agent_id": "recon_agent_001",
    "agent_type": "red_team_recon",
    "status": "active",
    "current_task": "OSINT gathering on target infrastructure",
    "progress": 75,
    "tasks_completed": 15,
    "tasks_failed": 2
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

#### Agent Task Completed
```json
{
  "type": "agent_task_completed",
  "data": {
    "agent_id": "recon_agent_001",
    "task_id": "task_20231231_123456",
    "task_type": "osint_gathering",
    "description": "OSINT gathering completed successfully",
    "success": true,
    "duration": 245,
    "findings": {
      "target": "energy-grid.example.com",
      "open_ports": [80, 443, 22],
      "technologies": ["Apache", "OpenSSH"]
    }
  },
  "timestamp": "2023-12-31T12:38:41Z"
}
```

#### Agent Error
```json
{
  "type": "agent_error",
  "data": {
    "agent_id": "exploitation_agent_001",
    "error_type": "task_failed",
    "error_message": "Failed to exploit target vulnerability",
    "task_id": "task_20231231_123457",
    "severity": "medium",
    "retry_count": 2
  },
  "timestamp": "2023-12-31T12:40:15Z"
}
```

### Event Messages

#### Security Alert
```json
{
  "type": "security_alert",
  "data": {
    "alert_id": "alert_20231231_123456",
    "severity": "medium",
    "alert_type": "suspicious_activity",
    "description": "Unusual network traffic detected",
    "source_agent": "detection_agent_001",
    "details": {
      "source_ip": "192.168.1.100",
      "destination": "10.0.0.50",
      "protocol": "HTTP",
      "packet_count": 1250,
      "bytes_transferred": 2048576
    },
    "mitre_technique": "T1071"
  },
  "timestamp": "2023-12-31T12:35:02Z"
}
```

#### System Event
```json
{
  "type": "system_event",
  "data": {
    "event_type": "resource_warning",
    "description": "CPU usage approaching threshold",
    "severity": "warning",
    "details": {
      "cpu_usage": 78.5,
      "threshold": 80.0,
      "affected_services": ["mcp_server", "agent_coordinator"]
    }
  },
  "timestamp": "2023-12-31T12:36:00Z"
}
```

### MCP Messages

#### Message Delivered
```json
{
  "type": "message_delivered",
  "data": {
    "message_id": "msg_20231231_123456",
    "sender_id": "recon_agent_001",
    "receiver_id": "detection_agent_001",
    "message_type": "alert",
    "delivery_time": "2023-12-31T12:34:57Z",
    "status": "delivered"
  },
  "timestamp": "2023-12-31T12:34:57Z"
}
```

#### Message Failed
```json
{
  "type": "message_failed",
  "data": {
    "message_id": "msg_20231231_123457",
    "sender_id": "recon_agent_001",
    "receiver_id": "offline_agent_001",
    "message_type": "data",
    "error": "Receiver not connected",
    "retry_count": 3
  },
  "timestamp": "2023-12-31T12:35:30Z"
}
```

### Dashboard Messages

#### Metrics Update
```json
{
  "type": "metrics_update",
  "data": {
    "simulation": {
      "progress": 46,
      "elapsed_time": 1860
    },
    "agents": {
      "red_team": {
        "tasks_completed": 24,
        "success_rate": 92.0
      },
      "blue_team": {
        "tasks_completed": 18,
        "success_rate": 94.7
      }
    },
    "scores": {
      "red_team": 67,
      "blue_team": 33
    }
  },
  "timestamp": "2023-12-31T12:35:00Z"
}
```

#### Chart Data Update
```json
{
  "type": "chart_update",
  "data": {
    "chart_id": "agent_performance",
    "chart_type": "line_chart",
    "series": [
      {
        "name": "recon_agent_001",
        "data": [
          {"timestamp": "2023-12-31T12:30:00Z", "value": 0},
          {"timestamp": "2023-12-31T12:35:00Z", "value": 3}
        ]
      }
    ]
  },
  "timestamp": "2023-12-31T12:35:00Z"
}
```

## 🔧 Client Implementation

### JavaScript Client
```javascript
class SimulationWebSocketClient {
    constructor(url, token) {
        this.url = url;
        this.token = token;
        this.ws = null;
        this.messageHandlers = {};
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
    }

    connect() {
        this.ws = new WebSocket(this.url);
        
        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.authenticate();
            this.reconnectAttempts = 0;
        };

        this.ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleMessage(message);
        };

        this.ws.onclose = (event) => {
            console.log('WebSocket disconnected');
            this.handleReconnect();
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }

    authenticate() {
        this.send({
            type: 'auth',
            token: this.token,
            client_id: 'web_client_' + Date.now()
        });
    }

    handleMessage(message) {
        const handler = this.messageHandlers[message.type];
        if (handler) {
            handler(message);
        } else {
            console.log('Unhandled message type:', message.type);
        }
    }

    on(messageType, handler) {
        this.messageHandlers[messageType] = handler;
    }

    send(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        } else {
            console.error('WebSocket not connected');
        }
    }

    handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);
            
            setTimeout(() => {
                this.connect();
            }, this.reconnectDelay * this.reconnectAttempts);
        } else {
            console.error('Max reconnect attempts reached');
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

// Usage example
const client = new SimulationWebSocketClient(
    'ws://localhost:8080/ws/simulation/sim_20231231_123456',
    'your-auth-token'
);

// Set up message handlers
client.on('simulation_status', (message) => {
    console.log('Simulation status:', message.data.status);
    updateProgressBar(message.data.progress);
});

client.on('agent_task_completed', (message) => {
    console.log('Task completed:', message.data.description);
    updateAgentStatus(message.data.agent_id, 'idle');
});

client.on('security_alert', (message) => {
    console.log('Security alert:', message.data.description);
    showAlert(message.data);
});

// Connect to WebSocket
client.connect();
```

### Python Client
```python
import asyncio
import websockets
import json
from typing import Dict, Callable, Any

class SimulationWebSocketClient:
    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token
        self.message_handlers: Dict[str, Callable] = {}
        self.websocket = None
        self.running = False

    async def connect(self):
        """Connect to WebSocket server"""
        try:
            self.websocket = await websockets.connect(self.url)
            await self.authenticate()
            self.running = True
            await self.listen()
        except Exception as e:
            print(f"Connection error: {e}")
            await self.reconnect()

    async def authenticate(self):
        """Authenticate with the server"""
        auth_message = {
            "type": "auth",
            "token": self.token,
            "client_id": "python_client_" + str(int(time.time()))
        }
        await self.send(auth_message)

    async def listen(self):
        """Listen for incoming messages"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                await self.handle_message(data)
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
            await self.reconnect()
        except Exception as e:
            print(f"Error listening for messages: {e}")

    async def handle_message(self, message: Dict[str, Any]):
        """Handle incoming message"""
        message_type = message.get("type")
        handler = self.message_handlers.get(message_type)
        
        if handler:
            try:
                await handler(message)
            except Exception as e:
                print(f"Error handling message {message_type}: {e}")
        else:
            print(f"Unhandled message type: {message_type}")

    async def send(self, message: Dict[str, Any]):
        """Send message to server"""
        if self.websocket:
            try:
                await self.websocket.send(json.dumps(message))
            except Exception as e:
                print(f"Error sending message: {e}")

    def on(self, message_type: str, handler: Callable):
        """Register message handler"""
        self.message_handlers[message_type] = handler

    async def reconnect(self):
        """Reconnect to WebSocket server"""
        if self.running:
            print("Attempting to reconnect...")
            await asyncio.sleep(2)
            await self.connect()

    async def disconnect(self):
        """Disconnect from WebSocket server"""
        self.running = False
        if self.websocket:
            await self.websocket.close()

# Usage example
async def main():
    client = SimulationWebSocketClient(
        'ws://localhost:8080/ws/simulation/sim_20231231_123456',
        'your-auth-token'
    )

    # Set up message handlers
    async def handle_simulation_status(message):
        print(f"Simulation status: {message['data']['status']}")
        # Update UI or process data

    async def handle_agent_task_completed(message):
        print(f"Task completed: {message['data']['description']}")
        # Process task completion

    client.on('simulation_status', handle_simulation_status)
    client.on('agent_task_completed', handle_agent_task_completed)

    # Connect and listen
    await client.connect()

if __name__ == "__main__":
    asyncio.run(main())
```

## 📊 Real-time Data Streaming

### Subscribe to Events
```javascript
// Subscribe to specific event types
client.send({
    type: 'subscribe',
    channels: ['simulation_status', 'agent_events', 'security_alerts'],
    filters: {
        severity: ['medium', 'high'],
        agent_types: ['red_team_recon', 'blue_team_detection']
    }
});
```

### Unsubscribe from Events
```javascript
// Unsubscribe from specific event types
client.send({
    type: 'unsubscribe',
    channels: ['system_events']
});
```

### Event Filtering
```javascript
// Set up event filters
client.send({
    type: 'set_filters',
    filters: {
        severity: ['high'],
        agent_ids: ['recon_agent_001', 'detection_agent_001'],
        mitre_techniques: ['T1595', 'T1071']
    }
});
```

## 🧪 Error Handling

### Connection Errors
```javascript
client.ws.onerror = function(error) {
    console.error('WebSocket error:', error);
    
    // Attempt reconnection
    if (client.reconnectAttempts < client.maxReconnectAttempts) {
        setTimeout(() => {
            client.connect();
        }, 5000);
    }
};
```

### Message Errors
```javascript
client.on('error', (message) => {
    console.error('Server error:', message.data.error);
    
    // Handle specific errors
    if (message.data.error_code === 'AUTHENTICATION_FAILED') {
        // Re-authenticate
        client.authenticate();
    }
});
```

### Rate Limiting
```javascript
// Implement rate limiting for outgoing messages
class RateLimitedClient extends SimulationWebSocketClient {
    constructor(url, token, rateLimit = 100) {
        super(url, token);
        this.rateLimit = rateLimit;
        this.messageQueue = [];
        this.lastMessageTime = 0;
    }

    send(message) {
        const now = Date.now();
        const timeSinceLastMessage = now - this.lastMessageTime;
        
        if (timeSinceLastMessage >= 1000 / this.rateLimit) {
            super.send(message);
            this.lastMessageTime = now;
        } else {
            this.messageQueue.push(message);
            setTimeout(() => this.processQueue(), 1000 / this.rateLimit - timeSinceLastMessage);
        }
    }

    processQueue() {
        if (this.messageQueue.length > 0) {
            const message = this.messageQueue.shift();
            super.send(message);
            this.lastMessageTime = Date.now();
            
            if (this.messageQueue.length > 0) {
                setTimeout(() => this.processQueue(), 1000 / this.rateLimit);
            }
        }
    }
}
```

## 📚 SDK Examples

### React Integration
```javascript
import React, { useState, useEffect } from 'react';
import { SimulationWebSocketClient } from './websocket-client';

function SimulationDashboard({ simulationId, token }) {
    const [simulationStatus, setSimulationStatus] = useState({});
    const [events, setEvents] = useState([]);
    const [connected, setConnected] = useState(false);

    useEffect(() => {
        const client = new SimulationWebSocketClient(
            `ws://localhost:8080/ws/simulation/${simulationId}`,
            token
        );

        client.on('simulation_status', (message) => {
            setSimulationStatus(message.data);
        });

        client.on('security_alert', (message) => {
            setEvents(prev => [message.data, ...prev.slice(0, 99)]);
        });

        client.on('connection_status', (status) => {
            setConnected(status.connected);
        });

        client.connect();

        return () => {
            client.disconnect();
        };
    }, [simulationId, token]);

    return (
        <div>
            <div>Status: {connected ? 'Connected' : 'Disconnected'}</div>
            <div>Progress: {simulationStatus.progress}%</div>
            <div>Events: {events.length}</div>
        </div>
    );
}
```

### Vue.js Integration
```javascript
import { ref, onMounted, onUnmounted } from 'vue';
import { SimulationWebSocketClient } from './websocket-client';

export default {
    props: ['simulationId', 'token'],
    setup(props) {
        const simulationStatus = ref({});
        const events = ref([]);
        const connected = ref(false);
        let client = null;

        onMounted(() => {
            client = new SimulationWebSocketClient(
                `ws://localhost:8080/ws/simulation/${props.simulationId}`,
                props.token
            );

            client.on('simulation_status', (message) => {
                simulationStatus.value = message.data;
            });

            client.on('security_alert', (message) => {
                events.value.unshift(message.data);
            });

            client.on('connection_status', (status) => {
                connected.value = status.connected;
            });

            client.connect();
        });

        onUnmounted(() => {
            if (client) {
                client.disconnect();
            }
        });

        return {
            simulationStatus,
            events,
            connected
        };
    }
};
```

## 📖 Additional Resources

- [Main API Documentation](README.md)
- [Agents API Documentation](agents.md)
- [Scenarios API Documentation](scenarios.md)
- [MCP API Documentation](mcp.md)
- [Dashboard API Documentation](dashboard.md)
- [WebSocket RFC 6455](https://tools.ietf.org/html/rfc6455)
- [WebSocket.org](https://websocket.org/)

## 🆘 Support

For WebSocket API support:
- Create an issue on GitHub
- Check the [examples](../../examples/)
- Review the [testing guide](../../tests/)
- Contact the development team
