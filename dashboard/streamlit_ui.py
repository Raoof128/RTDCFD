"""
Streamlit Dashboard for Autonomous Multi-Agent Red/Blue Team Simulation System

This module provides a real-time web-based dashboard for monitoring
simulation progress, agent activities, and attack/defense narratives.
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings
from scenarios import get_available_scenarios, get_scenario_metadata
from utils.logging_handler import get_logger
from utils.validation import check_system_health, list_available_scenarios

# Configure page
st.set_page_config(
    page_title="Autonomous Multi-Agent Simulation Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .agent-status {
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
    }
    .agent-active {
        background-color: #d4edda;
        border-left: 3px solid #28a745;
    }
    .agent-idle {
        background-color: #fff3cd;
        border-left: 3px solid #ffc107;
    }
    .agent-error {
        background-color: #f8d7da;
        border-left: 3px solid #dc3545;
    }
    .phase-indicator {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #2196f3;
        margin: 1rem 0;
    }
    .attack-timeline {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9800;
    }
    .defense-timeline {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "simulation_data" not in st.session_state:
    st.session_state.simulation_data = {
        "active": False,
        "scenario": None,
        "start_time": None,
        "current_phase": None,
        "agents": {},
        "attack_timeline": [],
        "defense_timeline": [],
        "scores": {"red_team": 0, "blue_team": 0},
    }

if "refresh_interval" not in st.session_state:
    st.session_state.refresh_interval = 5

# Logger
logger = get_logger(__name__)


def render_header():
    """Render dashboard header."""
    st.markdown(
        '<h1 class="main-header">🛡️ Autonomous Multi-Agent Simulation Dashboard</h1>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # System status
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "System Status",
            (
                "🟢 Operational"
                if check_system_health()["checks"]["configuration"]
                else "🔴 Issues"
            ),
            delta=None,
        )

    with col2:
        available_scenarios = len(get_available_scenarios())
        st.metric("Available Scenarios", available_scenarios)

    with col3:
        st.metric(
            "Simulation Status",
            (
                "🟢 Active"
                if st.session_state.simulation_data["active"]
                else "🔴 Inactive"
            ),
        )

    with col4:
        if st.session_state.simulation_data["start_time"]:
            elapsed = datetime.now() - st.session_state.simulation_data["start_time"]
            st.metric("Elapsed Time", str(elapsed).split(".")[0])
        else:
            st.metric("Elapsed Time", "00:00:00")


def render_sidebar():
    """Render sidebar controls."""
    st.sidebar.header("🎮 Simulation Controls")

    # Scenario selection
    if not st.session_state.simulation_data["active"]:
        scenarios = get_available_scenarios()
        selected_scenario = st.sidebar.selectbox(
            "Select Scenario",
            scenarios,
            index=0 if scenarios else None,
            help="Choose a SOCI Act critical infrastructure scenario",
        )

        if selected_scenario:
            # Display scenario metadata
            metadata = get_scenario_metadata(selected_scenario)
            st.sidebar.markdown(f"**Sector:** {metadata['sector']}")
            st.sidebar.markdown(f"**Duration:** {metadata['duration_hours']} hours")
            st.sidebar.markdown(f"**Difficulty:** {metadata['difficulty']}")

            # Start simulation button
            if st.sidebar.button("🚀 Start Simulation", type="primary"):
                start_simulation(selected_scenario)

    else:
        # Active simulation controls
        st.sidebar.markdown(
            f"**Active Scenario:** {st.session_state.simulation_data['scenario']}"
        )
        st.sidebar.markdown(
            f"**Current Phase:** {st.session_state.simulation_data['current_phase']}"
        )

        # Stop simulation button
        if st.sidebar.button("⏹️ Stop Simulation", type="secondary"):
            stop_simulation()

        # Refresh control
        st.sidebar.markdown("---")
        refresh_interval = st.sidebar.slider(
            "Refresh Interval (seconds)",
            min_value=1,
            max_value=30,
            value=st.session_state.refresh_interval,
        )
        st.session_state.refresh_interval = refresh_interval

    st.sidebar.markdown("---")
    st.sidebar.header("📊 Display Options")

    # Display toggles
    show_agent_details = st.sidebar.checkbox("Show Agent Details", value=True)
    show_timeline = st.sidebar.checkbox("Show Timeline", value=True)
    show_mitre = st.sidebar.checkbox("Show MITRE ATT&CK", value=True)

    return {
        "show_agent_details": show_agent_details,
        "show_timeline": show_timeline,
        "show_mitre": show_mitre,
    }


def render_simulation_overview():
    """Render simulation overview section."""
    if not st.session_state.simulation_data["active"]:
        st.info(
            "👋 Welcome! Select a scenario from the sidebar and click 'Start Simulation' to begin."
        )
        return

    # Phase indicator
    phase = st.session_state.simulation_data["current_phase"]
    phase_descriptions = {
        "initialization": "🔧 Setting up simulation environment",
        "reconnaissance": "🔍 Red team gathering intelligence",
        "initial_access": "🚪 Red team attempting initial compromise",
        "execution": "⚡ Red team executing attack techniques",
        "persistence": "🔄 Red team establishing persistence",
        "defense_response": "🛡️ Blue team responding to threats",
        "lateral_movement": "↔️ Red team moving laterally",
        "exfiltration": "📤 Red team exfiltrating data",
        "post_incident": "🔍 Post-incident analysis",
        "completed": "✅ Simulation completed",
    }

    st.markdown(
        f"""
    <div class="phase-indicator">
        <h3>Current Phase: {phase.replace('_', ' ').title()}</h3>
        <p>{phase_descriptions.get(phase, 'Phase in progress...')}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Score metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🔴 Red Team Score",
            st.session_state.simulation_data["scores"]["red_team"],
            delta=None,
        )

    with col2:
        st.metric(
            "🔵 Blue Team Score",
            st.session_state.simulation_data["scores"]["blue_team"],
            delta=None,
        )

    # Progress bar
    phases = [
        "initialization",
        "reconnaissance",
        "initial_access",
        "execution",
        "persistence",
        "defense_response",
        "lateral_movement",
        "exfiltration",
        "post_incident",
    ]

    if phase in phases:
        current_index = phases.index(phase)
        progress = (current_index + 1) / len(phases)
        st.progress(progress, text=f"Simulation Progress: {int(progress * 100)}%")


