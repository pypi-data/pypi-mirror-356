"""Router module for classifying ideas into personal or product categories."""

from typing import Literal


def route_idea(pitch: str) -> Literal["personal", "product"]:
    """
    Route an idea to personal or product category based on keywords.

    Args:
        pitch: The idea description

    Returns:
        "personal" or "product" based on keyword classification
    """
    pitch_lower = pitch.lower()

    # Simple keyword-based routing
    product_keywords = [
        "saas",
        "business",
        "startup",
        "revenue",
        "customer",
        "user",
        "market",
        "scale",
        "enterprise",
        "commercial",
        "sell",
        "profit",
        "monetize",
    ]

    personal_keywords = [
        "my",
        "me",
        "personal",
        "hobby",
        "learn",
        "practice",
        "experiment",
        "fun",
        "quick",
        "simple",
        "tool",
        "utility",
        "script",
    ]

    product_score = sum(1 for keyword in product_keywords if keyword in pitch_lower)
    personal_score = sum(1 for keyword in personal_keywords if keyword in pitch_lower)

    # Default to personal if no clear indication
    return "product" if product_score > personal_score else "personal"
