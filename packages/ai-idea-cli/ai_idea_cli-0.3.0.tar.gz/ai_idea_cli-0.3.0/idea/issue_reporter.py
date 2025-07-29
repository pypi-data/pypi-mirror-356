"""Issue reporting functionality for idea-cli."""

import json
import platform
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from idea.config import ConfigError, load_config

console = Console()


def get_cli_version() -> str:
    """Get the CLI version."""
    try:
        import idea

        return getattr(idea, "__version__", "unknown")
    except ImportError:
        return "unknown"


def get_system_info() -> dict[str, str]:
    """Get system information."""
    return {
        "os": platform.system(),
        "version": platform.version(),
        "architecture": platform.machine(),
        "python": sys.version.split()[0],
    }


def get_config_summary() -> dict:
    """Get non-sensitive configuration summary."""
    try:
        config = load_config()
        # Remove sensitive information
        safe_config = {
            "demoMode": config.get("demoMode", False),
            "retentionDays": config.get("retentionDays", 30),
            "models": {
                "plan": config.get("models", {}).get("plan", "unknown"),
                "queue": config.get("models", {}).get("queue", "unknown"),
                "summarise": config.get("models", {}).get("summarise", "unknown"),
            },
            "validator": {
                "minScore": config.get("validator", {}).get("minScore", 0.7),
                "acceptField": config.get("validator", {}).get(
                    "acceptField", "accepted"
                ),
                "scoreField": config.get("validator", {}).get("scoreField", "score"),
            },
        }
        return safe_config
    except ConfigError:
        return {"error": "Configuration could not be loaded"}


def collect_logs(project_dir: Path) -> list[Path]:
    """Collect available log files."""
    logs_dir = project_dir / ".idea" / "_logs"
    if not logs_dir.exists():
        return []

    log_files = []
    for pattern in ["*.log", "*.json"]:
        log_files.extend(logs_dir.glob(pattern))

    return sorted(log_files)


def check_gh_cli() -> bool:
    """Check if GitHub CLI is available and authenticated."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"], capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def create_issue_content(
    description: str, project_dir: Path, error_details: str = ""
) -> str:
    """Create GitHub issue content."""
    cli_version = get_cli_version()
    system_info = get_system_info()
    config_summary = get_config_summary()
    log_files = collect_logs(project_dir)

    content = f"""## Description
{description}

{error_details}

## Environment
- idea-cli version: {cli_version}
- OS: {system_info["os"]} {system_info["version"]}
- Architecture: {system_info["architecture"]}
- Python: {system_info["python"]}

## Configuration
```json
{json.dumps(config_summary, indent=2)}
```

## Log Files
"""

    if log_files:
        content += f"Found {len(log_files)} log files in .idea/_logs/:\n"
        for log_file in log_files[-5:]:  # Last 5 files
            content += f"- {log_file.name}\n"

        content += "\n### Recent Log Contents\n"
        for log_file in log_files[-2:]:  # Last 2 files
            try:
                with open(log_file) as f:
                    log_content = f.read()
                    if len(log_content) > 1000:
                        log_content = log_content[-1000:] + "\n... (truncated)"
                content += f"\n#### {log_file.name}\n```\n{log_content}\n```\n"
            except Exception:
                content += f"\n#### {log_file.name}\n```\nError reading log file\n```\n"
    else:
        content += "No log files found in .idea/_logs/\n"

    content += """
## Steps to Reproduce
1.
2.
3.

## Expected Behavior


## Actual Behavior

"""

    return content


def report_issue(
    description: str, project_dir: Path, error_details: str = "", dry_run: bool = False
) -> None:
    """Report an issue via GitHub CLI or provide manual instructions."""
    issue_content = create_issue_content(description, project_dir, error_details)
    title = f"idea-cli bug report: {description[:50]}..."

    if dry_run:
        console.print(
            Panel(
                f"[yellow]DRY RUN MODE[/yellow]\n\n"
                f"Would create GitHub issue with:\n"
                f"Title: {title}\n\n"
                f"Content preview:\n{issue_content[:300]}...",
                title="Issue Report Preview",
            )
        )
        return

    if check_gh_cli():
        try:
            # Create temporary file for issue content
            import tempfile

            with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
                f.write(issue_content)
                temp_file = f.name

            cmd = ["gh", "issue", "create", "--title", title, "--body-file", temp_file]

            console.print("🚀 Creating GitHub issue...")
            result = subprocess.run(cmd, capture_output=True, text=True)

            # Clean up temp file
            Path(temp_file).unlink()

            if result.returncode == 0:
                issue_url = result.stdout.strip()
                console.print(f"✅ Issue created: {issue_url}")
            else:
                console.print(f"❌ Failed to create issue: {result.stderr}")
                _show_manual_instructions(title, issue_content)

        except Exception as e:
            console.print(f"❌ Error creating issue: {e}")
            _show_manual_instructions(title, issue_content)
    else:
        _show_manual_instructions(title, issue_content)


def _show_manual_instructions(title: str, content: str) -> None:
    """Show manual issue creation instructions."""
    console.print(
        Panel(
            f"[yellow]GitHub CLI not available or not authenticated[/yellow]\n\n"
            f"Please manually create an issue at:\n"
            f"https://github.com/<<<FILL_ME_YOUR_REPO>>>/issues/new\n\n"
            f"Title: {title}\n\n"
            f"Copy the content below:\n",
            title="Manual Issue Creation",
        )
    )

    console.print("--- Issue Content (copy below) ---")
    console.print(content)
    console.print("--- End Issue Content ---")
