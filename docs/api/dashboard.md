# Dashboard API Documentation

## 📊 Dashboard Overview

The Dashboard API provides endpoints for accessing real-time simulation data, metrics, and visualizations through the Streamlit-based dashboard interface. The API enables programmatic access to dashboard data, real-time updates, and integration with external monitoring systems.

## 🔗 Base URL
```
http://localhost:8501/api
```

## 📈 Dashboard Components

### Real-time Metrics
- Simulation status and progress
- Agent performance metrics
- Team scores and rankings
- System resource usage
- Event timeline and alerts

### Visualizations
- Network topology maps
- Attack path visualizations
- MITRE ATT&CK technique mapping
- Compliance status dashboards
- Performance charts and graphs

## 🚀 API Endpoints

### Get Real-time Metrics
```http
GET /api/metrics
```

**Response:**
```json
{
  "success": true,
  "data": {
    "simulation": {
      "status": "running",
      "phase": "execution",
      "progress": 45,
      "elapsed_time": 1800,
      "estimated_remaining": 1200,
      "start_time": "2023-12-31T12:30:00Z",
      "current_phase_duration": 900
    },
    "agents": {
      "total": 7,
      "active": 7,
      "red_team": {
        "active": 4,
        "tasks_completed": 23,
        "tasks_failed": 2,
        "success_rate": 92.0,
        "average_response_time": 45.5
      },
      "blue_team": {
        "active": 3,
        "tasks_completed": 18,
        "tasks_failed": 1,
        "success_rate": 94.7,
        "average_response_time": 38.2
      }
    },
    "scores": {
      "red_team": 65,
      "blue_team": 35,
      "trend": "red_team_up",
      "last_updated": "2023-12-31T12:35:00Z",
      "score_history": [
        {"timestamp": "2023-12-31T12:30:00Z", "red_team": 0, "blue_team": 0},
        {"timestamp": "2023-12-31T12:32:00Z", "red_team": 15, "blue_team": 5},
        {"timestamp": "2023-12-31T12:34:00Z", "red_team": 35, "blue_team": 20},
        {"timestamp": "2023-12-31T12:35:00Z", "red_team": 65, "blue_team": 35}
      ]
    },
    "system": {
      "cpu_usage": 45.2,
      "memory_usage": 512,
      "disk_usage": 25.8,
      "network_io": 1024,
      "active_connections": 7,
      "error_rate": 0.01
    }
  },
  "timestamp": "2023-12-31T12:35:00Z"
}
```

### Get Event Timeline
```http
GET /api/events
```

**Query Parameters:**
- `limit` (integer, optional): Number of events to return (default: 50)
- `since` (string, optional): Return events since this timestamp
- `event_type` (string, optional): Filter by event type
- `severity` (string, optional): Filter by severity level

**Response:**
```json
{
  "success": true,
  "data": {
    "events": [
      {
        "event_id": "evt_20231231_123456",
        "timestamp": "2023-12-31T12:34:56Z",
        "event_type": "agent_task_completed",
        "severity": "info",
        "agent_id": "recon_agent_001",
        "description": "OSINT gathering completed",
        "details": {
          "task": "OSINT gathering on target infrastructure",
          "duration": 245,
          "success": true,
          "findings": {
            "target": "energy-grid.example.com",
            "open_ports": [80, 443, 22],
            "technologies": ["Apache", "OpenSSH"]
          }
        },
        "mitre_technique": "T1595"
      },
      {
        "event_id": "evt_20231231_123457",
        "timestamp": "2023-12-31T12:35:02Z",
        "event_type": "alert_generated",
        "severity": "medium",
        "agent_id": "detection_agent_001",
        "description": "Suspicious network activity detected",
        "details": {
          "alert_type": "suspicious_activity",
          "source_ip": "192.168.1.100",
          "destination": "10.0.0.50",
          "protocol": "HTTP",
          "packet_count": 1250
        },
        "mitre_technique": "T1071"
      }
    ],
    "total": 156,
    "limit": 50,
    "filters": {
      "event_type": "agent_task_completed",
      "severity": "info"
    }
  },
  "timestamp": "2023-12-31T12:35:00Z"
}
```

