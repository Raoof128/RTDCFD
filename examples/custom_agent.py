#!/usr/bin/env python3
"""
Custom Agent Example

This example demonstrates how to create a custom agent and integrate it
into the simulation system.
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain.tools import BaseOutputParser, BaseTool
from pydantic import BaseModel, Field

from agents.base_agent import AgentMessage, BaseAgent
from utils.logging_handler import get_logger


class CustomToolInput(BaseModel):
    """Input schema for custom tool."""

    query: str = Field(description="Query to process")
    context: str = Field(default="", description="Additional context")


class CustomToolOutput(BaseModel):
    """Output schema for custom tool."""

    result: str = Field(description="Processing result")
    confidence: float = Field(description="Confidence in result (0.0-1.0)")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")


class CustomTool(BaseTool):
    """Custom tool for demonstration purposes."""

    name = "custom_processor"
    description = "Process queries with custom logic"
    args_schema = CustomToolInput

    def _run(self, query: str, context: str = "") -> str:
        """Run the custom tool."""
        logger = get_logger(__name__)

        # Simulate processing
        processed_query = f"Processed: {query}"
        if context:
            processed_query += f" (Context: {context})"

        # Simulate confidence calculation
        confidence = 0.8 if len(query) > 10 else 0.6

        # Create output
        output = CustomToolOutput(
            result=processed_query,
            confidence=confidence,
            metadata={
                "processed_at": datetime.now().isoformat(),
                "query_length": len(query),
                "has_context": bool(context),
            },
        )

        logger.info(f"Custom tool processed query: {query[:50]}...")
        return output.model_dump_json()


class CustomAgent(BaseAgent):
    """Custom agent example with specialized capabilities."""

    def __init__(self, agent_id: str = None):
        """Initialize the custom agent."""
        agent_id = (
            agent_id or f"custom_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        # Custom system prompt
        system_prompt = """
        You are a Custom Agent for the Autonomous Multi-Agent Red/Blue Team Simulation System.
        
        Your capabilities include:
        - Query processing and analysis
        - Custom data transformation
        - Pattern recognition
        - Report generation
        
        You operate in simulation-only mode and must not perform any real-world actions.
        Always prioritize safety and ethical considerations.
        Follow Australian cybersecurity regulations and best practices.
        
        When processing queries, provide detailed analysis and recommendations.
        Include confidence levels and supporting evidence when possible.
        """

        # Create custom tools
        tools = self._create_custom_tools()

        super().__init__(
            agent_id=agent_id,
            agent_type="custom_agent",
            system_prompt=system_prompt,
            tools=tools,
            enable_mcp=True,
        )

        self.logger = get_logger(agent_id, "custom_agent")

        # Custom agent state
        self.processed_queries = []
        self.analysis_results = {}
        self.custom_capabilities = {
            "query_processing": True,
            "pattern_analysis": True,
            "report_generation": True,
            "data_transformation": True,
        }

        self.logger.info(f"Custom Agent {agent_id} initialized")

    def _create_custom_tools(self) -> List[BaseTool]:
        """Create custom tools for the agent."""
        return [
            CustomTool(),
            PatternRecognitionTool(),
            ReportGeneratorTool(),
            DataTransformerTool(),
        ]

    async def process_command(self, command: Dict[str, Any]) -> None:
        """Process custom agent commands."""
        self.logger.info(f"Processing custom command: {command}")

        command_type = command.get("type", "unknown")

        if command_type == "process_query":
            await self._handle_process_query_command(command)
        elif command_type == "analyze_pattern":
            await self._handle_analyze_pattern_command(command)
        elif command_type == "generate_report":
            await self._handle_generate_report_command(command)
        elif command_type == "transform_data":
            await self._handle_transform_data_command(command)
        else:
            self.logger.warning(f"Unknown command type: {command_type}")

    async def _handle_process_query_command(self, command: Dict[str, Any]) -> None:
        """Handle query processing command."""
        query = command.get("query")
        context = command.get("context", "")
        query_id = command.get(
            "query_id", f"query_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        self.logger.info(f"Processing query: {query_id}")

        # Execute query processing task
        task = f"Process the following query: {query}"
        if context:
            task += f"\nContext: {context}"

        result = await self.execute_task(task)

        if result["success"]:
            # Store processed query
            self.processed_queries.append(
                {
                    "query_id": query_id,
                    "query": query,
                    "context": context,
                    "result": result["result"],
                    "timestamp": datetime.now().isoformat(),
                }
            )

            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "process_query",
                    "query_id": query_id,
                    "result": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"Query processing failed: {result.get('error')}")

    async def _handle_analyze_pattern_command(self, command: Dict[str, Any]) -> None:
        """Handle pattern analysis command."""
        data = command.get("data", "")
        pattern_type = command.get("pattern_type", "general")
        analysis_id = command.get(
            "analysis_id", f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        self.logger.info(f"Analyzing pattern: {analysis_id}")

        # Execute pattern analysis task
        task = f"Analyze patterns in the following data: {data}"
        task += f"\nPattern type: {pattern_type}"

        result = await self.execute_task(task)

        if result["success"]:
            # Store analysis results
            self.analysis_results[analysis_id] = {
                "data": data,
                "pattern_type": pattern_type,
                "analysis": result["result"],
                "timestamp": datetime.now().isoformat(),
            }

            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "analyze_pattern",
                    "analysis_id": analysis_id,
                    "result": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"Pattern analysis failed: {result.get('error')}")

    async def _handle_generate_report_command(self, command: Dict[str, Any]) -> None:
        """Handle report generation command."""
        report_type = command.get("report_type", "summary")
        data = command.get("data", {})
        report_id = command.get(
            "report_id", f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        self.logger.info(f"Generating report: {report_id}")

        # Execute report generation task
        task = f"Generate a {report_type} report based on: {data}"

        result = await self.execute_task(task)

        if result["success"]:
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "generate_report",
                    "report_id": report_id,
                    "report_type": report_type,
                    "result": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"Report generation failed: {result.get('error')}")

    async def _handle_transform_data_command(self, command: Dict[str, Any]) -> None:
        """Handle data transformation command."""
        data = command.get("data", {})
        transformation_type = command.get("transformation_type", "normalize")
        transform_id = command.get(
            "transform_id", f"transform_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        self.logger.info(f"Transforming data: {transform_id}")

        # Execute data transformation task
        task = f"Transform the following data: {data}"
        task += f"\nTransformation type: {transformation_type}"

        result = await self.execute_task(task)

        if result["success"]:
            # Send results to coordinator
            await self.send_message(
                receiver_id="coordinator",
                message_type="response",
                content={
                    "command_type": "transform_data",
                    "transform_id": transform_id,
                    "transformation_type": transformation_type,
                    "result": result["result"],
                    "success": True,
                },
            )
        else:
            self.logger.error(f"Data transformation failed: {result.get('error')}")

    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Get custom agent capabilities."""
        return {
            "agent_type": "custom_agent",
            "capabilities": list(self.custom_capabilities.keys()),
            "tools": [tool.name for tool in self.tools],
            "processed_queries_count": len(self.processed_queries),
            "analysis_results_count": len(self.analysis_results),
            "custom_features": {
                "query_processing": self.custom_capabilities["query_processing"],
                "pattern_analysis": self.custom_capabilities["pattern_analysis"],
                "report_generation": self.custom_capabilities["report_generation"],
                "data_transformation": self.custom_capabilities["data_transformation"],
            },
        }

    def get_agent_summary(self) -> Dict[str, Any]:
        """Get comprehensive agent summary."""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "processed_queries": self.processed_queries,
            "analysis_results": self.analysis_results,
            "capabilities": self.get_agent_capabilities(),
            "status": "active",
            "last_activity": datetime.now().isoformat(),
        }


