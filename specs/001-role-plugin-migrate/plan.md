# Implementation Plan: Role Plugin Migration Command

**Branch**: `001-role-plugin-migrate` | **Date**: 2025-11-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-role-plugin-migrate/spec.md`

## Summary

既存の context-forge role plugin を最新仕様（version 0.0.1）に更新するための migrate コマンドを実装する。これは Claude Code の slash command (`/context-forge.migrate`) として動作し、Claude（LLM）がプラグインを分析・更新する。また、CLI の `context-forge init` コマンドを拡張して、migrate コマンドを含む全ての context-forge.* コマンドファイルをインストールできるようにする。

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Typer (CLI), Rich (terminal UI), PyYAML
**Storage**: ファイルシステム（`.claude/plugins/`, `.claude/commands/`）
**Testing**: pytest
**Target Platform**: Linux, macOS, Windows (cross-platform CLI)
**Project Type**: Single project (CLI + slash commands)
**Performance Goals**: 10プラグイン以下の処理に対応
**Constraints**: Claude Code slash command として実行（LLM による処理）
**Scale/Scope**: ローカルプロジェクト単位での使用

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: テスタビリティチェック
- [x] 全ての公開APIにテストが存在するか → init コマンドの拡張部分にテストを追加
- [x] 依存関係はモック/スタブ可能か → ファイルシステム操作は Path オブジェクト経由で注入可能
- [x] 副作用は分離されているか → ファイル操作は独立したヘルパー関数に分離

### Gate 2: LLM品質チェック
- [x] LLMレビューが実施されたか → migrate コマンドは LLM が実行するため自己レビュー
- [x] 評価結果が記録されたか → マイグレーションレポートで結果を記録
- [x] 指摘事項に対応したか → N/A（新規実装）

### Gate 3: シンプリシティチェック
- [x] 不要な抽象化が導入されていないか → 既存のヘルパー関数パターンを踏襲
- [x] 複雑さの正当化がドキュメントされているか → N/A（シンプルな実装）
- [x] コードは第三者が理解可能か → 既存コードスタイルに従う

### Gate 4: モジュラリティチェック
- [x] モジュールの責務は単一か → init: ファイル配置、migrate.md: プラグイン更新
- [x] 循環依存は存在しないか → N/A（単一モジュール）
- [x] モジュール間インターフェースは明確か → ファイルシステムベースの疎結合

### Gate 5: 型安全性チェック
- [x] 静的型チェックがエラーなしで通過するか → mypy strict モード
- [x] any型やas型アサーションの使用は正当化されているか → 最小限に抑える
- [x] 外部入力の型検証が境界で実装されているか → plugin.json パース時に検証

### Gate 6: 最適化チェック
- [x] パフォーマンス最適化は計測データに基づいているか → N/A（最適化不要）
- [x] 最適化前後のベンチマーク結果が記録されているか → N/A
- [x] 可読性を犠牲にした最適化は正当化されているか → N/A

## Project Structure

### Documentation (this feature)

```text
specs/001-role-plugin-migrate/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A for this feature)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/
└── context_forge_cli/
    ├── __init__.py           # CLI implementation (init コマンド拡張)
    └── templates/
        └── commands/
            ├── add-role-knowledge.md  # 既存
            └── migrate.md             # 新規追加

.claude/
└── commands/
    └── context-forge.migrate.md  # インストール後のコマンドファイル
```

**Structure Decision**: 既存の single project 構造を維持。migrate.md は templates/commands/ に追加し、init コマンドでインストールされる。

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

該当なし - すべてのゲートをパス
