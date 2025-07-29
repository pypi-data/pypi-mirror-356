"""
Commands and command sets for RunLy.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class Command:
    """Represents a command in a justfile."""
    name: str
    script: str
    args: List[str] = field(default_factory=list)
    description: str = ""
    dependencies: Set[str] = field(default_factory=set)
    
    def __post_init__(self):
        """Validate command after initialization."""
        if not self.name:
            raise ValueError("Command name cannot be empty")
        
        if not isinstance(self.dependencies, set):
            self.dependencies = set(self.dependencies)


@dataclass
class CommandSet:
    """A set of commands parsed from a justfile."""
    commands: List[Command]
    variables: Dict[str, str] = field(default_factory=dict)
    default_command: Optional[str] = None
    
    def __post_init__(self):
        """Validate command set after initialization."""
        # Check for duplicate command names
        command_names = [cmd.name for cmd in self.commands]
        if len(command_names) != len(set(command_names)):
            dupes = [name for name in command_names if command_names.count(name) > 1]
            raise ValueError(f"Duplicate command names found: {', '.join(set(dupes))}")
        
        # Check if default command exists
        if self.default_command and self.default_command not in command_names:
            raise ValueError(f"Default command '{self.default_command}' not found")
    
    def get_command(self, name: str) -> Optional[Command]:
        """Get a command by name."""
        for cmd in self.commands:
            if cmd.name == name:
                return cmd
        return None
    
    def get_commands_with_dependencies(self) -> Dict[str, Set[str]]:
        """Get a dictionary mapping command names to their dependencies."""
        return {cmd.name: cmd.dependencies for cmd in self.commands}