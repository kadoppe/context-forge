# Feature Specification: Skill/SubAgent 発動率向上

**Feature Branch**: `003-skill-subagent-activation`
**Created**: 2025-11-30
**Status**: Draft
**Input**: User description: "add_role_knowledge コマンドで追加された Skill や Subagent が自動で起動しないことが多い問題。context-forge cli が生成するコマンドの仕組みから改善。CLAUDE.md から context-forge 用の専用 md を参照する形式に変更。"

## Clarifications

### Session 2025-11-30

- Q: CLAUDE.md から専用ファイルを参照する方式は？ → A: `@.claude/context-forge.md` 形式（Claude Code 公式の @ 記法）
- Q: context-forge.md 内の発動条件記述形式は？ → A: 明示的なルール形式（「〇〇の場合、△△を使用すること」のような指示形式）
- Q: 既存ユーザーの新形式への移行タイミングは？ → A: `context-forge init` 実行時に自動移行（確認メッセージ表示）

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Skill/SubAgent の自動発動 (Priority: P1)

ユーザーが context-forge で追加した Skill や SubAgent が、関連する作業を行う際に Claude Code によって自動的に発動・参照される。

**Why this priority**: Skill/SubAgent が発動しなければ、せっかく追加した知見が活用されず、ツールとしての価値がなくなるため最優先。

**Independent Test**: ユーザーがロールに関連する質問をした際、対応する Skill/SubAgent が自動的に呼び出されることを確認。

**Acceptance Scenarios**:

1. **Given** software-engineer ロールに「PRレビュー支援」SubAgent が追加されている, **When** ユーザーが「PRをレビューして」と依頼する, **Then** 対応する SubAgent が自動的に Task ツールで呼び出される
2. **Given** frontend-engineer ロールに「React ベストプラクティス」Skill が追加されている, **When** ユーザーが React コンポーネントの実装について質問する, **Then** 対応する Skill が自動的に参照される
3. **Given** 複数のロールに複数の Skill/SubAgent が追加されている, **When** ユーザーが特定の作業を依頼する, **Then** 最も適切な Skill/SubAgent のみが発動する（過剰発動しない）

---

### User Story 2 - CLAUDE.md の肥大化防止 (Priority: P2)

CLAUDE.md が context-forge の設定情報で肥大化せず、専用ファイルから参照する形式になっている。

**Why this priority**: CLAUDE.md が長くなりすぎると可読性が低下し、他のプロジェクト固有の指示との混在で管理が困難になるため。

**Independent Test**: context-forge init 実行後、CLAUDE.md に追加される内容が参照リンクのみ（10行以下）であることを確認。

**Acceptance Scenarios**:

1. **Given** 新規プロジェクトで context-forge init を実行した, **When** CLAUDE.md が生成・更新される, **Then** `@.claude/context-forge.md` 形式の参照のみが追加される（実際の設定内容は別ファイル）
2. **Given** 既存の CLAUDE.md がある, **When** context-forge init を実行する, **Then** 既存の内容を保持しつつ、@ 参照リンクのみが追加される
3. **Given** context-forge 用の専用 md ファイルが存在する, **When** ユーザーが設定を編集したい, **Then** 専用ファイルのみを編集すれば良い（CLAUDE.md の編集不要）

---

### User Story 3 - 発動条件の明示的な記述 (Priority: P3)

context-forge が生成する Skill/SubAgent の description に、発動トリガーとなる具体的な表現パターンが含まれている。

**Why this priority**: 参考記事によると、description に複数のトリガー表現パターンを含めることで発動率が向上するため。

**Independent Test**: 生成された Skill/SubAgent の description を確認し、複数の呼び出し表現パターンが含まれていることを確認。

**Acceptance Scenarios**:

1. **Given** ユーザーが「コードレビューのチェックリスト」Skill を追加した, **When** Skill ファイルが生成される, **Then** description に「コードレビュー」「レビューして」「チェックリスト」など複数のトリガー表現が含まれる
2. **Given** ユーザーが「PRレビュー支援」SubAgent を追加した, **When** SubAgent ファイルが生成される, **Then** description に「PRをレビュー」「プルリクを確認」「レビューコメント」など複数のトリガー表現が含まれる

---

### Edge Cases

- 複数のロールで類似した Skill/SubAgent がある場合、どちらを発動するか？（→ 最も具体的にマッチするものを優先、Claude Code の判断に委ねる）
- CLAUDE.md が存在しない場合の初期化はどうなるか？（→ 新規作成し @ 参照リンクを追加）
- 専用 md ファイルを誤って削除した場合はどうなるか？（→ 次回 init 時に再生成、警告メッセージを表示）
- 既存の context-forge プラグインがすでに CLAUDE.md に記載されている場合は？（→ 移行処理で専用ファイルに移動）

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: システムは context-forge 用の設定を専用ファイル（`.claude/context-forge.md`）に保存し、CLAUDE.md からは `@.claude/context-forge.md` 形式の参照のみを追加すること
- **FR-002**: `context-forge init` コマンド実行時、CLAUDE.md に `@.claude/context-forge.md` 参照を自動追加すること
- **FR-003**: 専用ファイルには、追加されたすべての Skill/SubAgent の発動条件を明示的なルール形式（「ユーザーが〇〇と言った場合、必ず Task ツールで△△を使用すること」のような指示形式）で記述すること
- **FR-004**: Skill/SubAgent の description には、少なくとも3つ以上のトリガー表現パターンを含めること
- **FR-005**: add-role-knowledge コマンドで Skill/SubAgent を追加した際、専用ファイルの発動条件一覧を自動更新すること
- **FR-006**: 既存の CLAUDE.md 内の context-forge 関連設定がある場合、`context-forge init` 実行時に確認メッセージを表示し、専用ファイルへ自動移行すること
- **FR-007**: 専用ファイル内に、各ロールの Skill/SubAgent 一覧と発動条件を構造化して記述すること

### Key Entities

- **context-forge 設定ファイル**: `.claude/context-forge.md` - CLAUDE.md から `@` 記法で参照される専用設定ファイル。発動条件の明示的な記述を含む
- **発動条件（Trigger Pattern）**: Skill/SubAgent を自動発動させるためのトリガー表現パターンのリスト
- **@ 参照**: CLAUDE.md から専用ファイルを読み込むための `@path/to/file` 形式の記述

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 追加した Skill/SubAgent の発動率が 80% 以上に向上する（関連タスク依頼時）
  - 測定方法: 同一の Skill/SubAgent に対して 10 回の関連タスクを依頼し、8 回以上で適切な Skill/SubAgent が発動すること
  - 検証タイミング: 手動テスト（T032）実行時
- **SC-002**: CLAUDE.md への context-forge 関連の追加行数が 10 行以下に抑えられる
- **SC-003**: ユーザーが Skill/SubAgent の発動条件を確認・編集できる場所が 1 箇所（専用ファイル）に集約される
- **SC-004**: 既存ユーザーが新しい形式に移行する際、手動での設定変更が不要である（自動移行）

## Assumptions

- Claude Code は CLAUDE.md 内の `@path/to/file` 記法で他の md ファイルを参照・インクルードできる（公式ドキュメントで確認済み）
- description に具体的なトリガー表現を含めることで発動率が向上するという参考記事の知見は正しい
- `.claude/` ディレクトリ内にカスタム md ファイルを配置することが許容されている
