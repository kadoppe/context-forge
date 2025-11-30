# Implementation Plan: Skill/SubAgent 発動率向上

**Branch**: `003-skill-subagent-activation` | **Date**: 2025-11-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-skill-subagent-activation/spec.md`

## Summary

context-forge で追加された Skill/SubAgent の発動率を向上させるため、以下の改善を実装する：

1. **CLAUDE.md の肥大化防止**: 専用ファイル（`.claude/context-forge.md`）を導入し、CLAUDE.md からは `@.claude/context-forge.md` 形式の参照のみを追加
2. **発動条件の明示的記述**: 専用ファイルに「ユーザーが〇〇と言った場合、必ず Task ツールで△△を使用すること」形式のルールを記述
3. **description の改善**: Skill/SubAgent の description に 3 つ以上のトリガー表現パターンを含める
4. **add-role-knowledge コマンドの更新**: 上記の仕組みに対応するようコマンドプロンプトを更新

## Technical Context

**Language/Version**: Python 3.11+ / Markdown (Claude Code プロンプト形式)
**Primary Dependencies**: Typer (CLI), Rich (terminal UI), PyYAML
**Storage**: ファイルシステム（`.claude/` ディレクトリ）
**Testing**: pytest, 手動テスト（Claude Code での発動確認）
**Target Platform**: CLI (macOS, Linux, Windows)
**Project Type**: Single project (CLI + Claude Code plugin)
**Performance Goals**: N/A（パフォーマンス要件なし）
**Constraints**: Claude Code の `@` 記法に準拠、CLAUDE.md への追加は 10 行以下
**Scale/Scope**: 小規模（CLI コマンドとプロンプトファイルの更新）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: テスタビリティチェック
- [x] 全ての公開APIにテストが存在するか → 既存の CLI コマンドはテスト済み、新機能もテスト追加予定
- [x] 依存関係はモック/スタブ可能か → ファイルシステム操作は Path オブジェクト経由で注入可能
- [x] 副作用は分離されているか → ファイル I/O は専用関数に分離

### Gate 2: LLM品質チェック
- [x] LLMレビューが実施されたか → 設計段階で実施
- [x] 評価結果が記録されたか → spec.md の Clarifications セクションに記録
- [x] 指摘事項に対応したか → @ 記法の採用など反映済み

### Gate 3: シンプリシティチェック
- [x] 不要な抽象化が導入されていないか → ファイル操作のみ、抽象化なし
- [x] 複雑さの正当化がドキュメントされているか → N/A（複雑な処理なし）
- [x] コードは第三者が理解可能か → Markdown テンプレートベースで明快

### Gate 4: モジュラリティチェック
- [x] モジュールの責務は単一か → CLI: ファイル生成、Command: プロンプト定義
- [x] 循環依存は存在しないか → 依存関係なし
- [x] モジュール間インターフェースは明確か → ファイルパスのみで連携

### Gate 5: 型安全性チェック
- [x] 静的型チェックがエラーなしで通過するか → mypy strict mode 使用
- [x] any型やas型アサーションの使用は正当化されているか → N/A
- [x] 外部入力の型検証が境界で実装されているか → YAML パース時に検証

### Gate 6: 最適化チェック
- [x] パフォーマンス最適化は計測データに基づいているか → N/A（最適化不要）
- [x] 最適化前後のベンチマーク結果が記録されているか → N/A
- [x] 可読性を犠牲にした最適化は正当化されているか → N/A

**Gate Status**: ✅ ALL PASSED

## Project Structure

### Documentation (this feature)

```text
specs/003-skill-subagent-activation/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (by /speckit.tasks)
```

### Source Code (repository root)

```text
src/
└── context_forge_cli/
    ├── __init__.py          # CLI main (update init command)
    └── templates/
        └── commands/
            └── add-role-knowledge.md  # コマンドテンプレート（更新）

.claude/
├── commands/
│   └── context-forge.add-role-knowledge.md  # 更新対象
└── context-forge.md     # 新規作成（専用設定ファイル）

tests/
├── unit/
└── integration/
```

**Structure Decision**: 既存の Single project 構造を維持。主な変更は：
1. CLI の `init` コマンドに CLAUDE.md 更新ロジックを追加
2. `.claude/context-forge.md` テンプレートの作成
3. `add-role-knowledge.md` コマンドプロンプトの更新

## Complexity Tracking

> **No violations - all gates passed**

この機能は既存のシンプルな構造を維持し、新しい抽象化を導入しない。
