# Tasks: GitHub Actions CI Setup

**Input**: Design documents from `/specs/002-github-actions-ci/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md

**Tests**: テストタスクは仕様で明示的に要求されていないため、含まれていません。

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **CI Workflow**: `.github/workflows/ci.yml`
- **Repository Settings**: GitHub Web UI (Settings → Branches)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: ワークフローディレクトリの作成

- [x] T001 Create `.github/workflows/` directory structure

---

## Phase 2: User Story 1 - コード品質の自動検証 (Priority: P1) 🎯 MVP

**Goal**: PR作成・mainプッシュ時にruff、mypy、pytestを自動実行し、結果をGitHub上に表示する

**Independent Test**: PRを作成し、CIが自動実行されてチェック結果がGitHub PRページに表示されることを確認

### Implementation for User Story 1

- [x] T002 [US1] Create CI workflow file `.github/workflows/ci.yml` with workflow name and trigger configuration (on: pull_request, push to main)
- [x] T003 [P] [US1] Add lint job to `.github/workflows/ci.yml` with Python 3.11 setup, dependency install, and `ruff check .` execution
- [x] T004 [P] [US1] Add type-check job to `.github/workflows/ci.yml` with Python 3.11 setup, dependency install, and `mypy src` execution
- [x] T005 [P] [US1] Add test job to `.github/workflows/ci.yml` with Python 3.11 setup, dependency install, and `pytest` execution
- [x] T006 [US1] Configure pip caching using `actions/setup-python@v5` cache option in all jobs
- [x] T007 [US1] Set job timeout to 10 minutes for all jobs in `.github/workflows/ci.yml`
- [ ] T008 [US1] Verify workflow by pushing branch and creating PR to validate CI execution (manual verification after push)

**Checkpoint**: CIワークフローが動作し、PR上でruff、mypy、pytestの結果が確認できる状態

---

## Phase 3: User Story 2 - PRマージ前のCI必須チェック (Priority: P2)

**Goal**: CIチェックが失敗しているPRのマージをブロックする

**Independent Test**: CI失敗PRでマージボタンが無効化されていることを確認

### Implementation for User Story 2

- [x] T009 [US2] Document branch protection rule setup instructions in specs/002-github-actions-ci/quickstart.md
- [ ] T010 [US2] Configure branch protection rule for main branch via GitHub Settings → Branches → Add rule (manual)
- [ ] T011 [US2] Enable "Require status checks to pass before merging" and select CI jobs as required checks (manual)
- [ ] T012 [US2] Verify protection by confirming merge is blocked when CI fails (manual)

**Checkpoint**: CI失敗時にマージがブロックされ、成功時のみマージ可能な状態

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: ドキュメント整備と最終確認

- [x] T013 [P] Update quickstart.md with troubleshooting section for common CI failures
- [x] T014 Validate all acceptance scenarios from spec.md are satisfied

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **User Story 1 (Phase 2)**: Depends on Setup completion
- **User Story 2 (Phase 3)**: Depends on User Story 1 completion (CI must be working first)
- **Polish (Phase 4)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup - No dependencies on other stories
- **User Story 2 (P2)**: Requires User Story 1 to be complete (CI jobs must exist before configuring branch protection)

### Within User Story 1

- T002 (workflow base) → T003, T004, T005 (parallel jobs) → T006, T007 (configuration) → T008 (verification)

### Parallel Opportunities

- T003, T004, T005: lint, type-check, test jobs can be implemented in parallel (different sections of same file)
- T013: Documentation can be done in parallel with other polish tasks

---

## Parallel Example: User Story 1 Jobs

```bash
# After T002 (base workflow) is complete, launch job implementations in parallel:
Task: "Add lint job to .github/workflows/ci.yml"
Task: "Add type-check job to .github/workflows/ci.yml"
Task: "Add test job to .github/workflows/ci.yml"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: User Story 1 (T002-T008)
3. **STOP and VALIDATE**: Create PR and verify CI runs correctly
4. CI is now functional - can be used immediately

### Incremental Delivery

1. Complete Setup → Directory ready
2. Complete User Story 1 → CI running on PRs (MVP!)
3. Complete User Story 2 → Branch protection enabled
4. Complete Polish → Documentation finalized

---

## Notes

- すべてのジョブはPython 3.11で実行
- 各ジョブは並列実行され、1つ失敗しても他は継続（fail-fast: false）
- User Story 2はGitHub Web UIでの設定作業を含む
- ワークフローファイルは単一ファイル（`.github/workflows/ci.yml`）に統合
