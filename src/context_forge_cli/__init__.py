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

# CLAUDE.md reference markers for context-forge settings
CLAUDE_MD_START_MARKER = "<!-- context-forge settings -->"
CLAUDE_MD_END_MARKER = "<!-- end context-forge settings -->"
CONTEXT_FORGE_MD_REFERENCE = "@.claude/context-forge.md"
CONTEXT_FORGE_MD_PATH = ".claude/context-forge.md"

# Role section markers for context-forge.md parsing
ROLE_HEADER_PREFIX = "### "
ROLE_HEADER_SUFFIX = " ロール"

# Rich console for output
console = Console()
err_console = Console(stderr=True)


# =============================================================================
# CLAUDE.md Helpers (T004-T005)
# =============================================================================


# Patterns to detect legacy context-forge settings in CLAUDE.md
LEGACY_CONTEXT_FORGE_PATTERNS = [
    r"context-forge",
    r"@\.claude/plugins/context-forge\.role-",
    r"Skill/SubAgent\s*発動",
]


@dataclass
class ClaudeMdContent:
    """Represents parsed CLAUDE.md content with context-forge reference info."""

    full_content: str
    has_reference: bool
    reference_start_index: int | None = None
    reference_end_index: int | None = None
    has_legacy_settings: bool = False
    legacy_settings_content: str | None = None


def read_claude_md(project_root: Path) -> ClaudeMdContent | None:
    """Read and parse CLAUDE.md content.

    Args:
        project_root: Path to the project root directory.

    Returns:
        ClaudeMdContent if file exists and was read successfully,
        None if file doesn't exist.
        Raises IOError on permission errors.
    """
    claude_md_path = project_root / "CLAUDE.md"

    if not claude_md_path.exists():
        return None

    content = claude_md_path.read_text(encoding="utf-8")

    # Check for existing context-forge reference
    start_idx = content.find(CLAUDE_MD_START_MARKER)
    end_idx = content.find(CLAUDE_MD_END_MARKER)

    has_reference = start_idx != -1 and end_idx != -1 and end_idx > start_idx

    # T025: Detect legacy context-forge settings (outside of the reference block)
    has_legacy_settings = False
    legacy_settings_content = None

    # Content to check for legacy patterns (exclude the reference block if it exists)
    content_to_check = content
    if has_reference:
        # Remove the reference block from the content to check
        end_marker_len = len(CLAUDE_MD_END_MARKER)
        content_to_check = content[:start_idx] + content[end_idx + end_marker_len:]

    for pattern in LEGACY_CONTEXT_FORGE_PATTERNS:
        if re.search(pattern, content_to_check, re.IGNORECASE):
            has_legacy_settings = True
            legacy_settings_content = content_to_check
            break

    ref_end_idx = end_idx + len(CLAUDE_MD_END_MARKER) if has_reference else None
    return ClaudeMdContent(
        full_content=content,
        has_reference=has_reference,
        reference_start_index=start_idx if has_reference else None,
        reference_end_index=ref_end_idx,
        has_legacy_settings=has_legacy_settings,
        legacy_settings_content=legacy_settings_content,
    )


def write_claude_md_reference(
    project_root: Path, claude_md: ClaudeMdContent | None
) -> bool:
    """Add or update context-forge reference in CLAUDE.md.

    Args:
        project_root: Path to the project root directory.
        claude_md: Existing CLAUDE.md content, or None if file doesn't exist.

    Returns:
        True if file was updated/created, False if reference already exists.
        Raises IOError on permission errors.
    """
    claude_md_path = project_root / "CLAUDE.md"

    reference_block = f"""{CLAUDE_MD_START_MARKER}
{CONTEXT_FORGE_MD_REFERENCE}
{CLAUDE_MD_END_MARKER}"""

    if claude_md is None:
        # Create new CLAUDE.md with reference
        claude_md_path.write_text(reference_block + "\n", encoding="utf-8")
        return True

    if claude_md.has_reference:
        # Reference already exists
        return False

    # Append reference to existing content
    content = claude_md.full_content
    if not content.endswith("\n"):
        content += "\n"
    content += "\n" + reference_block + "\n"

    claude_md_path.write_text(content, encoding="utf-8")
    return True