def render_agent_status(display_options):
    """Render agent status section."""
    if not st.session_state.simulation_data["active"]:
        return

    st.header("🤖 Agent Status")

    agents = st.session_state.simulation_data["agents"]

    if not agents:
        st.info("No agent data available yet.")
        return

    # Create agent status dataframe
    agent_data = []
    for agent_id, agent_info in agents.items():
        agent_data.append(
            {
                "Agent ID": agent_id,
                "Type": agent_info.get("type", "unknown"),
                "Team": "Red Team" if "red" in agent_id else "Blue Team",
                "Status": agent_info.get("status", "unknown"),
                "Current Task": agent_info.get("current_task", "idle"),
                "Memory Count": agent_info.get("memory_count", 0),
                "Last Activity": agent_info.get("last_activity", "unknown"),
            }
        )

    df = pd.DataFrame(agent_data)

    # Status styling
    def color_status(val):
        if val == "active":
            return "background-color: #d4edda"
        elif val == "idle":
            return "background-color: #fff3cd"
        elif val == "error":
            return "background-color: #f8d7da"
        else:
            return ""

    if display_options["show_agent_details"]:
        styled_df = df.style.applymap(color_status, subset=["Status"])
        st.dataframe(styled_df, use_container_width=True)
    else:
        # Summary view
        red_agents = df[df["Team"] == "Red Team"]
        blue_agents = df[df["Team"] == "Blue Team"]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🔴 Red Team Agents")
            for _, agent in red_agents.iterrows():
                status_icon = (
                    "🟢"
                    if agent["Status"] == "active"
                    else "🟡" if agent["Status"] == "idle" else "🔴"
                )
                st.markdown(f"{status_icon} **{agent['Agent ID']}** - {agent['Type']}")

        with col2:
            st.markdown("### 🔵 Blue Team Agents")
            for _, agent in blue_agents.iterrows():
                status_icon = (
                    "🟢"
                    if agent["Status"] == "active"
                    else "🟡" if agent["Status"] == "idle" else "🔴"
                )
                st.markdown(f"{status_icon} **{agent['Agent ID']}** - {agent['Type']}")


