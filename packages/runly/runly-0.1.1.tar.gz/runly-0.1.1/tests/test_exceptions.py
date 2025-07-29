"""
Unit tests for RunLy exceptions.
"""

import pytest

from runly.exceptions import (
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


class TestRunLyError:
    """Test the base RunLy exception."""

    def test_basic_error(self):
        """Test basic error creation."""
        error = RunLyError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.details is None

    def test_error_with_details(self):
        """Test error with details."""
        error = RunLyError("Test error", details="Additional details")
        assert "Test error" in str(error)
        assert "Additional details" in str(error)
        assert error.details == "Additional details"


class TestJustfileError:
    """Test justfile-related exceptions."""

    def test_basic_justfile_error(self):
        """Test basic justfile error."""
        error = JustfileError("Parse failed")
        assert "Parse failed" in str(error)

    def test_justfile_error_with_filepath(self):
        """Test justfile error with filepath."""
        error = JustfileError("Parse failed", filepath="/path/to/justfile")
        assert "Parse failed" in str(error)
        assert "/path/to/justfile" in str(error)

    def test_justfile_error_with_line_number(self):
        """Test justfile error with line number."""
        error = JustfileError(
            "Parse failed", 
            filepath="/path/to/justfile", 
            line_number=42
        )
        assert "Parse failed" in str(error)
        assert "/path/to/justfile" in str(error)
        assert "line 42" in str(error)


class TestCommandError:
    """Test command-related exceptions."""

    def test_basic_command_error(self):
        """Test basic command error."""
        error = CommandError("Command failed")
        assert "Command failed" in str(error)

    def test_command_error_with_name(self):
        """Test command error with command name."""
        error = CommandError("Failed to execute", command_name="test")
        assert "Command 'test'" in str(error)
        assert "Failed to execute" in str(error)

    def test_command_execution_error(self):
        """Test command execution error with details."""
        error = CommandExecutionError(
            "Command failed",
            command_name="test",
            exit_code=1,
            stderr="Error output"
        )
        assert "Command 'test'" in str(error)
        assert "Exit code: 1" in str(error)
        assert "Error output" in str(error)


class TestDependencyError:
    """Test dependency-related exceptions."""

    def test_dependency_cycle_error(self):
        """Test dependency cycle detection."""
        cycle = ["cmd1", "cmd2", "cmd3", "cmd1"]
        error = DependencyCycleError(cycle)
        assert "cmd1 -> cmd2 -> cmd3 -> cmd1" in str(error)
        assert error.cycle_path == cycle

    def test_dependency_not_found_error(self):
        """Test dependency not found error."""
        error = DependencyNotFoundError(
            "Dependency not found",
            command_name="test"
        )
        assert "Command 'test'" in str(error)
        assert "Dependency not found" in str(error)


class TestArgumentError:
    """Test argument-related exceptions."""

    def test_argument_error(self):
        """Test argument mismatch error."""
        error = ArgumentError(
            "Wrong number of arguments",
            command_name="test",
            expected_args=2,
            provided_args=1
        )
        assert "Command 'test'" in str(error)
        assert "Expected 2 arguments, got 1" in str(error)


class TestVariableError:
    """Test variable-related exceptions."""

    def test_variable_error(self):
        """Test variable expansion error."""
        error = VariableError("Undefined variable", variable_name="missing_var")
        assert "Variable 'missing_var'" in str(error)
        assert "Undefined variable" in str(error)
