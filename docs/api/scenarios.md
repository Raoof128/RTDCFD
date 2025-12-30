# Scenarios API Documentation

## 📋 Scenario Overview

The Scenarios API provides endpoints for managing, configuring, and executing simulation scenarios. The API allows you to access available scenarios, validate configurations, and control scenario execution within the autonomous multi-agent simulation system.

## 🔗 Base URL
```
http://localhost:8080/api/v1/scenarios
```

## 🎯 Available Scenarios

### SOCI Act Scenarios
- **Energy Grid Scenario** (`soci_energy_grid`): Critical infrastructure simulation for energy grid systems
- **Telecommunications Network Scenario** (`soci_telco_network`): Critical infrastructure simulation for telecommunications
- **Water System Scenario** (`soci_water_system`): Critical infrastructure simulation for water treatment and distribution

## 🚀 API Endpoints

### List Available Scenarios
```http
GET /api/v1/scenarios
```

**Response:**
```json
{
  "success": true,
  "data": {
    "scenarios": [
      {
        "id": "soci_energy_grid",
        "name": "SOCI Act Energy Grid Scenario",
        "description": "Critical infrastructure simulation for energy grid systems under SOCI Act compliance",
        "sector": "energy",
        "difficulty": "advanced",
        "estimated_duration": 60,
        "critical_assets": 4,
        "attack_vectors": 5,
        "defensive_measures": 5,
        "compliance_frameworks": ["SOCI Act", "ASD Essential Eight"],
        "mitre_coverage": 15,
        "status": "available",
        "version": "1.0.0"
      },
      {
        "id": "soci_telco_network",
        "name": "SOCI Act Telecommunications Network Scenario",
        "description": "Critical infrastructure simulation for telecommunications infrastructure",
        "sector": "telecommunications",
        "difficulty": "advanced",
        "estimated_duration": 45,
        "critical_assets": 3,
        "attack_vectors": 5,
        "defensive_measures": 5,
        "compliance_frameworks": ["SOCI Act", "ASD Essential Eight"],
        "mitre_coverage": 12,
        "status": "available",
        "version": "1.0.0"
      },
      {
        "id": "soci_water_system",
        "name": "SOCI Act Water System Scenario",
        "description": "Critical infrastructure simulation for water treatment and distribution systems",
        "sector": "water",
        "difficulty": "advanced",
        "estimated_duration": 50,
        "critical_assets": 3,
        "attack_vectors": 5,
        "defensive_measures": 5,
        "compliance_frameworks": ["SOCI Act", "ASD Essential Eight"],
        "mitre_coverage": 13,
        "status": "available",
        "version": "1.0.0"
      }
    ],
    "total": 3,
    "sectors": ["energy", "telecommunications", "water"],
    "compliance_frameworks": ["SOCI Act", "ASD Essential Eight"]
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

### Get Scenario Details
```http
GET /api/v1/scenarios/{scenario_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "soci_energy_grid",
    "name": "SOCI Act Energy Grid Scenario",
    "description": "Critical infrastructure simulation for energy grid systems under SOCI Act compliance",
    "sector": "energy",
    "difficulty": "advanced",
    "estimated_duration": 60,
    "version": "1.0.0",
    "critical_assets": [
      {
        "id": "scada_system",
        "name": "SCADA Control System",
        "description": "Supervisory Control and Data Acquisition system",
        "criticality": "high",
        "location": "Main Control Center",
        "dependencies": ["power_grid", "communication_network"],
        "security_controls": ["firewall", "ids", "access_control"]
      },
      {
        "id": "power_grid",
        "name": "Power Distribution Grid",
        "description": "Power distribution and transmission infrastructure",
        "criticality": "high",
        "location": "Multiple Locations",
        "dependencies": ["scada_system", "substations"],
        "security_controls": ["physical_security", "monitoring"]
      }
    ],
    "attack_vectors": [
      {
        "id": "scada_compromise",
        "name": "SCADA System Compromise",
        "description": "Compromise SCADA system through various attack vectors",
        "mitre_techniques": ["T1190", "T1078", "T1059"],
        "difficulty": "high",
        "impact": "critical",
        "detection_methods": ["anomaly_detection", "log_analysis"]
      },
      {
        "id": "supply_chain_attack",
        "name": "Supply Chain Attack",
        "description": "Attack through compromised software or hardware supply chain",
        "mitre_techniques": ["T1195", "T1195.001", "T1195.002"],
        "difficulty": "medium",
        "impact": "high",
        "detection_methods": ["vendor_monitoring", "code_analysis"]
      }
    ],
    "defensive_measures": [
      {
        "id": "network_segmentation",
        "name": "Network Segmentation",
        "description": "Implement network segmentation to limit lateral movement",
        "mitre_techniques": ["T1021", "T1028"],
        "effectiveness": "high",
        "implementation_complexity": "medium"
      },
      {
        "id": "multi_factor_auth",
        "name": "Multi-Factor Authentication",
        "description": "Implement MFA for all critical systems",
        "mitre_techniques": ["T1110", "T1110.001"],
        "effectiveness": "high",
        "implementation_complexity": "low"
      }
    ],
    "success_criteria": [
      {
        "id": "system_availability",
        "name": "System Availability",
        "description": "Maintain 99.9% system availability during simulation",
        "threshold": 99.9,
        "measurement": "uptime_percentage"
      },
      {
        "id": "incident_response",
        "name": "Incident Response Time",
        "description": "Detect and respond to incidents within 5 minutes",
        "threshold": 300,
        "measurement": "response_time_seconds"
      }
    ],
    "compliance_requirements": [
      {
        "framework": "SOCI Act",
        "requirements": [
          "Critical infrastructure risk management",
          "Incident response planning",
          "Business continuity planning",
          "Information sharing obligations"
        ]
      },
      {
        "framework": "ASD Essential Eight",
        "requirements": [
          "Application control",
          "Patch applications",
          "Configure Microsoft Office macro settings",
          "User application hardening",
          "Restrict administrative privileges",
          "Patch operating systems",
          "Multi-factor authentication",
          "Daily backups"
        ]
      }
    ],
    "agent_requirements": {
      "red_team": ["recon_agent", "social_engineering_agent", "exploitation_agent", "lateral_movement_agent"],
      "blue_team": ["detection_agent", "response_agent", "threat_intel_agent"]
    },
    "configuration": {
      "simulation_mode_only": true,
      "enable_safety_checks": true,
      "audit_logging": true,
      "max_duration_minutes": 120,
      "enable_mitigation": true
    }
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

### Validate Scenario
```http
POST /api/v1/scenarios/{scenario_id}/validate
Content-Type: application/json
```

**Request Body:**
```json
{
  "configuration": {
    "simulation_mode_only": true,
    "enable_safety_checks": true,
    "audit_logging": true,
    "max_duration_minutes": 120
  },
  "agents": {
    "red_team": ["recon_agent", "social_engineering_agent", "exploitation_agent", "lateral_movement_agent"],
    "blue_team": ["detection_agent", "response_agent", "threat_intel_agent"]
  },
  "custom_settings": {
    "attack_intensity": "medium",
    "defense_strength": "high",
    "enable_compliance_checks": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "scenario_id": "soci_energy_grid",
    "validation_status": "passed",
    "valid": true,
    "checks": [
      {
        "name": "agent_availability",
        "status": "passed",
        "description": "All required agents are available",
        "details": {
          "red_team_agents": 4,
          "blue_team_agents": 3,
          "total_agents": 7
        }
      },
      {
        "name": "configuration_validity",
        "status": "passed",
        "description": "Scenario configuration is valid",
        "details": {
          "simulation_mode_only": true,
          "enable_safety_checks": true,
          "max_duration_minutes": 120
        }
      },
      {
        "name": "compliance_requirements",
        "status": "passed",
        "description": "All compliance requirements can be met",
        "details": {
          "soci_act": "compliant",
          "asd_essential_eight": "compliant"
        }
      }
    ],
    "warnings": [
      {
        "level": "info",
        "message": "Custom attack intensity may affect simulation duration",
        "recommendation": "Monitor simulation progress and adjust as needed"
      }
    ],
    "estimated_resources": {
      "cpu_usage": "medium",
      "memory_usage": "medium",
      "storage_usage": "low",
      "network_usage": "medium"
    }
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

### Execute Scenario
```http
POST /api/v1/scenarios/{scenario_id}/execute
Content-Type: application/json
```

**Request Body:**
```json
{
  "configuration": {
    "simulation_mode_only": true,
    "enable_safety_checks": true,
    "audit_logging": true,
    "max_duration_minutes": 120
  },
  "agents": {
    "red_team": ["recon_agent", "social_engineering_agent", "exploitation_agent", "lateral_movement_agent"],
    "blue_team": ["detection_agent", "response_agent", "threat_intel_agent"]
  },
  "custom_settings": {
    "attack_intensity": "medium",
    "defense_strength": "high",
    "enable_compliance_checks": true
  },
  "execution_options": {
    "enable_dashboard": true,
    "generate_report": true,
    "include_timeline": true,
    "include_mitre_analysis": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "execution_id": "exec_20231231_123456",
    "scenario_id": "soci_energy_grid",
    "status": "started",
    "start_time": "2023-12-31T12:34:56Z",
    "estimated_duration": 60,
    "agents": {
      "red_team": ["recon_agent_001", "social_engineering_agent_001", "exploitation_agent_001", "lateral_movement_agent_001"],
      "blue_team": ["detection_agent_001", "response_agent_001", "threat_intel_agent_001"]
    },
    "configuration": {
      "simulation_mode_only": true,
      "enable_safety_checks": true,
      "audit_logging": true,
      "max_duration_minutes": 120
    },
    "monitoring": {
      "dashboard_url": "http://localhost:8501",
      "real_time_updates": true,
      "event_streaming": true
    }
  },
  "timestamp": "2023-12-31T12:34:56Z"
}
```

### Get Execution Status
```http
GET /api/v1/scenarios/{scenario_id}/executions/{execution_id}/status
```

**Response:**
```json
{
  "success": true,
  "data": {
    "execution_id": "exec_20231231_123456",
    "scenario_id": "soci_energy_grid",
    "status": "running",
    "start_time": "2023-12-31T12:34:56Z",
    "elapsed_time": 1800,
    "estimated_remaining": 3600,
    "progress": 25,
    "current_phase": "initial_access",
    "phases": [
      {
        "name": "initial_access",
        "status": "completed",
        "start_time": "2023-12-31T12:34:56Z",
        "end_time": "2023-12-31T12:45:00Z",
        "duration": 624
      },
      {
        "name": "execution",
        "status": "running",
        "start_time": "2023-12-31T12:45:00Z",
        "duration": 1176
      }
    ],
    "agents": {
      "total": 7,
      "active": 7,
      "tasks_completed": 23,
      "tasks_failed": 2,
      "success_rate": 92.0
    },
    "scores": {
      "red_team": 45,
      "blue_team": 55,
      "trend": "blue_team_up"
    },
    "events": [
      {
        "timestamp": "2023-12-31T12:45:30Z",
        "type": "agent_task_completed",
        "agent_id": "recon_agent_001",
        "description": "OSINT gathering completed",
        "mitre_technique": "T1595"
      },
      {
        "timestamp": "2023-12-31T12:46:15Z",
        "type": "alert_generated",
        "agent_id": "detection_agent_001",
        "description": "Suspicious network activity detected",
        "severity": "medium"
      }
    ],
    "compliance": {
      "soci_act": {
        "status": "compliant",
        "score": 85,
        "issues": []
      },
      "asd_essential_eight": {
        "status": "compliant",
        "score": 90,
        "issues": []
      }
    }
  },
  "timestamp": "2023-12-31T12:55:56Z"
}
```

### Stop Execution
```http
POST /api/v1/scenarios/{scenario_id}/executions/{execution_id}/stop
Content-Type: application/json
```

**Request Body:**
```json
{
  "reason": "User requested stop",
  "generate_report": true,
  "include_partial_results": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "execution_id": "exec_20231231_123456",
    "scenario_id": "soci_energy_grid",
    "status": "stopped",
    "stop_time": "2023-12-31T12:55:56Z",
    "total_duration": 1260,
    "final_progress": 35,
    "reason": "User requested stop",
    "report_generated": true,
    "report_path": "/reports/exec_20231231_123456_report.json"
  },
  "timestamp": "2023-12-31T12:55:56Z"
}
```

### Generate Report
```http
POST /api/v1/scenarios/{scenario_id}/executions/{execution_id}/report
Content-Type: application/json
```

**Request Body:**
```json
{
  "format": "json",
  "include_timeline": true,
  "include_mitre_analysis": true,
  "include_compliance": true,
  "include_agent_metrics": true,
  "include_recommendations": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "report_id": "report_20231231_123456",
    "execution_id": "exec_20231231_123456",
    "scenario_id": "soci_energy_grid",
    "format": "json",
    "status": "generating",
    "estimated_completion": "2023-12-31T12:58:00Z",
    "download_url": "/api/v1/reports/report_20231231_123456/download"
  },
  "timestamp": "2023-12-31T12:55:56Z"
}
```

### Download Report
```http
GET /api/v1/reports/{report_id}/download
```

**Response:**
```json
{
  "success": true,
  "data": {
    "report_id": "report_20231231_123456",
    "execution_id": "exec_20231231_123456",
    "scenario_id": "soci_energy_grid",
    "format": "json",
    "generated_at": "2023-12-31T12:58:00Z",
    "content": {
      "summary": {
        "execution_id": "exec_20231231_123456",
        "scenario_name": "SOCI Act Energy Grid Scenario",
        "start_time": "2023-12-31T12:34:56Z",
        "end_time": "2023-12-31T12:55:56Z",
        "total_duration": 1260,
        "final_status": "stopped",
        "final_progress": 35
      },
      "scores": {
        "red_team": 45,
        "blue_team": 55,
        "winner": "blue_team"
      },
      "compliance": {
        "soci_act": {
          "score": 85,
          "status": "compliant"
        },
        "asd_essential_eight": {
          "score": 90,
          "status": "compliant"
        }
      },
      "mitre_analysis": {
        "techniques_used": ["T1595", "T1596", "T1190", "T1021"],
        "coverage": 15,
        "attribution": "red_team"
      },
      "recommendations": [
        "Implement network segmentation for SCADA systems",
        "Enhance monitoring for lateral movement attempts",
        "Improve incident response time"
      ]
    }
  },
  "timestamp": "2023-12-31T12:58:00Z"
}
```

## 📊 Scenario Templates

### Create Custom Scenario
```http
POST /api/v1/scenarios/custom
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Custom Critical Infrastructure Scenario",
  "description": "Custom scenario for specific critical infrastructure",
  "sector": "healthcare",
  "difficulty": "intermediate",
  "estimated_duration": 45,
  "critical_assets": [
    {
      "id": "his_system",
      "name": "Hospital Information System",
      "description": "Electronic health records and patient management",
      "criticality": "high",
      "location": "Main Hospital",
      "dependencies": ["network_infrastructure", "backup_systems"],
      "security_controls": ["encryption", "access_control", "audit_logging"]
    }
  ],
  "attack_vectors": [
    {
      "id": "ransomware_attack",
      "name": "Ransomware Attack",
      "description": "Ransomware attack on hospital systems",
      "mitre_techniques": ["T1486", "T1485", "T1059"],
      "difficulty": "high",
      "impact": "critical",
      "detection_methods": ["behavioral_analysis", "file_integrity_monitoring"]
    }
  ],
  "defensive_measures": [
    {
      "id": "backup_recovery",
      "name": "Backup and Recovery",
      "description": "Regular backups and recovery procedures",
      "mitre_techniques": ["T1490"],
      "effectiveness": "high",
      "implementation_complexity": "medium"
    }
  ],
  "success_criteria": [
    {
      "id": "data_protection",
      "name": "Patient Data Protection",
      "description": "Protect patient data from unauthorized access",
      "threshold": 100,
      "measurement": "data_protection_percentage"
    }
  ],
  "compliance_requirements": [
    {
      "framework": "HIPAA",
      "requirements": ["Data privacy", "Security safeguards", "Breach notification"]
    }
  ],
  "agent_requirements": {
    "red_team": ["recon_agent", "exploitation_agent"],
    "blue_team": ["detection_agent", "response_agent"]
  }
}
```

## 🧪 Error Handling

### Common Scenario Errors

#### Scenario Not Found
```json
{
  "success": false,
  "error": {
    "code": "SCENARIO_NOT_FOUND",
    "message": "Scenario 'invalid_scenario' does not exist"
  }
}
```

#### Validation Failed
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Scenario validation failed",
    "details": {
      "failed_checks": [
        {
          "name": "agent_availability",
          "error": "Required agent 'exploitation_agent' not available"
        }
      ]
    }
  }
}
```

