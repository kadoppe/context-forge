# Tasks: context-forge CLI 初期実装

**Input**: Design documents from `/specs/001-context-forge-cli/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Basic test coverage for core CLI commands per Constitution Principle I (Testability First).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md structure (single project):
- Source: `src/context_forge_cli/`
- Templates: `src/context_forge_cli/templates/commands/`
- Tests: `tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure: `src/context_forge_cli/`, `src/context_forge_cli/templates/commands/`, `tests/unit/`, `tests/integration/`
- [x] T002 Create pyproject.toml with Hatchling build system, dependencies (typer, rich, pytest), and entry point `context-forge = "context_forge_cli:main"`
- [x] T003 [P] Create empty `src/context_forge_cli/__init__.py` with version constant and main() stub
- [x] T004 [P] Create `.gitignore` for Python project (venv, __pycache__, .pytest_cache, dist/, etc.)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Define data models (Command, CommandTemplate, InstallTarget, InstallResult) as dataclasses in `src/context_forge_cli/__init__.py`
- [x] T006 Implement template loading function to read embedded templates from package using `importlib.resources` in `src/context_forge_cli/__init__.py`
- [x] T007 Create Typer app instance with name="context-forge" and help text (in English) in `src/context_forge_cli/__init__.py`

**Checkpoint**: Foundation ready - user story implementation can now begin ✅

---

## Phase 3: User Story 1 - CLI Installation & Version (Priority: P1) 🎯 MVP

**Goal**: Developers can install context-forge and verify installation with `--version`

**Independent Test**: Run `context-forge --version` and confirm version is displayed

### Tests for User Story 1

- [x] T008 [P] [US1] Create test file `tests/integration/test_cli.py` with CliRunner setup
- [x] T009 [US1] Write test for `--version` command output in `tests/integration/test_cli.py`

### Implementation for User Story 1

- [x] T010 [US1] Implement `--version` callback in Typer app showing "context-forge-cli v{VERSION}" in `src/context_forge_cli/__init__.py`
- [x] T011 [US1] Add `--help` command descriptions in English for all commands in `src/context_forge_cli/__init__.py`
- [x] T012 [US1] Verify package can be installed with `uv pip install -e .` and `context-forge --version` works
- [x] T013 [US1] Run pytest and verify US1 tests pass

**Checkpoint**: User Story 1 complete - CLI is installable and version displays correctly ✅

---

## Phase 4: User Story 2 - Install hello-world Command (Priority: P1) 🎯 MVP

**Goal**: Developers can install hello-world command to Claude Code

**Independent Test**: Run `context-forge install hello-world` and verify `.claude/commands/context-forge.hello-world.md` is created

### Tests for User Story 2

- [x] T014 [P] [US2] Write test for `install` command creating file in tmp directory in `tests/integration/test_cli.py`
- [x] T015 [P] [US2] Write test for `install` with unknown command name returning error in `tests/integration/test_cli.py`

### Implementation for User Story 2

- [x] T016 [P] [US2] Create hello-world.md template (in English) in `src/context_forge_cli/templates/commands/hello-world.md`
- [x] T017 [US2] Implement `install` command with command-name argument in `src/context_forge_cli/__init__.py`
- [x] T018 [US2] Implement logic to resolve InstallTarget (project_root = cwd, commands_dir = .claude/commands/) in `src/context_forge_cli/__init__.py`
- [x] T019 [US2] Implement directory creation (mkdir -p equivalent) for .claude/commands/ in `src/context_forge_cli/__init__.py`
- [x] T020 [US2] Implement file existence check and overwrite confirmation prompt (in English) using Rich in `src/context_forge_cli/__init__.py`
- [x] T021 [US2] Implement file copy with `context-forge.` prefix to target path in `src/context_forge_cli/__init__.py`
- [x] T022 [US2] Add success message (in English) using Rich console in `src/context_forge_cli/__init__.py`
- [x] T023 [US2] Add `--force` flag to skip overwrite confirmation in `src/context_forge_cli/__init__.py`
- [x] T024 [US2] Add error handling for unknown command names with helpful message (in English) in `src/context_forge_cli/__init__.py`
- [x] T025 [US2] Run pytest and verify US2 tests pass

**Checkpoint**: User Story 2 complete - hello-world command can be installed to Claude Code ✅

---

## Phase 5: User Story 3 - Project Initialization (Priority: P2)

**Goal**: Developers can initialize a project for context-forge

**Independent Test**: Run `context-forge init` and verify `.claude/` directory structure is created

### Tests for User Story 3

- [x] T026 [P] [US3] Write test for `init` command creating directories in tmp directory in `tests/integration/test_cli.py`

### Implementation for User Story 3

- [x] T027 [US3] Implement `init` command in `src/context_forge_cli/__init__.py`
- [x] T028 [US3] Implement .claude/ and .claude/commands/ directory creation in `src/context_forge_cli/__init__.py`
- [x] T029 [US3] Add check for existing .claude/ directory with overwrite/skip prompt (in English) in `src/context_forge_cli/__init__.py`
- [x] T030 [US3] Add success message (in English) showing created directories in `src/context_forge_cli/__init__.py`
- [x] T031 [US3] Run pytest and verify US3 tests pass

**Checkpoint**: User Story 3 complete - Projects can be initialized for context-forge ✅

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T032 [P] Add error handling with Rich error panels and appropriate exit codes (0=success, 1=error, 2=file error, 3=user cancel) in `src/context_forge_cli/__init__.py`
- [x] T033 [P] Add command name validation (alphanumeric, hyphens, underscores only; max 64 chars) in `src/context_forge_cli/__init__.py`
- [x] T034 [P] Run mypy type checking and fix any type errors
- [x] T035 [P] Run ruff linting and fix any issues
- [x] T036 Run all pytest tests and ensure 100% pass rate
- [x] T037 Validate quickstart.md flow: install → version → install hello-world → verify in Claude Code

**Checkpoint**: Phase 6 complete - All polish tasks finished ✅

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP part 1
- **User Story 2 (Phase 4)**: Depends on Foundational - MVP part 2, can run parallel with US1
- **User Story 3 (Phase 5)**: Depends on Foundational - can run parallel with US1/US2
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Test tasks (T008-T009, T014-T015, T026) should be written before implementation
- T016 (template file) can be done in parallel with other US2 tasks
- All other US2 tasks (T017-T025) should be done sequentially
- US3 tasks (T027-T031) should be done sequentially

### Parallel Opportunities

- Setup tasks T003, T004 can run in parallel
- US2 task T016 (template) can run in parallel with US1 tasks
- All User Stories can be worked on in parallel after Foundational phase
- Polish tasks T032, T033, T034, T035 can run in parallel

---

## Parallel Example: Setup Phase

```bash
# Launch parallel setup tasks:
Task: "Create empty src/context_forge_cli/__init__.py"
Task: "Create .gitignore for Python project"
```

## Parallel Example: After Foundational

```bash
# All user stories can start in parallel (tests first):
Task: "[US1] Create test file tests/integration/test_cli.py"
Task: "[US2] Write test for install command"
Task: "[US3] Write test for init command"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (--version)
4. Complete Phase 4: User Story 2 (install hello-world)
5. **STOP and VALIDATE**: Test full flow per quickstart.md
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test `--version` → Working CLI!
3. Add User Story 2 → Test `install hello-world` → Core feature complete!
4. Add User Story 3 → Test `init` → Full feature set
5. Polish → Production ready

---

## Notes

- All CLI output (help, errors, success messages) MUST be in English (FR-010)
- All command templates MUST be in English (FR-011)
- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
