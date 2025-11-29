"""context-forge CLI - A tool to manage context for AI coding assistants."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.panel import Panel

__version__ = "0.1.0"

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_FILE_ERROR = 2
EXIT_USER_CANCEL = 3

# Rich console for output
console = Console()
err_console = Console(stderr=True)


# =============================================================================
# Validation (T033)
# =============================================================================

# Command name pattern: alphanumeric, hyphens, underscores only
COMMAND_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")
COMMAND_NAME_MAX_LENGTH = 64


def validate_command_name(name: str) -> str | None:
    """Validate command name format.

    Args:
        name: Command name to validate.

    Returns:
        Error message if invalid, None if valid.
    """
    if not name:
        return "Command name cannot be empty."

    if len(name) > COMMAND_NAME_MAX_LENGTH:
        return f"Command name too long (max {COMMAND_NAME_MAX_LENGTH} characters)."

    if not COMMAND_NAME_PATTERN.match(name):
        return (
            "Command name can only contain letters, numbers, "
            "hyphens (-), and underscores (_)."
        )

    return None


# =============================================================================
# Error Handling (T032)
# =============================================================================


def show_error(message: str, hint: str | None = None) -> None:
    """Display an error message in a Rich panel.

    Args:
        message: The error message to display.
        hint: Optional hint for resolving the error.
    """
    content = f"[red bold]Error:[/red bold] {message}"
    if hint:
        content += f"\n\n[dim]Hint: {hint}[/dim]"

    err_console.print(Panel(content, title="Error", border_style="red"))


# =============================================================================
# Data Models (T005)
# =============================================================================


@dataclass
class Command:
    """Represents an installable command template."""

    name: str
    description: str
    content: str
    metadata: dict[str, Any]


@dataclass
class CommandTemplate:
    """Represents a command template file packaged with context-forge."""

    path: Path
    command: Command

    @property
    def target_filename(self) -> str:
        """Generate target filename with context-forge prefix."""
        return f"context-forge.{self.command.name}.md"


@dataclass
class InstallTarget:
    """Represents the installation target directory."""

    project_root: Path

    @property
    def commands_dir(self) -> Path:
        """Get the commands directory path."""
        return self.project_root / ".claude" / "commands"

    @property
    def exists(self) -> bool:
        """Check if commands directory exists."""
        return self.commands_dir.exists()


@dataclass
class InstallResult:
    """Represents the result of an install operation."""

    success: bool
    command_name: str
    target_path: Path
    overwritten: bool = False
    error: str | None = None


# =============================================================================
# Template Loading (T006)
# =============================================================================


def get_templates_path() -> Path:
    """Get the path to embedded templates using importlib.resources."""
    import importlib.resources

    return Path(str(importlib.resources.files("context_forge_cli"))) / "templates"


def load_template(command_name: str) -> CommandTemplate | None:
    """Load a command template by name.

    Args:
        command_name: Name of the command template to load.

    Returns:
        CommandTemplate if found, None otherwise.
    """
    templates_dir = get_templates_path() / "commands"
    template_path = templates_dir / f"{command_name}.md"

    if not template_path.exists():
        return None

    content = template_path.read_text(encoding="utf-8")

    # Parse YAML frontmatter if present
    metadata: dict[str, Any] = {}
    description = ""
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            import yaml

            try:
                metadata = yaml.safe_load(parts[1]) or {}
                description = metadata.get("description", "")
                body = parts[2].strip()
            except yaml.YAMLError:
                # If YAML parsing fails, use content as-is
                body = content

    command = Command(
        name=command_name,
        description=description,
        content=body,
        metadata=metadata,
    )

    return CommandTemplate(path=template_path, command=command)


def list_available_templates() -> list[str]:
    """List all available command template names.

    Returns:
        List of command names available for installation.
    """
    templates_dir = get_templates_path() / "commands"
    if not templates_dir.exists():
        return []

    return [p.stem for p in templates_dir.glob("*.md")]


# =============================================================================
# Typer App (T007)
# =============================================================================


def version_callback(value: bool) -> None:
    """Display version information and exit."""
    if value:
        console.print(f"context-forge-cli v{__version__}")
        raise typer.Exit()


app = typer.Typer(
    name="context-forge",
    help="A CLI tool to manage context for AI coding assistants like Claude Code.",
    add_completion=False,
)


@app.callback()
def main_callback(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version information and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """context-forge CLI - Manage context for AI coding assistants."""
    pass


# =============================================================================
# Install Command (T017-T024)
# =============================================================================


@app.command()
def install(
    command_name: str = typer.Argument(
        ...,
        help="Name of the command template to install (e.g., hello-world).",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing file without prompting.",
    ),
) -> None:
    """Install a command template to Claude Code.

    Installs the specified command template to .claude/commands/ directory
    with the 'context-forge.' prefix.
    """
    # Validate command name (T033)
    validation_error = validate_command_name(command_name)
    if validation_error:
        show_error(
            validation_error,
            hint="Use only letters, numbers, hyphens, and underscores.",
        )
        raise typer.Exit(EXIT_ERROR)

    # Load template
    template = load_template(command_name)
    if template is None:
        available = list_available_templates()
        hint = None
        if available:
            hint = f"Available commands: {', '.join(available)}"
        show_error(f"Command '{command_name}' not found.", hint=hint)
        raise typer.Exit(EXIT_ERROR)

    # Determine install target
    target = InstallTarget(project_root=Path.cwd())
    target_path = target.commands_dir / template.target_filename

    # Check if file exists
    if target_path.exists() and not force:
        overwrite = typer.confirm(
            f"File '{target_path}' already exists. Overwrite?",
            default=False,
        )
        if not overwrite:
            console.print("[yellow]Installation cancelled.[/yellow]")
            raise typer.Exit(EXIT_USER_CANCEL)

    # Create directories
    try:
        target.commands_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        show_error(
            f"Cannot create directory: {target.commands_dir}",
            hint="Check write permissions for the project directory.",
        )
        raise typer.Exit(EXIT_FILE_ERROR)

    # Read original template file (preserve frontmatter)
    original_content = template.path.read_text(encoding="utf-8")

    # Write file
    try:
        target_path.write_text(original_content, encoding="utf-8")
    except PermissionError:
        show_error(
            f"Cannot write file: {target_path}",
            hint="Check write permissions for the target directory.",
        )
        raise typer.Exit(EXIT_FILE_ERROR)

    # Success message
    console.print(
        f"[green]Success![/green] Installed '{command_name}' to {target_path}"
    )
    console.print(
        f"[dim]Use '/context-forge.{command_name}' in Claude Code "
        "to run this command.[/dim]"
    )


# =============================================================================
# Init Command (T027-T030)
# =============================================================================


def _install_command(command_name: str, target: InstallTarget, force: bool) -> bool:
    """Install a single command (internal helper for init --install).

    Args:
        command_name: Name of the command to install.
        target: Installation target.
        force: Whether to overwrite existing files.

    Returns:
        True if successful, False otherwise.
    """
    # Validate command name
    validation_error = validate_command_name(command_name)
    if validation_error:
        show_error(
            validation_error,
            hint="Use only letters, numbers, hyphens, and underscores.",
        )
        return False

    # Load template
    template = load_template(command_name)
    if template is None:
        available = list_available_templates()
        hint = None
        if available:
            hint = f"Available commands: {', '.join(available)}"
        show_error(f"Command '{command_name}' not found.", hint=hint)
        return False

    target_path = target.commands_dir / template.target_filename

    # Check if file exists
    if target_path.exists() and not force:
        overwrite = typer.confirm(
            f"File '{target_path}' already exists. Overwrite?",
            default=False,
        )
        if not overwrite:
            console.print(f"[yellow]Skipped '{command_name}'.[/yellow]")
            return True  # Not a failure, just skipped

    # Write file
    try:
        original_content = template.path.read_text(encoding="utf-8")
        target_path.write_text(original_content, encoding="utf-8")
    except PermissionError:
        show_error(
            f"Cannot write file: {target_path}",
            hint="Check write permissions for the target directory.",
        )
        return False

    console.print(f"[green]Installed[/green] '{command_name}'")
    return True


@app.command()
def init(
    skip_install: bool = typer.Option(
        False,
        "--skip-install",
        "-s",
        help="Skip automatic installation of all available commands.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing files without prompting.",
    ),
) -> None:
    """Initialize a project for context-forge.

    Creates the .claude/ and .claude/commands/ directories for storing
    Claude Code slash commands. By default, installs all available commands.

    Examples:
        context-forge init                  # Initialize and install all commands
        context-forge init --skip-install   # Initialize without installing commands
        context-forge init --force          # Overwrite existing files
    """
    project_root = Path.cwd()
    claude_dir = project_root / ".claude"
    commands_dir = claude_dir / "commands"

    # Track what we created
    created_dirs: list[Path] = []

    try:
        # Create .claude/ directory
        if not claude_dir.exists():
            claude_dir.mkdir(parents=True)
            created_dirs.append(claude_dir)

        # Create .claude/commands/ directory
        if not commands_dir.exists():
            commands_dir.mkdir(parents=True)
            created_dirs.append(commands_dir)
    except PermissionError:
        show_error(
            f"Cannot create directory in: {project_root}",
            hint="Check write permissions for the project directory.",
        )
        raise typer.Exit(EXIT_FILE_ERROR)

    # Success message for directories
    if created_dirs:
        console.print("[green]Success![/green] Initialized context-forge project.")
        console.print("Created directories:")
        for d in created_dirs:
            console.print(f"  - {d.relative_to(project_root)}")
    else:
        console.print(
            "[yellow]Project already initialized.[/yellow] "
            "All required directories exist."
        )

    # Install all available commands by default
    if not skip_install:
        available_commands = list_available_templates()
        if available_commands:
            console.print()  # Blank line before install output
            console.print("Installing commands...")
            target = InstallTarget(project_root=project_root)
            failed_commands: list[str] = []

            for cmd_name in available_commands:
                if not _install_command(cmd_name, target, force):
                    failed_commands.append(cmd_name)

            if failed_commands:
                console.print()
                show_error(
                    f"Failed to install: {', '.join(failed_commands)}",
                    hint="Check the command names and try again.",
                )
                raise typer.Exit(EXIT_ERROR)

            console.print()
            console.print(
                "[dim]Installed commands are available as "
                "'/context-forge.<command>' in Claude Code.[/dim]"
            )
        else:
            console.print(
                "\n[dim]No commands available to install.[/dim]"
            )
    else:
        console.print(
            "\n[dim]You can install commands later with "
            "'context-forge install <command>'[/dim]"
        )


def main() -> None:
    """Entry point for the context-forge CLI."""
    app()
