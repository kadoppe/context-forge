# Tasks: SubAgent品質向上のためのプロンプト改善

**Input**: Design documents from `/specs/001-improve-subagent-quality/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: 手動テストのみ（SubAgent生成→PRレビュー→指摘件数計測）

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Target File

```
src/context_forge_cli/templates/commands/add-role-knowledge.md
```

---

## Phase 1: Setup (現状分析)

**Purpose**: 現在のテンプレート構造を理解し、改善計画を確認

- [x] T001 現在のテンプレートファイルをバックアップ（任意）
- [x] T002 research.md の改善項目を確認し、実装順序を決定

---

## Phase 2: Foundational (共通インフラ)

**Purpose**: 全ユーザーストーリーで使用する共通テンプレート構造を定義

**⚠️ CRITICAL**: この Phase が完了するまで、ユーザーストーリーの実装は開始できない

- [x] T003 Sub Agentテンプレートの必須セクション構造を定義（セクション名・順序のみ。具体的な内容はT007-T008で追加）in `src/context_forge_cli/templates/commands/add-role-knowledge.md`

**Checkpoint**: テンプレート構造が定義され、ユーザーストーリーの実装を開始できる

---

## Phase 3: User Story 1 - SubAgentの高品質な自動生成 (Priority: P1) 🎯 MVP

**Goal**: 生成されるSubAgentファイルにプレースホルダーが残らず、bashコマンドとgit操作が安全パターンに従うようにする

**Independent Test**: コマンドでSubAgentを生成し、生成ファイルにプレースホルダーがなく、bash/gitの安全パターンが適用されていることを確認

### Implementation for User Story 1

- [x] T004 [US1] Phase 5 の Sub Agent テンプレートにプレースホルダー禁止ルールを追加 in `src/context_forge_cli/templates/commands/add-role-knowledge.md`
- [x] T005 [US1] Sub Agent テンプレートに bash コマンドの**ルール**（変数キャッシュ必須、クォーティング必須、エラーハンドリング必須）を追加 in `src/context_forge_cli/templates/commands/add-role-knowledge.md`
- [x] T006 [US1] Sub Agent テンプレートに git 操作の**ルール**（`git add -A`禁止、個別ファイル指定必須、diff確認必須）を追加 in `src/context_forge_cli/templates/commands/add-role-knowledge.md`
- [x] T007 [US1] Sub Agent テンプレートに必須の「注意事項」セクションテンプレートを追加（git add -A禁止、確認手順等）in `src/context_forge_cli/templates/commands/add-role-knowledge.md`
- [x] T008 [US1] Sub Agent テンプレートに必須の「トラブルシューティング」セクションテンプレートを追加 in `src/context_forge_cli/templates/commands/add-role-knowledge.md`

**Checkpoint**: User Story 1 が完了。生成されるSubAgentに品質ガイドラインが組み込まれている

---

## Phase 4: User Story 2 - 品質チェックリストの自動適用 (Priority: P2)

**Goal**: SubAgent生成時に品質チェックが自動実行され、問題があれば自動修正または警告される

**Independent Test**: 意図的に問題のあるSubAgentを生成させ、品質チェックが問題を検出・修正することを確認

### Implementation for User Story 2

- [x] T009 [US2] Phase 5 と Phase 6 の間に新しい「Phase 5.5: 品質チェック」セクションを追加 in `src/context_forge_cli/templates/commands/add-role-knowledge.md`
- [x] T010 [US2] 品質チェック項目（プレースホルダー検出、変数クォーティング、危険なgit操作、必須セクション存在）を定義 in `src/context_forge_cli/templates/commands/add-role-knowledge.md`
- [x] T011 [US2] 各チェック項目の自動修正ロジックをプロンプトに記述 in `src/context_forge_cli/templates/commands/add-role-knowledge.md`
- [x] T012 [US2] 自動修正不可能な項目の警告表示フォーマットを定義 in `src/context_forge_cli/templates/commands/add-role-knowledge.md`

**Checkpoint**: User Story 2 が完了。品質チェックが自動実行される

---

## Phase 5: User Story 3 - ベストプラクティスの組み込み (Priority: P3)

**Goal**: SubAgentテンプレートにベストプラクティスが組み込まれ、一貫した品質のSubAgentを作成できる

**Independent Test**: 異なる種類のSubAgentを生成し、すべてに一貫した品質パターンが適用されていることを確認

### Implementation for User Story 3

- [x] T013 [US3] bashコマンドの**具体的なコード例**（変数キャッシュ、エラーハンドリング、クォーティングの良い例・悪い例）を追加 in `src/context_forge_cli/templates/commands/add-role-knowledge.md`
- [x] T014 [US3] git操作の**具体的なコード例**（安全なステージング、コミット前確認、プッシュ前確認の良い例・悪い例）を追加 in `src/context_forge_cli/templates/commands/add-role-knowledge.md`
- [x] T015 [US3] API呼び出しのベストプラクティス例（gh コマンドなど）を追加 in `src/context_forge_cli/templates/commands/add-role-knowledge.md`

**Checkpoint**: User Story 3 が完了。ベストプラクティスがテンプレートに組み込まれている

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 全体的な品質向上と最終確認

- [x] T016 テンプレート全体の整合性と可読性を確認・修正 in `src/context_forge_cli/templates/commands/add-role-knowledge.md`
- [x] T017 改善前後のテンプレートを比較し、すべての要件が満たされていることを確認
- [ ] T018 手動テスト: 改善後のテンプレートでSubAgentを生成し、品質ガイドラインが適用されることを確認
- [ ] T019 手動テスト: 生成されたSubAgentでPRを作成し、レビュー指摘が減少することを確認

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories should proceed sequentially (P1 → P2 → P3)
  - 同一ファイルを編集するため並列実行は推奨しない
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on User Story 1 (テンプレート構造に依存)
- **User Story 3 (P3)**: Depends on User Story 1 (テンプレート構造に依存)

### Within Each User Story

- すべてのタスクは同一ファイルを編集するため、順次実行
- 各タスク完了後にファイルの整合性を確認

### Parallel Opportunities

- **限定的**: すべてのタスクが同一ファイル（`add-role-knowledge.md`）を編集するため、並列実行の機会は限られる
- Phase 6 の手動テスト（T018, T019）は独立して実行可能

---

## Parallel Example: User Story 1

```bash
# User Story 1 のタスクは同一ファイルを編集するため、順次実行が推奨
# T004 → T005 → T006 → T007 → T008 の順で実行
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (現状確認)
2. Complete Phase 2: Foundational (テンプレート構造定義)
3. Complete Phase 3: User Story 1 (プレースホルダー禁止、bash/git安全パターン)
4. **STOP and VALIDATE**: 改善されたテンプレートでSubAgentを生成してテスト
5. PRを作成してレビュー指摘を確認

### Incremental Delivery

1. Complete Setup + Foundational → 基盤準備完了
2. Add User Story 1 → テスト → MVP完了！
3. Add User Story 2 → テスト → 品質チェック追加
4. Add User Story 3 → テスト → ベストプラクティス追加
5. 各ストーリーで品質が段階的に向上

---

## Notes

- すべてのタスクが同一ファイルを編集するため、コンフリクトを避けるよう順次実行
- 各タスク完了後にファイルの整合性を確認
- 手動テストはSubAgent生成→PRレビューのサイクルで実施
- 成功基準: PRレビューでの指摘件数が50%以上減少
