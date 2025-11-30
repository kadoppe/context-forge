# Implementation Plan: SubAgent品質向上のためのプロンプト改善

**Branch**: `001-improve-subagent-quality` | **Date**: 2025-11-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-improve-subagent-quality/spec.md`

## Summary

`add-role-knowledge` コマンドで生成されるSubAgentの品質を向上させる。具体的には、SubAgentテンプレートの改善、品質チェックリストのプロンプトへの組み込み、ベストプラクティスの自動適用を行い、PRレビューでの指摘を50%以上削減することを目指す。

## Technical Context

**Language/Version**: Markdown (Claude Code プロンプト形式)
**Primary Dependencies**: Claude Code Plugin System (commands, agents)
**Storage**: N/A (ファイルベースのMarkdownプロンプト)
**Testing**: 手動テスト（SubAgent生成→PRレビュー→指摘件数計測）
**Target Platform**: Claude Code CLI
**Project Type**: Single project (プロンプトファイルの改善)
**Performance Goals**: N/A (プロンプト改善のため性能目標なし)
**Constraints**: 既存のコマンド構造を維持、破壊的変更を避ける
**Scale/Scope**: 1つのテンプレートファイル（`src/context_forge_cli/templates/commands/add-role-knowledge.md`）の改善。`context-forge init` でインストールされるコマンドのソースを改善する。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: テスタビリティチェック
- [x] 全ての公開APIにテストが存在するか → N/A（プロンプト改善はコード実行を伴わないため自動テスト対象外。手動テストで検証）
- [x] 依存関係はモック/スタブ可能か → N/A（Markdownテンプレートのため該当なし）
- [x] 副作用は分離されているか → N/A（Markdownテンプレートのため該当なし）

### Gate 2: LLM品質チェック
- [x] LLMレビューが実施されたか → PRでClaude Code Reviewを使用
- [x] 評価結果が記録されたか → PRコメントとして記録
- [x] 指摘事項に対応したか → 今回の改善で対応

### Gate 3: シンプリシティチェック
- [x] 不要な抽象化が導入されていないか → プロンプトテンプレートのみ
- [x] 複雑さの正当化がドキュメントされているか → spec.mdで定義
- [x] コードは第三者が理解可能か → Markdown形式で可読性高い

### Gate 4: モジュラリティチェック
- [x] モジュールの責務は単一か → コマンドファイル1つのみ改善
- [x] 循環依存は存在しないか → N/A
- [x] モジュール間インターフェースは明確か → N/A

### Gate 5: 型安全性チェック
- [x] N/A（Markdownプロンプトのため型チェック対象外）

### Gate 6: 最適化チェック
- [x] N/A（パフォーマンス最適化不要）

**Result**: ✅ All gates passed

## Project Structure

### Documentation (this feature)

```text
specs/001-improve-subagent-quality/
├── spec.md              # 機能仕様
├── plan.md              # このファイル
├── research.md          # Phase 0 出力
├── data-model.md        # Phase 1 出力
├── quickstart.md        # Phase 1 出力
└── tasks.md             # Phase 2 出力（/speckit.tasks コマンド）
```

### Source Code (repository root)

```text
src/
└── context_forge_cli/
    ├── __init__.py                    # CLI実装（init コマンド含む）
    └── templates/
        └── commands/
            └── add-role-knowledge.md  # 改善対象テンプレート

# context-forge init 実行後にインストールされる先:
.claude/
├── commands/
│   └── context-forge.add-role-knowledge.md  # テンプレートからコピーされる
└── plugins/
    └── context-forge.role-*/
        └── agents/
            └── *.md  # 生成されるSubAgentファイル
```

**Structure Decision**: `context-forge init` でインストールされるテンプレート（`src/context_forge_cli/templates/commands/add-role-knowledge.md`）を改善対象とする。これにより、新規プロジェクトで `context-forge init` を実行した際に、改善されたコマンドが自動的にインストールされる。

## Complexity Tracking

> 違反なし。既存構造の改善のみで、新たな複雑さは導入しない。
