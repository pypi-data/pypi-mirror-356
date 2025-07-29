"""Node.js project scaffolding using Copier."""

from pathlib import Path

from copier import run_copy

from ..models import Plan


def scaffold_node(plan: Plan, target_dir: Path) -> None:
    """
    Scaffold a Node.js project using Copier templates.

    Args:
        plan: The project plan
        target_dir: Target directory for the scaffolded project
    """
    template_path = Path(__file__).parent.parent.parent / "templates" / "node"

    # Prepare template data
    template_data = {
        "project_name": plan.project_slug,
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
