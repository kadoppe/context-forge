"""Unit tests for context-forge.md helper functions."""

from pathlib import Path

import pytest

from context_forge_cli import (
    CONTEXT_FORGE_MD_PATH,
    read_context_forge_md,
    write_context_forge_md,
)


class TestReadContextForgeMd:
    """Tests for read_context_forge_md function."""

    def test_returns_none_when_file_not_exists(self, tmp_path: Path) -> None:
        """Should return None when .claude/context-forge.md doesn't exist."""
        result = read_context_forge_md(tmp_path)
        assert result is None

    def test_reads_empty_file(self, tmp_path: Path) -> None:
        """Should read empty context-forge.md file."""
        context_forge_md = tmp_path / CONTEXT_FORGE_MD_PATH
        context_forge_md.parent.mkdir(parents=True, exist_ok=True)
        context_forge_md.write_text("", encoding="utf-8")

        result = read_context_forge_md(tmp_path)

        assert result is not None
        assert result.full_content == ""
        assert result.roles == {}

    def test_reads_file_without_roles(self, tmp_path: Path) -> None:
        """Should read context-forge.md without any role sections."""
        context_forge_md = tmp_path / CONTEXT_FORGE_MD_PATH
        context_forge_md.parent.mkdir(parents=True, exist_ok=True)
        content = """# context-forge 設定

## Skill/SubAgent 発動ルール

以下のルールに従って、適切な Skill または SubAgent を使用してください。
"""
        context_forge_md.write_text(content, encoding="utf-8")

        result = read_context_forge_md(tmp_path)

        assert result is not None
        assert result.roles == {}

    def test_parses_single_role_with_rules(self, tmp_path: Path) -> None:
        """Should parse a single role with activation rules."""
        context_forge_md = tmp_path / CONTEXT_FORGE_MD_PATH
        context_forge_md.parent.mkdir(parents=True, exist_ok=True)
        content = """# context-forge 設定

## Skill/SubAgent 発動ルール

### software-engineer ロール

- ユーザーが「PRをレビューして」と言った場合、Task ツールで pr-review-assistant を使用すること
- ユーザーが「コードレビュー」と言った場合、Task ツールで pr-review-assistant を使用すること
"""
        context_forge_md.write_text(content, encoding="utf-8")

        result = read_context_forge_md(tmp_path)

        assert result is not None
        assert "software-engineer" in result.roles
        assert len(result.roles["software-engineer"]) == 2

    def test_parses_multiple_roles(self, tmp_path: Path) -> None:
        """Should parse multiple roles with their activation rules."""
        context_forge_md = tmp_path / CONTEXT_FORGE_MD_PATH
        context_forge_md.parent.mkdir(parents=True, exist_ok=True)
        content = """# context-forge 設定

## Skill/SubAgent 発動ルール

### software-engineer ロール

- ユーザーが「PRをレビューして」と言った場合、Task ツールで pr-review-assistant を使用すること

### frontend-engineer ロール

- ユーザーが「Reactのベストプラクティス」と言った場合、Skill を参照すること
- ユーザーが「コンポーネントの書き方」と言った場合、Skill を参照すること
"""
        context_forge_md.write_text(content, encoding="utf-8")

        result = read_context_forge_md(tmp_path)

        assert result is not None
        assert len(result.roles) == 2
        assert "software-engineer" in result.roles
        assert "frontend-engineer" in result.roles
        assert len(result.roles["software-engineer"]) == 1
        assert len(result.roles["frontend-engineer"]) == 2


class TestWriteContextForgeMd:
    """Tests for write_context_forge_md function."""

    def test_creates_file_from_template(self, tmp_path: Path) -> None:
        """Should create context-forge.md from template when file doesn't exist."""
        result = write_context_forge_md(tmp_path, None)

        assert result is True
        context_forge_md = tmp_path / CONTEXT_FORGE_MD_PATH
        assert context_forge_md.exists()

        content = context_forge_md.read_text(encoding="utf-8")
        assert "# context-forge 設定" in content
        assert "## Skill/SubAgent 発動ルール" in content

    def test_creates_claude_directory_if_needed(self, tmp_path: Path) -> None:
        """Should create .claude directory if it doesn't exist."""
        claude_dir = tmp_path / ".claude"
        assert not claude_dir.exists()

        write_context_forge_md(tmp_path, None)

        assert claude_dir.exists()

    def test_adds_new_role_section(self, tmp_path: Path) -> None:
        """Should add a new role section with activation rule."""
        # First create the template
        write_context_forge_md(tmp_path, None)

        # Read existing content
        existing = read_context_forge_md(tmp_path)

        # Add a role with activation rule
        rule = "- ユーザーが「PRをレビューして」と言った場合、Task ツールで pr-review-assistant を使用すること"
        write_context_forge_md(tmp_path, existing, "software-engineer", rule)

        # Read and verify
        result = read_context_forge_md(tmp_path)
        assert result is not None
        assert "software-engineer" in result.roles
        assert len(result.roles["software-engineer"]) == 1

        content = (tmp_path / CONTEXT_FORGE_MD_PATH).read_text(encoding="utf-8")
        assert "### software-engineer ロール" in content
        assert rule in content

    def test_appends_rule_to_existing_role(self, tmp_path: Path) -> None:
        """Should append a rule to an existing role section."""
        context_forge_md = tmp_path / CONTEXT_FORGE_MD_PATH
        context_forge_md.parent.mkdir(parents=True, exist_ok=True)
        initial_content = """# context-forge 設定

## Skill/SubAgent 発動ルール

### software-engineer ロール

- ユーザーが「PRをレビューして」と言った場合、Task ツールで pr-review-assistant を使用すること
"""
        context_forge_md.write_text(initial_content, encoding="utf-8")

        existing = read_context_forge_md(tmp_path)
        new_rule = "- ユーザーが「コードレビュー」と言った場合、Task ツールで code-reviewer を使用すること"
        write_context_forge_md(tmp_path, existing, "software-engineer", new_rule)

        result = read_context_forge_md(tmp_path)
        assert result is not None
        assert len(result.roles["software-engineer"]) == 2

    def test_adds_second_role_without_breaking_first(self, tmp_path: Path) -> None:
        """Should add a second role while preserving the first."""
        context_forge_md = tmp_path / CONTEXT_FORGE_MD_PATH
        context_forge_md.parent.mkdir(parents=True, exist_ok=True)
        initial_content = """# context-forge 設定

## Skill/SubAgent 発動ルール

### software-engineer ロール

- ユーザーが「PRをレビューして」と言った場合、Task ツールで pr-review-assistant を使用すること
"""
        context_forge_md.write_text(initial_content, encoding="utf-8")

        existing = read_context_forge_md(tmp_path)
        new_rule = "- ユーザーが「Reactのベストプラクティス」と言った場合、Skill を参照すること"
        write_context_forge_md(tmp_path, existing, "frontend-engineer", new_rule)

        result = read_context_forge_md(tmp_path)
        assert result is not None
        assert len(result.roles) == 2
        assert "software-engineer" in result.roles
        assert "frontend-engineer" in result.roles
        assert len(result.roles["software-engineer"]) == 1
        assert len(result.roles["frontend-engineer"]) == 1

    def test_no_modification_when_no_role_provided(self, tmp_path: Path) -> None:
        """Should create template but not add role section when role_name is None."""
        write_context_forge_md(tmp_path, None)

        result = read_context_forge_md(tmp_path)
        assert result is not None
        assert result.roles == {}
