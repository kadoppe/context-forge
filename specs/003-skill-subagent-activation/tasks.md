# Tasks: Skill/SubAgent 発動率向上

**Input**: Design documents from `/specs/003-skill-subagent-activation/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the feature specification. Manual testing in Claude Code is specified.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/context_forge_cli/`, `.claude/` at repository root
- Paths shown below are based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project preparation and template creation

- [x] T001 Verify src/context_forge_cli/templates/ directory exists and create if needed
- [x] T002 [P] Verify existing CLI structure in src/context_forge_cli/__init__.py supports new functionality

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Define CLAUDE.md reference markers (start/end) as constants in src/context_forge_cli/__init__.py
- [x] T004 [P] Create helper function to read/parse CLAUDE.md content in src/context_forge_cli/__init__.py
- [x] T005 [P] Create helper function to write/update CLAUDE.md content in src/context_forge_cli/__init__.py
- [x] T006 Create helper function to read/parse .claude/context-forge.md content in src/context_forge_cli/__init__.py
- [x] T007 Create helper function to write/update .claude/context-forge.md content in src/context_forge_cli/__init__.py
- [x] T007a [P] Add unit tests for CLAUDE.md read/write helpers in tests/unit/test_claude_md_helpers.py
- [x] T007b [P] Add unit tests for context-forge.md read/write helpers in tests/unit/test_context_forge_md_helpers.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 2 - CLAUDE.md の肥大化防止 (Priority: P2) 🎯 MVP

**Goal**: CLAUDE.md に追加される内容を @ 参照のみに抑え、設定を専用ファイルに分離する

**Independent Test**: `context-forge init` 実行後、CLAUDE.md に追加される行数が 10 行以下であることを確認

**Why US2 first**: US1（発動率向上）を実現するには、まず専用ファイル（`.claude/context-forge.md`）の仕組みが必要。US2 はその基盤を提供する。

### Implementation for User Story 2

- [x] T008 [US2] Create context-forge.md template with header and empty rules section in src/context_forge_cli/templates/context-forge.md
- [x] T009 [US2] Update `init` command to create .claude/context-forge.md if not exists in src/context_forge_cli/__init__.py
- [x] T010 [US2] Update `init` command to add @ reference to CLAUDE.md with markers in src/context_forge_cli/__init__.py
- [x] T011 [US2] Handle case when CLAUDE.md does not exist (create new file with reference) in src/context_forge_cli/__init__.py
- [x] T012 [US2] Handle case when @ reference already exists (skip adding duplicate) in src/context_forge_cli/__init__.py
- [x] T013 [US2] Add success message showing created/updated files in src/context_forge_cli/__init__.py
- [x] T013a [US2] Add integration test for init command creating context-forge.md in tests/integration/test_cli.py

**Checkpoint**: At this point, `context-forge init` creates .claude/context-forge.md and adds @ reference to CLAUDE.md

---

## Phase 4: User Story 1 - Skill/SubAgent の自動発動 (Priority: P1)

**Goal**: 追加した Skill/SubAgent が関連タスク依頼時に自動発動する

**Independent Test**: ロールに SubAgent を追加し、関連するタスクを依頼した際に Task ツールで呼び出されることを確認

**Dependency**: US2 の完了が前提（専用ファイルの仕組みが必要）

### Implementation for User Story 1

