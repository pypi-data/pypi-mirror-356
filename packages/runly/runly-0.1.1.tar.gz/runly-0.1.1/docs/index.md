# RunLy Documentation

Welcome to RunLy, a simple yet powerful task runner inspired by justfile.

## Table of Contents

- [Installation](installation.md)
- [Quick Start](quickstart.md)
- [Configuration](configuration.md)
- [Command Reference](commands.md)
- [API Reference](api.md)
- [Contributing](../CONTRIBUTING.md)
- [Changelog](../CHANGELOG.md)

## Overview

RunLy is designed to make running project tasks simple and consistent. Whether you're building, testing, or deploying your project, RunLy provides a unified interface for all your automation needs.

### Key Features

- **Simple Configuration**: Use either justfile syntax or YAML format
- **Dependency Management**: Commands can depend on other commands
- **Variable Expansion**: Support for variables and environment variables
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Extensible**: Easy to integrate with existing build systems

### Why RunLy?

- **Familiar Syntax**: If you know justfile, you already know RunLy
- **Modern Python**: Built with modern Python practices and type hints
- **Rich CLI**: Beautiful command-line interface with helpful error messages
- **Well Tested**: Comprehensive test suite with high coverage
- **Developer Friendly**: Excellent documentation and examples

## Quick Example

Create a `justfile` in your project root:

```justfile
# Variables
project := "my-app"
version := "1.0.0"

# Default command
test:
    echo "Running tests for {{project}}"
    pytest tests/

# Build the project
build target="debug":
    echo "Building {{project}} v{{version}} in {{target}} mode"
    python -m build

# Deploy (depends on build)
deploy env:
    just build release
    echo "Deploying to {{env}}"
    docker deploy {{project}}:{{version}}
```

Then run commands:

```bash
# Run the default command
runly

# Run specific commands
runly test
runly build release
runly deploy production

# List available commands
runly --list
```

## Next Steps

- [Install RunLy](installation.md)
- [Follow the Quick Start guide](quickstart.md)
- [Learn about configuration options](configuration.md)
