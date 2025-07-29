# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0]

### Added
- Comprehensive exception handling system
- Modern src/ layout project structure
- Rich CLI interface with colored output
- Verbose mode for detailed command output
- Type hints throughout the codebase
- Comprehensive test suite with fixtures
- Detailed documentation and examples
- Contributing guidelines and code of conduct

### Changed
- Migrated from setup.py to modern pyproject.toml
- Improved error messages with detailed context
- Enhanced command dependency resolution
- Better variable expansion with environment variable support
- Modernized CLI using argparse with better help text

### Fixed
- Dependency cycle detection and reporting
- Command argument validation
- File path resolution across platforms
- Error handling in command execution

## [Unreleased] - 2025-06-16

### Added
- Initial release of RunLy
- Basic justfile parsing support
- YAML configuration file support
- Command execution with dependency resolution
- Variable expansion in commands
- Command-line interface
- Support for command arguments
- Default command execution
- Command listing functionality

### Features
- **Justfile Compatibility**: Parse and execute justfile format
- **YAML Support**: Alternative YAML configuration format
- **Dependencies**: Commands can depend on other commands
- **Variables**: Support for variable substitution
- **Cross-platform**: Works on Windows, macOS, and Linux
- **CLI Interface**: Easy-to-use command-line interface

### Technical Details
- Python 3.7+ support
- PyYAML dependency for YAML parsing
- Subprocess-based command execution
- Comprehensive error handling
- Unit test coverage

---

## Release Notes Template

### [X.Y.Z] - YYYY-MM-DD

#### Added
- New features

#### Changed
- Changes in existing functionality

#### Deprecated
- Soon-to-be removed features

#### Removed
- Now removed features

#### Fixed
- Bug fixes

#### Security
- Vulnerability fixes