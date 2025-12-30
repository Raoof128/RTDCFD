"""
Base Agent Class for Autonomous Multi-Agent Red/Blue Team Simulation System

This module provides the foundation for all agents in the simulation system,
including LangChain integration, memory management, tool calling, and MCP client integration.
"""

import asyncio
import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import BaseTool
from langchain_anthropic import ChatAnthropic

from config import AgentConfig, settings
from utils.logging_handler import get_logger
from utils.mcp_client import MCPClient

logger = get_logger(__name__)


@dataclass
class AgentMessage:
    """Message structure for inter-agent communication."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = ""
    receiver_id: str = ""
    message_type: str = "command"  # command, response, alert, status
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    priority: str = "normal"  # low, normal, high, critical
    requires_response: bool = False


@dataclass
class AgentState:
    """Current state of an agent."""

    agent_id: str
    agent_type: str
    status: str = "idle"  # idle, active, busy, error
    current_task: Optional[str] = None
    memory_count: int = 0
    last_activity: datetime = field(default_factory=datetime.now)
    tools_available: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Base class for all agents in the simulation system.

    Provides common functionality for:
    - LangChain ReAct agent implementation
    - Memory management (conversation + episodic)
    - Tool calling interface
    - MCP client integration
    - Inter-agent communication
    """

    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        system_prompt: str,
        tools: Optional[List[BaseTool]] = None,
        memory_window: int = AgentConfig.MAX_MEMORY_TURNS,
        enable_mcp: bool = True,
    ):
        """
        Initialize the base agent.

        Args:
            agent_id: Unique identifier for this agent
            agent_type: Type of agent (recon, detection, etc.)
            system_prompt: System prompt defining agent role and behavior
            tools: List of tools available to this agent
            memory_window: Number of conversation turns to remember
            enable_mcp: Whether to enable MCP communication
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.system_prompt = system_prompt

        # Initialize state
        self.state = AgentState(
            agent_id=agent_id,
            agent_type=agent_type,
            tools_available=[tool.name for tool in tools] if tools else [],
        )

        # LangChain components
        self.llm = ChatAnthropic(
            model=settings.anthropic_model,
            anthropic_api_key=settings.anthropic_api_key,
            temperature=0.1,  # Low temperature for consistent behavior
            max_tokens=AgentConfig.RESPONSE_MAX_TOKENS,
        )

        # Memory management
        self.memory = ConversationBufferWindowMemory(
            k=memory_window, memory_key="chat_history", return_messages=True
        )

        # Tools
        self.tools = tools or []

        # MCP client for inter-agent communication
        self.mcp_client = None
        if enable_mcp:
            self.mcp_client = MCPClient(
                agent_id=agent_id,
                server_host=settings.mcp_server_host,
                server_port=self._get_mcp_port(),
            )

        # Agent executor
        self.agent_executor = None
        self._setup_agent_executor()

        # Message handlers
        self.message_handlers = {
            "command": self._handle_command,
            "response": self._handle_response,
            "alert": self._handle_alert,
            "status": self._handle_status,
        }

        logger.info(f"Initialized {agent_type} agent: {agent_id}")

    def _get_mcp_port(self) -> int:
        """Get appropriate MCP port based on agent type."""
        if "red" in self.agent_type.lower():
            return settings.mcp_red_team_port
        elif "blue" in self.agent_type.lower():
            return settings.mcp_blue_team_port
        else:
            return settings.mcp_server_port

    def _setup_agent_executor(self) -> None:
        """Set up the LangChain agent executor with ReAct prompt."""
        # Create ReAct prompt template
        react_prompt = PromptTemplate.from_template(
            f"""{self.system_prompt}

