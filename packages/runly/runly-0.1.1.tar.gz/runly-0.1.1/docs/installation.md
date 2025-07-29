# Installation Guide

This guide will help you install RunLy on your system.

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Installation Methods

### From PyPI (Recommended)

```bash
pip install runly
```

### From Source

1. Clone the repository:
```bash
git clone https://github.com/kedjar/runly.git
cd runly
```

2. Install in development mode:
```bash
pip install -e .
```

### Using pipx (Isolated Installation)

If you want to install RunLy in an isolated environment:

```bash
pipx install runly
```

## Verify Installation

After installation, verify that RunLy is working correctly:

```bash
runly --version
```

You should see output similar to:
```
RunLy 0.1.0
```

## Shell Completion (Optional)

### Bash

Add to your `~/.bashrc`:

```bash
eval "$(_RUNLY_COMPLETE=bash_source runly)"
```

### Zsh

Add to your `~/.zshrc`:

```bash
eval "$(_RUNLY_COMPLETE=zsh_source runly)"
```

### Fish

Add to your `~/.config/fish/completions/runly.fish`:

```fish
eval (env _RUNLY_COMPLETE=fish_source runly)
```

## Troubleshooting

### Command Not Found

If you get a "command not found" error after installation:

1. Make sure pip installed the package correctly:
   ```bash
   pip show runly
   ```

2. Check if your Python scripts directory is in your PATH:
   ```bash
   python -m site --user-base
   ```

3. On Windows, you might need to add the Scripts directory to your PATH.

### Permission Errors

If you encounter permission errors during installation:

1. Use a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install runly
   ```

2. Or install for the current user only:
   ```bash
   pip install --user runly
   ```

### Python Version Issues

RunLy requires Python 3.8 or higher. Check your Python version:

```bash
python --version
```

If you have multiple Python versions, you might need to use `python3` or `python3.8` explicitly.

## Development Installation

If you want to contribute to RunLy or modify it for your needs:

1. Clone the repository:
   ```bash
   git clone https://github.com/kedjar/runly.git
   cd runly
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode with all dependencies:
   ```bash
   pip install -e ".[dev,test,docs]"
   ```

4. Run the tests to verify everything works:
   ```bash
   pytest
   ```

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Configuration Reference](configuration.md)
