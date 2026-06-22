"""Release metadata collection."""

from __future__ import annotations

import importlib.metadata
import platform

from karakana import __version__


def package_version() -> str:
    try:
        return importlib.metadata.version("karakana")
    except importlib.metadata.PackageNotFoundError:
        return __version__


def release_status() -> str:
    return "in-progress"


def version_summary() -> dict[str, str]:
    return {
        "version": package_version(),
        "package": "karakana",
        "python": platform.python_version(),
        "status": release_status(),
    }
