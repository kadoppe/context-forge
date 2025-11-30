# Feature Specification: Role Plugin Migration Command

**Feature Branch**: `001-role-plugin-migrate`
**Created**: 2025-11-30
**Status**: Draft
**Input**: User description: "既存のrole plugin を、最新の context-forge.* コマンドを使って最新化・更新するための migrate コマンドをcontext-forge.* コマンドの１つとして実装して欲しいです。context-forge init コマンドでインストールできるようにしたい"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 既存プラグインの最新化 (Priority: P1)

開発者が以前のバージョンの context-forge で作成した role plugin を持っている場合、Claude Code で `/context-forge.migrate` コマンドを実行することで、Claude（LLM）が既存プラグインを分析し、最新の context-forge 仕様に準拠した形式に更新する。

**Why this priority**: これが機能の核心であり、ユーザーが既存の資産を失わずに最新機能を活用できるようにするため最優先

**Independent Test**: 旧形式のプラグインディレクトリを用意し、`/context-forge.migrate` 実行後に最新仕様に準拠しているか検証できる

**Acceptance Scenarios**:

1. **Given** `.claude/plugins/context-forge.role-*` ディレクトリに旧形式のプラグインが存在する, **When** Claude Code で `/context-forge.migrate` を実行する, **Then** Claude がプラグインを分析し、最新の仕様に更新して変更内容のサマリーを表示する
2. **Given** 複数の role plugin が存在する, **When** `/context-forge.migrate` を実行する, **Then** Claude がすべてのプラグインを順次分析・更新する
3. **Given** 更新前のプラグイン, **When** migrate を実行する, **Then** 更新前のファイルがバックアップとして保存される

---

### User Story 2 - init コマンドでのインストール (Priority: P2)

開発者が新しいプロジェクトで context-forge を初期化する際、CLI で `context-forge init` コマンドを実行することで、migrate 機能を含む context-forge の slash command ファイル群がプロジェクトにインストールされる。

**Why this priority**: 新規ユーザーのオンボーディング体験を向上させ、機能の発見性を高めるため

**Independent Test**: context-forge が未設定のプロジェクトで `context-forge init` を実行し、migrate コマンドファイルが配置されることを確認できる

**Acceptance Scenarios**:

1. **Given** context-forge がまだ設定されていないプロジェクト, **When** ターミナルで `context-forge init` を実行する, **Then** `context-forge.migrate.md` を含むコマンドファイルが `.claude/commands/` に配置される
2. **Given** init が完了したプロジェクト, **When** Claude Code で `/context-forge.migrate` を入力する, **Then** migrate コマンドが認識されて実行可能

---

### User Story 3 - 選択的なマイグレーション (Priority: P3)

開発者が特定のプラグインのみを更新したい場合、コマンド引数でプラグイン名を指定して migrate を実行することで、Claude が指定したプラグインのみを更新する。

**Why this priority**: 大規模プロジェクトでの柔軟な運用を可能にするため

**Independent Test**: 複数プラグインが存在する環境で、特定のプラグイン名を指定してmigrateを実行し、そのプラグインのみが更新されることを確認できる

**Acceptance Scenarios**:

1. **Given** 複数の role plugin が存在する, **When** `/context-forge.migrate software-engineer` を実行する, **Then** Claude が指定したプラグインのみを分析・更新する

---

### Edge Cases

- マイグレーション対象のプラグインが見つからない場合は何が起きるか？ → わかりやすいメッセージを表示して終了
- すでに最新形式のプラグインに対してmigrateを実行した場合は何が起きるか？ → 「すでに最新です」と表示してスキップ
- マイグレーション中にエラーが発生した場合は何が起きるか？ → バックアップから復元してエラー内容を表示
- バックアップ先に同名のファイルが既に存在する場合は何が起きるか？ → タイムスタンプ付きのバックアップ名を使用

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Claude は `.claude/plugins/context-forge.role-*` パターンに一致する既存のプラグインを検出できなければならない
- **FR-002**: Claude は検出したプラグインの `plugin.json` 内の version フィールドを確認し、現在の context-forge バージョン（コマンドファイル内に埋め込まれた値）より古い場合に更新が必要と判断しなければならない
- **FR-003**: Claude は更新が必要なプラグインについて、全コンポーネント（plugin.json, agents/, skills/, commands/, hooks/）を最新の仕様に準拠した形式に変換できなければならない
- **FR-004**: Claude はマイグレーション実行前に現在のプラグインファイルをバックアップとして保存しなければならない
- **FR-005**: ユーザーはコマンド引数でプラグイン名を指定してマイグレーション対象を限定できなければならない
- **FR-006**: Claude はマイグレーションの結果（更新されたファイル、スキップされたファイル、エラー）をユーザーに報告しなければならない
- **FR-007**: CLI の `context-forge init` コマンドは context-forge.* の全 slash command ファイルを `.claude/commands/` ディレクトリに配置しなければならない（既存ファイルがある場合は上書きする）
- **FR-008**: Claude はマイグレーション中にエラーが発生した場合、バックアップから復元できなければならない

### Key Entities

- **Role Plugin**: context-forge で生成された職能別知見プラグイン。`context-forge.role-{role-name}` の命名規則に従う
- **Slash Command File**: Claude Code で実行可能なコマンド定義ファイル（`.claude/commands/*.md`）
- **Backup**: マイグレーション前の状態を保存したファイル群。復元に使用
- **Migration Report**: マイグレーション結果のサマリー情報（更新・スキップ・エラーの一覧）

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: ユーザーは `/context-forge.migrate` を1回実行するだけで、すべての旧形式プラグインを最新化できる
- **SC-002**: Claude によるマイグレーション分析・更新は10個以下のプラグインに対して完了できる
- **SC-003**: エラー発生時はバックアップからの復元により既存機能を維持できる
- **SC-004**: ユーザーは `context-forge init` 実行後、追加設定なしで migrate コマンドを利用できる
- **SC-005**: 95%のユーザーがドキュメントを参照せずにマイグレーションを完了できる

## Clarifications

### Session 2025-11-30

- Q: 旧形式と最新形式を判別するための基準は何ですか？ → A: plugin.json の version フィールドで判定
- Q: init 実行時に既存のコマンドファイルが存在する場合、どう処理しますか？ → A: 上書きする（既存ファイルを置き換え）
- Q: マイグレーション対象となるプラグインコンポーネントは何ですか？ → A: 全コンポーネント（plugin.json, agents/, skills/, commands/, hooks/）
- Q: context-forge プラグインの現在の最新バージョン番号は何ですか？ → A: pyproject.toml の version フィールドを参照（init 時に {{VERSION}} プレースホルダーが置換される）
- Q: init コマンドで配置する context-forge コマンドファイルの範囲は？ → A: context-forge.* の全コマンド（将来追加分も含む）

## Assumptions

- 既存のプラグインは `.claude/plugins/context-forge.role-*` のディレクトリ構造に従っている
- マイグレーション対象は context-forge が生成したプラグインのみ（手動作成のプラグインは対象外）
- バックアップは `.claude/plugins/.backup/` ディレクトリに保存される
- `/context-forge.migrate` は Claude Code の slash command として実行される（LLM による処理）
- `context-forge init` は CLI コマンドとして実行される（ファイルコピー処理）
- init コマンドで配置されるファイルは context-forge パッケージに含まれるコマンドテンプレートからコピーする
