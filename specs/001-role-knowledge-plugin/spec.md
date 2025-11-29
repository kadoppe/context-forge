# Feature Specification: Role Knowledge Plugin Generator

**Feature Branch**: `001-role-knowledge-plugin`
**Created**: 2025-11-29
**Status**: Draft
**Input**: チームの職能ごとの知見をClaude Codeのコンテキストに追加するためのClaude Code Commandを追加し、context-forge CLIでインストールできるようにする

## Clarifications

### Session 2025-11-29

- Q: 生成されたロールプラグインをどこに保存するか？ → A: プロジェクトディレクトリ（`.claude/plugins/`）に保存。Git経由でチーム共有可能。
- Q: context-forge CLIのインストールコマンド名は？ → A: `context-forge init`（全コマンドを一括インストール）
- Q: Claude Code内で実行するスラッシュコマンド名は？ → A: `/add-role-knowledge`（ユーザー視点で知見追加という意図が明確）
- Q: 対応OSの範囲は？ → A: macOS + Linux（Windowsは初期バージョンでは対象外）
- Q: 公式ドキュメント取得失敗時の動作は？ → A: 警告を表示して前回キャッシュで続行

## Overview

チーム内の各職能（ロール）が持つ専門知識やスキルを、Claude Codeプラグインとして対話的に作成・更新できるClaude Code Commandを提供する。このCommandはcontext-forge CLIを通じてインストールされ、ユーザーはClaude Code内でスラッシュコマンドを実行することで、職能ごとのプラグインを簡単に生成・管理できるようになる。

### 機能の構成

1. **context-forge CLI** → 「ロールプラグイン生成Command」をClaude Code環境にインストール
2. **ロールプラグイン生成Command**（Claude Code内で実行）→ 対話的に職能プラグインを作成・更新
3. **職能プラグイン**（生成物）→ 各ロールの知見をSub Agent/Command/Skill/Hookとして含む

## User Scenarios & Testing *(mandatory)*

### User Story 1 - ロールプラグイン生成Commandのインストール (Priority: P1)

開発者が、context-forge CLIを使用して、ロールプラグインを対話的に作成・更新するためのClaude Code Commandを自分の環境にインストールしたい。

**Why this priority**: このCommandがインストールされていなければ、ロールプラグインの作成・更新機能を利用できない。

**Independent Test**: context-forge CLIでインストールコマンドを実行し、Claude Code内でロールプラグイン生成用のスラッシュコマンドが利用可能になることを確認できる。

**Acceptance Scenarios**:

1. **Given** context-forge CLIがインストールされている状態で、**When** ユーザーがロールプラグイン生成Commandのインストールコマンドを実行すると、**Then** Claude Codeの適切な場所にCommandがインストールされる
2. **Given** Commandのインストールが完了した状態で、**When** ユーザーがClaude Codeを起動してスラッシュコマンド一覧を確認すると、**Then** ロールプラグイン生成用のコマンドが表示される
3. **Given** 既にCommandがインストールされている状態で、**When** 再度インストールを試みると、**Then** 更新確認プロンプトが表示され、承諾すると既存のCommandが更新される

---

### User Story 2 - 新規ロールプラグインの作成 (Priority: P1)

チームリードが、Claude Code内でスラッシュコマンドを実行し、フロントエンドエンジニアの知見を新しいプラグインとして対話的に作成したい。

**Why this priority**: これがCommand機能の核心であり、新しいロールプラグインを作成できなければ他の機能は意味をなさない。

**Independent Test**: Claude Code内でスラッシュコマンドを実行し、新規ロールを定義してプラグインが正しく生成されることを確認できる。

**Acceptance Scenarios**:

