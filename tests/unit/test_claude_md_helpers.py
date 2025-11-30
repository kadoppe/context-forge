"""Unit tests for CLAUDE.md helper functions."""

from pathlib import Path

from context_forge_cli import (
    CLAUDE_MD_END_MARKER,
    CLAUDE_MD_START_MARKER,
    CONTEXT_FORGE_MD_REFERENCE,
    read_claude_md,
    write_claude_md_reference,
)


class TestReadClaudeMd:
    """Tests for read_claude_md function."""

    def test_returns_none_when_file_not_exists(self, tmp_path: Path) -> None:
        """Should return None when CLAUDE.md doesn't exist."""
        result = read_claude_md(tmp_path)
        assert result is None

    def test_reads_empty_file(self, tmp_path: Path) -> None:
        """Should read empty CLAUDE.md file."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("", encoding="utf-8")

        result = read_claude_md(tmp_path)

        assert result is not None
        assert result.full_content == ""
        assert result.has_reference is False
        assert result.reference_start_index is None
        assert result.reference_end_index is None

    def test_reads_file_without_reference(self, tmp_path: Path) -> None:
        """Should read CLAUDE.md without context-forge reference."""
        claude_md = tmp_path / "CLAUDE.md"
        content = "# My Project\n\nSome instructions here.\n"
        claude_md.write_text(content, encoding="utf-8")

        result = read_claude_md(tmp_path)

        assert result is not None
        assert result.full_content == content
        assert result.has_reference is False

    def test_reads_file_with_reference(self, tmp_path: Path) -> None:
        """Should detect existing context-forge reference."""
        claude_md = tmp_path / "CLAUDE.md"
        content = f"""# My Project

Some instructions.

{CLAUDE_MD_START_MARKER}
{CONTEXT_FORGE_MD_REFERENCE}
{CLAUDE_MD_END_MARKER}
"""
        claude_md.write_text(content, encoding="utf-8")

        result = read_claude_md(tmp_path)

        assert result is not None
        assert result.has_reference is True
        assert result.reference_start_index is not None
        assert result.reference_end_index is not None
        assert result.reference_start_index < result.reference_end_index

    def test_detects_invalid_marker_order(self, tmp_path: Path) -> None:
        """Should not detect reference if markers are in wrong order."""
        claude_md = tmp_path / "CLAUDE.md"
        content = f"""{CLAUDE_MD_END_MARKER}
{CONTEXT_FORGE_MD_REFERENCE}
{CLAUDE_MD_START_MARKER}
"""
        claude_md.write_text(content, encoding="utf-8")

        result = read_claude_md(tmp_path)

        assert result is not None
        assert result.has_reference is False


class TestWriteClaudeMdReference:
    """Tests for write_claude_md_reference function."""

    def test_creates_new_file_when_none_exists(self, tmp_path: Path) -> None:
        """Should create new CLAUDE.md with reference when file doesn't exist."""
        result = write_claude_md_reference(tmp_path, None)

        assert result is True
        claude_md = tmp_path / "CLAUDE.md"
        assert claude_md.exists()

        content = claude_md.read_text(encoding="utf-8")
        assert CLAUDE_MD_START_MARKER in content
        assert CONTEXT_FORGE_MD_REFERENCE in content
        assert CLAUDE_MD_END_MARKER in content

    def test_appends_to_existing_file(self, tmp_path: Path) -> None:
        """Should append reference to existing CLAUDE.md."""
        claude_md = tmp_path / "CLAUDE.md"
        original_content = "# My Project\n\nSome instructions.\n"
        claude_md.write_text(original_content, encoding="utf-8")

        existing = read_claude_md(tmp_path)
        result = write_claude_md_reference(tmp_path, existing)

        assert result is True
        content = claude_md.read_text(encoding="utf-8")
        assert original_content.strip() in content
        assert CLAUDE_MD_START_MARKER in content
        assert CONTEXT_FORGE_MD_REFERENCE in content

    def test_skips_if_reference_already_exists(self, tmp_path: Path) -> None:
        """Should return False and not modify file if reference exists."""
        claude_md = tmp_path / "CLAUDE.md"
        content = f"""# My Project

{CLAUDE_MD_START_MARKER}
{CONTEXT_FORGE_MD_REFERENCE}
{CLAUDE_MD_END_MARKER}
"""
        claude_md.write_text(content, encoding="utf-8")

        existing = read_claude_md(tmp_path)
        result = write_claude_md_reference(tmp_path, existing)

        assert result is False
        # Content should be unchanged
        assert claude_md.read_text(encoding="utf-8") == content

    def test_handles_file_without_trailing_newline(self, tmp_path: Path) -> None:
        """Should properly handle files without trailing newline."""
        claude_md = tmp_path / "CLAUDE.md"
        original_content = "# My Project"  # No trailing newline
        claude_md.write_text(original_content, encoding="utf-8")

        existing = read_claude_md(tmp_path)
        write_claude_md_reference(tmp_path, existing)

        content = claude_md.read_text(encoding="utf-8")
        # Should have proper separation
        assert "# My Project\n\n" in content
