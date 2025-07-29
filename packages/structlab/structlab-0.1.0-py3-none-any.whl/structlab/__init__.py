"""Structlab - A CLI tool to generate folder structures and files."""

import importlib.metadata
from .core.scan_struct import save_structure
from .utils.cli_helper import cli_help

__version__ = importlib.metadata.version("structlab")


def get_version():
    """Returns the package version."""
    return __version__


__all__ = [
    "generate_from_layout",
    "save_structure",
    "create_project_structure",
    "cli_help",
    "get_version",
    "__version__",
]
