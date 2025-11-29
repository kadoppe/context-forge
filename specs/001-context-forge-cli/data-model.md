# Data Model: context-forge CLI

**Date**: 2025-11-29
**Branch**: `001-context-forge-cli`

## Entities

### 1. Command

インストール可能なコマンドテンプレートを表す。

```
Command
├── name: str                    # コマンド名（例: "hello-world"）
├── description: str             # コマンドの説明
├── content: str                 # Markdown 本文（プロンプトテンプレート）
└── metadata: dict[str, Any]     # YAML frontmatter から抽出したメタデータ
```

**Validation rules**:
- `name` は英数字、ハイフン、アンダースコアのみ許可
- `name` は空文字不可、64文字以下
- `content` は空文字不可

**State transitions**: N/A（静的エンティティ）

### 2. CommandTemplate

パッケージに同梱されるコマンドテンプレートファイル。

```
CommandTemplate
├── path: Path                   # パッケージ内のファイルパス
├── command: Command             # パース済みのコマンドデータ
└── target_filename: str         # インストール先ファイル名（context-forge.{name}.md）
```

**Built-in templates**:
| Name | File | Target |
|------|------|--------|
| hello-world | templates/commands/hello-world.md | context-forge.hello-world.md |

### 3. InstallTarget

コマンドのインストール先を表す。

```
InstallTarget
├── project_root: Path           # プロジェクトルートディレクトリ
├── commands_dir: Path           # コマンドディレクトリ（.claude/commands/）
└── exists: bool                 # ディレクトリが既に存在するか
```

**Derived paths**:
- `commands_dir = project_root / ".claude" / "commands"`

### 4. InstallResult

インストール操作の結果を表す。

```
InstallResult
├── success: bool                # 成功したか
├── command_name: str            # インストールしたコマンド名
├── target_path: Path            # インストール先パス
├── overwritten: bool            # 上書きしたか
└── error: str | None            # エラーメッセージ（失敗時）
```

## Relationships

```
┌─────────────────┐
│ CommandTemplate │
│                 │
│  - path         │
│  - command ─────┼──────┐
│  - target_name  │      │
└─────────────────┘      │
                         ▼
                  ┌─────────────┐
                  │   Command   │
                  │             │
                  │  - name     │
                  │  - desc     │
                  │  - content  │
                  │  - metadata │
                  └─────────────┘

┌─────────────────┐         ┌─────────────────┐
│  InstallTarget  │         │  InstallResult  │
│                 │         │                 │
│  - project_root │────────▶│  - success      │
│  - commands_dir │ install │  - command_name │
│  - exists       │         │  - target_path  │
└─────────────────┘         │  - overwritten  │
                            │  - error        │
                            └─────────────────┘
```

## Data Flow

### Install Command Flow

```
1. User invokes: context-forge install hello-world
                        │
                        ▼
2. Load CommandTemplate from package
   └── Parse YAML frontmatter + Markdown content
                        │
                        ▼
3. Determine InstallTarget
   └── project_root = cwd()
   └── commands_dir = project_root/.claude/commands/
                        │
                        ▼
4. Check existing file
   └── If exists: prompt for overwrite confirmation
                        │
                        ▼
5. Write file
   └── Create directories if needed
   └── Write content to target_path
                        │
                        ▼
6. Return InstallResult
```

## File Format

### Command Template (Markdown with YAML frontmatter)

```markdown
---
description: コマンドの説明文
arguments:
  - name: arg1
    description: 引数の説明
    required: false
---

コマンドの本文（プロンプトテンプレート）

$ARGUMENTS は Claude Code によって実際の引数に置換されます。
```

### Installed Command (`.claude/commands/context-forge.*.md`)

テンプレートと同一形式。`context-forge.` 接頭辞がファイル名に付与される。

## Type Definitions (Python)

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Any

@dataclass
class Command:
    name: str
    description: str
    content: str
    metadata: dict[str, Any]

@dataclass
class CommandTemplate:
    path: Path
    command: Command

    @property
    def target_filename(self) -> str:
        return f"context-forge.{self.command.name}.md"

@dataclass
class InstallTarget:
    project_root: Path

    @property
    def commands_dir(self) -> Path:
        return self.project_root / ".claude" / "commands"

    @property
    def exists(self) -> bool:
        return self.commands_dir.exists()

@dataclass
class InstallResult:
    success: bool
    command_name: str
    target_path: Path
    overwritten: bool = False
    error: str | None = None
```
