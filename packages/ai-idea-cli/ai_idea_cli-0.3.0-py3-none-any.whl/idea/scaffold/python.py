"""Python project scaffolding using Copier."""

from pathlib import Path

from copier import run_copy

from ..models import Plan


def scaffold_python(plan: Plan, target_dir: Path) -> None:
    """
    Scaffold a Python project using Copier templates.

    Args:
        plan: The project plan
        target_dir: Target directory for the scaffolded project
    """
    template_path = Path(__file__).parent.parent.parent / "templates" / "python"

    # Prepare template data
    template_data = {
        "project_name": plan.project_slug,
        "python_package_name": plan.python_package_name,
        "one_liner": plan.one_liner,
        "category": plan.category,
        "language": plan.recommended_language,
    }

    # Run Copier
    run_copy(
        src_path=str(template_path),
        dst_path=str(target_dir),
        data=template_data,
        quiet=True,
    )
