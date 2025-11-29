# context-forge-cli

A CLI tool to manage context for AI coding assistants like Claude Code.

## Installation

```bash
uv pip install context-forge-cli
```

## Usage

```bash
# Check version
context-forge --version

# Initialize a project
context-forge init

# Install a command to Claude Code
context-forge install hello-world
```

## Development

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended package manager)

### Setup

```bash
# Clone the repository
git clone https://github.com/kadoppe/context-forge.git
cd context-forge

# Install dependencies (including dev dependencies)
uv sync --dev
```

### Running Commands

```bash
# Run the CLI directly
uv run context-forge --version
uv run context-forge init
uv run context-forge install hello-world

# Or use the installed command (after `uv sync`)
context-forge --version
```

### Testing

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run a specific test file
uv run pytest tests/integration/test_cli.py
```

### Code Quality

```bash
# Type checking with mypy
uv run mypy src/context_forge_cli/

# Linting with ruff
uv run ruff check src/context_forge_cli/ tests/

# Fix linting issues automatically
uv run ruff check --fix src/context_forge_cli/ tests/
```

### Project Structure

```
src/context_forge_cli/
├── __init__.py              # CLI entry point and main logic
└── templates/
    └── commands/
        └── hello-world.md   # Built-in command template

tests/
└── integration/
    └── test_cli.py          # CLI integration tests
```

## License

MIT
