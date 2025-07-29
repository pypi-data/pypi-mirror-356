"""Demo mode implementations for idea-cli."""

from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel

from idea.models import Plan, Story

console = Console()


def demo_validate_idea(pitch: str) -> dict[str, Any]:
    """Demo implementation of idea validation."""
    console.print(
        Panel(
            f"[yellow]🎭 DEMO MODE[/yellow]\n"
            f"Validating: {pitch}\n\n"
            f"In demo mode, all ideas receive a neutral score.\n"
            f"Configure your API keys for real validation.",
            title="Demo Validation",
        )
    )

    return {
        "accepted": True,
        "score": 0.5,
        "rationale": "Demo mode placeholder - configure API keys for real validation",
        "suggestions": [
            "This is demo mode - configure your API keys for real validation",
            "Set demoMode: false in your config once keys are configured",
            "Use 'idea init-config' to set up your configuration",
        ],
    }


def demo_scaffold_project(pitch: str, target_dir: Path) -> None:
    """Demo implementation of project scaffolding."""
    console.print(
        Panel(
            f"[yellow]🎭 DEMO MODE[/yellow]\n"
            f"Creating minimal 'hello world' project for: {pitch}\n\n"
            f"This is a basic template. Configure scaffoldEndpoint for full features.",
            title="Demo Scaffolding",
        )
    )

    # Create basic project structure
    target_dir.mkdir(exist_ok=True)

    # Create a simple README
    readme_content = f"""# {pitch}

This is a demo project created by idea-cli in demo mode.

## Getting Started

This project was created with minimal scaffolding. To get full project
generation capabilities:

1. Configure your API keys in ~/.idea-cli/config.json
2. Set demoMode: false
3. Run idea-cli again for complete project scaffolding

## Demo Files

- README.md (this file)
- hello.py (basic Python script)

## Next Steps

1. Set up your development environment
2. Configure idea-cli with your API keys
3. Re-run with full scaffolding enabled
"""

    with open(target_dir / "README.md", "w") as f:
        f.write(readme_content)

    # Create a simple Python hello world
    python_content = f'''#!/usr/bin/env python3
"""
{pitch} - Demo Project

This is a minimal demo project created by idea-cli.
Configure your API keys for full project generation.
"""

def main():
    print("Hello from {pitch}!")
    print("This is a demo project. Configure idea-cli for full features.")

if __name__ == "__main__":
    main()
'''

    with open(target_dir / "hello.py", "w") as f:
        f.write(python_content)

    console.print(f"✅ Demo project created at: {target_dir}")
    console.print("📝 Configure API keys for full scaffolding features")


def demo_generate_plan(pitch: str, category: str = "personal") -> Plan:
    """Demo implementation of project planning."""
    console.print(
        Panel(
            f"[yellow]🎭 DEMO MODE[/yellow]\n"
            f"Generating demo plan for: {pitch}\n\n"
            f"This is a basic demo plan. Configure API keys for AI-powered planning.",
            title="Demo Planning",
        )
    )

    # Create a simple slug from the pitch
    project_slug = pitch.lower().replace(" ", "-").replace("'", "").replace('"', "")

    # Generate demo plan based on pitch keywords
    if any(
        word in pitch.lower()
        for word in ["web", "site", "app", "frontend", "react", "vue", "angular"]
    ):
        language = "node"
        package_name = None
        epics = [
            "User Interface",
            "Backend API",
            "Database",
            "Authentication",
            "Deployment",
        ]
        stories = [
            Story(
                id="story-1",
                name="Create landing page",
                description="Build main landing page with hero section",
            ),
            Story(
                id="story-2",
                name="Set up routing",
                description="Configure client-side routing",
            ),
            Story(
                id="story-3",
                name="Add user authentication",
                description="Implement login/signup functionality",
            ),
            Story(
                id="story-4",
                name="Connect to database",
                description="Set up database connection and models",
            ),
            Story(
                id="story-5",
                name="Deploy to production",
                description="Configure deployment pipeline",
            ),
        ]
        stack = ["React", "Node.js", "Express", "MongoDB", "JWT"]
    else:
        language = "python"
        package_name = project_slug.replace("-", "_")
        epics = [
            "Core Logic",
            "Data Processing",
            "Testing",
            "Documentation",
            "Deployment",
        ]
        stories = [
            Story(
                id="story-1",
                name="Set up project structure",
                description="Create Python package structure",
            ),
            Story(
                id="story-2",
                name="Implement main functionality",
                description="Build core application logic",
            ),
            Story(
                id="story-3",
                name="Add data processing",
                description="Handle input/output data processing",
            ),
            Story(
                id="story-4",
                name="Write tests",
                description="Create comprehensive test suite",
            ),
            Story(
                id="story-5",
                name="Create documentation",
                description="Write README and API documentation",
            ),
        ]
        stack = ["Python 3.12", "pytest", "Click", "SQLAlchemy", "FastAPI"]

    return Plan(
        project_slug=project_slug,
        one_liner=f"Demo project for {pitch}",
        recommended_language=language,
        category=category,
        python_package_name=package_name,
        epics=epics,
        stories=stories,
        stack_recommendations=stack,
    )


def demo_not_available(command: str) -> None:
    """Show not available message for demo mode."""
    console.print(
        Panel(
            f"[yellow]🎭 DEMO MODE[/yellow]\n\n"
            f"The '{command}' command is not available in demo mode.\n\n"
            f"To use this feature:\n"
            f"1. Configure your API keys in ~/.idea-cli/config.json\n"
            f"2. Set demoMode: false\n"
            f"3. Run the command again",
            title="Feature Not Available",
        )
    )
