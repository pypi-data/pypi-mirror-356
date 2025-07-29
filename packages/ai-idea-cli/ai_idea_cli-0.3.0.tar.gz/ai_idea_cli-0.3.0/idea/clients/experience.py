"""
HTTP client for experience backend service.

This module provides HTTP client functionality for the development
experience collection and lesson generation service.
"""

from pathlib import Path
from typing import Any

from .base import BackendClient


class ExperienceClient(BackendClient):
    """Client for experience backend service."""

    def __init__(self):
        super().__init__("experience", "/api/v1/experience")

    async def collect_failure(self, context: str, error: str, command: str = "") -> str:
        """
        Collect a development failure for learning.

        Args:
            context: Context of the failure
            error: Error message or description
            command: Command that failed

        Returns:
            Log ID of the collected experience
        """
        request_data = {"context": context, "error": error, "command": command}

        response = await self.post("/collect", request_data)
        return response["log_id"]

    async def summarise_failures(self, hours: int = 24) -> list[dict[str, Any]]:
        """
        Summarize recent failures into actionable lessons.

        Args:
            hours: Hours to look back for failures

        Returns:
            List of generated lessons
        """
        request_data = {"hours": hours}

        response = await self.post("/summarise", request_data)
        return response["lessons"]


class ExperienceManager:
    """
    Experience manager that uses backend service for processing.

    This class maintains the same interface as the original ExperienceManager
    but delegates to the backend service when not in demo mode.
    """

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.logs_dir = project_dir / ".idea" / "_logs"

    def collect_failure(self, context: str, error: str, command: str = "") -> str:
        """
        Collect a failure for learning.

        In demo mode, this would store locally.
        In full mode, this would use the backend service.
        """
        # For now, this is a placeholder
        # Real implementation would check if demo mode and either:
        # 1. Store locally (demo mode)
        # 2. Send to backend service (full mode)

        # Generate a simple log ID for demo purposes
        import time

        log_id = f"exp-{int(time.time())}"

        # In demo mode, we could store locally
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = self.logs_dir / f"{log_id}.json"

        import json

        with open(log_file, "w") as f:
            json.dump(
                {
                    "log_id": log_id,
                    "context": context,
                    "error": error,
                    "command": command,
                    "timestamp": time.time(),
                },
                f,
                indent=2,
            )

        return log_id

    async def summarise_failures(self, hours: int = 24) -> list[dict[str, Any]]:
        """
        Summarize failures into lessons.

        In demo mode, this would return demo lessons.
        In full mode, this would use the backend service.
        """
        # This is a placeholder implementation
        # Real implementation would check demo mode and either:
        # 1. Return demo lessons (demo mode)
        # 2. Call backend service (full mode)

        return [
            {
                "id": "lesson-demo",
                "title": "Demo Experience Lesson",
                "description": "This is a demo lesson",
                "tags": ["demo"],
                "severity": "low",
            }
        ]
