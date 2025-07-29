from typing import Optional

from pydantic import BaseModel


class Story(BaseModel):
    id: str
    name: str
    description: str


class Plan(BaseModel):
    project_slug: str
    one_liner: str
    recommended_language: str
    category: str
    python_package_name: Optional[str]
    epics: list[str]
    stories: list[Story]
    stack_recommendations: list[str]


class QueueItem(BaseModel):
    id: str
    prompt: str
    status: str  # "pending", "testing", "implementing", "done", "failed"


class Lesson(BaseModel):
    id: str
    title: str
    description: str
    tags: list[str]
    severity: str
    pattern: str
    solution: str
