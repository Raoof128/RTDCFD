"""
Logging utilities for the Autonomous Multi-Agent Red/Blue Team Simulation System.

Provides structured JSON logging with attack/defense narrative generation,
agent activity tracking, and security event logging.
"""

import json
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Optional

from config import LOGS_DIR, settings


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, "agent_id"):
            log_entry["agent_id"] = record.agent_id
        if hasattr(record, "agent_type"):
            log_entry["agent_type"] = record.agent_type
        if hasattr(record, "scenario"):
            log_entry["scenario"] = record.scenario
        if hasattr(record, "attack_stage"):
            log_entry["attack_stage"] = record.attack_stage
        if hasattr(record, "mitre_technique"):
            log_entry["mitre_technique"] = record.mitre_technique
        if hasattr(record, "event_type"):
            log_entry["event_type"] = record.event_type
        if hasattr(record, "severity"):
            log_entry["severity"] = record.severity

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, default=str)


class NarrativeLogger:
    """
    Specialized logger for generating attack/defense narratives.

    This logger creates structured narratives that can be used for:
    - After-action reports
    - Timeline reconstruction
    - MITRE ATT&CK mapping
    - Executive summaries
    """

    def __init__(self, log_file: Optional[str] = None):
        """Initialize narrative logger."""
        self.logger = logging.getLogger("narrative")
        self.logger.setLevel(logging.INFO)

        # Create formatter
        formatter = JSONFormatter()

        # Console handler
        if settings.enable_console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # File handler
        if log_file:
            log_path = LOGS_DIR / log_file
            file_handler = RotatingFileHandler(
                log_path, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log_agent_action(
        self,
        agent_id: str,
        agent_type: str,
        action: str,
        details: Dict[str, Any],
        severity: str = "info",
    ) -> None:
        """Log an agent action with context."""
        self.logger.info(
            f"Agent {agent_id} ({agent_type}) performed action: {action}",
            extra={
                "agent_id": agent_id,
                "agent_type": agent_type,
                "event_type": "agent_action",
                "severity": severity,
                "action": action,
                "details": details,
            },
        )

    def log_attack_event(
        self,
        agent_id: str,
        attack_stage: str,
        mitre_technique: str,
        description: str,
        target: Optional[str] = None,
        success: bool = False,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log an attack event with MITRE ATT&CK mapping."""
        self.logger.info(
            f"Attack event: {attack_stage} - {mitre_technique} - {description}",
            extra={
                "agent_id": agent_id,
                "event_type": "attack_event",
                "attack_stage": attack_stage,
                "mitre_technique": mitre_technique,
                "target": target,
                "success": success,
                "details": details or {},
            },
        )

    def log_defense_event(
        self,
        agent_id: str,
        defense_action: str,
        detection_type: str,
        description: str,
        mitigated_threat: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a defense event."""
        self.logger.info(
            f"Defense event: {defense_action} - {detection_type} - {description}",
            extra={
                "agent_id": agent_id,
                "event_type": "defense_event",
                "defense_action": defense_action,
                "detection_type": detection_type,
                "mitigated_threat": mitigated_threat,
                "details": details or {},
            },
        )

    def log_coordination_event(
        self,
        coordinator_id: str,
        event_type: str,
        description: str,
        participants: Optional[list] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a coordination event between agents."""
        self.logger.info(
            f"Coordination event: {event_type} - {description}",
            extra={
                "agent_id": coordinator_id,
                "event_type": "coordination_event",
                "coordination_type": event_type,
                "participants": participants or [],
                "details": details or {},
            },
        )

    def log_scenario_event(
        self,
        scenario: str,
        event_type: str,
        description: str,
        stage: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a scenario-level event."""
        self.logger.info(
            f"Scenario event: {scenario} - {event_type} - {description}",
            extra={
                "scenario": scenario,
                "event_type": "scenario_event",
                "stage": stage,
                "details": details or {},
            },
        )


# Global narrative logger instance
_narrative_logger = None


def get_narrative_logger() -> NarrativeLogger:
    """Get the global narrative logger instance."""
    global _narrative_logger
    if _narrative_logger is None:
        _narrative_logger = NarrativeLogger(settings.log_file)
    return _narrative_logger


def setup_logging(
    log_level: str = "INFO", log_file: Optional[str] = None, enable_console: bool = True
) -> None:
    """
    Set up logging for the application.

    Args:
        log_level: Logging level
        log_file: Log file path
        enable_console: Whether to enable console output
    """
    # Create logs directory if it doesn't exist
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    root_logger.handlers.clear()

    # Create formatter
    formatter = JSONFormatter()

    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # File handler
    if log_file:
        log_path = LOGS_DIR / log_file
        file_handler = RotatingFileHandler(
            log_path, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Initialize narrative logger
    global _narrative_logger
    _narrative_logger = NarrativeLogger(log_file)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class AgentLoggerAdapter(logging.LoggerAdapter):
    """Logger adapter that automatically adds agent context."""

    def __init__(self, logger: logging.Logger, agent_id: str, agent_type: str):
        """Initialize agent logger adapter."""
        super().__init__(logger, {"agent_id": agent_id, "agent_type": agent_type})
        self.agent_id = agent_id
        self.agent_type = agent_type

    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """Process log message with agent context."""
        if "extra" not in kwargs:
            kwargs["extra"] = {}

        kwargs["extra"].update(self.extra)
        return msg, kwargs


def get_agent_logger(agent_id: str, agent_type: str) -> AgentLoggerAdapter:
    """
    Get a logger adapter for a specific agent.

    Args:
        agent_id: Agent ID
        agent_type: Agent type

    Returns:
        Agent logger adapter
    """
    logger = logging.getLogger(f"agent.{agent_type}.{agent_id}")
    return AgentLoggerAdapter(logger, agent_id, agent_type)
