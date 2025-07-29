"""
Custom exceptions for RunLy.
"""

from typing import List, Optional


class RunLyError(Exception):
    """Base exception for all RunLy errors."""

    def __init__(self, message: str, details: Optional[str] = None) -> None:
        self.message = message
        self.details = details
        super().__init__(message)

    def __str__(self) -> str:
        if self.details:
            return f"{self.message}\nDetails: {self.details}"
        return self.message


class JustfileError(RunLyError):
    """Base exception for justfile-related errors."""

    def __init__(
        self,
        message: str,
        filepath: Optional[str] = None,
        line_number: Optional[int] = None,
        details: Optional[str] = None,
    ) -> None:
        self.filepath = filepath
        self.line_number = line_number

        location = ""
        if filepath:
            location = f" in {filepath}"
            if line_number:
                location += f" at line {line_number}"

        super().__init__(f"{message}{location}", details)


class JustfileParseError(JustfileError):
    """Exception raised when parsing a justfile fails."""
    pass


class JustfileSyntaxError(JustfileError):
    """Exception raised when justfile has syntax errors."""
    pass


class JustfileNotFoundError(JustfileError):
    """Exception raised when justfile cannot be found."""
    pass


class CommandError(RunLyError):
    """Base exception for command-related errors."""

    def __init__(
        self,
        message: str,
        command_name: Optional[str] = None,
        details: Optional[str] = None,
    ) -> None:
        self.command_name = command_name

        if command_name:
            message = f"Command '{command_name}': {message}"

        super().__init__(message, details)


class CommandNotFoundError(CommandError):
    """Exception raised when a command is not found."""
    pass


class CommandExecutionError(CommandError):
    """Exception raised when command execution fails."""

    def __init__(
        self,
        message: str,
        command_name: Optional[str] = None,
        exit_code: Optional[int] = None,
        stdout: Optional[str] = None,
        stderr: Optional[str] = None,
    ) -> None:
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr

        details = []
        if exit_code is not None:
            details.append(f"Exit code: {exit_code}")
        if stderr:
            details.append(f"Error output: {stderr}")
        if stdout and not stderr:  # Only show stdout if no stderr
            details.append(f"Output: {stdout}")

        super().__init__(message, command_name, "\n".join(details) if details else None)


class DependencyError(CommandError):
    """Base exception for dependency-related errors."""
    pass


class DependencyCycleError(DependencyError):
    """Exception raised when a dependency cycle is detected."""

    def __init__(self, cycle_path: List[str]) -> None:
        self.cycle_path = cycle_path
        cycle_str = " -> ".join(cycle_path)
        super().__init__(
            f"Dependency cycle detected: {cycle_str}",
            details=f"Commands involved: {', '.join(set(cycle_path))}"
        )


class DependencyNotFoundError(DependencyError):
    """Exception raised when a command dependency is not found."""
    pass


class ArgumentError(CommandError):
    """Exception raised when command arguments are invalid."""

    def __init__(
        self,
        message: str,
        command_name: Optional[str] = None,
        expected_args: Optional[int] = None,
        provided_args: Optional[int] = None,
    ) -> None:
        self.expected_args = expected_args
        self.provided_args = provided_args

        details = None
        if expected_args is not None and provided_args is not None:
            details = f"Expected {expected_args} arguments, got {provided_args}"

        super().__init__(message, command_name, details)


class VariableError(RunLyError):
    """Exception raised when variable expansion fails."""

    def __init__(self, message: str, variable_name: Optional[str] = None) -> None:
        self.variable_name = variable_name

        if variable_name:
            message = f"Variable '{variable_name}': {message}"

        super().__init__(message)


class ConfigurationError(RunLyError):
    """Exception raised when configuration is invalid."""
    pass
