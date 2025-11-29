# Quickstart: Role Knowledge Plugin Generator

**Feature**: 001-role-knowledge-plugin
**Date**: 2025-11-29

## Overview

このガイドでは、ロール知見プラグイン機能の開発を始めるための手順を説明します。

## Prerequisites

- Python 3.11+
- uv (パッケージマネージャー)
- Claude Code がインストール済み

## Development Setup

### 1. 依存関係のインストール

```bash
cd /Users/kadoppe/Sources/github.com/kadoppe/context-forge
uv sync --dev
```

### 2. 既存CLIの動作確認

```bash
uv run context-forge --version
uv run context-forge init
```

## Implementation Tasks

### Task 1: コマンドテンプレートの作成

新しいテンプレートファイルを作成:

```bash
# テンプレートディレクトリ
src/context_forge_cli/templates/commands/add-role-knowledge.md
```

**内容の参考**: `.claude/commands/speckit.specify.md` のパターンを参照

### Task 2: テンプレートの登録

`list_available_templates()` で新しいテンプレートが認識されることを確認:

```python
# テスト
from context_forge_cli import list_available_templates
assert "add-role-knowledge" in list_available_templates()
```

### Task 3: インストールテスト

```bash
uv run context-forge init
cat .claude/commands/context-forge.add-role-knowledge.md
```

## Testing

### Unit Tests

```bash
uv run pytest tests/ -v
```

### Manual Testing

1. テストプロジェクトで `context-forge init` を実行（全コマンドがインストールされる）
2. Claude Code で `/context-forge.add-role-knowledge` を実行
3. 対話フローを確認

## Key Files

| File | Purpose |
|------|---------|
| `src/context_forge_cli/__init__.py` | CLI実装（Typer） |
| `src/context_forge_cli/templates/commands/` | コマンドテンプレート |
| `.claude/commands/speckit.*.md` | 参考実装（spec-kit） |

## Architecture Notes

### CLI → Command Flow

```
context-forge init
         │
         ▼
┌─────────────────────────────────────────┐
│ list_available_templates()              │
│ → ["hello-world", "add-role-knowledge"] │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ load_template() for each template       │
│ → templates/commands/*.md               │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ InstallTarget.commands_dir              │
│ → .claude/commands/                     │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ Write all templates:                    │
│ context-forge.{name}.md                 │
└─────────────────────────────────────────┘
```

### Generated Plugin Structure

```
.claude/plugins/{role-name}/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── {knowledge}.md
├── agents/
│   └── {knowledge}.md
├── skills/
│   └── {knowledge}/
│       └── SKILL.md
└── hooks/
    └── hooks.json
```

## Next Steps After Implementation

1. `uv run ruff check .` - リントチェック
2. `uv run mypy src` - 型チェック
3. `uv run pytest` - テスト実行
4. 手動でClaude Codeでの動作確認