- [x] T014 [US1] Update add-role-knowledge.md command to generate activation rule in .claude/commands/context-forge.add-role-knowledge.md
- [x] T015 [US1] Define activation rule format template (「ユーザーが〇〇と言った場合...」形式) in .claude/commands/context-forge.add-role-knowledge.md
- [x] T016 [US1] Add Phase 7.3 step to append activation rule to .claude/context-forge.md in .claude/commands/context-forge.add-role-knowledge.md
- [x] T017 [US1] Update rule generation to group by role name (### {role-name} ロール section) in .claude/commands/context-forge.add-role-knowledge.md
- [x] T018 [US1] Add logic to check if role section exists before creating new one in .claude/commands/context-forge.add-role-knowledge.md
- [x] T019 [US1] Display completion message showing added activation rule in .claude/commands/context-forge.add-role-knowledge.md

**Checkpoint**: At this point, add-role-knowledge command automatically adds activation rules to context-forge.md

---

## Phase 5: User Story 3 - 発動条件の明示的な記述 (Priority: P3)

**Goal**: Skill/SubAgent の description に 3 つ以上のトリガー表現パターンを含める

**Independent Test**: 生成された Skill/SubAgent ファイルの description を確認し、複数のトリガー表現が含まれていることを確認

### Implementation for User Story 3

- [x] T020 [US3] Update Skill template to require 3+ trigger patterns in description in .claude/commands/context-forge.add-role-knowledge.md
- [x] T021 [US3] Update SubAgent template to require 3+ trigger patterns in description in .claude/commands/context-forge.add-role-knowledge.md
- [x] T022 [US3] Add Phase 4.5 step to prompt user for multiple trigger expressions in .claude/commands/context-forge.add-role-knowledge.md
- [x] T023 [US3] Update description generation to include all trigger patterns in .claude/commands/context-forge.add-role-knowledge.md
- [x] T024 [US3] Add validation to ensure minimum 3 trigger patterns are provided in .claude/commands/context-forge.add-role-knowledge.md

**Checkpoint**: Generated Skill/SubAgent files now include multiple trigger patterns in description

---

## Phase 6: Migration & Edge Cases

**Purpose**: Handle existing users and edge cases

- [x] T025 Implement migration detection for existing context-forge settings in CLAUDE.md in src/context_forge_cli/__init__.py
- [x] T026 Add confirmation prompt for migration ("既存の設定を移行しますか？") in src/context_forge_cli/__init__.py
- [x] T027 Implement migration logic to move settings to .claude/context-forge.md in src/context_forge_cli/__init__.py
- [x] T028 Add warning message when .claude/context-forge.md is missing but @ reference exists in src/context_forge_cli/__init__.py

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and validation

- [x] T029 [P] Update quickstart.md with actual usage examples in specs/003-skill-subagent-activation/quickstart.md
- [x] T030 Run manual validation: execute `context-forge init` and verify file creation
- [ ] T031 Run manual validation: add a SubAgent with add-role-knowledge and verify activation rule
- [ ] T032 Run manual validation: test activation by asking Claude Code a related question
- [x] T033 Verify CLAUDE.md reference is under 10 lines (SC-002)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 2 (Phase 3)**: Depends on Foundational - MUST complete before US1
- **User Story 1 (Phase 4)**: Depends on US2 (needs context-forge.md infrastructure)
- **User Story 3 (Phase 5)**: Depends on Foundational - can run parallel with US1
- **Migration (Phase 6)**: Depends on US2 completion
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 2 (P2)**: Foundation for other stories - implements file infrastructure
- **User Story 1 (P1)**: Depends on US2 - uses context-forge.md to store activation rules
- **User Story 3 (P3)**: Independent of US1/US2 - only modifies description generation

### Within Each User Story

- Helper functions before command updates
- Template creation before usage
- Core implementation before edge cases

### Parallel Opportunities

- T002 can run parallel with T001 (different files)
- T004, T005 can run parallel (read vs write helpers)
- T006, T007 can run parallel (read vs write for different file)
- T020, T021 can run parallel (Skill vs SubAgent templates)
- T029 can run parallel with validation tasks

---

## Parallel Example: Foundational Phase

```bash
# Launch read/write helpers for CLAUDE.md together:
Task: "Create helper function to read/parse CLAUDE.md content in src/context_forge_cli/__init__.py"
Task: "Create helper function to write/update CLAUDE.md content in src/context_forge_cli/__init__.py"

# Launch read/write helpers for context-forge.md together:
Task: "Create helper function to read/parse .claude/context-forge.md content in src/context_forge_cli/__init__.py"
Task: "Create helper function to write/update .claude/context-forge.md content in src/context_forge_cli/__init__.py"
```

---

## Implementation Strategy

### MVP First (User Story 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 2
4. **STOP and VALIDATE**: Run `context-forge init` and verify:
   - `.claude/context-forge.md` is created
   - `CLAUDE.md` has @ reference (under 10 lines added)
5. This provides the foundation for activation rules

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 2 → Test independently → Deploy (Infrastructure MVP!)
3. Add User Story 1 → Test independently → Deploy (Activation rules work!)
4. Add User Story 3 → Test independently → Deploy (Better descriptions!)
5. Each story adds value without breaking previous stories

### Recommended Order

Due to dependencies:
1. Phase 1 (Setup)
2. Phase 2 (Foundational)
3. Phase 3 (US2 - file infrastructure)
4. Phase 4 (US1 - activation rules)
5. Phase 5 (US3 - description improvement) - can start after Phase 2
6. Phase 6 (Migration)
7. Phase 7 (Polish)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently testable after completion
- US2 is implemented before US1 due to technical dependency (file infrastructure)
- Manual testing in Claude Code required for activation verification
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
