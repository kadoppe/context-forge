# Tasks: Role Plugin Migration Command

**Input**: Design documents from `/specs/001-role-plugin-migrate/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: テスト明示的にリクエストされていないため、テストタスクは含まれていません。

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/context_forge_cli/` at repository root
- **Templates**: `src/context_forge_cli/templates/commands/`
- **Slash commands**: `.claude/commands/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: テンプレートディレクトリの確認と基盤整備

- [x] T001 Verify templates directory exists at src/context_forge_cli/templates/commands/
- [x] T002 [P] Review existing add-role-knowledge.md template structure for consistency

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: migrate コマンドのテンプレートファイル作成（すべてのユーザーストーリーで使用）

**⚠️ CRITICAL**: User Story 1 と User Story 2 はこのテンプレートに依存

- [x] T003 Create migrate.md template file at src/context_forge_cli/templates/commands/migrate.md with YAML frontmatter (description field)
- [x] T004 Define migrate command structure: Phase 1 (plugin detection), Phase 2 (version check), Phase 3 (backup), Phase 4 (migration), Phase 5 (report)
- [x] T005 Add plugin detection logic instructions (FR-001): scan `.claude/plugins/context-forge.role-*` pattern
- [x] T006 Add version comparison logic instructions (FR-002): check plugin.json version < context-forge current version
- [x] T007 Add backup creation instructions (FR-004): copy to `.claude/plugins/.backup/{timestamp}_{plugin-name}/`
- [x] T008 Add migration execution instructions (FR-003): update plugin.json version, add trigger expressions to agents/skills descriptions
- [x] T009 Add error handling and recovery instructions (FR-008): restore from backup on failure
- [x] T010 Add migration report format (FR-006): display migrated, skipped, and error lists

**Checkpoint**: migrate.md テンプレートが完成し、インストール可能な状態

---

## Phase 3: User Story 1 - 既存プラグインの最新化 (Priority: P1) 🎯 MVP

**Goal**: `/context-forge.migrate` コマンドで旧形式プラグインを最新仕様に更新できる

**Independent Test**: 旧形式のプラグインディレクトリを用意し、`/context-forge.migrate` 実行後に最新仕様に準拠しているか検証

### Implementation for User Story 1

- [x] T011 [US1] Add edge case handling: no plugins found message in migrate.md
- [x] T012 [US1] Add edge case handling: already up-to-date plugins skip logic in migrate.md
- [x] T013 [US1] Add edge case handling: timestamp-based backup naming for conflicts in migrate.md
- [x] T014 [US1] Add multiple plugins sequential processing instructions in migrate.md
- [x] T015 [US1] Validate migrate.md can be parsed by Claude Code (frontmatter format check)

**Checkpoint**: `/context-forge.migrate` が単独で動作可能

---

## Phase 4: User Story 2 - init コマンドでのインストール (Priority: P2)

**Goal**: `context-forge init` コマンドで migrate.md を含む全コマンドがインストールされる

**Independent Test**: 新規プロジェクトで `context-forge init` 実行後、`.claude/commands/context-forge.migrate.md` が存在することを確認

### Implementation for User Story 2

- [x] T016 [US2] Verify init command in src/context_forge_cli/__init__.py already installs all templates (FR-007)
- [x] T017 [US2] Confirm existing --force option handles file overwrite correctly
- [x] T018 [US2] Test that migrate.md is discovered by list_available_templates() function
- [x] T019 [US2] Verify installed command follows naming convention: context-forge.migrate.md in .claude/commands/

**Checkpoint**: `context-forge init` で migrate コマンドがインストールされる

---

## Phase 5: User Story 3 - 選択的なマイグレーション (Priority: P3)

**Goal**: プラグイン名を引数で指定して特定のプラグインのみをマイグレーション

**Independent Test**: 複数プラグイン環境で `/context-forge.migrate software-engineer` 実行し、指定プラグインのみ更新されることを確認

### Implementation for User Story 3

- [x] T020 [US3] Add command argument handling instructions in migrate.md (FR-005): parse $ARGUMENTS for plugin name
- [x] T021 [US3] Add plugin filtering logic: match specified name against detected plugins
- [x] T022 [US3] Add argument validation: display error if specified plugin not found
- [x] T023 [US3] Update migration report to show which plugin was targeted

**Checkpoint**: 選択的マイグレーションが動作可能

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: ドキュメント整備と最終確認

- [x] T024 [P] Update quickstart.md with actual command usage examples
- [x] T025 [P] Add migrate command description to any existing documentation
- [x] T026 Run `uv run ruff check src/` to verify no linting issues
- [x] T027 Run `uv run mypy src/` to verify type checking passes
- [x] T028 Manual test: run `context-forge init` in a test project and verify migrate.md is installed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - creates migrate.md template
- **User Story 1 (Phase 3)**: Depends on Foundational - extends migrate.md
- **User Story 2 (Phase 4)**: Depends on Foundational - verifies init command
- **User Story 3 (Phase 5)**: Depends on Foundational - extends migrate.md
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Requires migrate.md template (Phase 2) - Core migration functionality
- **User Story 2 (P2)**: Requires migrate.md template (Phase 2) - Can run in parallel with US1
- **User Story 3 (P3)**: Requires migrate.md template (Phase 2) - Can run in parallel with US1/US2

### Within Each User Story

- Template creation before logic instructions
- Core functionality before edge cases
- Implementation before validation

### Parallel Opportunities

- T001, T002 can run in parallel (Phase 1)
- User Stories 1, 2, 3 can run in parallel after Phase 2 completion
- T024, T025 can run in parallel (Polish phase)

---

## Parallel Example: After Foundational Phase

```bash
# Once Phase 2 is complete, all user stories can start in parallel:

# User Story 1 tasks:
Task: "T011 [US1] Add edge case handling: no plugins found message in migrate.md"
Task: "T012 [US1] Add edge case handling: already up-to-date plugins skip logic"

# User Story 2 tasks (in parallel):
Task: "T016 [US2] Verify init command installs all templates"
Task: "T017 [US2] Confirm existing --force option handles file overwrite"

# User Story 3 tasks (in parallel):
Task: "T020 [US3] Add command argument handling instructions in migrate.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T010) - migrate.md template
3. Complete Phase 3: User Story 1 (T011-T015) - edge cases and validation
4. **STOP and VALIDATE**: Test `/context-forge.migrate` with a sample plugin
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → migrate.md template ready
2. Add User Story 1 → Test migration → MVP complete!
3. Add User Story 2 → Verify init installs migrate
4. Add User Story 3 → Add selective migration
5. Each story adds value without breaking previous stories

### Suggested MVP Scope

**MVP = Phase 1 + Phase 2 + Phase 3 (User Story 1)**

これにより、基本的なマイグレーション機能が利用可能になります。init コマンドとの統合（US2）と選択的マイグレーション（US3）は追加で実装可能です。

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- migrate.md は Claude Code slash command として実行されるため、LLM への指示として記述
- 既存の init コマンドは templates/commands/ 内の全ファイルを自動検出するため、migrate.md を追加するだけで自動的にインストール対象になる
- テストは明示的にリクエストされていないため省略
