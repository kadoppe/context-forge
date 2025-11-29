# Implementation Plan: Role Knowledge Plugin Generator

**Branch**: `001-role-knowledge-plugin` | **Date**: 2025-11-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-role-knowledge-plugin/spec.md`

## Summary

チームの職能（ロール）ごとの知見をClaude Codeプラグインとして対話的に作成・更新できるClaude Code Commandを提供する。context-forge CLIでCommandをインストールし、Claude Code内で `/add-role-knowledge` を実行することで、職能プラグインを生成・管理する。

**主要コンポーネント**:
1. `context-forge init` - CLIコマンド（初期化 + 全コマンドを一括インストール）
2. `/context-forge.add-role-knowledge` - Claude Code Command（インストール後に利用可能）
3. 生成される職能プラグイン - `.claude/plugins/{role-name}/`

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Typer (CLI), Rich (terminal UI), PyYAML
**Storage**: ファイルシステム（.claude/plugins/, ~/.cache/context-forge/docs/）
**Testing**: pytest
**Target Platform**: macOS + Linux
**Project Type**: single (CLIツール + コマンドテンプレート)
**Performance Goals**: N/A（CLI操作、即時応答）
**Constraints**: Claude Code プラグイン仕様準拠
**Scale/Scope**: 単一プロジェクト内での使用

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: テスタビリティチェック
- [x] 全ての公開APIにテストが存在するか → 既存CLIパターンに従いテスト作成
- [x] 依存関係はモック/スタブ可能か → ファイルシステム操作は Path で抽象化済み
- [x] 副作用は分離されているか → ファイル書き込みは InstallTarget に集約

### Gate 2: LLM品質チェック
- [x] LLMレビューが実施されたか → Claude Code Command内でLLMが実行
- [x] 評価結果が記録されたか → 生成されたプラグインの検証フロー含む
- [x] 指摘事項に対応したか → N/A（実装前）

### Gate 3: シンプリシティチェック
- [x] 不要な抽象化が導入されていないか → 既存CLIパターンを再利用
- [x] 複雑さの正当化がドキュメントされているか → N/A
- [x] コードは第三者が理解可能か → spec-kitコマンドのパターンを踏襲

### Gate 4: モジュラリティチェック
- [x] モジュールの責務は単一か → CLI（インストール）とCommand（生成）を分離
- [x] 循環依存は存在しないか → 既存構造維持
- [x] モジュール間インターフェースは明確か → CLIはテンプレートを読み込むのみ

### Gate 5: 型安全性チェック
- [x] 静的型チェックがエラーなしで通過するか → mypy対応
- [x] any型やas型アサーションの使用は正当化されているか → 既存パターン維持
- [x] 外部入力の型検証が境界で実装されているか → validate_command_name() パターン

### Gate 6: 最適化チェック
- [x] パフォーマンス最適化は計測データに基づいているか → 最適化不要（CLI操作）
- [x] 最適化前後のベンチマーク結果が記録されているか → N/A
- [x] 可読性を犠牲にした最適化は正当化されているか → N/A

## Project Structure

### Documentation (this feature)

```text
specs/001-role-knowledge-plugin/
├── spec.md              # 機能仕様
├── plan.md              # 本ファイル
├── research.md          # Phase 0 リサーチ結果
├── data-model.md        # データモデル定義
├── quickstart.md        # 開発者向けクイックスタート
├── contracts/           # インターフェース定義
│   ├── cli-interface.md
│   └── command-interface.md
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/
├── context_forge_cli/
│   ├── __init__.py              # 既存CLI実装（install コマンド拡張）
│   └── templates/
│       └── commands/
│           ├── hello-world.md   # 既存
│           └── add-role-knowledge.md  # 新規追加

tests/
├── unit/
│   └── test_cli.py              # 既存テスト拡張
└── integration/
    └── test_install_role_plugin_command.py  # 新規
```

**Structure Decision**: Single project 構造を維持。新規ファイルはテンプレートとテストのみ追加。

## Complexity Tracking

> 憲法違反なし。既存パターンを踏襲し、新規抽象化は導入しない。

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (なし) | - | - |

## Design Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Research | [research.md](./research.md) | Complete |
| Data Model | [data-model.md](./data-model.md) | Complete |
| CLI Interface | [contracts/cli-interface.md](./contracts/cli-interface.md) | Complete |
| Command Interface | [contracts/command-interface.md](./contracts/command-interface.md) | Complete |
| Quickstart | [quickstart.md](./quickstart.md) | Complete |

## Implementation Summary

### Phase 1: コマンドテンプレート追加

1. `templates/commands/add-role-knowledge.md` テンプレート作成
2. 既存 `context-forge init` で自動的にインストール対象として認識
3. `install` コマンドを削除（`init` に統合）
4. インストールテスト追加

### Phase 2: Command実装（`/add-role-knowledge`）

1. 対話フロー実装（ロール選択、知見入力、タイプ判定）
2. 公式ドキュメントフェッチ + キャッシュ機構
3. プラグインファイル生成ロジック
4. 既存プラグイン更新フロー

### 依存関係

```
Phase 1 ─────► Phase 2
(CLI)         (Command)
              └─ 公式ドキュメントの構造に依存
```

## Next Steps

`/speckit.tasks` を実行してタスク分解を行ってください。
