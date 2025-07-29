"""
HTTP client for queue backend service.

This module provides HTTP client functionality for the implementation
queue execution service.
"""

from typing import Any

from .base import BackendClient


class QueueClient(BackendClient):
    """Client for queue backend service."""

    def __init__(self):
        super().__init__("queue", "/api/v1/queue")

    async def execute_story(
        self, story_id: str, project_context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Execute a story using the backend queue service.

        Args:
            story_id: Story ID to implement
            project_context: Project context and metadata

        Returns:
            Execution result with generated code and commit message
        """
        request_data = {"story_id": story_id, "project_context": project_context}

        return await self.post("/execute", request_data)


class QueueRunner:
    """
    Queue runner that uses backend service for implementation.

    This class maintains the same interface as the original QueueRunner
    but delegates to the backend service when not in demo mode.
    """

    def __init__(self, project_dir):
        self.project_dir = project_dir

    async def run_queue(self, dry_run: bool = False):
        """
        Execute the implementation queue.

        Args:
            dry_run: If True, show what would be executed without calling backend
        """
        # This is a placeholder implementation
        # In demo mode, this would be handled by demo_not_available
        # In full mode, this would use the QueueClient to execute stories

        if dry_run:
            print(f"Would execute queue for project: {self.project_dir}")
            return

        # For now, this is a placeholder
        # Real implementation would:
        # 1. Load queue from project
        # 2. For each pending story, call QueueClient.execute_story
        # 3. Apply the generated code changes
        # 4. Create commits

        raise NotImplementedError(
            "Queue execution via backend service not yet implemented"
        )