def render_timeline(display_options):
    """Render attack and defense timeline."""
    if (
        not st.session_state.simulation_data["active"]
        or not display_options["show_timeline"]
    ):
        return

    st.header("📈 Attack & Defense Timeline")

    attack_timeline = st.session_state.simulation_data["attack_timeline"]
    defense_timeline = st.session_state.simulation_data["defense_timeline"]

    if not attack_timeline and not defense_timeline:
        st.info("No timeline events yet.")
        return

    # Create timeline visualization
    fig = go.Figure()

    # Add attack events
    if attack_timeline:
        attack_times = [event.get("timestamp", "") for event in attack_timeline]
        attack_descriptions = [
            event.get("description", "")[:50] + "..." for event in attack_timeline
        ]

        fig.add_trace(
            go.Scatter(
                x=attack_times,
                y=[1] * len(attack_timeline),
                mode="markers+text",
                name="Attack Events",
                text=attack_descriptions,
                textposition="top center",
                marker=dict(color="red", size=10),
                hovertemplate="<b>Attack Event</b><br>%{text}<br>%{x}<extra></extra>",
            )
        )

    # Add defense events
    if defense_timeline:
        defense_times = [event.get("timestamp", "") for event in defense_timeline]
        defense_descriptions = [
            event.get("description", "")[:50] + "..." for event in defense_timeline
        ]

        fig.add_trace(
            go.Scatter(
                x=defense_times,
                y=[0] * len(defense_timeline),
                mode="markers+text",
                name="Defense Events",
                text=defense_descriptions,
                textposition="bottom center",
                marker=dict(color="blue", size=10),
                hovertemplate="<b>Defense Event</b><br>%{text}<br>%{x}<extra></extra>",
            )
        )

    fig.update_layout(
        title="Attack vs Defense Events Timeline",
        xaxis_title="Time",
        yaxis_title="Event Type",
        yaxis=dict(tickvals=[0, 1], ticktext=["Defense", "Attack"]),
        height=400,
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed timeline
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔴 Attack Events")
        if attack_timeline:
            for event in attack_timeline[-5:]:  # Show last 5 events
                st.markdown(
                    f"""
                <div class="attack-timeline">
                    <strong>{event.get('timestamp', 'Unknown time')}</strong><br>
                    {event.get('description', 'No description')}
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No attack events yet.")

    with col2:
        st.markdown("### 🔵 Defense Events")
        if defense_timeline:
            for event in defense_timeline[-5:]:  # Show last 5 events
                st.markdown(
                    f"""
                <div class="defense-timeline">
                    <strong>{event.get('timestamp', 'Unknown time')}</strong><br>
                    {event.get('description', 'No description')}
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No defense events yet.")


def render_mitre_analysis(display_options):
    """Render MITRE ATT&CK analysis section."""
    if (
        not st.session_state.simulation_data["active"]
        or not display_options["show_mitre"]
    ):
        return

    st.header("🎯 MITRE ATT&CK Analysis")

    # Collect MITRE techniques from timeline events
    attack_timeline = st.session_state.simulation_data["attack_timeline"]
    defense_timeline = st.session_state.simulation_data["defense_timeline"]

    mitre_techniques = {}

    for event in attack_timeline:
        technique = event.get("mitre_technique")
        if technique:
            mitre_techniques[technique] = mitre_techniques.get(technique, 0) + 1

    if not mitre_techniques:
        st.info("No MITRE ATT&CK techniques detected yet.")
        return

    # Create technique frequency chart
    techniques = list(mitre_techniques.keys())
    frequencies = list(mitre_techniques.values())

    fig = px.bar(
        x=techniques,
        y=frequencies,
        title="MITRE ATT&CK Technique Frequency",
        labels={"x": "Technique", "y": "Frequency"},
        color=frequencies,
        color_continuous_scale="Reds",
    )

    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Technique details
    st.markdown("### Technique Details")

    technique_details = []
    for event in attack_timeline:
        technique = event.get("mitre_technique")
        if technique:
            technique_details.append(
                {
                    "Technique": technique,
                    "Description": event.get("description", ""),
                    "Timestamp": event.get("timestamp", ""),
                    "Agent": event.get("agent_id", ""),
                }
            )

    if technique_details:
        df = pd.DataFrame(technique_details)
        st.dataframe(df, use_container_width=True)


def render_system_logs():
    """Render system logs section."""
    st.header("📋 System Logs")

    # Log level filter
    log_level = st.selectbox(
        "Filter by Log Level", ["All", "INFO", "WARNING", "ERROR", "CRITICAL"], index=0
    )

    # Number of logs to show
    num_logs = st.slider("Number of logs to show", 10, 100, 50)

    # Mock log data for demonstration
    log_data = [
        {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "message": "Simulation started",
        },
        {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "message": "Red team agent initialized",
        },
        {
            "timestamp": datetime.now().isoformat(),
            "level": "WARNING",
            "message": "Unusual network activity detected",
        },
        {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "message": "Blue team agent responding",
        },
        {
            "timestamp": datetime.now().isoformat(),
            "level": "ERROR",
            "message": "Agent communication timeout",
        },
    ]

    # Filter logs
    if log_level != "All":
        log_data = [log for log in log_data if log["level"] == log_level]

    # Display logs
    if log_data:
        df = pd.DataFrame(log_data)
        st.dataframe(df.head(num_logs), use_container_width=True)
    else:
        st.info("No logs available.")


def start_simulation(scenario_name):
    """Start simulation with selected scenario."""
    st.session_state.simulation_data.update(
        {
            "active": True,
            "scenario": scenario_name,
            "start_time": datetime.now(),
            "current_phase": "initialization",
            "agents": {
                "red_recon": {
                    "type": "reconnaissance",
                    "status": "active",
                    "current_task": "osint_gathering",
                },
                "red_social": {
                    "type": "social_engineering",
                    "status": "idle",
                    "current_task": "none",
                },
                "red_exploit": {
                    "type": "exploitation",
                    "status": "idle",
                    "current_task": "none",
                },
                "red_lateral": {
                    "type": "lateral_movement",
                    "status": "idle",
                    "current_task": "none",
                },
                "blue_detection": {
                    "type": "detection",
                    "status": "active",
                    "current_task": "monitoring",
                },
                "blue_response": {
                    "type": "response",
                    "status": "idle",
                    "current_task": "none",
                },
                "blue_intel": {
                    "type": "threat_intel",
                    "status": "idle",
                    "current_task": "none",
                },
            },
            "attack_timeline": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "description": "Reconnaissance initiated",
                    "mitre_technique": "T1592",
                    "agent_id": "red_recon",
                }
            ],
            "defense_timeline": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "description": "Monitoring activated",
                    "agent_id": "blue_detection",
                }
            ],
            "scores": {"red_team": 10, "blue_team": 5},
        }
    )

    st.success(f"🚀 Simulation started for scenario: {scenario_name}")