1. **Given** ロールプラグイン生成Commandがインストールされている状態で、**When** ユーザーがClaude Code内で`/add-role-knowledge`を実行すると、**Then** 対話的なロール作成フローが開始される
2. **Given** 対話フローが開始された状態で、**When** ユーザーが「フロントエンドエンジニア」という新規ロール名と説明を入力すると、**Then** 対応するClaude Codeプラグインのディレクトリ構造とplugin.jsonが生成される
3. **Given** ロール作成フローにいる状態で、**When** ユーザーが知見・スキルの内容を入力すると、**Then** 入力に基づいてSub Agent/Command/Skill/Hookのいずれかが適切に選択され、対応するファイルが生成される
4. **Given** プラグイン生成が完了した状態で、**When** ユーザーがClaude Codeでプラグインをロードすると、**Then** 定義したロールの知見がClaude Codeのコンテキストとして利用可能になる

---

### User Story 3 - 既存ロールプラグインの更新 (Priority: P2)

既存のバックエンドエンジニア向けプラグインに、新しいマイクロサービス設計のスキルを追加したい。Claude Code内でスラッシュコマンドを実行し、既存プラグインを選択して新しいスキルを追加する。

**Why this priority**: ロールの知見は時間とともに進化するため、既存プラグインを更新できることが継続的な価値を提供する。

**Independent Test**: Claude Code内でスラッシュコマンドを実行し、既存プラグインを選択して新しいスキルを追加できることを確認できる。

**Acceptance Scenarios**:

1. **Given** 既存のロールプラグインが存在する状態で、**When** ユーザーが`/add-role-knowledge`を実行してそのロールを選択すると、**Then** 既存プラグインの内容が表示され、追加・編集オプションが提示される
2. **Given** 既存プラグインの編集モードにいる状態で、**When** ユーザーが新しいスキルの説明を入力すると、**Then** 適切な形式（Sub Agent/Command/Skill/Hook）でプラグインに追加される
3. **Given** プラグインの更新が完了した状態で、**When** ユーザーがClaude Codeでプラグインを再ロードすると、**Then** 新しく追加したスキルが利用可能になる

---

### User Story 4 - 知見タイプの自動判別と適切な形式での実装 (Priority: P2)

ユーザーが入力した知見やスキルの内容を分析し、Sub Agent、Command、Skill、Hookのうち最適な実装形式を自動的に提案する。

**Why this priority**: ユーザーがClaude Codeのプラグイン構造に詳しくなくても、適切な形式でプラグインを構成できるようにするため。

**Independent Test**: 様々なタイプの知見入力に対して、適切な実装形式が提案されることを確認できる。

**Acceptance Scenarios**:

1. **Given** ロール知見追加フローにいる状態で、**When** ユーザーが「コードレビューのチェックリスト」という知見を入力すると、**Then** システムはこれをSkillとして実装することを提案する
2. **Given** ロール知見追加フローにいる状態で、**When** ユーザーが「設計ドキュメント作成の自動化」という知見を入力すると、**Then** システムはこれをCommandとして実装することを提案する
3. **Given** ロール知見追加フローにいる状態で、**When** ユーザーが「アーキテクチャレビューを自律的に行う」という知見を入力すると、**Then** システムはこれをSub Agentとして実装することを提案する
4. **Given** ロール知見追加フローにいる状態で、**When** ユーザーが「コミット前にセキュリティチェックを実行」という知見を入力すると、**Then** システムはこれをHookとして実装することを提案する

---

### Edge Cases

- ユーザーが空のロール名を入力した場合、どのように処理するか？ → エラーメッセージを表示し再入力を促す
- 既存プラグインと同名の新規プラグインを作成しようとした場合、どのように処理するか？ → 既存プラグインの更新フローに誘導する
- Commandのインストール先ディレクトリが存在しない場合、どのように処理するか？ → ディレクトリを作成するか確認プロンプトを表示する
- ユーザーの入力からSub Agent/Command/Skill/Hookのどれが最適か判断できない場合、どのように処理するか？ → ユーザーに選択を求める
- Claude Code環境が検出できない場合、どのように処理するか？ → エラーメッセージを表示し、Claude Codeのインストールを案内する
- 公式ドキュメントの取得に失敗した場合、どのように処理するか？ → 警告を表示して前回キャッシュで続行する

