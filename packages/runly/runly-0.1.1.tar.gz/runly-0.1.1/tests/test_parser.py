"""
Tests for the JustfileParser.
"""

import os
import tempfile
import unittest

from runly.parser import JustfileParser
from runly.commands import Command, CommandSet


class TestJustfileParser(unittest.TestCase):
    """Test cases for the JustfileParser class."""
    
    def test_parse_simple_justfile(self):
        """Test parsing a simple justfile."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"""
# This is a simple justfile

# Set variables
name := "world"
greeting := "Hello"

# Default test command
test *:
    echo "Running tests"
    pytest

# A command with arguments
greet name="world":
    echo "{{greeting}} {{name}}!"

# A more complex command
build target="debug":
    cargo build --{{target}}
""")
            f.flush()
            
            parser = JustfileParser(f.name)
            command_set = parser.parse()
            
            # Check variables
            self.assertEqual(command_set.variables.get('name'), 'world')
            self.assertEqual(command_set.variables.get('greeting'), 'Hello')
            
            # Check commands
            self.assertEqual(len(command_set.commands), 3)
            
            # Check default command
            self.assertEqual(command_set.default_command, 'test')
            
            # Check test command
            test_cmd = command_set.get_command('test')
            self.assertIsNotNone(test_cmd)
            self.assertEqual(test_cmd.name, 'test')
            self.assertEqual(test_cmd.script.strip(), 'echo "Running tests"\npytest')
            
            # Check greet command
            greet_cmd = command_set.get_command('greet')
            self.assertIsNotNone(greet_cmd)
            self.assertEqual(greet_cmd.name, 'greet')
            self.assertEqual(len(greet_cmd.args), 1)
            self.assertEqual(greet_cmd.args[0], 'name="world"')
            
            # Check build command
            build_cmd = command_set.get_command('build')
            self.assertIsNotNone(build_cmd)
            self.assertEqual(build_cmd.name, 'build')
            self.assertEqual(len(build_cmd.args), 1)
            self.assertEqual(build_cmd.args[0], 'target="debug"')
        
        os.unlink(f.name)
    
    def test_parse_yaml_justfile(self):
        """Test parsing a YAML justfile."""
        with tempfile.NamedTemporaryFile(suffix='.yml', delete=False) as f:
            f.write(b"""
# RunLy YAML configuration

variables:
  name: world
  greeting: Hello

default: test

commands:
  test:
    script:
      - echo "Running tests"
      - pytest
    description: Run all tests
  
  greet:
    script: echo "{{greeting}} {{name}}!"
    args:
      - name="world"
    description: Greet someone
  
  build:
    script: cargo build --{{target}}
    args:
      - target="debug"
    description: Build the project
    dependencies:
      - test
""")
            f.flush()
            
            parser = JustfileParser(f.name)
            command_set = parser.parse()
            
            # Check variables
            self.assertEqual(command_set.variables.get('name'), 'world')
            self.assertEqual(command_set.variables.get('greeting'), 'Hello')
            
            # Check commands
            self.assertEqual(len(command_set.commands), 3)
            
            # Check default command
            self.assertEqual(command_set.default_command, 'test')
            
            # Check test command
            test_cmd = command_set.get_command('test')
            self.assertIsNotNone(test_cmd)
            self.assertEqual(test_cmd.name, 'test')
            self.assertEqual(test_cmd.script.strip(), 'echo "Running tests"\npytest')
            self.assertEqual(test_cmd.description, 'Run all tests')
            
            # Check greet command
            greet_cmd = command_set.get_command('greet')
            self.assertIsNotNone(greet_cmd)
            self.assertEqual(greet_cmd.name, 'greet')
            self.assertEqual(len(greet_cmd.args), 1)
            self.assertEqual(greet_cmd.args[0], 'name="world"')
            self.assertEqual(greet_cmd.description, 'Greet someone')
            
            # Check build command
            build_cmd = command_set.get_command('build')
            self.assertIsNotNone(build_cmd)
            self.assertEqual(build_cmd.name, 'build')
            self.assertEqual(len(build_cmd.args), 1)
            self.assertEqual(build_cmd.args[0], 'target="debug"')
            self.assertEqual(build_cmd.description, 'Build the project')
            self.assertEqual(build_cmd.dependencies, {'test'})
        
        os.unlink(f.name)


if __name__ == '__main__':
    unittest.main()