### Get MITRE ATT&CK Analysis
```http
GET /api/mitre/analysis
```

**Response:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_techniques": 15,
      "red_team_techniques": 12,
      "blue_team_techniques": 8,
      "coverage_percentage": 75.0
    },
    "techniques": [
      {
        "technique_id": "T1595",
        "name": "Active Scanning",
        "description": "Actively scanning victims to gather information",
        "team": "red_team",
        "usage_count": 3,
        "success_rate": 100.0,
        "detection_rate": 66.7,
        "agents": ["recon_agent_001"],
        "timeline": [
          {
            "timestamp": "2023-12-31T12:32:15Z",
            "agent_id": "recon_agent_001",
            "action": "Technique used for OSINT gathering",
            "success": true
          }
        ]
      },
      {
        "technique_id": "T1071",
        "name": "Application Layer Protocol",
        "description": "Communication using application layer protocols",
        "team": "both",
        "usage_count": 5,
        "success_rate": 80.0,
        "detection_rate": 100.0,
        "agents": ["recon_agent_001", "detection_agent_001"],
        "timeline": [
          {
            "timestamp": "2023-12-31T12:35:02Z",
            "agent_id": "detection_agent_001",
            "action": "Detected suspicious HTTP traffic",
            "success": true
          }
        ]
      }
    ],
    "tactics": {
      "reconnaissance": {
        "techniques": ["T1592", "T1595", "T1596", "T1598"],
        "usage_count": 8,
        "success_rate": 87.5
      },
      "initial_access": {
        "techniques": ["T1190", "T1078"],
        "usage_count": 3,
        "success_rate": 66.7
      },
      "defense_evasion": {
        "techniques": ["T1027", "T1564"],
        "usage_count": 2,
        "success_rate": 100.0
      }
    }
  },
  "timestamp": "2023-12-31T12:35:00Z"
}
```

### Get Compliance Status
```http
GET /api/compliance/status
```

**Response:**
```json
{
  "success": true,
  "data": {
    "overall_status": "compliant",
    "overall_score": 87.5,
    "frameworks": [
      {
        "framework": "SOCI Act",
        "status": "compliant",
        "score": 85.0,
        "requirements": {
          "critical_infrastructure_risk_management": {
            "status": "compliant",
            "score": 90.0,
            "details": "Risk management procedures implemented and tested"
          },
          "incident_response_planning": {
            "status": "compliant",
            "score": 80.0,
            "details": "Incident response plan tested during simulation"
          },
          "business_continuity_planning": {
            "status": "partially_compliant",
            "score": 75.0,
            "details": "Business continuity procedures partially implemented"
          },
          "information_sharing": {
            "status": "compliant",
            "score": 95.0,
            "details": "Information sharing procedures implemented"
          }
        }
      },
      {
        "framework": "ASD Essential Eight",
        "status": "compliant",
        "score": 90.0,
        "strategies": {
          "application_control": {
            "status": "compliant",
            "score": 85.0,
            "details": "Application control measures implemented"
          },
          "patch_applications": {
            "status": "compliant",
            "score": 95.0,
            "details": "Application patching procedures tested"
          },
          "configure_microsoft_office_macro_settings": {
            "status": "not_applicable",
            "score": 100.0,
            "details": "Microsoft Office not used in this scenario"
          },
          "user_application_hardening": {
            "status": "compliant",
            "score": 80.0,
            "details": "User application hardening implemented"
          },
          "restrict_administrative_privileges": {
            "status": "compliant",
            "score": 90.0,
            "details": "Administrative privileges properly restricted"
          },
          "patch_operating_systems": {
            "status": "compliant",
            "score": 95.0,
            "details": "OS patching procedures tested"
          },
          "multi_factor_authentication": {
            "status": "compliant",
            "score": 85.0,
            "details": "MFA implemented for critical systems"
          },
          "daily_backups": {
            "status": "compliant",
            "score": 90.0,
            "details": "Backup procedures tested and verified"
          }
        }
      }
    ],
    "recommendations": [
      "Improve business continuity planning procedures",
      "Enhance user application hardening measures",
      "Strengthen multi-factor authentication implementation"
    ]
  },
  "timestamp": "2023-12-31T12:35:00Z"
}
```

### Get Network Topology
```http
GET /api/network/topology
```

**Response:**
```json
{
  "success": true,
  "data": {
    "topology": {
      "nodes": [
        {
          "id": "scada_system",
          "name": "SCADA Control System",
          "type": "critical_asset",
          "status": "active",
          "location": "Main Control Center",
          "connections": ["power_grid", "network_infrastructure"],
          "security_level": "high",
          "vulnerabilities": ["CVE-2023-1234"],
          "last_scan": "2023-12-31T12:30:00Z"
        },
        {
          "id": "power_grid",
          "name": "Power Distribution Grid",
          "type": "critical_asset",
          "status": "active",
          "location": "Multiple Locations",
          "connections": ["scada_system", "substations"],
          "security_level": "high",
          "vulnerabilities": [],
          "last_scan": "2023-12-31T12:32:00Z"
        }
      ],
      "edges": [
        {
          "source": "scada_system",
          "target": "power_grid",
          "type": "control_connection",
          "protocol": "Modbus",
          "status": "active",
          "traffic_volume": "medium",
          "security_controls": ["encryption", "authentication"]
        }
      ],
      "metrics": {
        "total_nodes": 15,
        "critical_assets": 4,
        "active_connections": 12,
        "vulnerabilities": 3,
        "security_level_distribution": {
          "high": 4,
          "medium": 8,
          "low": 3
        }
      }
    },
    "threats": [
      {
        "threat_id": "threat_001",
        "type": "lateral_movement",
        "description": "Potential lateral movement path detected",
        "source": "recon_agent_001",
        "confidence": 0.75,
        "affected_nodes": ["scada_system", "power_grid"],
        "mitre_technique": "T1021"
      }
    ]
  },
  "timestamp": "2023-12-31T12:35:00Z"
}
```

### Get Attack Path Visualization
```http
GET /api/attack-paths
```

**Response:**
```json
{
  "success": true,
  "data": {
    "attack_paths": [
      {
        "path_id": "path_001",
        "name": "SCADA System Compromise Path",
        "description": "Attack path targeting SCADA control system",
        "probability": 0.65,
        "impact": "critical",
        "techniques": ["T1595", "T1190", "T1021"],
        "steps": [
          {
            "step": 1,
            "technique": "T1595",
            "description": "Active Scanning",
            "target": "external_network",
            "success_probability": 0.85,
            "estimated_duration": 300,
            "mitigation": "Network segmentation"
          },
          {
            "step": 2,
            "technique": "T1190",
            "description": "Exploit Public-Facing Application",
            "target": "web_server",
            "success_probability": 0.45,
            "estimated_duration": 600,
            "mitigation": "Patch management"
          },
          {
            "step": 3,
            "technique": "T1021",
            "description": "Remote Services",
            "target": "scada_system",
            "success_probability": 0.70,
            "estimated_duration": 900,
            "mitigation": "Access control"
          }
        ],
        "defensive_measures": [
          {
            "measure": "Network segmentation",
            "effectiveness": 0.75,
            "implementation_complexity": "medium"
          },
          {
            "measure": "Multi-factor authentication",
            "effectiveness": 0.85,
            "implementation_complexity": "low"
          }
        ]
      }
    ],
    "summary": {
      "total_paths": 3,
      "high_risk_paths": 1,
      "medium_risk_paths": 2,
      "average_probability": 0.58,
      "most_likely_path": "path_001"
    }
  },
  "timestamp": "2023-12-31T12:35:00Z"
}
```

### Get Performance Charts Data
```http
GET /api/charts/{chart_type}
```

**Chart Types:**
- `agent_performance`: Agent performance over time
- `team_scores`: Team scores progression
- `system_resources`: System resource usage
- `mitre_coverage`: MITRE technique coverage
- `compliance_scores`: Compliance score trends

**Response for `agent_performance`:**
```json
{
  "success": true,
  "data": {
    "chart_type": "agent_performance",
    "time_series": [
      {
        "timestamp": "2023-12-31T12:30:00Z",
        "recon_agent_001": {
          "tasks_completed": 0,
          "success_rate": 0,
          "response_time": 0
        },
        "detection_agent_001": {
          "tasks_completed": 0,
          "success_rate": 0,
          "response_time": 0
        }
      },
      {
        "timestamp": "2023-12-31T12:35:00Z",
        "recon_agent_001": {
          "tasks_completed": 3,
          "success_rate": 100.0,
          "response_time": 45.5
        },
        "detection_agent_001": {
          "tasks_completed": 2,
          "success_rate": 100.0,
          "response_time": 38.2
        }
      }
    ],
    "summary": {
      "total_agents": 7,
      "average_success_rate": 95.2,
      "average_response_time": 42.1,
      "peak_performance": {
        "agent": "recon_agent_001",
        "success_rate": 100.0,
        "timestamp": "2023-12-31T12:35:00Z"
      }
    }
  },
  "timestamp": "2023-12-31T12:35:00Z"
}
```

### Get Dashboard Configuration
```http
GET /api/config
```

**Response:**
```json
{
  "success": true,
  "data": {
    "dashboard_settings": {
      "refresh_interval": 5,
      "auto_scroll_events": true,
      "show_advanced_metrics": false,
      "theme": "dark",
      "language": "en"
    },
    "panels": [
      {
        "id": "simulation_status",
        "name": "Simulation Status",
        "type": "status_panel",
        "position": {"x": 0, "y": 0, "width": 6, "height": 3},
        "visible": true,
        "config": {
          "show_progress": true,
          "show_phase": true,
          "show_timer": true
        }
      },
      {
        "id": "agent_metrics",
        "name": "Agent Metrics",
        "type": "metrics_panel",
        "position": {"x": 6, "y": 0, "width": 6, "height": 3},
        "visible": true,
        "config": {
          "show_performance": true,
          "show_success_rate": true,
          "group_by_team": true
        }
      }
    ],
    "alerts": {
      "enabled": true,
      "thresholds": {
        "cpu_usage": 80,
        "memory_usage": 85,
        "error_rate": 0.05
      }
    }
  },
  "timestamp": "2023-12-31T12:35:00Z"
}
```

### Update Dashboard Configuration
```http
PUT /api/config
Content-Type: application/json
```

**Request Body:**
```json
{
  "dashboard_settings": {
    "refresh_interval": 10,
    "auto_scroll_events": false,
    "show_advanced_metrics": true,
    "theme": "light"
  },
  "panels": [
    {
      "id": "simulation_status",
      "visible": true,
      "config": {
        "show_progress": true,
        "show_phase": true
      }
    }
  ]
}
```

## 📡 WebSocket Connections

### Real-time Updates
```javascript
const ws = new WebSocket('ws://localhost:8501/ws/dashboard');