def stop_simulation():
    """Stop current simulation."""
    st.session_state.simulation_data.update(
        {
            "active": False,
            "scenario": None,
            "current_phase": None,
            "agents": {},
            "attack_timeline": [],
            "defense_timeline": [],
        }
    )

    st.success("⏹️ Simulation stopped")


def update_simulation_data():
    """Update simulation data with mock real-time updates."""
    if not st.session_state.simulation_data["active"]:
        return

    # Mock updates for demonstration
    import random

    # Update scores
    st.session_state.simulation_data["scores"]["red_team"] += random.randint(0, 5)
    st.session_state.simulation_data["scores"]["blue_team"] += random.randint(0, 5)

    # Randomly update agent status
    agents = st.session_state.simulation_data["agents"]
    for agent_id in agents:
        if random.random() < 0.1:  # 10% chance of status change
            current_status = agents[agent_id]["status"]
            if current_status == "active":
                agents[agent_id]["status"] = "idle"
            elif current_status == "idle":
                agents[agent_id]["status"] = "active"

    # Add random timeline events
    if random.random() < 0.2:  # 20% chance of new event
        event_type = random.choice(["attack", "defense"])

        if event_type == "attack":
            attack_events = [
                "Vulnerability scan completed",
                "Phishing email sent",
                "Exploitation attempt made",
                "Lateral movement initiated",
            ]
            mitre_techniques = ["T1595", "T1566", "T1203", "T1021"]

            st.session_state.simulation_data["attack_timeline"].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "description": random.choice(attack_events),
                    "mitre_technique": random.choice(mitre_techniques),
                    "agent_id": random.choice(
                        ["red_recon", "red_social", "red_exploit", "red_lateral"]
                    ),
                }
            )
        else:
            defense_events = [
                "Anomaly detected",
                "Alert generated",
                "Containment initiated",
                "Threat intelligence updated",
            ]

            st.session_state.simulation_data["defense_timeline"].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "description": random.choice(defense_events),
                    "agent_id": random.choice(
                        ["blue_detection", "blue_response", "blue_intel"]
                    ),
                }
            )


def main():
    """Main dashboard application."""
    # Auto-refresh
    if st.session_state.simulation_data["active"]:
        update_simulation_data()
        st.rerun()

    # Render components
    render_header()

    display_options = render_sidebar()

    render_simulation_overview()

    st.markdown("---")

    render_agent_status(display_options)

    st.markdown("---")

    render_timeline(display_options)

    st.markdown("---")

    render_mitre_analysis(display_options)

    st.markdown("---")

    render_system_logs()


if __name__ == "__main__":
    main()
