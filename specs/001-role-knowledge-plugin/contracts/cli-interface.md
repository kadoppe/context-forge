# CLI Interface Contract: Role Knowledge Plugin Generator

**Feature**: 001-role-knowledge-plugin
**Date**: 2025-11-29

## Commands

### `context-forge init`

プロジェクトを初期化し、全てのコマンドテンプレート（add-role-knowledgeを含む）をインストールする。

**Synopsis**:
```bash
context-forge init [OPTIONS]
```

**Options**:

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--skip-install` | `-s` | bool | false | コマンドのインストールをスキップ |
| `--force` | `-f` | bool | false | 既存ファイルを確認なしで上書き |
| `--help` | `-h` | bool | false | ヘルプを表示 |

**Behavior**:

1. `.claude/` と `.claude/commands/` ディレクトリを作成
2. テンプレートディレクトリから全ての `.md` ファイルを読み込む
3. 各テンプレートを `context-forge.{name}.md` として保存
4. 既存ファイルがある場合は確認プロンプト（`--force` で省略可）

**Note**: `add-role-knowledge.md` は他のテンプレートと同様に自動的にインストールされる。`install` コマンドは存在せず、`init` コマンドで全てのセットアップが完了する。

**Exit Codes**:

| Code | Constant | Description |
|------|----------|-------------|
| 0 | EXIT_SUCCESS | 正常終了 |
| 1 | EXIT_ERROR | 一般エラー |
| 2 | EXIT_FILE_ERROR | ファイル操作エラー |
| 3 | EXIT_USER_CANCEL | ユーザーキャンセル |

**Output Examples**:

Success:
```
Success! Initialized context-forge project.
Created directories:
  - .claude
  - .claude/commands

Installing commands...
Installed 'hello-world'
Installed 'add-role-knowledge'

Installed commands are available as '/context-forge.<command>' in Claude Code.
```

Error (file exists):
```
File '.claude/commands/context-forge.add-role-knowledge.md' already exists. Overwrite? [y/N]
```

Error (no templates):
```
No commands available to install.
```

---

## Template Structure

### Source Template Location

```
src/context_forge_cli/templates/commands/add-role-knowledge.md
```

### Target Installation Location

```
{project-root}/.claude/commands/context-forge.add-role-knowledge.md
```

---

## Integration Points

### Existing CLI Functions to Reuse

| Function | Location | Purpose |
|----------|----------|---------|
| `validate_command_name()` | `__init__.py` | コマンド名検証 |
| `load_template()` | `__init__.py` | テンプレート読み込み |
| `InstallTarget` | `__init__.py` | インストール先管理 |
| `show_error()` | `__init__.py` | エラー表示 |

### New Functions Required

| Function | Purpose |
|----------|---------|
| (none) | 既存パターンで対応可能 |

---

## Error Handling

| Scenario | Response |
|----------|----------|
| テンプレートが見つからない | EXIT_ERROR + 利用可能コマンド一覧表示 |
| 書き込み権限なし | EXIT_FILE_ERROR + 権限確認ヒント |
| ユーザーが上書きを拒否 | EXIT_USER_CANCEL + キャンセルメッセージ |
| ディレクトリ作成失敗 | EXIT_FILE_ERROR + 権限確認ヒント |
