"""
RunLy: A simple, powerful task runner inspired by justfile.

RunLy is a task runner that allows you to organize and run project-related tasks
using a simple configuration file format. It supports both justfile syntax and
YAML configuration files.

Example:
    Basic usage:
        $ runly test
        $ runly build --target=release
        $ runly deploy production

    List available commands:
        $ runly --list
"""

__version__ = "0.1.1"
__author__ = "RunLy Team"
__email__ = "runly@mkedjar.com"
__license__ = "MIT"

# Main classes for public API
from .commands import Command, CommandSet
from .parser import JustfileParser
from .runner import CommandRunner

# Exceptions for error handling
from .exceptions import (
    RunLyError,
    JustfileError,
    JustfileParseError,
    JustfileSyntaxError,
    JustfileNotFoundError,
    CommandError,
    CommandNotFoundError,
    CommandExecutionError,
    DependencyError,
    DependencyCycleError,
    DependencyNotFoundError,
    ArgumentError,
    VariableError,
    ConfigurationError,
)

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    # Core classes
    "Command",
    "CommandSet",
    "JustfileParser",
    "CommandRunner",
    # Exceptions
    "RunLyError",
    "JustfileError",
    "JustfileParseError",
    "JustfileSyntaxError",
    "JustfileNotFoundError",
    "CommandError",
    "CommandNotFoundError",
    "CommandExecutionError",
    "DependencyError",
    "DependencyCycleError",
    "DependencyNotFoundError",
    "ArgumentError",
    "VariableError",
    "ConfigurationError",
]