"""
CLI module for idea-cli: AI-Driven SDLC Engine

This module provides the main command-line interface for the idea-cli tool,
offering comprehensive demo mode functionality with optional upgrade to full
LLM-powered features.

Key Features:
- Global error handling with automated issue reporting
- Demo mode for immediate usage without API keys
- Multi-provider LLM support (Anthropic Claude, OpenAI GPT)
- Progressive enhancement from demo to full mode
- Configuration management with JSON schema validation

Commands:
- init-config: Initialize user configuration
- validate: Validate project ideas
- new: Create scaffolded projects with AI planning
- run-queue: Execute implementation queues
- queue-status: Monitor queue progress
- experience: Collect and summarize development experiences
- upgrade: Apply template updates and guard-rails
- report-issue: Automated bug reporting
"""

import asyncio
import functools
import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from idea.clients.experience import ExperienceManager

# Import HTTP clients for backend services
from idea.clients.planner import generate_plan
from idea.clients.queue import QueueRunner
from idea.config import (
    ConfigError,
    check_api_key,
    init_user_config,
    is_demo_mode,
    load_config,
)
from idea.demo import demo_not_available, demo_scaffold_project, demo_validate_idea
from idea.issue_reporter import report_issue
from idea.models import Plan
from idea.queue import create_queue, load_queue
from idea.router import route_idea
from idea.scaffold.node import scaffold_node
from idea.scaffold.python import scaffold_python
from idea.validator import ValidationError, display_validation_result, validate_idea


# Local utility functions
def save_plan(plan: Plan, target_dir: Path) -> None:
    """Save the plan to .idea/plan.json."""
    import json

    idea_dir = target_dir / ".idea"
    idea_dir.mkdir(exist_ok=True)

    plan_file = idea_dir / "plan.json"
    with open(plan_file, "w") as f:
        json.dump(plan.model_dump(), f, indent=2)


app = typer.Typer(help="AI-powered meta-scaffolder and SDLC engine")
console = Console()


