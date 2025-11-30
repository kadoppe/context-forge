"""Integration tests for context-forge CLI."""

from pathlib import Path

from typer.testing import CliRunner

from context_forge_cli import __version__, app

runner = CliRunner()


# =============================================================================
# User Story 1: CLI Installation & Version (T008-T009)
# =============================================================================


def test_version_option() -> None:
    """Test that --version displays the correct version."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"context-forge-cli v{__version__}" in result.stdout


def test_version_option_short() -> None:
    """Test that -v displays the correct version."""
    result = runner.invoke(app, ["-v"])
    assert result.exit_code == 0
    assert f"context-forge-cli v{__version__}" in result.stdout


def test_help_option() -> None:
    """Test that --help displays help message."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "context-forge" in result.stdout.lower()
    assert "A CLI tool to manage context for AI coding assistants" in result.stdout


# =============================================================================
# User Story 2: Project Initialization (T026)
# =============================================================================


def test_init_command_creates_directories_and_installs(tmp_path: Path) -> None:
    """Test that init creates directories and installs all commands by default."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0

        # Check that directories were created
        claude_dir = tmp_path / ".claude"
        commands_dir = tmp_path / ".claude" / "commands"
        assert claude_dir.exists()
        assert claude_dir.is_dir()
        assert commands_dir.exists()
        assert commands_dir.is_dir()

        # Check that add-role-knowledge command was installed by default
        add_role_knowledge = commands_dir / "context-forge.add-role-knowledge.md"
        assert add_role_knowledge.exists()
        assert "ロール" in add_role_knowledge.read_text()
    finally:
        os.chdir(original_cwd)


def test_init_command_skip_install(tmp_path: Path) -> None:
    """Test that init --skip-install skips command installation."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        result = runner.invoke(app, ["init", "--skip-install"])
        assert result.exit_code == 0

        # Check that directories were created
        commands_dir = tmp_path / ".claude" / "commands"
        assert commands_dir.exists()

        # Check that no commands were installed
        add_role_knowledge = commands_dir / "context-forge.add-role-knowledge.md"
        assert not add_role_knowledge.exists()
    finally:
        os.chdir(original_cwd)


def test_init_command_existing_directory(tmp_path: Path) -> None:
    """Test that init handles existing .claude/ directory."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # Create existing directory
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        # Run init - should succeed and create commands subdirectory
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0

        commands_dir = tmp_path / ".claude" / "commands"
        assert commands_dir.exists()
    finally:
        os.chdir(original_cwd)


# =============================================================================
# Init Command: Overwrite and Force (T033)
# =============================================================================


def test_init_command_overwrite_prompt(tmp_path: Path) -> None:
    """Test that init prompts for overwrite when files exist."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # First init
        runner.invoke(app, ["init"])

        # Second init - should prompt for each file, decline with 'n'
        result = runner.invoke(app, ["init"], input="n\n")
        # Should complete (skipping existing files)
        assert result.exit_code == 0
        assert "Skipped" in result.stdout or "already" in result.stdout.lower()
    finally:
        os.chdir(original_cwd)


def test_init_command_force_flag(tmp_path: Path) -> None:
    """Test that --force flag skips overwrite confirmation."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # First init
        runner.invoke(app, ["init"])

        # Second init with --force
        result = runner.invoke(app, ["init", "--force"])
        assert result.exit_code == 0

        # Files should still exist
        commands_dir = tmp_path / ".claude" / "commands"
        add_role_knowledge = commands_dir / "context-forge.add-role-knowledge.md"
        assert add_role_knowledge.exists()
    finally:
        os.chdir(original_cwd)
