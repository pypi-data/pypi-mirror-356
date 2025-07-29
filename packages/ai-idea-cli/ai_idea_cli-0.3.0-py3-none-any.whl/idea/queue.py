import json
from pathlib import Path

from idea.models import Plan, QueueItem


def create_queue(plan: Plan, target_dir: Path) -> None:
    """Create queue.json from plan stories."""
    idea_dir = target_dir / ".idea"
    idea_dir.mkdir(exist_ok=True)

    queue_items = []
    for story in plan.stories:
        queue_items.append(
            QueueItem(
                id=story.id, prompt=story.description, status="pending"
            ).model_dump()
        )

    queue_file = idea_dir / "queue.json"
    with open(queue_file, "w") as f:
        json.dump(queue_items, f, indent=2)


def load_queue(project_dir: Path) -> list[QueueItem]:
    """Load queue from project directory."""
    queue_file = project_dir / ".idea" / "queue.json"
    if not queue_file.exists():
        return []

    with open(queue_file) as f:
        data = json.load(f)

    return [QueueItem(**item) for item in data]


def save_queue(queue: list[QueueItem], project_dir: Path) -> None:
    """Save queue to project directory."""
    queue_file = project_dir / ".idea" / "queue.json"
    with open(queue_file, "w") as f:
        json.dump([item.model_dump() for item in queue], f, indent=2)


def get_next_pending(project_dir: Path) -> QueueItem | None:
    """Get the next pending queue item."""
    queue = load_queue(project_dir)
    for item in queue:
        if item.status == "pending":
            return item
    return None


def update_status(project_dir: Path, story_id: str, status: str) -> None:
    """Update the status of a queue item."""
    queue = load_queue(project_dir)
    for item in queue:
        if item.id == story_id:
            item.status = status
            break
    save_queue(queue, project_dir)