ws.onopen = function(event) {
    console.log('Connected to dashboard WebSocket');
    
    // Subscribe to updates
    ws.send(JSON.stringify({
        type: 'subscribe',
        channels: ['metrics', 'events', 'alerts']
    }));
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    switch(data.channel) {
        case 'metrics':
            updateMetricsPanel(data.data);
            break;
        case 'events':
            updateEventsPanel(data.data);
            break;
        case 'alerts':
            showAlert(data.data);
            break;
    }
};
```

### WebSocket Message Types

#### Metrics Update
```json
{
  "channel": "metrics",
  "type": "update",
  "data": {
    "simulation": {
      "progress": 46,
      "elapsed_time": 1860
    },
    "agents": {
      "red_team": {
        "tasks_completed": 24
      }
    }
  }
}
```

#### Event Update
```json
{
  "channel": "events",
  "type": "new_event",
  "data": {
    "event_id": "evt_20231231_123458",
    "timestamp": "2023-12-31T12:35:15Z",
    "event_type": "agent_task_completed",
    "description": "Network mapping completed"
  }
}
```

#### Alert
```json
{
  "channel": "alerts",
  "type": "alert",
  "data": {
    "alert_id": "alert_20231231_123456",
    "severity": "medium",
    "message": "CPU usage exceeded threshold",
    "value": 82.5,
    "threshold": 80
  }
}
```

## 🧪 Error Handling

### Common Dashboard Errors

#### Invalid Chart Type
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CHART_TYPE",
    "message": "Invalid chart type specified",
    "details": "Chart type 'invalid_chart' is not supported"
  }
}
```

