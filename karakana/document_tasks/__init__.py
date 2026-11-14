"""Explicit local document-task preparation. No checking or execution is implicit."""

VERSION = "0.2.0"


def prepare_task(root, request_path, output=None):
    """Prepare and save a new local prompt/result bundle; return its typed result."""
    from .prepare import prepare_task as prepare

    return prepare(root, request_path, output)


def check_task(root, request_path, output=None):
    """Check explicit content and save a new raw report/result bundle."""
    from .assessment import check_task as check

    return check(root, request_path, output)


def verify_task(root, request_path, bundle, output=None):
    """Recompute a saved assessment and its independent task provenance."""
    from .verify import verify_task as verify

    return verify(root, request_path, bundle, output)
