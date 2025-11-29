# Research: context-forge CLI 初期実装

**Date**: 2025-11-29
**Branch**: `001-context-forge-cli`

## 1. CLI フレームワーク選定

### Decision: Typer + Rich

**Rationale**:
- spec-kit が採用している実績のある組み合わせ
- Typer は Python の型ヒントを活用した直感的な CLI 構築が可能
- Rich はリッチなターミナル出力（進捗表示、カラー、パネル）を提供
- 両ライブラリは活発にメンテナンスされている

**Alternatives considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Click | Typer のベースだが、型ヒント活用が劣る |
| argparse | 標準ライブラリだが、UX が貧弱 |
| Fire | シンプルだが、ヘルプ生成やバリデーションが弱い |

## 2. パッケージ構造

### Decision: Single-file CLI with embedded templates

**Rationale**:
- spec-kit と同様に `src/context_forge_cli/__init__.py` に主要ロジックを集約
- 初期実装はシンプルさを優先し、単一ファイル構成
- テンプレート（hello-world コマンド）はパッケージ内のリソースとして同梱
- 将来的な拡張時にモジュール分割可能

**Directory structure**:
```
src/
└── context_forge_cli/
    ├── __init__.py      # CLI エントリポイント + 主要ロジック
    └── templates/
        └── commands/
            └── hello-world.md  # 組み込みコマンドテンプレート
```

**Alternatives considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| 複数モジュール分割 | 初期実装には過剰な複雑さ |
| 外部テンプレートリポジトリ | ネットワーク依存を避けたい |

## 3. パッケージ管理・ビルドシステム

### Decision: Hatchling + uv

**Rationale**:
- spec-kit が採用しているビルドバックエンド
- PEP 517/518 準拠のモダンなビルドシステム
- uv は高速な Python パッケージマネージャー
- `uv tool install` でグローバルインストールが容易

**pyproject.toml 構成**:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "context-forge-cli"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "typer",
    "rich",
]

[project.scripts]
context-forge = "context_forge_cli:main"
```

**Alternatives considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| setuptools | レガシー、設定が冗長 |
| Poetry | 依存関係管理に優れるが、uv の方が高速 |
| Flit | シンプルだが、Hatchling の方が柔軟 |

## 4. コマンドインストール先

### Decision: `.claude/commands/` ディレクトリ

**Rationale**:
- Claude Code の標準的なスラッシュコマンド配置場所
- プロジェクトルートからの相対パス
- ディレクトリが存在しない場合は自動作成

**Installation flow**:
1. カレントディレクトリをプロジェクトルートとして扱う
2. `.claude/commands/` ディレクトリの存在確認・作成
3. テンプレートファイルを `context-forge.{command-name}.md` としてコピー
4. 既存ファイルがある場合は上書き確認

**Alternatives considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| `~/.claude/commands/` (グローバル) | プロジェクト固有のコマンドに適さない |
| 設定ファイルで指定 | 初期実装には過剰 |

## 5. テンプレートファイル形式

### Decision: Markdown with optional YAML frontmatter

**Rationale**:
- Claude Code のスラッシュコマンドは `.md` ファイル
- YAML frontmatter でメタデータ（説明、引数など）を定義可能
- 本文はプロンプトテンプレートとして機能

**hello-world.md 例**:
```markdown
---
description: context-forge のテストコマンド
---

Hello from context-forge! このコマンドは正常にインストールされています。

現在のプロジェクト: $PWD
```

## 6. エラーハンドリング戦略

### Decision: Rich パネルによる詳細エラー表示

**Rationale**:
- spec-kit のパターンを踏襲
- エラー発生時に次のアクションを明示
- 終了コードで自動化スクリプトとの連携を考慮

**Error codes**:
| Code | Meaning |
|------|---------|
| 0 | 成功 |
| 1 | 一般エラー |
| 2 | ファイル操作エラー（権限、存在しない等） |
| 3 | ユーザーキャンセル |

## 7. テスト戦略

### Decision: pytest + typer.testing.CliRunner

**Rationale**:
- Typer 公式のテストユーティリティを活用
- CLI の入出力を統合テストで検証
- ファイルシステム操作は `tmp_path` fixture でテスト

**Test structure**:
```
tests/
├── unit/
│   └── test_templates.py    # テンプレート読み込みのユニットテスト
└── integration/
    └── test_cli.py          # CLI コマンドの統合テスト
```

## 8. 依存関係まとめ

| Package | Version | Purpose |
|---------|---------|---------|
| typer | latest | CLI フレームワーク |
| rich | latest | ターミナル出力装飾 |

**Development dependencies**:
| Package | Purpose |
|---------|---------|
| pytest | テストフレームワーク |
| ruff | リンター・フォーマッター |
| mypy | 静的型チェック |
