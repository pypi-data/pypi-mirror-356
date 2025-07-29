# Contributing to RunLy

Thank you for your interest in contributing to RunLy! This document provides guidelines and instructions for contributing to the project.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please:

1. **Search existing issues** to avoid duplicates
2. **Use the issue template** if available
3. **Provide clear reproduction steps** for bugs
4. **Include system information** (OS, Python version, RunLy version)

### Suggesting Features

We welcome feature suggestions! Please:

1. **Check if the feature already exists** or is planned
2. **Describe the use case** and benefit
3. **Provide examples** of how it would work
4. **Consider backward compatibility** implications

### Code Contributions

1. **Fork the repository** on GitHub
2. **Create a feature branch** from `main`
3. **Make your changes** following our coding standards
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Submit a pull request**

## 🛠 Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- pip or pipx

### Local Development

1. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/runly.git
   cd runly
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode:**
   ```bash
   pip install -e ".[dev,test,docs]"
   ```

4. **Verify the setup:**
   ```bash
   pytest
   runly --version
   ```

### Project Structure

```
runly/
├── src/runly/           # Main package source
│   ├── __init__.py      # Package initialization
│   ├── cli.py           # Command-line interface
│   ├── commands.py      # Command models
│   ├── exceptions.py    # Custom exceptions
│   ├── parser.py        # Justfile/YAML parser
│   ├── runner.py        # Command runner
│   └── utils.py         # Utility functions
├── tests/               # Test suite
│   ├── conftest.py      # Test configuration
│   ├── test_*.py        # Test modules
│   └── fixtures/        # Test fixtures
├── docs/                # Documentation
├── pyproject.toml       # Project configuration
└── README.md            # Project overview
```

## 📝 Coding Standards

### Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run these before submitting:

```bash
# Format code
black .
isort .

# Check linting
flake8

# Type checking
mypy src/runly
```

### Code Guidelines

1. **Follow PEP 8** style guide
2. **Use type hints** for all functions and methods
3. **Write docstrings** for all public APIs
4. **Keep functions small** and focused
5. **Use meaningful variable names**
6. **Handle errors gracefully** with custom exceptions

### Example Code Style

```python
from typing import List, Optional

from .exceptions import CommandNotFoundError


def find_command(name: str, commands: List[Command]) -> Optional[Command]:
    """Find a command by name in the command list.
    
    Args:
        name: The command name to search for
        commands: List of available commands
        
    Returns:
        The command if found, None otherwise
        
    Raises:
        CommandNotFoundError: If command is not found and strict mode is enabled
    """
    for command in commands:
        if command.name == name:
            return command
    return None
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/runly --cov-report=html

# Run specific test file
pytest tests/test_parser.py

# Run with verbose output
pytest -v
```

### Writing Tests

1. **Place tests** in the `tests/` directory
2. **Name test files** with `test_*.py` pattern
3. **Use descriptive test names** that explain what is being tested
4. **Follow the Arrange-Act-Assert pattern**
5. **Use fixtures** for common test setup
6. **Mock external dependencies**

### Test Example

```python
import pytest
from runly.parser import JustfileParser
from runly.exceptions import JustfileParseError


def test_parse_simple_justfile(temp_dir):
    """Test parsing a simple justfile with one command."""
    # Arrange
    justfile_content = """
test:
    echo "Running tests"
    pytest
"""
    justfile_path = temp_dir / "justfile"
    justfile_path.write_text(justfile_content)
    
    # Act
    parser = JustfileParser(str(justfile_path))
    command_set = parser.parse()
    
    # Assert
    assert len(command_set.commands) == 1
    assert command_set.commands[0].name == "test"
    assert "echo" in command_set.commands[0].script
```

## 📚 Documentation

### Writing Documentation

1. **Use Markdown** for all documentation
2. **Include code examples** where helpful
3. **Keep explanations clear** and concise
4. **Update relevant docs** when changing functionality
5. **Test examples** to ensure they work

### Documentation Structure

- `README.md` - Project overview and quick start
- `docs/` - Detailed documentation
- Docstrings - API documentation in code
- Type hints - Type information for IDEs

## 🔄 Pull Request Process

### Before Submitting

1. **Ensure all tests pass:** `pytest`
2. **Check code style:** `black . && isort . && flake8`
3. **Verify type hints:** `mypy src/runly`
4. **Update documentation** if needed
5. **Add tests** for new features
6. **Update CHANGELOG.md** if applicable

### PR Guidelines

1. **Use a clear title** describing the change
2. **Reference related issues** using `Fixes #123`
3. **Provide a detailed description** of changes
4. **Include screenshots** for UI changes
5. **Keep PRs focused** on a single feature/fix
6. **Respond promptly** to review feedback

### PR Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings introduced
```

## 🏷 Release Process

Releases follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

## 🆘 Getting Help

- **GitHub Issues** - For bug reports and feature requests
- **GitHub Discussions** - For questions and general discussion
- **Email** - runly@mkedjar.com for private inquiries

## 📜 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). By participating, you are expected to uphold this code.

## 🙏 Recognition

Contributors will be:

- **Listed in CONTRIBUTORS.md**
- **Mentioned in release notes** for significant contributions
- **Given credit** in relevant documentation

Thank you for contributing to RunLy! 🎉