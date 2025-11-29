# Quickstart: context-forge CLI

**Date**: 2025-11-29
**Branch**: `001-context-forge-cli`

## Prerequisites

- Python 3.11 以上
- uv（推奨）または pip
- Claude Code がインストール済み

## Installation

### Option 1: uv tool install（推奨）

```bash
uv tool install context-forge-cli
```

### Option 2: pip install

```bash
pip install context-forge-cli
```

### Option 3: 開発用インストール

```bash
git clone https://github.com/kadoppe/context-forge.git
cd context-forge
uv pip install -e .
```

## Verify Installation

```bash
context-forge --version
```

Expected output:
```
context-forge-cli v0.1.0
```

## Basic Usage

### 1. Install hello-world command

プロジェクトディレクトリで以下を実行：

```bash
context-forge install hello-world
```

Expected output:
```
✓ Installed context-forge.hello-world to .claude/commands/
```

### 2. Use in Claude Code

Claude Code を起動し、スラッシュコマンドを実行：

```
/context-forge.hello-world
```

Expected result:
```
Hello from context-forge! このコマンドは正常にインストールされています。
```

## Command Reference

### `context-forge --version`

バージョン情報を表示。

```bash
context-forge --version
```

### `context-forge install <command-name>`

指定したコマンドをプロジェクトにインストール。

```bash
context-forge install hello-world
```

Options:
- `--force`, `-f`: 既存ファイルを確認なしで上書き

### `context-forge init`

プロジェクトを context-forge 用に初期化。

```bash
context-forge init
```

Creates:
- `.claude/` directory
- `.claude/commands/` directory

## Directory Structure After Installation

```
your-project/
├── .claude/
│   └── commands/
│       └── context-forge.hello-world.md
└── ... (other project files)
```

## Troubleshooting

### "command not found: context-forge"

uv でインストールした場合、PATH に `~/.local/bin` が含まれているか確認：

```bash
echo $PATH | grep -q "$HOME/.local/bin" && echo "OK" || echo "Add ~/.local/bin to PATH"
```

### "Permission denied" error

`.claude/commands/` ディレクトリへの書き込み権限を確認：

```bash
ls -la .claude/
```

### Overwrite confirmation

既存のコマンドファイルがある場合、上書き確認が表示されます：

```
? File already exists: .claude/commands/context-forge.hello-world.md
  Overwrite? [y/N]
```

`--force` オプションで確認をスキップできます。

## Next Steps

1. `context-forge install hello-world` でインストールを確認
2. `.claude/commands/context-forge.hello-world.md` の内容を確認
3. Claude Code で `/context-forge.hello-world` を実行
4. 独自のコマンドテンプレートを作成（将来の機能拡張予定）