#### Execution Already Running
```json
{
  "success": false,
  "error": {
    "code": "EXECUTION_ALREADY_RUNNING",
    "message": "Scenario execution is already in progress",
    "details": {
      "execution_id": "exec_20231231_123456",
      "status": "running"
    }
  }
}
```

#### Configuration Invalid
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CONFIGURATION",
    "message": "Invalid scenario configuration",
    "details": {
      "field": "max_duration_minutes",
      "error": "Value must be between 10 and 240"
    }
  }
}
```

## 📚 SDK Examples

### Python SDK
```python
from simulation_client import ScenarioClient

# Initialize scenario client
scenario_client = ScenarioClient(
    base_url="http://localhost:8080",
    api_key="your-api-key"
)

# List available scenarios
scenarios = scenario_client.list_scenarios()
print(f"Found {len(scenarios['data']['scenarios'])} scenarios")

# Get specific scenario
scenario = scenario_client.get_scenario("soci_energy_grid")
print(f"Scenario: {scenario['data']['name']}")

# Validate scenario
validation = scenario_client.validate_scenario("soci_energy_grid", {
    "simulation_mode_only": True,
    "enable_safety_checks": True
})

if validation['data']['valid']:
    # Execute scenario
    execution = scenario_client.execute_scenario("soci_energy_grid", {
        "configuration": {
            "simulation_mode_only": True,
            "enable_safety_checks": True
        },
        "execution_options": {
            "enable_dashboard": True,
            "generate_report": True
        }
    })
    
    # Monitor execution
    while execution.get_status()['data']['status'] == 'running':
        status = execution.get_status()
        print(f"Progress: {status['data']['progress']}%")
        time.sleep(10)
    
    # Generate report
    report = execution.generate_report()
    print(f"Report: {report['data']['report_id']}")
