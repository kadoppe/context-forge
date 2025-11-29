# Implementation Tasks: Role Knowledge Plugin Generator

**Feature**: 001-role-knowledge-plugin
**Date**: 2025-11-29
**Plan**: [plan.md](./plan.md)

## Task Summary

| Story | Tasks | Estimated Complexity |
|-------|-------|---------------------|
| US1 (P1) | 4 | Low |
| US2 (P1) | 8 | High |
| US3 (P2) | 3 | Medium |
| US4 (P2) | 2 | Medium |

---

## US1: ロールプラグイン生成Commandのインストール (P1)

### T001: add-role-knowledge テンプレートファイルの作成
- [X] `src/context_forge_cli/templates/commands/add-role-knowledge.md` を作成
- [X] YAML frontmatter を定義（name, description）
- [X] コマンド本文のプレースホルダーを作成（Phase 2で詳細実装）

**File**: `src/context_forge_cli/templates/commands/add-role-knowledge.md`
**Depends on**: なし
**Parallel**: Yes (T002と並行可能)

### T002: CLI install コマンドの削除
- [X] `install` コマンドを削除（`init` コマンドで全てカバー）
- [X] `init` コマンドは既存実装のまま（全テンプレート自動インストール）
- [X] 関連するヘルプメッセージの確認

**File**: `src/context_forge_cli/__init__.py`
**Depends on**: なし
**Parallel**: Yes (T001と並行可能)

### T003: CLI テストの更新
- [X] `install` コマンド関連のテストを削除
- [X] `init` コマンドで全テンプレートがインストールされることを検証
- [X] `--force` オプションのテストを確認
- [X] 上書き確認プロンプトのテストを確認

**File**: `tests/unit/test_cli.py`
**Depends on**: T002
**Parallel**: No

### T004: インテグレーションテストの作成
- [X] `tests/integration/test_init_command.py` を作成
- [X] 実際のファイルシステムでの `init` コマンドをテスト
- [X] `add-role-knowledge` テンプレートの存在確認
- [X] インストール後のファイル内容検証

**File**: `tests/integration/test_init_command.py`
**Depends on**: T001, T002
**Parallel**: No

---

## US2: 新規ロールプラグインの作成 (P1)

### T005: 対話フローの基本構造実装
- [X] Phase 1: ロール選択フローの実装（テンプレート内）
- [X] 既存プラグインのスキャンロジック（`.claude/plugins/` 検索）
- [X] 新規作成 vs 既存選択の分岐処理

**File**: `src/context_forge_cli/templates/commands/add-role-knowledge.md`
**Depends on**: T001
**Parallel**: Yes (T006と並行可能)

### T006: 公式ドキュメントフェッチ指示の追加
- [X] WebFetch を使用したドキュメント取得指示
- [X] 4つのURL（plugins, sub-agents, skills, hooks-guide）の参照
- [X] 取得失敗時の警告メッセージとキャッシュ利用指示

**File**: `src/context_forge_cli/templates/commands/add-role-knowledge.md`
**Depends on**: T001
**Parallel**: Yes (T005と並行可能)

**URLs**:
- https://code.claude.com/docs/en/plugins
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/hooks-guide

### T007: ロール定義フロー実装
- [X] Phase 2: 新規ロール作成フローの実装
- [X] ロール名の入力とバリデーション（小文字英数字+ハイフン、最大64文字）
- [X] ロール説明の入力

**File**: `src/context_forge_cli/templates/commands/add-role-knowledge.md`
**Depends on**: T005
**Parallel**: No

### T008: 知見入力フロー実装
- [X] Phase 3: 知見入力フローの実装
- [X] 知見の名前と説明の入力
- [X] 複数知見の連続追加サポート

**File**: `src/context_forge_cli/templates/commands/add-role-knowledge.md`
**Depends on**: T007
**Parallel**: No

### T009: LLMによる知見タイプ判定ロジック
- [X] Phase 4: タイプ判定フローの実装
- [X] LLM分析による最適タイプの推奨
- [X] 推奨理由の表示
- [X] ユーザー確認または変更の受付

**File**: `src/context_forge_cli/templates/commands/add-role-knowledge.md`
**Depends on**: T008
**Parallel**: No

**Type Guidelines**:
| Pattern | Type |
|---------|------|
| 参照情報、チェックリスト | Skill |
| ワークフロー自動化 | Command |
| 自律的タスク遂行 | Sub Agent |
| イベントトリガー処理 | Hook |

