"""
Test configuration and fixtures for RunLy tests.
"""

import pytest
import tempfile
from pathlib import Path
from typing import Generator

from runly.commands import Command, CommandSet
from runly.parser import JustfileParser


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_justfile_content() -> str:
    """Sample justfile content for testing."""
    return """
# Variables
name := "test-project"
version := "1.0.0"

# Default command
test *:
    echo "Running tests for {{name}}"
    pytest

# Build command with an argument
build target="debug":
    echo "Building {{name}} version {{version}} in {{target}} mode"
    python -m build

# Deploy command that depends on build
deploy env:
    echo "Deploying to {{env}}"
    just build release
    echo "Deployment complete"
""".strip()


@pytest.fixture
def sample_yaml_content() -> str:
    """Sample YAML justfile content for testing."""
    return """
variables:
  name: test-project
  version: 1.0.0

default: test

commands:
  test:
    script:
      - echo "Running tests for {{name}}"
      - pytest
    description: Run all tests
  
  build:
    script: python -m build --{{target}}
    args:
      - target=debug
    description: Build the project
    dependencies:
      - test
  
  deploy:
    script:
      - echo "Deploying to {{env}}"
      - just build release
      - echo "Deployment complete"
    args:
      - env
    description: Deploy to an environment
    dependencies:
      - build
""".strip()


@pytest.fixture
def sample_command_set() -> CommandSet:
    """Create a sample CommandSet for testing."""
    commands = [
        Command(
            name="test",
            script="echo 'Running tests'\\npytest",
            args=[],
            description="Run tests",
            dependencies=set()
        ),
        Command(
            name="build",
            script="echo 'Building project'\\npython -m build",
            args=["target=debug"],
            description="Build the project",
            dependencies={"test"}
        ),
        Command(
            name="deploy",
            script="echo 'Deploying to {{env}}'\\njust build release",
            args=["env"],
            description="Deploy to an environment",
            dependencies={"build"}
        ),
    ]
    
    variables = {
        "project": "runly",
        "version": "0.1.0"
    }
    
    return CommandSet(
        commands=commands,
        variables=variables,
        default_command="test"
    )


@pytest.fixture
def justfile_parser(temp_dir: Path, sample_justfile_content: str) -> JustfileParser:
    """Create a JustfileParser with a temporary justfile."""
    justfile_path = temp_dir / "justfile"
    justfile_path.write_text(sample_justfile_content)
    return JustfileParser(str(justfile_path))


@pytest.fixture
def yaml_parser(temp_dir: Path, sample_yaml_content: str) -> JustfileParser:
    """Create a JustfileParser with a temporary YAML file."""
    yaml_path = temp_dir / "runly.yml"
    yaml_path.write_text(sample_yaml_content)
    return JustfileParser(str(yaml_path))


class MockProcess:
    """Mock subprocess.run result for testing."""
    
    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = ""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
