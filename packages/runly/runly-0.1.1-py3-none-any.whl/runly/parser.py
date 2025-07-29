"""
Parser for justfile format.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

from .commands import Command, CommandSet
from .exceptions import JustfileParseError, JustfileSyntaxError
from .utils import expand_variables


class JustfileParser:
    """Parser for justfile and YAML configuration files."""
    
    def __init__(self, filepath: str):
        """Initialize the parser with a justfile path."""
        self.filepath = filepath
        self.dirname = os.path.dirname(os.path.abspath(filepath))
        self._variables: Dict[str, str] = {}
    
    def parse(self) -> CommandSet:
        """Parse the justfile and return a CommandSet."""
        # Determine file format based on extension
        _, ext = os.path.splitext(self.filepath)
        
        if ext.lower() in ('.yml', '.yaml'):
            return self._parse_yaml()
        else:
            return self._parse_justfile()
    
    def _parse_yaml(self) -> CommandSet:
        """Parse a YAML-based justfile."""
        with open(self.filepath, 'r') as f:
            config = yaml.safe_load(f)
        
        if not isinstance(config, dict):
            raise ValueError("Invalid YAML file: root must be a dictionary")
        
        # Extract variables
        variables = config.get('variables', {})
        self._variables = {k: str(v) for k, v in variables.items()}
        
        # Extract commands
        commands_data = config.get('commands', {})
        if not isinstance(commands_data, dict):
            raise ValueError("Invalid YAML file: 'commands' must be a dictionary")
        
        commands = []
        default_command = config.get('default')
        
        for name, data in commands_data.items():
            if isinstance(data, str):
                # Simple string command
                commands.append(Command(
                    name=name,
                    script=data,
                    args=[],
                    description="",
                    dependencies=set()
                ))
            elif isinstance(data, dict):
                # Detailed command object
                script = data.get('script', '')
                if isinstance(script, list):
                    script = '\n'.join(script)
                
                args = data.get('args', [])
                description = data.get('description', '')
                dependencies = set(data.get('dependencies', []))
                
                commands.append(Command(
                    name=name,
                    script=script,
                    args=args,
                    description=description,
                    dependencies=dependencies
                ))
            else:
                raise ValueError(f"Invalid command format for '{name}'")
        
        return CommandSet(commands=commands, default_command=default_command, variables=self._variables)
    
    def _parse_justfile(self) -> CommandSet:
        """Parse a traditional justfile."""
        with open(self.filepath, 'r') as f:
            content = f.read()
        
        # Split content into lines and remove comments
        lines = []
        for line in content.split('\n'):
            if '#' in line:
                line = line[:line.index('#')]
            lines.append(line)
        
        # Parse variables
        self._variables = self._extract_variables(lines)
        
        # Parse commands
        commands, default_command = self._extract_commands(lines)
        
        return CommandSet(commands=commands, default_command=default_command, variables=self._variables)
    
    def _extract_variables(self, lines: List[str]) -> Dict[str, str]:
        """Extract variable definitions."""
        variables = {}
        var_pattern = re.compile(r'^([A-Za-z0-9_-]+)\s*:=\s*(.+)$')
        
        for line in lines:
            line = line.strip()
            match = var_pattern.match(line)
            if match:
                name, value = match.groups()
                # Remove quotes from values if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                # Expand variables in the value
                value = expand_variables(value, variables)
                variables[name] = value
        
        return variables
    
    def _extract_commands(self, lines: List[str]) -> Tuple[List[Command], Optional[str]]:
        """Extract command definitions."""
        commands = []
        current_command = None
        current_description = []
        current_script = []
        current_dependencies = set()
        default_command = None
        
        # Pattern to match command definitions with dependencies (e.g., "deploy env: build" or "test *:")
        # but not variable assignments (e.g., "project := value")
        cmd_pattern = re.compile(r'^([A-Za-z0-9_-]+)(\s+([^:]*?))?\s*(\*)?\s*:\s*(.*)$')
        
        for line_num, line in enumerate(lines):
            stripped = line.strip()
            
            # Skip variable assignments
            if re.match(r'^[A-Za-z0-9_-]+\s*:=', stripped):
                continue
            
            # Check for command definition
            match = cmd_pattern.match(stripped)
            if match:
                # Save previous command if exists
                if current_command:
                    commands.append(Command(
                        name=current_command[0],
                        script='\n'.join(current_script),
                        args=current_command[1],
                        description='\n'.join(current_description).strip(),
                        dependencies=current_dependencies
                    ))
                
                # Start new command
                cmd_name = match.group(1)
                args_str = match.group(3) or ""
                is_default = bool(match.group(4))  # The * marker
                deps_str = match.group(5) or ""
                
                # Parse arguments - in justfile format, args are space-separated
                args = [arg.strip() for arg in args_str.split() if arg.strip()]
                
                # Parse dependencies from the command line
                dependencies = set()
                if deps_str.strip():
                    dependencies = {dep.strip() for dep in deps_str.split() if dep.strip()}
                
                # Set default command if marked with *
                if is_default and default_command is None:
                    default_command = cmd_name
                
                current_command = (cmd_name, args)
                current_description = []
                current_script = []
                current_dependencies = dependencies
                
                # No script part on the command line in this format
            
            elif line.startswith('@') and current_command is None:
                # This is a command description before the actual command
                current_description.append(line[1:].strip())
            
            elif current_command is not None:
                # This line belongs to the current command's script
                # Check for indentation
                if line and (line.startswith(' ') or line.startswith('\t')):
                    current_script.append(line.strip())
                elif not line.strip():
                    # Empty line within command script
                    current_script.append('')
                else:
                    # No indentation means end of command
                    commands.append(Command(
                        name=current_command[0],
                        script='\n'.join(current_script),
                        args=current_command[1],
                        description='\n'.join(current_description).strip(),
                        dependencies=current_dependencies
                    ))
                    current_command = None
                    current_description = []
                    current_script = []
                    current_dependencies = set()
                    
                    # Re-process this line
                    lines.insert(line_num, line)
        
        # Add the last command if exists
        if current_command:
            commands.append(Command(
                name=current_command[0],
                script='\n'.join(current_script),
                args=current_command[1],
                description='\n'.join(current_description).strip(),
                dependencies=current_dependencies
            ))
        
        return commands, default_command
    
    def _extract_dependencies(self, script: str) -> Set[str]:
        """Extract command dependencies from script."""
        dependencies = set()
        
        # Look for patterns like "just command" or "just command arg1 arg2"
        pattern = re.compile(r'(?:^|\n|\s)just\s+([A-Za-z0-9_-]+)')
        
        for match in pattern.finditer(script):
            dependencies.add(match.group(1))
        
        return dependencies