"""
MCP Servers Package

This package provides the Model Context Protocol (MCP) servers for
agent communication in the autonomous multi-agent simulation system.
"""

from .mcp_server import MCPServer, start_main_server, stop_all_servers
from .red_team_mcp import RedTeamMCPServer, start_red_team_server, get_red_team_server, stop_red_team_server
from .blue_team_mcp import BlueTeamMCPServer, start_blue_team_server, get_blue_team_server, stop_blue_team_server

__all__ = [
    "MCPServer",
    "RedTeamMCPServer", 
    "BlueTeamMCPServer",
    "start_main_server",
    "start_red_team_server",
    "start_blue_team_server",
    "get_red_team_server",
    "get_blue_team_server",
    "stop_all_servers",
    "stop_red_team_server",
    "stop_blue_team_server"
]
