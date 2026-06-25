"""Compatibility wrapper for Karakana model routing."""

from __future__ import annotations

from karakana.models.router import DEFAULT_MODEL_ROUTING as ROUTES

DEFAULT_MODEL_ROUTING = {task_type: route["model"] for task_type, route in ROUTES.items()}


def select_model(task_type: str) -> str:
    """Return the configured model name for a task type."""
    return DEFAULT_MODEL_ROUTING.get(task_type, "mock-model")
