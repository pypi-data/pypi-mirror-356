# RunLy

[![PyPI version](https://badge.fury.io/py/runly.svg)](https://badge.fury.io/py/runly)
[![Python Support](https://img.shields.io/pypi/pyversions/runly.svg)](https://pypi.org/project/runly/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/kedjar/runly/workflows/Tests/badge.svg)](https://github.com/kedjar/runly/actions)
[![Coverage](https://codecov.io/gh/kedjar/runly/branch/main/graph/badge.svg)](https://codecov.io/gh/kedjar/runly)

> A simple, powerful task runner inspired by justfile

RunLy is a modern Python task runner that brings the simplicity and power of [justfile](https://github.com/casey/just) to Python projects. Define your project tasks in a simple configuration file and run them with a single command.

## ✨ Features

- **🎯 Simple**: Easy-to-understand configuration syntax
- **🔗 Dependencies**: Commands can depend on other commands
- **🔧 Variables**: Support for variables and environment variables  
- **📁 Flexible**: Supports both justfile and YAML formats
- **🚀 Fast**: Minimal overhead, maximum performance
- **🌐 Cross-platform**: Works on Windows, macOS, and Linux
- **🎨 Modern CLI**: Beautiful command-line interface with rich output
- **🧪 Well-tested**: Comprehensive test suite with high coverage

## 🚀 Quick Start

### Installation

```bash
pip install runly
```

### Basic Usage

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
```

Run your tasks:

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

### YAML Configuration

Alternatively, use YAML format (`runly.yml`):

```yaml
variables:
  project: my-app
  version: 1.0.0

default: test

commands:
  test:
    script:
      - echo "Running tests for {{project}}"
      - pytest tests/
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
      - just build release
      - echo "Deploying to {{env}}"
    args:
      - env
    description: Deploy to environment
    dependencies:
      - build
```

## 📖 Documentation

- **[Installation Guide](docs/installation.md)** - Detailed installation instructions
- **[Quick Start](docs/quickstart.md)** - Get up and running quickly
- **[Configuration](docs/configuration.md)** - Complete configuration reference
- **[Command Reference](docs/commands.md)** - All available CLI commands
- **[API Reference](docs/api.md)** - Python API documentation

## 🎯 Why RunLy?

### Before RunLy

```bash
# Scattered scripts and commands
python -m pytest tests/
python -m build --wheel
docker build -t myapp:latest .
kubectl apply -f deployment.yaml
python scripts/cleanup.py
```

### After RunLy

```bash
# One unified interface
runly test
runly build
runly deploy production
runly cleanup
```

## 🔧 Advanced Features

### Command Dependencies

```justfile
deploy: build test
    echo "Deploying application"
    
build:
    echo "Building application"
    
test:
    echo "Running tests"
```

### Variable Expansion

```justfile
name := "myapp"
version := env_var("VERSION", "dev")

build:
    docker build -t {{name}}:{{version}} .
    
deploy env:
    docker run {{name}}:{{version}} --env={{env}}
```

### Environment Variables

```justfile
backup:
    aws s3 sync ./data s3://{{env("BACKUP_BUCKET")}}/{{datetime()}}
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/kedjar/runly.git
cd runly

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev,test,docs]"

# Run tests
pytest

# Run linting
black . && isort . && flake8

# Build documentation
cd docs && make html
```

## 📋 Requirements

- Python 3.8+
- PyYAML 6.0+
- Click 8.0+ (for enhanced CLI)
- Rich 12.0+ (for beautiful output)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [Casey Rodarmor's just](https://github.com/casey/just)
- Built with modern Python practices and tools
- Thanks to all contributors and users

## 📊 Project Status

RunLy is actively maintained and used in production. We follow [Semantic Versioning](https://semver.org/) and maintain backward compatibility.

---

<div align="center">
  <b>Star ⭐ this repo if you find RunLy useful!</b>
</div>
