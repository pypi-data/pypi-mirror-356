"""
Command runner for RunLy.
"""

import os
import re
import subprocess
from typing import List, Set, Optional

from .commands import CommandSet
from .exceptions import (
    ArgumentError,
    CommandExecutionError,
    CommandNotFoundError,
    DependencyCycleError,
    DependencyNotFoundError,
)
from .utils import expand_variables


class CommandRunner:
    """Runs commands from a CommandSet."""

    def __init__(
        self,
        command_set: CommandSet,
        dry_run: bool = False,
        quiet: bool = False,
        verbose: bool = False,
    ):
        """Initialize the runner with a command set."""
        self.command_set = command_set
        self.dry_run = dry_run
        self.quiet = quiet
        self.verbose = verbose
        self._visited: Set[str] = set()
        self._in_progress: Set[str] = set()

    def run(self, command_name: str, args: Optional[List[str]] = None) -> int:
        """Run a command by name with optional arguments."""
        if args is None:
            args = []

        command = self.command_set.get_command(command_name)
        if not command:
            raise CommandNotFoundError(f"Command '{command_name}' not found")

        try:
            # Check for dependencies and run them first
            self._run_dependencies(command_name)

            # Prepare arguments
            if len(args) != len(command.args):
                raise ArgumentError(
                    "Incorrect number of arguments",
                    command_name=command_name,
                    expected_args=len(command.args),
                    provided_args=len(args),
                )

            arg_dict = dict(zip(command.args, args))

            # Merge with variables
            variables = {**self.command_set.variables, **arg_dict}

            # Expand variables in script
            script = expand_variables(command.script, variables)

            if not self.quiet:
                print(f"Running command: {command_name}")

            if self.dry_run:
                print(f"Would execute:\n{script}")
                return 0

            # Execute the script
            return self._execute_script(script, command_name)

        except (
            DependencyCycleError,
            CommandNotFoundError,
            ArgumentError,
            CommandExecutionError,
        ):
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            raise CommandExecutionError(
                f"Unexpected error: {e}", command_name=command_name
            ) from e

    def _run_dependencies(self, command_name: str, path: Optional[List[str]] = None) -> None:
        """Run dependencies for a command, checking for cycles."""
        if path is None:
            path = []

        if command_name in self._visited:
            return

        if command_name in self._in_progress:
            cycle_path = path + [command_name]
            raise DependencyCycleError(cycle_path)

        command = self.command_set.get_command(command_name)
        if not command:
            raise DependencyNotFoundError(
                f"Dependency '{command_name}' not found", command_name=command_name
            )

        self._in_progress.add(command_name)

        # Run each dependency
        for dep in command.dependencies:
            if dep not in self._visited:
                self._run_dependencies(dep, path + [command_name])

        self._in_progress.remove(command_name)
        self._visited.add(command_name)

        # Run the actual dependency command (only if it's not the original command)
        if path:  # Only run if it's a dependency of another command
            if not self.quiet:
                print(f"Running dependency: {command_name}")
            # For dependencies, provide empty arguments even if the command expects arguments
            self._run_dependency_command(command_name)

    def _run_dependency_command(self, command_name: str) -> int:
        """Run a dependency command, providing default arguments if needed."""
        command = self.command_set.get_command(command_name)
        if not command:
            raise CommandNotFoundError(f"Command '{command_name}' not found")

        # For dependencies, provide empty string arguments for all required args
        default_args = [""] * len(command.args)

        try:
            # Prepare arguments
            arg_dict = dict(zip(command.args, default_args))

            # Merge with variables
            variables = {**self.command_set.variables, **arg_dict}

            # Expand variables in script
            script = expand_variables(command.script, variables)

            if not self.quiet:
                print(f"Running command: {command_name}")

            if self.dry_run:
                print(f"Would execute:\n{script}")
                return 0

            # Execute the script
            return self._execute_script(script, command_name)

        except (
            DependencyCycleError,
            CommandNotFoundError,
            ArgumentError,
            CommandExecutionError,
        ):
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            # Convert any other exception to our custom exception
            raise CommandExecutionError(
                f"Error running command: {e}", command_name=command_name
            ) from e

    def _execute_script(self, script: str, command_name: str) -> int:
        """Execute a script using the system shell."""
        try:
            # Split the script into lines
            lines = [line.strip() for line in script.splitlines() if line.strip()]

            for line in lines:
                if self.verbose or not self.quiet:
                    print(f"$ {line}")

                # Replace `just` commands with `runly` commands
                line = re.sub(r'(?:^|\s)just(\s+)', r'runly\1', line)

                try:
                    proc = subprocess.run(
                        line,
                        shell=True,
                        cwd=os.getcwd(),
                        text=True,
                        capture_output=self.quiet and not self.verbose,
                        check=False,
                    )

                    if proc.returncode != 0:
                        error_msg = f"Command failed with exit code {proc.returncode}"
                        stderr = getattr(proc, "stderr", "") or ""
                        stdout = getattr(proc, "stdout", "") or ""

                        raise CommandExecutionError(
                            error_msg,
                            command_name=command_name,
                            exit_code=proc.returncode,
                            stdout=stdout,
                            stderr=stderr,
                        )

                except subprocess.SubprocessError as e:
                    raise CommandExecutionError(
                        f"Failed to execute command: {e}",
                        command_name=command_name,
                    ) from e

            return 0

        except CommandExecutionError:
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            raise CommandExecutionError(
                f"Error executing script: {e}", command_name=command_name
            ) from e