class PatternRecognitionTool(BaseTool):
    """Tool for pattern recognition."""

    name = "pattern_recognition"
    description = "Recognize patterns in data"
    args_schema = CustomToolInput

    def _run(self, query: str, context: str = "") -> str:
        """Run pattern recognition."""
        # Simulate pattern recognition
        patterns = ["temporal", "behavioral", "network", "communication"]
        detected_patterns = []

        for pattern in patterns:
            if pattern.lower() in query.lower():
                detected_patterns.append(pattern)

        result = {
            "detected_patterns": detected_patterns,
            "confidence": len(detected_patterns) / len(patterns),
            "analysis": f"Detected {len(detected_patterns)} patterns: {', '.join(detected_patterns)}",
        }

        return str(result)


class ReportGeneratorTool(BaseTool):
    """Tool for generating reports."""

    name = "report_generator"
    description = "Generate structured reports"
    args_schema = CustomToolInput

    def _run(self, query: str, context: str = "") -> str:
        """Run report generation."""
        # Simulate report generation
        report = {
            "title": "Custom Analysis Report",
            "timestamp": datetime.now().isoformat(),
            "summary": query[:100] + "..." if len(query) > 100 else query,
            "findings": [
                "Pattern detected in data",
                "Anomaly identified in behavior",
                "Recommendations provided",
            ],
            "confidence": 0.85,
        }

        return str(report)


class DataTransformerTool(BaseTool):
    """Tool for data transformation."""

    name = "data_transformer"
    description = "Transform and normalize data"
    args_schema = CustomToolInput

    def _run(self, query: str, context: str = "") -> str:
        """Run data transformation."""
        # Simulate data transformation
        transformed = {
            "original": query,
            "normalized": query.lower().strip(),
            "tokenized": query.split(),
            "length": len(query),
            "has_context": bool(context),
            "transformation_timestamp": datetime.now().isoformat(),
        }

        return str(transformed)


async def main():
    """Main function for the custom agent example."""

    print("🤖 Custom Agent Example")
    print("=" * 50)

    # Create custom agent
    agent = CustomAgent()

    try:
        # Test custom capabilities
        print(f"Agent ID: {agent.agent_id}")
        print(f"Agent Type: {agent.agent_type}")
        print(f"Capabilities: {list(agent.custom_capabilities.keys())}")

        # Test query processing
        print("\n🔍 Testing query processing...")
        await agent.process_command(
            {
                "type": "process_query",
                "query": "Analyze the security implications of this scenario",
                "context": "Energy grid simulation",
            }
        )

        # Wait for processing
        await asyncio.sleep(2)

        # Test pattern analysis
        print("\n🔍 Testing pattern analysis...")
        await agent.process_command(
            {
                "type": "analyze_pattern",
                "data": "User login patterns show unusual temporal behavior",
                "pattern_type": "temporal",
            }
        )

        # Wait for processing
        await asyncio.sleep(2)

        # Test report generation
        print("\n📊 Testing report generation...")
        await agent.process_command(
            {
                "type": "generate_report",
                "report_type": "security_analysis",
                "data": {"findings": ["Pattern detected", "Anomaly identified"]},
            }
        )

        # Wait for processing
        await asyncio.sleep(2)

        # Get agent summary
        summary = agent.get_agent_summary()
        print(f"\n📋 Agent Summary:")
        print(f"  Processed Queries: {summary['processed_queries_count']}")
        print(f"  Analysis Results: {summary['analysis_results_count']}")
        print(f"  Status: {summary['status']}")

        # Cleanup
        await agent.cleanup()

        print("\n✅ Custom agent example completed successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