# =============================================================================
# context-forge.md Helpers (T006-T007)
# =============================================================================


@dataclass
class ContextForgeMdContent:
    """Represents parsed .claude/context-forge.md content."""

    full_content: str
    roles: dict[str, list[str]]  # role_name -> list of activation rules


def read_context_forge_md(project_root: Path) -> ContextForgeMdContent | None:
    """Read and parse .claude/context-forge.md content.

    Args:
        project_root: Path to the project root directory.

    Returns:
        ContextForgeMdContent if file exists, None if file doesn't exist.
        Raises IOError on permission errors.
    """
    context_forge_md_path = project_root / CONTEXT_FORGE_MD_PATH

    if not context_forge_md_path.exists():
        return None

    content = context_forge_md_path.read_text(encoding="utf-8")

    # Parse roles and their activation rules
    roles: dict[str, list[str]] = {}
    current_role: str | None = None
    current_rules: list[str] = []

    for line in content.split("\n"):
        # Check for role section header: ### {role-name} ロール
        if line.startswith(ROLE_HEADER_PREFIX) and line.endswith(ROLE_HEADER_SUFFIX):
            # Save previous role if exists
            if current_role is not None:
                roles[current_role] = current_rules

            # Extract role name by removing prefix and suffix
            current_role = (
                line[len(ROLE_HEADER_PREFIX):]
                .removesuffix(ROLE_HEADER_SUFFIX)
                .strip()
            )
            current_rules = []
        elif current_role is not None and line.strip().startswith("- "):
            # This is an activation rule
            current_rules.append(line.strip())

    # Save last role
    if current_role is not None:
        roles[current_role] = current_rules

    return ContextForgeMdContent(full_content=content, roles=roles)


def write_context_forge_md(
    project_root: Path,
    existing: ContextForgeMdContent | None,
    role_name: str | None = None,
    activation_rule: str | None = None,
) -> bool:
    """Write or update .claude/context-forge.md content.

    Args:
        project_root: Path to the project root directory.
        existing: Existing content, or None to create from template.
        role_name: Optional role name to add/update activation rule for.
        activation_rule: Optional activation rule to add for the role.

    Returns:
        True if file was created/updated successfully.
        Raises IOError on permission errors.
    """
    context_forge_md_path = project_root / CONTEXT_FORGE_MD_PATH

    # Ensure .claude directory exists
    context_forge_md_path.parent.mkdir(parents=True, exist_ok=True)

    if existing is None:
        # Create from template
        template_content = _get_context_forge_md_template()
        context_forge_md_path.write_text(template_content, encoding="utf-8")
        existing = ContextForgeMdContent(full_content=template_content, roles={})

    if role_name is not None and activation_rule is not None:
        # Add activation rule to role section
        content = existing.full_content
        role_header = f"### {role_name} ロール"

        if role_name in existing.roles:
            # Role section exists, append rule after header
            header_idx = content.find(role_header)
            if header_idx != -1:
                # Find the end of this role's rules (next ### or end of file)
                next_section_idx = content.find("\n### ", header_idx + len(role_header))
                if next_section_idx == -1:
                    # Append at end of file
                    if not content.endswith("\n"):
                        content += "\n"
                    content += f"{activation_rule}\n"
                else:
                    # Insert before next section
                    content = (
                        content[:next_section_idx]
                        + f"{activation_rule}\n"
                        + content[next_section_idx:]
                    )
        else:
            # Create new role section
            if not content.endswith("\n"):
                content += "\n"
            content += f"\n{role_header}\n\n{activation_rule}\n"

        context_forge_md_path.write_text(content, encoding="utf-8")

    return True


