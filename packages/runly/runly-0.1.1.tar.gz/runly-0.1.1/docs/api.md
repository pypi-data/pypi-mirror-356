# API Reference

This section provides detailed documentation for the RunLy Python API.

## Core Classes

### Command

```{eval-rst}
.. autoclass:: runly.Command
   :members:
   :show-inheritance:
```

### CommandSet

```{eval-rst}
.. autoclass:: runly.CommandSet
   :members:
   :show-inheritance:
```

### JustfileParser

```{eval-rst}
.. autoclass:: runly.JustfileParser
   :members:
   :show-inheritance:
```

### CommandRunner

```{eval-rst}
.. autoclass:: runly.CommandRunner
   :members:
   :show-inheritance:
```

## Exceptions

### Base Exceptions

```{eval-rst}
.. autoclass:: runly.RunLyError
   :members:
   :show-inheritance:
```

```{eval-rst}
.. autoclass:: runly.JustfileError
   :members:
   :show-inheritance:
```

```{eval-rst}
.. autoclass:: runly.CommandError
   :members:
   :show-inheritance:
```

### Specific Exceptions

```{eval-rst}
.. autoclass:: runly.JustfileParseError
   :members:
   :show-inheritance:
```

```{eval-rst}
.. autoclass:: runly.CommandNotFoundError
   :members:
   :show-inheritance:
```

```{eval-rst}
.. autoclass:: runly.DependencyCycleError
   :members:
   :show-inheritance:
```

## Usage Examples

### Basic Usage

```python
from runly import JustfileParser, CommandRunner

# Parse a justfile
parser = JustfileParser("justfile")
command_set = parser.parse()

# Run a command
runner = CommandRunner(command_set)
exit_code = runner.run("test")
```

### Error Handling

```python
from runly import JustfileParser, CommandNotFoundError, JustfileParseError

try:
    parser = JustfileParser("justfile")
    command_set = parser.parse()
    
    runner = CommandRunner(command_set)
    exit_code = runner.run("nonexistent-command")
    
except JustfileParseError as e:
    print(f"Failed to parse justfile: {e}")
except CommandNotFoundError as e:
    print(f"Command not found: {e}")
```

### Custom Configuration

```python
from runly import CommandRunner

# Create a runner with custom options
runner = CommandRunner(
    command_set,
    dry_run=True,      # Don't actually execute commands
    quiet=True,        # Suppress output
    verbose=False      # Disable verbose logging
)

exit_code = runner.run("build", ["release"])
```

## Utilities

### Variable Expansion

```{eval-rst}
.. automodule:: runly.utils
   :members:
   :undoc-members:
   :show-inheritance:
```