def global_error_handler(func):
    """Decorator to handle global errors and offer issue reporting."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            console.print(f"❌ Unexpected error: {e}")

            report_option = typer.confirm(
                "Would you like to report this issue?", default=False
            )
            if report_option:
                report_issue(
                    description=f"Error in {func.__name__}",
                    project_dir=Path.cwd(),
                    error_details=f"Error: {str(e)}\nFunction: {func.__name__}",
                )

            raise typer.Exit(1) from None

    return wrapper


@app.command()
def init_config():
    """Initialize user configuration file."""
    try:
        config_path = init_user_config()
        console.print(f"✅ Configuration initialized at: {config_path}")
        console.print("\n📝 Next steps:")
        console.print("1. Edit the configuration file to add your API keys")
        console.print("2. Set demoMode: false to enable full features")
        console.print("3. Run 'idea validate --help' to see available commands")
    except Exception as e:
        console.print(f"❌ Failed to initialize config: {e}")
        raise typer.Exit(1) from e


@app.command()
@global_error_handler
def validate(
    pitch: str = typer.Argument(..., help="Your project idea description"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be validated"
    ),
):
    """Validate a project idea using the configured validator."""

    if is_demo_mode():
        result = demo_validate_idea(pitch)
        if not dry_run:
            display_validation_result(result)
        return

    try:
        config = load_config()
        check_api_key(config, "validator")

        result = asyncio.run(validate_idea(pitch, dry_run))
        if not dry_run:
            display_validation_result(result)
    except ConfigError as e:
        console.print(f"❌ Configuration error: {e}")
        console.print("💡 Run 'idea init-config' to set up configuration")
        raise typer.Exit(1) from e
    except ValidationError as e:
        console.print(f"❌ {e}")
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"❌ Unexpected error: {e}")
        raise typer.Exit(1) from e


@app.command()
@global_error_handler
def new(
    pitch: str = typer.Argument(..., help="Your project idea description"),
    output_dir: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output directory"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be created"),
    skip_validation: bool = typer.Option(
        False, "--skip-validation", help="Skip idea validation"
    ),
    demo: bool = typer.Option(False, "--demo", help="Force demo mode"),
):
    """Create a new scaffolded project with enhanced planning and queue seeding."""

    if output_dir is None:
        output_dir = Path.cwd()

    console.print(Panel(f"💡 Idea: {pitch}", title="Enhanced Scaffolding"))

    # Check if we should use simple demo mode (--demo flag)
    if demo:
        # Simple demo mode scaffolding
        target_dir = output_dir / pitch.lower().replace(" ", "-")
        if not dry_run:
            demo_scaffold_project(pitch, target_dir)
        else:
            console.print(
                f"🔍 [bold yellow]DRY RUN (DEMO)[/bold yellow] - Would create demo project at: {target_dir}"
            )
        return

    # Full mode - check configuration (demo mode can proceed without real API keys)
    try:
        config = load_config()
        if not is_demo_mode():
            check_api_key(config, "validator")
            check_api_key(config, "llm")
    except ConfigError as e:
        console.print(f"❌ Configuration error: {e}")
        console.print("💡 Use --demo flag for demo mode or configure API keys")
        raise typer.Exit(1) from e

    # Step 1: Validate idea
    if not skip_validation:
        try:
            console.print("🔍 Validating idea...")
            result = asyncio.run(validate_idea(pitch, dry_run))
            if not dry_run:
                display_validation_result(result)
        except ValidationError as e:
            console.print(f"❌ {e}")
            raise typer.Exit(1) from e

    # Step 2: Generate plan
    console.print("🎯 Generating enhanced plan...")
    category = route_idea(pitch)

    try:
        plan = asyncio.run(generate_plan(pitch, category))
    except Exception as e:
        console.print(f"❌ Planning failed: {e}")
        raise typer.Exit(1) from e

    console.print(f"📍 Category: {plan.category}")
    console.print(f"🎯 Language: {plan.recommended_language}")
    console.print(f"📁 Slug: {plan.project_slug}")
    console.print(f"📋 Epics: {len(plan.epics)}")
    console.print(f"📝 Stories: {len(plan.stories)}")

    if dry_run:
        _show_plan_preview(plan, output_dir)
        return

    # Step 3: Create project structure
    target_dir = output_dir / plan.project_slug
    target_dir.mkdir(exist_ok=True)

    # Step 4: Save plan and create queue
    console.print("💾 Saving plan and creating queue...")
    save_plan(plan, target_dir)
    create_queue(plan, target_dir)

    # Step 5: Scaffold project
    console.print("🏗️ Scaffolding project...")
    if plan.recommended_language == "python":
        scaffold_python(plan, target_dir)
    else:
        scaffold_node(plan, target_dir)

    console.print(f"✅ Project created at: {target_dir}")
    console.print(f"🚀 Next: cd {plan.project_slug} && idea run-queue")


@app.command("run-queue")
@global_error_handler
def run_queue(
    project_dir: Optional[Path] = typer.Option(
        None, "--project-dir", help="Project directory"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be executed"
    ),
):
    """Execute the micro-prompt queue to implement stories."""

    if is_demo_mode():
        demo_not_available("run-queue")
        return

    if project_dir is None:
        project_dir = Path.cwd()

    try:
        config = load_config()
        check_api_key(config, "llm")
    except ConfigError as e:
        console.print(f"❌ Configuration error: {e}")
        raise typer.Exit(1) from e

    runner = QueueRunner(project_dir)

    try:
        asyncio.run(runner.run_queue(dry_run=dry_run))
    except Exception as e:
        console.print(f"❌ Queue execution failed: {e}")
        raise typer.Exit(1) from e


@app.command()
@global_error_handler
def queue_status(
    project_dir: Optional[Path] = typer.Option(
        None, "--project-dir", help="Project directory"
    ),
):
    """Show the current status of the micro-prompt queue."""

    if is_demo_mode():
        demo_not_available("queue-status")
        return

    if project_dir is None:
        project_dir = Path.cwd()

    queue = load_queue(project_dir)

    if not queue:
        console.print("No queue found in project directory")
        return

    # Count by status
    status_counts = {}
    for item in queue:
        status_counts[item.status] = status_counts.get(item.status, 0) + 1

    table = Table(title="Queue Status")
    table.add_column("Status", style="bold")
    table.add_column("Count", style="cyan")

    for status, count in status_counts.items():
        table.add_row(status.title(), str(count))

    console.print(table)


# Experience management commands
experience_app = typer.Typer(help="Experience collection and learning commands")
app.add_typer(experience_app, name="experience")


@experience_app.command("collect")
@global_error_handler
def experience_collect(
    context: str = typer.Argument(..., help="Context of the failure"),
    error: str = typer.Argument(..., help="Error message or description"),
    project_dir: Optional[Path] = typer.Option(
        None, "--project-dir", help="Project directory"
    ),
    command: str = typer.Option("", "--command", help="Command that failed"),
):
    """Collect a development experience/failure for learning."""

    if is_demo_mode():
        demo_not_available("experience collect")
        return

    if project_dir is None:
        project_dir = Path.cwd()

    manager = ExperienceManager(project_dir)
    log_id = manager.collect_failure(context, error, command)

    console.print(f"📝 Collected experience: {log_id}")


@experience_app.command("summarise")
@global_error_handler
def experience_summarise(
    hours: int = typer.Option(24, "--hours", help="Hours to look back for failures"),
    project_dir: Optional[Path] = typer.Option(
        None, "--project-dir", help="Project directory"
    ),
):
    """Summarize recent failures into actionable lessons."""

    if is_demo_mode():
        demo_not_available("experience summarise")
        return

    if project_dir is None:
        project_dir = Path.cwd()

    try:
        config = load_config()
        check_api_key(config, "llm")
    except ConfigError as e:
        console.print(f"❌ Configuration error: {e}")
        raise typer.Exit(1) from e

    manager = ExperienceManager(project_dir)

    try:
        lessons = asyncio.run(manager.summarise_failures(hours))
        console.print(f"✅ Generated {len(lessons)} lessons from recent failures")

        for lesson in lessons:
            console.print(f"📚 {lesson.title} ({lesson.severity})")

    except Exception as e:
        console.print(f"❌ Summarization failed: {e}")
        raise typer.Exit(1) from e


@app.command()
@global_error_handler
def upgrade(
    project_dir: Optional[Path] = typer.Option(
        None, "--project-dir", help="Project directory"
    ),
):
    """Upgrade project with latest templates and guard-rails from lessons."""

    if is_demo_mode():
        demo_not_available("upgrade")
        return

    if project_dir is None:
        project_dir = Path.cwd()

    try:
        config = load_config()
        template_version = config["scaffold"]["templateVersion"]

        console.print(f"🔄 Upgrading project with template version: {template_version}")

        # Run copier update
        result = subprocess.run(
            ["copier", "-f", "update", "--vcs-ref", template_version], cwd=project_dir
        )

        if result.returncode != 0:
            console.print("❌ Copier update failed")
            raise typer.Exit(1) from None

        console.print("✅ Project upgraded successfully")
    except ConfigError as e:
        console.print(f"❌ Configuration error: {e}")
        raise typer.Exit(1) from e


@app.command("report-issue")
def report_issue_command(
    description: str = typer.Argument(..., help="Brief description of the issue"),
    project_dir: Optional[Path] = typer.Option(
        None, "--project-dir", help="Project directory"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be reported without creating issue"
    ),
):
    """Report an issue with idea-cli."""

    if project_dir is None:
        project_dir = Path.cwd()

    report_issue(description=description, project_dir=project_dir, dry_run=dry_run)


def _show_plan_preview(plan: Plan, output_dir: Path):
    """Show what would be created in dry-run mode."""
    console.print(
        "🔍 [bold yellow]DRY RUN MODE[/bold yellow] - No files will be created"
    )
    console.print(f"Would create project in: {output_dir / plan.project_slug}")

    table = Table(title="Generated Plan")
    table.add_column("Epic", style="cyan")
    table.add_column("Stories", style="green")

    for i, epic in enumerate(plan.epics):
        epic_stories = [s.name for s in plan.stories if i < len(plan.stories)]
        table.add_row(epic, "\n".join(epic_stories[:3]))

    console.print(table)


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