def _get_context_forge_md_template() -> str:
    """Get the template content for context-forge.md.

    Returns:
        Template string for context-forge.md.
    """
    return """# context-forge 設定

このファイルは context-forge によって自動生成されます。
手動で編集した内容は、`add-role-knowledge` コマンド実行時に
上書きされる可能性があります。

## Skill/SubAgent 発動ルール

以下のルールに従って、適切な Skill または SubAgent を使用してください。

"""


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
    Claude Code slash commands. Creates .claude/context-forge.md for
    activation rules and adds a reference to CLAUDE.md.
    By default, installs all available commands.

    Examples:
        context-forge init                  # Initialize and install all commands
        context-forge init --skip-install   # Initialize without installing commands
        context-forge init --force          # Overwrite existing files
    """
    project_root = Path.cwd()
    claude_dir = project_root / ".claude"
    commands_dir = claude_dir / "commands"

    # Track what we created/updated
    created_dirs: list[Path] = []
    created_files: list[Path] = []
    updated_files: list[Path] = []

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

    # T009: Create .claude/context-forge.md if not exists
    context_forge_md_path = project_root / CONTEXT_FORGE_MD_PATH
    context_forge_existing = read_context_forge_md(project_root)

    if context_forge_existing is None:
        try:
            write_context_forge_md(project_root, None)
            created_files.append(context_forge_md_path)
        except PermissionError:
            show_error(
                f"Cannot write file: {context_forge_md_path}",
                hint="Check write permissions for the .claude directory.",
            )
            raise typer.Exit(EXIT_FILE_ERROR)

    # T010-T012: Add @ reference to CLAUDE.md with markers
    claude_md = read_claude_md(project_root)

    # T025-T027: Migration detection and handling
    if claude_md is not None and claude_md.has_legacy_settings:
        # T026: Confirmation prompt for migration
        console.print()
        console.print(
            "[yellow]既存の context-forge 設定が CLAUDE.md で検出されました。[/yellow]"
        )
        migrate = typer.confirm(
            "既存の設定を .claude/context-forge.md に移行しますか？",
            default=True,
        )
        if migrate:
            # T027: Migration - add reference and inform user about manual steps
            # Note: Full content migration is not implemented due to parsing
            # complexity. Users need to manually move activation rules.
            console.print()
            console.print(
                "[yellow]注意: @ 参照は自動で追加されますが、"
                "発動ルールの移行は手動で行ってください。[/yellow]"
            )
            console.print(
                "[dim]CLAUDE.md 内の context-forge 関連の設定を "
                ".claude/context-forge.md にコピーしてください。[/dim]"
            )

    try:
        if claude_md is None:
            # T011: CLAUDE.md does not exist - create new file with reference
            write_claude_md_reference(project_root, None)
            created_files.append(project_root / "CLAUDE.md")
        elif not claude_md.has_reference:
            # Reference doesn't exist - add it
            write_claude_md_reference(project_root, claude_md)
            updated_files.append(project_root / "CLAUDE.md")
        # T012: Reference already exists - skip (no action needed)
    except PermissionError:
        show_error(
            f"Cannot write file: {project_root / 'CLAUDE.md'}",
            hint="Check write permissions for the project directory.",
        )
        raise typer.Exit(EXIT_FILE_ERROR)

    # T028: Warning when context-forge.md is missing but @ reference exists
    has_ref = claude_md is not None and claude_md.has_reference
    if has_ref and context_forge_existing is None:
        console.print()
        console.print(
            "[yellow]警告: CLAUDE.md に @ 参照がありますが、"
            ".claude/context-forge.md が見つかりません。[/yellow]"
        )
        console.print("[dim]新しい context-forge.md を作成しました。[/dim]")

    # T013: Success message showing created/updated files
    if created_dirs or created_files or updated_files:
        console.print("[green]Success![/green] Initialized context-forge project.")

        if created_dirs:
            console.print("Created directories:")
            for d in created_dirs:
                console.print(f"  - {d.relative_to(project_root)}")

        if created_files:
            console.print("\nCreated files:")
            for f in created_files:
                console.print(f"  - {f.relative_to(project_root)}")

        if updated_files:
            console.print("\nUpdated files:")
            for f in updated_files:
                desc = ""
                if f.name == "CLAUDE.md":
                    desc = f" (added {CONTEXT_FORGE_MD_REFERENCE} reference)"
                console.print(f"  - {f.relative_to(project_root)}{desc}")
    else:
        console.print(
            "[yellow]Project already initialized.[/yellow] "
            "All required directories and files exist."
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
            "\n[dim]You can install commands later by running "
            "'context-forge init' without --skip-install.[/dim]"
        )


def main() -> None:
    """Entry point for the context-forge CLI."""
    app()
