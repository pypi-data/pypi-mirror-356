"""
Command-line interface for RunLy.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from . import __version__
from .exceptions import RunLyError, JustfileNotFoundError, CommandExecutionError
from .parser import JustfileParser
from .runner import CommandRunner


def find_justfile() -> Optional[Path]:
    """Find the justfile in the current directory or parent directories."""
    current_dir = Path.cwd()

    # Check common filenames
    justfile_names = ["justfile", "Justfile", ".justfile", "runly.yaml", "runly.yml"]

    while True:
        for name in justfile_names:
            path = current_dir / name
            if path.is_file():
                return path

        # Go up one directory
        parent_dir = current_dir.parent
        if parent_dir == current_dir:  # Reached root directory
            return None
        current_dir = parent_dir


def display_commands_table(command_set) -> None:
    """Display available commands in a formatted table."""
    print("Available commands:")

    max_name_len = max((len(cmd.name) for cmd in command_set.commands), default=0)
    max_args_len = max(
        (len(", ".join(cmd.args)) for cmd in command_set.commands), default=0
    )

    for cmd in command_set.commands:
        args_text = ", ".join(cmd.args) if cmd.args else ""
        description = cmd.description or ""

        # Mark default command
        command_name = cmd.name
        if cmd.name == command_set.default_command:
            command_name = f"{cmd.name} (default)"

        print(
            f"  {command_name.ljust(max_name_len + 10)}  "
            f"{args_text.ljust(max_args_len)}  {description}"
        )


def parse_arguments(args: List[str]) -> Tuple[argparse.Namespace, List[str]]:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="RunLy: A Python task runner inspired by justfile.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"RunLy {__version__}"
    )

    parser.add_argument(
        "-f",
        "--file",
        help="Path to the justfile (default: search for justfile in current and parent directories)",
    )

    parser.add_argument(
        "-l", "--list", action="store_true", help="List available commands"
    )

    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress output"
    )

    parser.add_argument(
        "-d", "--dry-run", action="store_true", help="Print commands but don't run them"
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    # Parse known args to handle command and its arguments separately
    return parser.parse_known_args(args)


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    try:
        if argv is None:
            argv = sys.argv[1:]

        args, remaining_args = parse_arguments(argv)

        # Find justfile
        justfile_path = None
        if args.file:
            justfile_path = Path(args.file)
            if not justfile_path.is_file():
                raise JustfileNotFoundError(f"Justfile not found at '{justfile_path}'")
        else:
            justfile_path = find_justfile()
            if not justfile_path:
                raise JustfileNotFoundError("No justfile found")

        # Parse justfile
        try:
            parser = JustfileParser(str(justfile_path))
            command_set = parser.parse()
        except Exception as e:
            raise RunLyError(f"Error parsing justfile: {e}") from e

        # List commands and exit if requested
        if args.list:
            display_commands_table(command_set)
            return 0

        # Extract command name and arguments
        if not remaining_args:
            # If no command specified, run the default command if available
            if command_set.default_command:
                cmd_name = command_set.default_command
                cmd_args = []
            else:
                # No command specified and no default command
                print("Error: No command specified", file=sys.stderr)
                print("Use --list to see available commands", file=sys.stderr)
                return 1
        else:
            cmd_name = remaining_args[0]
            cmd_args = remaining_args[1:]

        # Run the command
        runner = CommandRunner(
            command_set,
            dry_run=args.dry_run,
            quiet=args.quiet,
            verbose=getattr(args, "verbose", False),
        )
        return runner.run(cmd_name, cmd_args)

    except CommandExecutionError as e:
        print(f"Error: {e}", file=sys.stderr)
        # Return the actual exit code from the failed command
        return e.exit_code if e.exit_code is not None else 1
    except RunLyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())