## Requirements *(mandatory)*

### Functional Requirements

**context-forge CLI関連**

- **FR-001**: context-forge CLIは、`context-forge init`コマンドで全てのコマンド（add-role-knowledgeを含む）をClaude Code環境にインストールできなければならない
- **FR-002**: context-forge CLIは、インストール時に既存のCommandとの競合を検出し、ユーザーに確認を求めなければならない
- **FR-003**: context-forge CLIは、Claude Code環境の適切なインストール先を自動検出しなければならない

**ロールプラグイン生成Command関連**

- **FR-004**: Commandは、実行されるたびにClaude Code公式ドキュメントを参照し、最新のPlugin/Command/Skill/Hook/Sub Agent仕様に基づいてプラグインを生成しなければならない
  - 参照すべきドキュメント:
    - https://code.claude.com/docs/en/plugins
    - https://code.claude.com/docs/en/sub-agents
    - https://code.claude.com/docs/en/skills
    - https://code.claude.com/docs/en/hooks-guide
- **FR-005**: Commandは、対話的なプロンプトを通じてユーザーから職能（ロール）の情報を収集できなければならない
- **FR-006**: Commandは、新規ロール名の入力と既存ロールの選択の両方をサポートしなければならない
- **FR-007**: Commandは、各ロールに対してClaude Codeプラグイン形式のディレクトリ構造（plugin.json、commands/、agents/、skills/、hooks/）をプロジェクトの`.claude/plugins/`配下に生成しなければならない
- **FR-008**: Commandは、ユーザーが入力した知見・スキルの内容を分析し、Sub Agent、Command、Skill、Hookのいずれかの形式を提案しなければならない
- **FR-009**: Commandは、既存プラグインへの知見追加・更新機能を提供しなければならない
- **FR-010**: 生成されるロールプラグインは、Claude Codeのプラグイン仕様に準拠しなければならない

### Key Entities

- **Role Plugin Generator Command**: context-forge CLIによってインストールされるClaude Code Command。ロールプラグインを対話的に作成・更新する機能を提供
- **Role（職能）**: チーム内の専門職能を表す。名前、説明、関連スキルのリストを持つ
- **Role Plugin（ロールプラグイン）**: 生成されるClaude Codeプラグイン。plugin.json メタデータ、コマンド、エージェント、スキル、フックを含む
- **Knowledge Item（知見項目）**: 各ロールが持つ個別の知見やスキル。タイプ（Sub Agent/Command/Skill/Hook）、名前、説明、内容を持つ

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: ユーザーはcontext-forge CLIで1コマンドでロールプラグイン生成CommandをClaude Codeにインストールできる
- **SC-002**: ユーザーはClaude Code内で5分以内に新規ロールプラグインを作成し、利用可能な状態にできる
- **SC-003**: 生成されたロールプラグインの100%がClaude Codeで正常にロード・動作する
- **SC-004**: 知見タイプの自動判別により、ユーザーの80%以上が提案された形式をそのまま採用する
- **SC-005**: 既存プラグインへの知見追加が、既存の知見に影響を与えることなく完了する

## Assumptions

- ユーザーはcontext-forge CLIをすでにインストールしている
- ユーザーはClaude Code環境をセットアップ済みである
- Claude Codeはスラッシュコマンドによるプラグイン生成をサポートしている
- ユーザーはロールの知見・スキルをテキスト形式で記述できる

## Out of Scope

- ロールプラグイン自体のリモートリポジトリからの直接インストール
- ロールプラグインのバージョン管理機能
- ロールプラグインの依存関係管理
- ロールプラグインの削除・アンインストール機能（初期バージョン）
- チーム間でのロールプラグイン共有のためのレジストリ機能
- ロールプラグイン生成Commandのアンインストール機能（初期バージョン）
- Windows対応（初期バージョン）
