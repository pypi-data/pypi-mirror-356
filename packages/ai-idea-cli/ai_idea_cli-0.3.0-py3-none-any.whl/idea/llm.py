"""LLM integration for idea-cli."""

from idea.config import check_api_key, is_demo_mode, load_config


async def call_llm(task_type: str, prompt: str) -> str:
    """
    Call LLM service for various tasks.

    Args:
        task_type: Type of task (plan, queue, summarise)
        prompt: The prompt to send to the LLM

    Returns:
        LLM response text

    Raises:
        ConfigError: If API key is missing and not in demo mode
        RuntimeError: If LLM call fails
    """
    if is_demo_mode():
        return _demo_llm_response(task_type, prompt)

    config = load_config()
    api_key = check_api_key(config, "llm")
    model = config["models"][task_type]

    # Determine provider based on model name
    if "claude" in model.lower():
        return await _call_claude(model, prompt, api_key)
    elif "gpt" in model.lower() or "openai" in model.lower():
        return await _call_openai(model, prompt, api_key)
    else:
        raise RuntimeError(f"Unknown model type: {model}")


async def _call_claude(model: str, prompt: str, api_key: str) -> str:
    """Call Claude API."""
    try:
        import anthropic

        client = anthropic.AsyncAnthropic(api_key=api_key)

        response = await client.messages.create(
            model=model, max_tokens=4096, messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    except ImportError as e:
        raise RuntimeError(
            "Anthropic package not installed. Run: pip install anthropic"
        ) from e
    except Exception as e:
        raise RuntimeError(f"Claude API call failed: {e}") from e


async def _call_openai(model: str, prompt: str, api_key: str) -> str:
    """Call OpenAI API."""
    try:
        import openai

        client = openai.AsyncOpenAI(api_key=api_key)

        response = await client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}], max_tokens=4096
        )

        return response.choices[0].message.content

    except ImportError as e:
        raise RuntimeError(
            "OpenAI package not installed. Run: pip install openai"
        ) from e
    except Exception as e:
        raise RuntimeError(f"OpenAI API call failed: {e}") from e


def _demo_llm_response(task_type: str, prompt: str) -> str:
    """Generate demo responses for different task types."""
    if task_type == "plan":
        return """
{
  "project_slug": "demo-project",
  "one_liner": "A demo project created in demo mode",
  "recommended_language": "python",
  "category": "personal",
  "python_package_name": "demo_project",
  "epics": [
    "Project Setup",
    "Core Features",
    "Testing",
    "Documentation"
  ],
  "stories": [
    {
      "id": "story-1",
      "name": "Basic Setup",
      "description": "Set up basic project structure",
      "acceptance_criteria": ["Project structure created", "Dependencies configured"],
      "epic": "Project Setup"
    },
    {
      "id": "story-2",
      "name": "Core Logic",
      "description": "Implement core functionality",
      "acceptance_criteria": ["Core functions implemented", "Basic error handling"],
      "epic": "Core Features"
    },
    {
      "id": "story-3",
      "name": "Testing",
      "description": "Add unit tests",
      "acceptance_criteria": ["Test suite created", "Coverage >80%"],
      "epic": "Testing"
    }
  ],
  "stack_recommendations": ["Python 3.12", "pytest", "black", "ruff"]
}
"""
    elif task_type == "queue":
        return "Demo response for queue processing - this would contain implementation code."
    elif task_type == "summarise":
        return """
{
  "lessons": [
    {
      "id": "lesson-demo-001",
      "title": "Demo Mode Lesson",
      "description": "This is a demo lesson generated in demo mode",
      "tags": ["demo", "example"],
      "severity": "low",
      "pattern": "demo-pattern",
      "solution": "Configure API keys to get real lessons"
    }
  ]
}
"""
    else:
        return f"Demo response for task type: {task_type}"
