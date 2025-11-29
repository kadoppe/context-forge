# Implementation Plan: context-forge CLI 初期実装

**Branch**: `001-context-forge-cli` | **Date**: 2025-11-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-context-forge-cli/spec.md`

## Summary

context-forge は開発者向けの CLI ツールで、AI コーディング支援ツール（Claude Code 等）から参照できるコンテキストを管理する。初期実装では、hello-world コマンドを Claude Code にインストールする機能を提供する。技術スタックは spec-kit を参考に、Python 3.11 + Typer + Rich を採用する。

### CLI Commands

| Command | Description |
|---------|-------------|
| `context-forge --version` | バージョン情報を表示 |
| `context-forge init` | プロジェクトを初期化し、全コマンドをインストール |
| `context-forge init --skip-install` | 初期化のみ（コマンドインストールをスキップ） |
| `context-forge install <cmd>` | コマンドテンプレートをインストール |

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Typer (CLI), Rich (terminal UI)
**Storage**: ファイルシステム（.claude/commands/ ディレクトリ）
**Testing**: pytest + typer.testing.CliRunner
**Target Platform**: macOS, Linux, Windows（クロスプラットフォーム）
**Project Type**: single（CLI ツール）
**Performance Goals**: コマンドインストールが10秒以内に完了
**Constraints**: オフライン動作可能、Python 3.11+ 必須
**Scale/Scope**: 単一ユーザー、ローカルプロジェクト単位
**Localization**: English only (CLI output and command templates)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: テスタビリティチェック
- [x] 全ての公開APIにテストが存在するか → テスト計画策定済み（pytest + CliRunner）
- [x] 依存関係はモック/スタブ可能か → ファイルシステム操作は tmp_path でテスト可能
- [x] 副作用は分離されているか → ファイル操作は InstallTarget/InstallResult で抽象化

### Gate 2: LLM品質チェック
- [ ] LLMレビューが実施されたか → 実装後に実施
- [ ] 評価結果が記録されたか → 実装後に記録
- [ ] 指摘事項に対応したか → 実装後に対応

### Gate 3: シンプリシティチェック
- [x] 不要な抽象化が導入されていないか → 初期実装は単一ファイル構成
- [x] 複雑さの正当化がドキュメントされているか → N/A（複雑な設計なし）
- [x] コードは第三者が理解可能か → spec-kit パターンを踏襲

### Gate 4: モジュラリティチェック
- [x] モジュールの責務は単一か → CLI、テンプレート読み込み、ファイル操作で分離
- [x] 循環依存は存在しないか → データモデルは単方向依存
- [x] モジュール間インターフェースは明確か → dataclass で型定義済み

### Gate 5: 型安全性チェック
- [x] 静的型チェックがエラーなしで通過するか → mypy で検証予定
- [x] any型やas型アサーションの使用は正当化されているか → metadata の dict[str, Any] のみ使用
- [x] 外部入力の型検証が境界で実装されているか → コマンド名バリデーション実装予定

**Result**: Gate 1, 3, 4, 5 はパス。Gate 2 は実装後に完了予定。

## Project Structure

### Documentation (this feature)

```text
specs/001-context-forge-cli/
├── spec.md              # 仕様書
├── plan.md              # このファイル
├── research.md          # Phase 0: 技術調査
├── data-model.md        # Phase 1: データモデル
├── quickstart.md        # Phase 1: クイックスタートガイド
├── checklists/
│   └── requirements.md  # 要件チェックリスト
└── tasks.md             # Phase 2: タスク一覧（/speckit.tasks で生成）
```

### Source Code (repository root)

```text
src/
└── context_forge_cli/
    ├── __init__.py          # CLI エントリポイント + 主要ロジック
    └── templates/
        └── commands/
            └── hello-world.md  # 組み込みコマンドテンプレート

tests/
├── unit/
│   └── test_templates.py    # テンプレート読み込みのユニットテスト
└── integration/
    └── test_cli.py          # CLI コマンドの統合テスト

pyproject.toml               # パッケージ設定
```

**Structure Decision**: Single project 構成を採用。CLI ツールとして最小限の構成で、spec-kit のパターンを踏襲。テンプレートはパッケージリソースとして同梱。

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - 全てのゲートをパス（Gate 2 は実装後に完了予定）

## Phase 0 Output

- [research.md](./research.md) - 技術調査結果

## Phase 1 Output

- [data-model.md](./data-model.md) - データモデル定義
- [quickstart.md](./quickstart.md) - クイックスタートガイド

## Next Steps

1. `/speckit.tasks` を実行してタスク一覧を生成
2. タスクに従って実装を開始
3. 実装完了後に Gate 2（LLM品質チェック）を実施
