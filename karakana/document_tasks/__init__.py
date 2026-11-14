"""Explicit local document-task preparation. No checking or execution is implicit."""

VERSION = "0.1.0"


def prepare_task(root, request_path, output=None):
    """Prepare and save a new local prompt/result bundle; return its typed result."""
    from .prepare import prepare_task as prepare

    return prepare(root, request_path, output)
