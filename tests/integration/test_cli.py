"""Integration tests for context-forge CLI."""

from pathlib import Path

from typer.testing import CliRunner

from context_forge_cli import (
    CLAUDE_MD_END_MARKER,
    CLAUDE_MD_START_MARKER,
    CONTEXT_FORGE_MD_PATH,
    CONTEXT_FORGE_MD_REFERENCE,
    __version__,
    app,
)

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


# =============================================================================
# User Story 2: CLAUDE.md 肥大化防止 (T009-T013a)
# =============================================================================


def test_init_creates_context_forge_md(tmp_path: Path) -> None:
    """Test that init creates .claude/context-forge.md file."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        result = runner.invoke(app, ["init", "--skip-install"])
        assert result.exit_code == 0

        # Check that context-forge.md was created
        context_forge_md = tmp_path / CONTEXT_FORGE_MD_PATH
        assert context_forge_md.exists()

        # Check content
        content = context_forge_md.read_text(encoding="utf-8")
        assert "# context-forge 設定" in content
        assert "## Skill/SubAgent 発動ルール" in content
    finally:
        os.chdir(original_cwd)


def test_init_creates_claude_md_with_reference_when_not_exists(tmp_path: Path) -> None:
    """Test that init creates CLAUDE.md with @ reference when file doesn't exist."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        result = runner.invoke(app, ["init", "--skip-install"])
        assert result.exit_code == 0

        # Check that CLAUDE.md was created
        claude_md = tmp_path / "CLAUDE.md"
        assert claude_md.exists()

        # Check content contains reference
        content = claude_md.read_text(encoding="utf-8")
        assert CLAUDE_MD_START_MARKER in content
        assert CONTEXT_FORGE_MD_REFERENCE in content
        assert CLAUDE_MD_END_MARKER in content
    finally:
        os.chdir(original_cwd)


def test_init_adds_reference_to_existing_claude_md(tmp_path: Path) -> None:
    """Test that init adds @ reference to existing CLAUDE.md."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # Create existing CLAUDE.md
        claude_md = tmp_path / "CLAUDE.md"
        original_content = "# My Project\n\nSome instructions here.\n"
        claude_md.write_text(original_content, encoding="utf-8")

        result = runner.invoke(app, ["init", "--skip-install"])
        assert result.exit_code == 0

        # Check content
        content = claude_md.read_text(encoding="utf-8")
        # Original content should be preserved
        assert "# My Project" in content
        assert "Some instructions here." in content
        # Reference should be added
        assert CLAUDE_MD_START_MARKER in content
        assert CONTEXT_FORGE_MD_REFERENCE in content
        assert CLAUDE_MD_END_MARKER in content
    finally:
        os.chdir(original_cwd)


def test_init_skips_adding_duplicate_reference(tmp_path: Path) -> None:
    """Test that init doesn't add duplicate reference to CLAUDE.md."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # Create existing CLAUDE.md with reference
        claude_md = tmp_path / "CLAUDE.md"
        original_content = f"""# My Project

{CLAUDE_MD_START_MARKER}
{CONTEXT_FORGE_MD_REFERENCE}
{CLAUDE_MD_END_MARKER}
"""
        claude_md.write_text(original_content, encoding="utf-8")

        # Also create context-forge.md
        (tmp_path / ".claude").mkdir(parents=True, exist_ok=True)
        (tmp_path / CONTEXT_FORGE_MD_PATH).write_text("# test", encoding="utf-8")

        result = runner.invoke(app, ["init", "--skip-install"])
        assert result.exit_code == 0

        # Check that content is unchanged (no duplicate reference)
        content = claude_md.read_text(encoding="utf-8")
        # Count occurrences of the reference
        assert content.count(CONTEXT_FORGE_MD_REFERENCE) == 1
    finally:
        os.chdir(original_cwd)


def test_init_output_shows_created_files(tmp_path: Path) -> None:
    """Test that init output shows created files."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        result = runner.invoke(app, ["init", "--skip-install"])
        assert result.exit_code == 0

        # Check output mentions created files
        assert "context-forge.md" in result.stdout
        assert "CLAUDE.md" in result.stdout
    finally:
        os.chdir(original_cwd)


def test_claude_md_reference_is_under_10_lines(tmp_path: Path) -> None:
    """Test that CLAUDE.md reference block is under 10 lines (SC-002)."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        result = runner.invoke(app, ["init", "--skip-install"])
        assert result.exit_code == 0

        # Check CLAUDE.md line count
        claude_md = tmp_path / "CLAUDE.md"
        content = claude_md.read_text(encoding="utf-8")
        lines = content.strip().split("\n")

        # CLAUDE.md should have 10 or fewer lines when created fresh
        # (This verifies SC-002: CLAUDE.md reference should be minimal)
        assert len(lines) <= 10, f"CLAUDE.md has {len(lines)} lines, expected <= 10"
    finally:
        os.chdir(original_cwd)
