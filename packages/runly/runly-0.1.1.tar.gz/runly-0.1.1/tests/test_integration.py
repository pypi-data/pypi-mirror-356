"""
Integration tests for RunLy CLI.
"""
import os
import subprocess
import tempfile
from pathlib import Path

import pytest


class TestCLIIntegration:
    """Integration tests for the RunLy CLI."""

    def test_version_command(self):
        """Test that --version returns correct version."""
        result = subprocess.run(
            ["python", "-m", "runly", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "RunLy" in result.stdout
        assert "0.1.0" in result.stdout

    def test_help_command(self):
        """Test that --help shows usage information."""
        result = subprocess.run(
            ["python", "-m", "runly", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "RunLy" in result.stdout
        assert "usage:" in result.stdout.lower()

    def test_no_justfile_error(self, tmp_path):
        """Test error when no justfile is found."""
        # Change to temp directory with no justfile
        original_cwd = Path.cwd()
        try:            
            os.chdir(tmp_path)
            
            result = subprocess.run(
                ["python", "-m", "runly", "test"],
                capture_output=True,
                text=True
            )
            assert result.returncode == 1
            assert "No justfile found" in result.stderr
        finally:
            os.chdir(original_cwd)

    def test_list_commands(self, tmp_path):
        """Test listing commands from a justfile."""
        # Create a simple justfile
        justfile = tmp_path / "justfile"
        justfile.write_text("""
# A test command
test:
    echo "Running tests"

# Build the project  
build:
    echo "Building project"
""")
        
        original_cwd = Path.cwd()
        try:            
            os.chdir(tmp_path)
            
            result = subprocess.run(
                ["python", "-m", "runly", "--list"],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
            assert "test" in result.stdout
            assert "build" in result.stdout
        finally:
            os.chdir(original_cwd)

    def test_run_simple_command(self, tmp_path):
        """Test running a simple command."""
        # Create a simple justfile
        justfile = tmp_path / "justfile"
        justfile.write_text("""
test:
    echo "Hello from RunLy test"
""")
        
        original_cwd = Path.cwd()
        try:           
            os.chdir(tmp_path)
            
            result = subprocess.run(
                ["python", "-m", "runly", "test"],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
            assert "Running command: test" in result.stdout
        finally:
            os.chdir(original_cwd)

    def test_yaml_format(self, tmp_path):
        """Test running commands from YAML format."""
        # Create a YAML justfile
        yaml_file = tmp_path / "runly.yml"
        yaml_file.write_text("""
variables:
  name: test-project

default: test

commands:
  test:
    script: echo "Testing {{name}}"
    description: Run tests
""")
        
        original_cwd = Path.cwd()
        try:            
            os.chdir(tmp_path)
            
            result = subprocess.run(
                ["python", "-m", "runly", "--list"],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
            assert "test" in result.stdout
            assert "Run tests" in result.stdout
        finally:
            os.chdir(original_cwd)

    def test_dry_run(self, tmp_path):
        """Test dry run mode."""
        # Create a simple justfile
        justfile = tmp_path / "justfile"
        justfile.write_text("""
test:
    echo "This should not execute"
    exit 1
""")
        
        original_cwd = Path.cwd()
        try:            
            os.chdir(tmp_path)
            
            result = subprocess.run(
                ["python", "-m", "runly", "--dry-run", "test"],
                capture_output=True,
                text=True
            )
            # Should succeed in dry run even though command would fail
            assert result.returncode == 0
            assert "Would execute:" in result.stdout
        finally:
            os.chdir(original_cwd)

    def test_command_with_args(self, tmp_path):
        """Test running command with arguments."""
        # Create justfile with parameterized command
        justfile = tmp_path / "justfile"
        justfile.write_text("""
greet name="World":
    echo "Hello {{name}}!"
""")
        
        original_cwd = Path.cwd()
        try:            
            os.chdir(tmp_path)
            
            result = subprocess.run(
                ["python", "-m", "runly", "greet", "RunLy"],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
        finally:
            os.chdir(original_cwd)


class TestEndToEnd:
    """End-to-end tests simulating real usage scenarios."""

    def test_python_project_workflow(self, tmp_path):
        """Test a typical Python project workflow."""
        # Create a justfile for a Python project
        justfile = tmp_path / "justfile"
        justfile.write_text("""
# Variables
project := "myproject"

# Install dependencies
install:
    echo "Installing dependencies for {{project}}"

# Run tests
test: install
    echo "Running tests for {{project}}"

# Build package
build: test
    echo "Building {{project}}"

# Deploy
deploy env: build
    echo "Deploying {{project}} to {{env}}"
""")
        
        original_cwd = Path.cwd()
        try:            
            os.chdir(tmp_path)
            
            # Test the full workflow
            result = subprocess.run(
                ["python", "-m", "runly", "deploy", "production"],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
            
            # Should run dependencies in order
            output = result.stdout
            install_pos = output.find("Installing dependencies")
            test_pos = output.find("Running tests")
            build_pos = output.find("Building")
            deploy_pos = output.find("Deploying")
            
            # Check order of execution
            assert install_pos < test_pos < build_pos < deploy_pos
        finally:
            os.chdir(original_cwd)

    def test_error_handling(self, tmp_path):
        """Test error handling in real scenarios."""
        # Create justfile with failing command
        justfile = tmp_path / "justfile"
        justfile.write_text("""
test:
    echo "Starting tests"
    python -c "import sys; sys.exit(1)"
    echo "This should not run"
""")
        
        original_cwd = Path.cwd()
        try:            
            os.chdir(tmp_path)
            
            result = subprocess.run(
                ["python", "-m", "runly", "test"],
                capture_output=True,
                text=True
            )
            assert result.returncode == 1
            assert "Starting tests" in result.stdout
        finally:
            os.chdir(original_cwd)
