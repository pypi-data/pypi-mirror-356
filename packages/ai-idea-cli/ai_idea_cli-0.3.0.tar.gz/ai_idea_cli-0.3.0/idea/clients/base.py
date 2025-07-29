"""
Base HTTP client for backend services.

This module provides the base HTTP client functionality for communicating
with the backend services when not in demo mode.
"""

from typing import Any, Optional

import httpx

from idea.config import check_api_key, is_demo_mode, load_config


class BackendClient:
    """Base client for backend service communication."""

    def __init__(self, service_name: str, base_path: str):
        """
        Initialize backend client.

        Args:
            service_name: Name of the service (for error messages)
            base_path: Base path for the service (e.g., "/api/v1/validator")
        """
        self.service_name = service_name
        self.base_path = base_path
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        if is_demo_mode():
            return self

        config = load_config()

        # Get base URL from config
        base_url = config["backend"]["url"]
        if base_url.startswith("<<<"):
            # Backend not configured, should be in demo mode
            raise RuntimeError("Backend URL not configured - should be in demo mode")

        # Get API key
        api_key = check_api_key(config, "backend")

        # Create HTTP client
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "idea-cli/0.2.0",
            },
            timeout=30.0,
        )

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    async def post(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        """
        Make a POST request to the backend service.

        Args:
            endpoint: API endpoint path
            data: Request payload

        Returns:
            Response data

        Raises:
            httpx.HTTPError: If request fails
        """
        if is_demo_mode():
            raise NotImplementedError("Should be handled by demo mode")

        if not self._client:
            raise RuntimeError("Client not initialized - use async context manager")

        url = f"{self.base_path}{endpoint}"
        response = await self._client.post(url, json=data)
        response.raise_for_status()

        return response.json()

    async def get(
        self, endpoint: str, params: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Make a GET request to the backend service.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            Response data

        Raises:
            httpx.HTTPError: If request fails
        """
        if is_demo_mode():
            raise NotImplementedError("Should be handled by demo mode")

        if not self._client:
            raise RuntimeError("Client not initialized - use async context manager")

        url = f"{self.base_path}{endpoint}"
        response = await self._client.get(url, params=params)
        response.raise_for_status()

        return response.json()