#### Data Not Available
```json
{
  "success": false,
  "error": {
    "code": "DATA_NOT_AVAILABLE",
    "message": "Requested data is not available",
    "details": "No data available for the specified time range"
  }
}
```

#### Configuration Invalid
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CONFIGURATION",
    "message": "Invalid dashboard configuration",
    "details": "Refresh interval must be between 1 and 60 seconds"
  }
}
```

## 📚 SDK Examples

### Python SDK
```python
from simulation_client import DashboardClient

# Initialize dashboard client
dashboard_client = DashboardClient(
    base_url="http://localhost:8501",
    api_key="your-api-key"
)

# Get real-time metrics
metrics = dashboard_client.get_metrics()
print(f"Simulation progress: {metrics['data']['simulation']['progress']}%")

# Get event timeline
events = dashboard_client.get_events(limit=20, severity="medium")
for event in events['data']['events']:
    print(f"Event: {event['description']}")

# Get MITRE analysis
mitre = dashboard_client.get_mitre_analysis()
print(f"Techniques used: {mitre['data']['summary']['total_techniques']}")

# Get compliance status
compliance = dashboard_client.get_compliance_status()
print(f"Overall compliance score: {compliance['data']['overall_score']}")

# WebSocket connection for real-time updates
def handle_metrics_update(data):
    print(f"Metrics updated: {data['simulation']['progress']}%")