You have access to the following tools:
{{tools}}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{{tool_names}}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {{input}}
Thought: {{agent_scratchpad}}"""
        )

        # Create ReAct agent
        agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=react_prompt)

        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=5,
            early_stopping_method="generate",
            handle_parsing_errors=True,
            return_intermediate_steps=True,
        )

    async def start_mcp_client(self) -> None:
        """Start the MCP client for inter-agent communication."""
        if self.mcp_client:
            await self.mcp_client.start()
            logger.info(f"MCP client started for agent {self.agent_id}")

    async def stop_mcp_client(self) -> None:
        """Stop the MCP client."""
        if self.mcp_client:
            await self.mcp_client.stop()
            logger.info(f"MCP client stopped for agent {self.agent_id}")

    async def send_message(
        self,
        receiver_id: str,
        message_type: str,
        content: Dict[str, Any],
        priority: str = "normal",
        requires_response: bool = False,
    ) -> None:
        """
        Send a message to another agent via MCP.

        Args:
            receiver_id: ID of the receiving agent
            message_type: Type of message (command, response, alert, status)
            content: Message content
            priority: Message priority
            requires_response: Whether a response is required
        """
        if not self.mcp_client:
            logger.warning(f"MCP client not available for agent {self.agent_id}")
            return

        message = AgentMessage(
            sender_id=self.agent_id,
            receiver_id=receiver_id,
            message_type=message_type,
            content=content,
            priority=priority,
            requires_response=requires_response,
        )

        await self.mcp_client.send_message(message)
        logger.debug(f"Sent {message_type} message to {receiver_id}")

    async def receive_message(self, message: AgentMessage) -> None:
        """
        Receive and process a message from another agent.

        Args:
            message: The received message
        """
        logger.debug(
            f"Received {message.message_type} message from {message.sender_id}"
        )

        # Update state
        self.state.last_activity = datetime.now()

        # Handle message based on type
        handler = self.message_handlers.get(message.message_type)
        if handler:
            await handler(message)
        else:
            logger.warning(f"Unknown message type: {message.message_type}")

    async def _handle_command(self, message: AgentMessage) -> None:
        """Handle command message."""
        await self.process_command(message.content)

    async def _handle_response(self, message: AgentMessage) -> None:
        """Handle response message."""
        await self.process_response(message.content)

    async def _handle_alert(self, message: AgentMessage) -> None:
        """Handle alert message."""
        await self.process_alert(message.content)

    async def _handle_status(self, message: AgentMessage) -> None:
        """Handle status message."""
        await self.process_status(message.content)

    async def process_command(self, command: Dict[str, Any]) -> None:
        """Process a command message. Override in subclasses."""
        logger.info(f"Agent {self.agent_id} processing command: {command}")

    async def process_response(self, response: Dict[str, Any]) -> None:
        """Process a response message. Override in subclasses."""
        logger.info(f"Agent {self.agent_id} processing response: {response}")

    async def process_alert(self, alert: Dict[str, Any]) -> None:
        """Process an alert message. Override in subclasses."""
        logger.warning(f"Agent {self.agent_id} received alert: {alert}")

    async def process_status(self, status: Dict[str, Any]) -> None:
        """Process a status message. Override in subclasses."""
        logger.info(f"Agent {self.agent_id} received status: {status}")

    async def execute_task(
        self, task: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a task using the LangChain agent.

        Args:
            task: The task to execute
            context: Additional context for the task

        Returns:
            Dictionary containing task results
        """
        logger.info(f"Agent {self.agent_id} executing task: {task}")

        # Update state
        self.state.status = "active"
        self.state.current_task = task
        self.state.last_activity = datetime.now()

        try:
            # Prepare input with context
            input_text = task
            if context:
                input_text += f"\n\nContext: {json.dumps(context, indent=2)}"

            # Execute task
            result = await self.agent_executor.ainvoke({"input": input_text})

            # Update metrics
            self.state.metrics["tasks_completed"] = (
                self.state.metrics.get("tasks_completed", 0) + 1
            )
            self.state.memory_count = len(self.memory.chat_memory.messages)

            # Return result
            return {
                "success": True,
                "result": result.get("output", ""),
                "intermediate_steps": result.get("intermediate_steps", []),
                "agent_id": self.agent_id,
                "task": task,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Task execution failed for agent {self.agent_id}: {e}")
            self.state.status = "error"
            return {
                "success": False,
                "error": str(e),
                "agent_id": self.agent_id,
                "task": task,
                "timestamp": datetime.now().isoformat(),
            }
        finally:
            self.state.status = "idle"
            self.state.current_task = None

    def get_state(self) -> AgentState:
        """Get the current state of the agent."""
        self.state.last_activity = datetime.now()
        return self.state

    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of the agent's memory."""
        return {
            "agent_id": self.agent_id,
            "memory_count": len(self.memory.chat_memory.messages),
            "memory_window": self.memory.k,
            "last_messages": [
                {
                    "type": msg.__class__.__name__,
                    "content": (
                        msg.content[:100] + "..."
                        if len(msg.content) > 100
                        else msg.content
                    ),
                }
                for msg in self.memory.chat_memory.messages[-5:]
            ],
        }

    @abstractmethod
    def get_agent_capabilities(self) -> Dict[str, Any]:
        """
        Get the capabilities of this agent.
        Must be implemented by subclasses.

        Returns:
            Dictionary describing agent capabilities
        """
        pass

    async def cleanup(self) -> None:
        """Clean up resources."""
        await self.stop_mcp_client()
        logger.info(f"Agent {self.agent_id} cleaned up")
