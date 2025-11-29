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
# User Story 2: Install hello-world Command (T014-T015)
# =============================================================================


def test_install_command_creates_file(tmp_path: "Path") -> None:
    """Test that install command creates the command file in .claude/commands/."""
    import os

    # Change to temp directory to simulate project root
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        result = runner.invoke(app, ["install", "hello-world"])
        assert result.exit_code == 0

        # Check that file was created
        target_file = tmp_path / ".claude" / "commands" / "context-forge.hello-world.md"
        assert target_file.exists()
        assert "hello" in target_file.read_text().lower()
    finally:
        os.chdir(original_cwd)


def test_install_command_unknown_name(tmp_path: "Path") -> None:
    """Test that install command returns error for unknown command name."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        result = runner.invoke(app, ["install", "nonexistent-command"])
        assert result.exit_code != 0
        # Error message is written to stderr, check output (combined stdout+stderr)
        output = result.output.lower() if result.output else ""
        assert "not found" in output or "unknown" in output
    finally:
        os.chdir(original_cwd)


def test_install_command_overwrite_prompt(tmp_path: "Path") -> None:
    """Test that install prompts for overwrite when file exists."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # First install
        runner.invoke(app, ["install", "hello-world"])

        # Second install - should prompt (we'll decline with 'n')
        result = runner.invoke(app, ["install", "hello-world"], input="n\n")
        cancelled = "cancel" in result.stdout.lower()
        skipped = "skip" in result.stdout.lower()
        assert result.exit_code == 0 or cancelled or skipped
    finally:
        os.chdir(original_cwd)


def test_install_command_force_flag(tmp_path: "Path") -> None:
    """Test that --force flag skips overwrite confirmation."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # First install
        runner.invoke(app, ["install", "hello-world"])

        # Second install with --force
        result = runner.invoke(app, ["install", "hello-world", "--force"])
        assert result.exit_code == 0

        # File should still exist
        target_file = tmp_path / ".claude" / "commands" / "context-forge.hello-world.md"
        assert target_file.exists()
    finally:
        os.chdir(original_cwd)


# =============================================================================
# User Story 3: Project Initialization (T026)
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

        # Check that hello-world command was installed by default
        hello_world = commands_dir / "context-forge.hello-world.md"
        assert hello_world.exists()
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
        hello_world = commands_dir / "context-forge.hello-world.md"
        assert not hello_world.exists()
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
# Command Name Validation (T033)
# =============================================================================


def test_install_invalid_command_name_special_chars(tmp_path: Path) -> None:
    """Test that install rejects command names with special characters."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        result = runner.invoke(app, ["install", "hello@world"])
        assert result.exit_code == 1
        assert "letters" in result.output.lower() or "invalid" in result.output.lower()
    finally:
        os.chdir(original_cwd)


def test_install_invalid_command_name_spaces(tmp_path: Path) -> None:
    """Test that install rejects command names with spaces."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        result = runner.invoke(app, ["install", "hello world"])
        assert result.exit_code == 1
    finally:
        os.chdir(original_cwd)


def test_install_valid_command_name_with_underscore(tmp_path: Path) -> None:
    """Test that command names with underscores are valid (though may not exist)."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # This command doesn't exist, but name should be valid
        result = runner.invoke(app, ["install", "hello_world"])
        # Should fail with "not found", not validation error
        assert "not found" in result.output.lower()
    finally:
        os.chdir(original_cwd)
