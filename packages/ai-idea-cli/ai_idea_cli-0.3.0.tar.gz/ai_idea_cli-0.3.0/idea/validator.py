"""Critical Idea Validator integration for idea-cli."""

import json
from typing import Any

import httpx
from rich.console import Console
from rich.panel import Panel

from idea.config import check_api_key, is_demo_mode, load_config

console = Console()


class ValidationError(Exception):
    """Raised when idea validation fails."""

    pass


async def validate_idea(pitch: str, dry_run: bool = False) -> dict[str, Any]:
    """
    Validate an idea using the configured validator.

    Args:
        pitch: The idea description to validate
        dry_run: If True, show what would be validated without calling API

    Returns:
        Validation response dict with score and feedback

    Raises:
        ValidationError: If validation fails or idea is rejected
    """
    config = load_config()
    validator_config = config["validator"]

    endpoint = validator_config["endpoint"]
    if endpoint.startswith("<<<"):
        if dry_run:
            console.print(
                Panel(
                    f"Would validate idea: {pitch}\n"
                    f"Endpoint: {endpoint}\n"
                    f"API Key Env: {validator_config['apiKeyEnv']}",
                    title="Validation Dry Run",
                )
            )
            return {"accepted": True, "score": 0.8, "rationale": "Dry run mode"}

        console.print(
            Panel(
                "[yellow]⚠️ Validator not configured[/yellow]\n"
                "Set validator endpoint and API key in config\n"
                "Proceeding with validation bypass for development...",
                title="Validation Bypass",
            )
        )
        return {"accepted": True, "score": 0.8, "rationale": "Development bypass"}

    api_key = check_api_key(config, "validator")

    if dry_run:
        console.print(
            Panel(
                f"Would validate idea: {pitch}\n"
                f"Endpoint: {endpoint}\n"
                f"API Key: {api_key[:8] if len(api_key) > 8 else 'demo-key'}...",
                title="Validation Dry Run",
            )
        )
        return {"accepted": True, "score": 0.8, "rationale": "Dry run mode"}

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"idea": pitch}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()

        result = response.json()

        accept_field = validator_config["acceptField"]
        score_field = validator_config["scoreField"]
        min_score = validator_config["minScore"]

        if accept_field not in result or score_field not in result:
            raise ValidationError("Invalid response format from validator")

        accepted = result[accept_field]
        score = result[score_field]

        if not accepted or score < min_score:
            rationale = result.get("rationale", "Score below threshold")
            raise ValidationError(f"Idea validation failed: {rationale}")

        return result

    except httpx.HTTPError as e:
        raise ValidationError(f"Failed to validate idea: {e}") from e
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON response: {e}") from e


def display_validation_result(result: dict[str, Any]) -> None:
    """Display validation results to the user."""
    accepted = result.get("accepted", False)
    score = result.get("score", 0.0)
    rationale = result.get("rationale", "No rationale provided")
    suggestions = result.get("suggestions", [])

    if accepted and score >= 0.7:
        console.print(
            Panel(
                f"✅ [green]Idea validated[/green]\n"
                f"Score: {score:.2f}/1.0\n"
                f"Rationale: {rationale}",
                title="Validation Success",
            )
        )
    else:
        suggestion_text = ""
        if suggestions:
            suggestion_text = "\n\n[yellow]Suggestions:[/yellow]\n" + "\n".join(
                f"• {s}" for s in suggestions
            )

        console.print(
            Panel(
                f"❌ [red]Idea validation failed[/red]\n"
                f"Score: {score:.2f}/1.0\n"
                f"Rationale: {rationale}{suggestion_text}",
                title="Validation Failed",
            )
        )

        if not is_demo_mode():  # Only raise in non-demo mode
            raise ValidationError(f"Idea validation failed: {rationale}")