### T010: プラグインファイル生成ロジック
- [X] Phase 5: ファイル生成フローの実装
- [X] plugin.json の生成
- [X] タイプに応じたファイル生成（SKILL.md, *.md, hooks.json）
- [X] ディレクトリ構造の作成

**File**: `src/context_forge_cli/templates/commands/add-role-knowledge.md`
**Depends on**: T009
**Parallel**: No

**Generated Structure**:
```
.claude/plugins/{role-name}/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── {knowledge-item}.md
├── agents/
│   └── {knowledge-item}.md
├── skills/
│   └── {knowledge-item}/
│       └── SKILL.md
└── hooks/
    └── hooks.json
```

### T011: 継続・完了フロー実装
- [X] Phase 6-7: 継続/完了フローの実装
- [X] 追加知見の入力サポート
- [X] 完了時のサマリー表示
- [X] 次のステップの案内

**File**: `src/context_forge_cli/templates/commands/add-role-knowledge.md`
**Depends on**: T010
**Parallel**: No

### T012: エラーハンドリング実装
- [X] ロール名無効時のエラー処理
- [X] ファイル書き込み失敗時のエラー処理
- [X] キャンセル時のクリーンアップ処理
- [X] ドキュメント取得失敗時の警告表示

**File**: `src/context_forge_cli/templates/commands/add-role-knowledge.md`
**Depends on**: T010
**Parallel**: No

---

## US3: 既存ロールプラグインの更新 (P2)

### T013: 既存プラグイン検出ロジック
- [X] `.claude/plugins/` 配下のプラグインスキャン
- [X] plugin.json からのメタデータ読み取り
- [X] 既存知見の一覧表示

**File**: `src/context_forge_cli/templates/commands/add-role-knowledge.md`
**Depends on**: T005
**Parallel**: No

### T014: 既存プラグインへの知見追加フロー
- [X] 既存プラグイン選択後の追加フロー
- [X] 既存知見との重複チェック
- [X] hooks.json への追記処理（Hook追加時）

**File**: `src/context_forge_cli/templates/commands/add-role-knowledge.md`
**Depends on**: T013
**Parallel**: No

### T015: 更新フローのテスト
- [X] 既存プラグインへの知見追加の手動テスト手順作成
- [X] 既存ファイルが破損しないことの検証

**File**: `specs/001-role-knowledge-plugin/test-scenarios.md`
**Depends on**: T014
**Parallel**: No

---

## US4: 知見タイプの自動判別 (P2)

### T016: タイプ判定のプロンプト最適化
- [X] 各タイプの特徴を明確に定義
- [X] LLMが正確に判定できるプロンプト設計
- [X] 判定に自信がない場合のフォールバック処理

**File**: `src/context_forge_cli/templates/commands/add-role-knowledge.md`
**Depends on**: T009
**Parallel**: No

### T017: タイプ判定のテストケース作成
- [X] Skill判定のテストケース（チェックリスト、ガイドライン）
- [X] Command判定のテストケース（自動化、生成）
- [X] Sub Agent判定のテストケース（自律的レビュー、分析）
- [X] Hook判定のテストケース（イベントトリガー、検証）

**File**: `specs/001-role-knowledge-plugin/test-scenarios.md`
**Depends on**: T016
**Parallel**: No

---

## Verification Checklist

### After US1 Completion
- [X] `uv run context-forge init` で全コマンドがインストールされる
- [X] `.claude/commands/context-forge.add-role-knowledge.md` が作成される
- [X] `uv run pytest tests/` が全て通過する

### After US2 Completion
- [ ] Claude Code で `/context-forge.add-role-knowledge` が実行できる
- [ ] 新規ロールプラグインが `.claude/plugins/context-forge.role-{role-name}/` に生成される
- [ ] 生成された plugin.json が正しい形式である
- [ ] 知見タイプに応じた正しいファイルが生成される

### After US3 Completion
- [ ] 既存プラグインが一覧表示される
- [ ] 既存プラグインに新しい知見を追加できる
- [ ] 既存の知見が破損しない

### After US4 Completion
- [ ] 各タイプの知見入力に対して適切なタイプが推奨される
- [ ] ユーザーが推奨を上書きできる

---

## Quality Gates

### Before Merge
- [X] `uv run ruff check .` - リントチェック通過
- [X] `uv run mypy src` - 型チェック通過
- [X] `uv run pytest` - 全テスト通過
- [ ] 手動テスト: Claude Code での動作確認完了