```

### JavaScript SDK
```javascript
import { ScenarioClient } from '@autonomous-multi-agent/sdk';

// Initialize scenario client
const scenarioClient = new ScenarioClient({
    baseUrl: 'http://localhost:8080',
    apiKey: 'your-api-key'
});

// List available scenarios
const scenarios = await scenarioClient.listScenarios();
console.log(`Found ${scenarios.data.scenarios.length} scenarios`);

// Get specific scenario
const scenario = await scenarioClient.getScenario('soci_energy_grid');
console.log(`Scenario: ${scenario.data.name}`);

// Validate scenario
const validation = await scenarioClient.validateScenario('soci_energy_grid', {
    simulationModeOnly: true,
    enableSafetyChecks: true
});

if (validation.data.valid) {
    // Execute scenario
    const execution = await scenarioClient.executeScenario('soci_energy_grid', {
        configuration: {
            simulationModeOnly: true,
            enableSafetyChecks: true
        },
        executionOptions: {
            enableDashboard: true,
            generateReport: true
        }
    });

    // Monitor execution
    execution.on('progress', (progress) => {
        console.log(`Progress: ${progress.data.progress}%`);
    });

    // Wait for completion
    await execution.waitForCompletion();

    // Generate report
    const report = await execution.generateReport();
    console.log(`Report: ${report.data.reportId}`);
}
```

## 📖 Additional Resources

- [Main API Documentation](README.md)
- [Agents API Documentation](agents.md)
- [MCP API Documentation](mcp.md)
- [Dashboard API Documentation](dashboard.md)
- [Examples](../../examples/)
- [Compliance Documentation](../compliance/)

## 🆘 Support

For scenario API support:
- Create an issue on GitHub
- Check the [examples](../../examples/)
- Review the [testing guide](../../tests/)
- Contact the development team
