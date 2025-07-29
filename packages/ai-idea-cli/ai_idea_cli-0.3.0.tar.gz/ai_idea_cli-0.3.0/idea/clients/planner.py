"""
HTTP client for planner backend service.

This module provides HTTP client functionality for the AI-powered
project planning service.
"""

from idea.models import Plan

from .base import BackendClient


class PlannerClient(BackendClient):
    """Client for planner backend service."""

    def __init__(self):
        super().__init__("planner", "/api/v1/planner")

    async def generate_plan(self, pitch: str, category: str = "personal") -> Plan:
        """
        Generate a project plan using the backend planner service.

        Args:
            pitch: Project idea description
            category: Project category (personal or product)

        Returns:
            Generated plan object
        """
        request_data = {"idea": pitch, "category": category}

        response_data = await self.post("/generate", request_data)

        # Convert response to Plan model
        return Plan(
            project_slug=response_data["project_slug"],
            one_liner=response_data["one_liner"],
            recommended_language=response_data["recommended_language"],
            category=response_data["category"],
            python_package_name=response_data.get("python_package_name"),
            epics=response_data["epics"],
            stories=[
                {
                    "id": story["id"],
                    "name": story["name"],
                    "description": story["description"],
                    "acceptance_criteria": story["acceptance_criteria"],
                    "epic": story["epic"],
                }
                for story in response_data["stories"]
            ],
            stack_recommendations=response_data["stack_recommendations"],
        )


async def generate_plan(pitch: str, category: str = "personal") -> Plan:
    """
    Generate a plan using backend service or demo mode.

    This function maintains the same interface as the original
    generate_plan function but uses HTTP client for backend.
    """
    from idea.config import is_demo_mode

    if is_demo_mode():
        # Return demo plan
        from idea.demo import demo_generate_plan

        return demo_generate_plan(pitch, category)

    async with PlannerClient() as client:
        return await client.generate_plan(pitch, category)
