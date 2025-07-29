"""
Tests for the CommandRunner.
"""

import pytest
import unittest
from unittest.mock import patch, MagicMock

from runly.commands import Command, CommandSet
from runly.runner import CommandRunner
from runly.exceptions import CommandNotFoundError, DependencyCycleError


class TestCommandRunner(unittest.TestCase):
    """Test cases for the CommandRunner class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.commands = [
            Command(
                name="test",
                script="echo 'Running tests'",
                args=[],
                description="Run tests",
                dependencies=set()
            ),
            Command(
                name="build",
                script="echo 'Building project'",
                args=["target"],
                description="Build the project",
                dependencies={"test"}
            ),
            Command(
                name="deploy",
                script="echo 'Deploying to $env'",
                args=["env"],
                description="Deploy to an environment",
                dependencies={"build"}
            ),
            Command(
                name="cyclic1",
                script="echo 'Cyclic1'",
                args=[],
                description="Cyclic command 1",
                dependencies={"cyclic2"}
            ),
            Command(
                name="cyclic2",
                script="echo 'Cyclic2'",
                args=[],
                description="Cyclic command 2",
                dependencies={"cyclic1"}
            )
        ]
        
        self.variables = {
            "project": "runly",
            "version": "0.1.0"
        }
        
        self.command_set = CommandSet(
            commands=self.commands,
            variables=self.variables,
            default_command="test"
        )
        
        self.runner = CommandRunner(self.command_set)
    
    @patch('subprocess.run')
    def test_run_simple_command(self, mock_run):
        """Test running a simple command."""
        mock_run.return_value = MagicMock(returncode=0)
        
        exit_code = self.runner.run("test")
        
        self.assertEqual(exit_code, 0)
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        self.assertEqual(args[0], "echo 'Running tests'")
    
    @patch('subprocess.run')
    def test_run_command_with_args(self, mock_run):
        """Test running a command with arguments."""
        mock_run.return_value = MagicMock(returncode=0)
        
        exit_code = self.runner.run("build", ["debug"])
        
        self.assertEqual(exit_code, 0)
        self.assertEqual(mock_run.call_count, 2)  # Once for test (dependency) and once for build
    
    @patch('subprocess.run')
    def test_run_command_with_variables(self, mock_run):
        """Test running a command with variables."""
        mock_run.return_value = MagicMock(returncode=0)
        
        self.command_set.variables["env"] = "staging"
        exit_code = self.runner.run("deploy", ["production"])
        
        self.assertEqual(exit_code, 0)
        self.assertEqual(mock_run.call_count, 3)  # test, build, deploy
    
    def test_command_not_found(self):
        """Test running a non-existent command."""
        with pytest.raises(CommandNotFoundError):
            self.runner.run("nonexistent")

    def test_dependency_cycle(self):
        """Test detecting a dependency cycle."""
        with pytest.raises(DependencyCycleError):
            self.runner.run("cyclic1")
    
    @patch('subprocess.run')
    def test_dry_run(self, mock_run):
        """Test dry run mode."""
        runner = CommandRunner(self.command_set, dry_run=True)
        exit_code = runner.run("test")
        
        self.assertEqual(exit_code, 0)
        mock_run.assert_not_called()


if __name__ == '__main__':
    unittest.main()