def handle_event_update(data):
    print(f"New event: {data['description']}")

dashboard_client.connect_websocket({
    'metrics': handle_metrics_update,
    'events': handle_event_update
})
```

### JavaScript SDK
```javascript
import { DashboardClient } from '@autonomous-multi-agent/sdk';

// Initialize dashboard client
const dashboardClient = new DashboardClient({
    baseUrl: 'http://localhost:8501',
    apiKey: 'your-api-key'
});

// Get real-time metrics
const metrics = await dashboardClient.getMetrics();
console.log(`Simulation progress: ${metrics.data.simulation.progress}%`);

// Get event timeline
const events = await dashboardClient.getEvents({ limit: 20, severity: 'medium' });
events.data.events.forEach(event => {
    console.log(`Event: ${event.description}`);
});

// Get MITRE analysis
const mitre = await dashboardClient.getMitreAnalysis();
console.log(`Techniques used: ${mitre.data.summary.totalTechniques}`);

// Get compliance status
const compliance = await dashboardClient.getComplianceStatus();
console.log(`Overall compliance score: ${compliance.data.overallScore}`);

// WebSocket connection for real-time updates
dashboardClient.connectWebSocket({
    metrics: (data) => {
        console.log(`Metrics updated: ${data.simulation.progress}%`);
    },
    events: (data) => {
        console.log(`New event: ${data.description}`);
    }
});
```

## 📖 Additional Resources

- [Main API Documentation](README.md)
- [Agents API Documentation](agents.md)
- [Scenarios API Documentation](scenarios.md)
- [MCP API Documentation](mcp.md)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Examples](../../examples/)

## 🆘 Support

For dashboard API support:
- Create an issue on GitHub
- Check the [examples](../../examples/)
- Review the [testing guide](../../tests/)
- Contact the development team
