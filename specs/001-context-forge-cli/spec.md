# Feature Specification: context-forge CLI 初期実装

**Feature Branch**: `001-context-forge-cli`
**Created**: 2025-11-29
**Status**: Draft

## Clarifications

### Session 2025-11-29

- Q: コマンドテンプレートの格納場所は？ → A: パッケージ内蔵（context-forge パッケージに組み込みコマンドとして同梱）
- Q: CLI の出力言語は？ → A: 英語（ヘルプメッセージ、エラーメッセージ、成功メッセージ等すべて英語）
- Q: コマンドテンプレートの言語は？ → A: 英語（Claude Code にインストールするコマンドの内容も英語）

**Input**: User description: "context-forge という開発者向けツールの開発。AIコーディング支援ツールから参照できるコンテキストを、LLMとの対話を通じて作成・更新できるツール。Claude Code をはじめとした様々なAIコーディング支援ツールにインストール可能。初期実装として hello-world コマンドを Claude Code にインストールできるようにする。"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - context-forge のインストール (Priority: P1)

開発者として、context-forge をローカル環境にインストールして、Claude Code で使用できるようにしたい。これにより、チームで共有可能なコンテキストやコマンドを管理する準備ができる。

**Why this priority**: ツールを使用するための最初のステップであり、これがなければ他の機能を利用できない。

**Independent Test**: パッケージマネージャーを使用してインストールし、バージョン確認コマンドが正常に動作することで検証できる。

**Acceptance Scenarios**:

1. **Given** 開発者がインストールコマンドを実行する, **When** インストールが完了する, **Then** context-forge コマンドが利用可能になる
2. **Given** context-forge がインストールされている, **When** バージョン確認コマンドを実行する, **Then** インストールされたバージョンが表示される

---

### User Story 2 - hello-world コマンドの Claude Code へのインストール (Priority: P1)

開発者として、context-forge を使用して hello-world サンプルコマンドを Claude Code にインストールしたい。これにより、context-forge のコマンドインストール機能が正常に動作することを確認でき、将来的にチーム固有のコマンドを追加する基盤となる。

**Why this priority**: context-forge の核となる機能であり、コマンド配布の仕組みを検証するために不可欠。

**Independent Test**: hello-world コマンドをインストール後、Claude Code 内で `/context-forge.hello-world` スラッシュコマンドを実行し、期待通りの出力が得られることで検証できる。

**Acceptance Scenarios**:

1. **Given** context-forge がインストールされている, **When** hello-world コマンドのインストールを実行する, **Then** プロジェクトの `.claude/commands/` ディレクトリに context-forge.hello-world.md ファイルが作成される
2. **Given** hello-world コマンドがインストールされている, **When** Claude Code で `/context-forge.hello-world` を実行する, **Then** 挨拶メッセージが表示される
3. **Given** hello-world コマンドが既にインストールされている, **When** 再度インストールを試みる, **Then** 上書き確認のプロンプトが表示される

---

### User Story 3 - プロジェクトの初期化 (Priority: P2)

開発者として、現在のプロジェクトに context-forge の設定を初期化したい。これにより、プロジェクト固有のコンテキストやコマンドを管理するための基盤が整う。

**Why this priority**: コマンドをインストールする前にプロジェクトを初期化することで、設定の一貫性が保たれる。ただし、初期実装では省略可能。

**Independent Test**: 初期化コマンドを実行後、`.claude/commands/` ディレクトリが作成されることで検証できる。

**Acceptance Scenarios**:

1. **Given** context-forge がインストールされている, **When** プロジェクトディレクトリで初期化コマンドを実行する, **Then** `.claude/` ディレクトリと `.claude/commands/` サブディレクトリが作成され、全ての利用可能なコマンドがインストールされる
2. **Given** プロジェクトが既に初期化されている, **When** 再度初期化を試みる, **Then** 既存設定を保持するか上書きするかの選択肢が提示される
3. **Given** context-forge がインストールされている, **When** `--skip-install` オプション付きで初期化コマンドを実行する, **Then** ディレクトリのみ作成され、コマンドはインストールされない
4. **Given** context-forge がインストールされている, **When** `context-forge init` を実行する, **Then** `.claude/commands/context-forge.hello-world.md` が自動的に作成される

---

### Edge Cases

- ディレクトリへの書き込み権限がない場合、適切なエラーメッセージを表示する
- 既存の `.claude/commands/` ディレクトリが存在する場合、ディレクトリ構造を壊さずに追加する
- コマンドファイル名に無効な文字が含まれる場合、エラーを返す
- ネットワーク接続なしでもローカルコマンドのインストールが可能

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: システムは、パッケージマネージャーを通じてインストール可能でなければならない
- **FR-002**: システムは、`context-forge --version` コマンドでバージョン情報を表示できなければならない
- **FR-003**: システムは、`context-forge init` コマンドでプロジェクトを初期化できなければならない
- **FR-012**: システムは、`context-forge init` でデフォルトで全ての利用可能なコマンドをインストールしなければならない
- **FR-013**: システムは、`context-forge init --skip-install` でコマンドのインストールをスキップできなければならない
- **FR-004**: システムは、`context-forge install hello-world` コマンドで hello-world コマンドを Claude Code にインストールできなければならない
- **FR-005**: システムは、インストール時に既存ファイルの上書き確認を行わなければならない
- **FR-006**: システムは、操作結果を分かりやすいメッセージで表示しなければならない（すべて英語）
- **FR-007**: システムは、Claude Code のスラッシュコマンド形式（.md ファイル）でコマンドを出力しなければならない
- **FR-008**: システムは、インストールするコマンドのファイル名に `context-forge.` 接頭辞を自動的に付与しなければならない（例: hello-world → context-forge.hello-world.md）
- **FR-009**: システムは、エラー発生時に適切なエラーメッセージと終了コードを返さなければならない
- **FR-010**: システムは、すべての CLI 出力（ヘルプ、エラー、成功メッセージ）を英語で表示しなければならない
- **FR-011**: システムは、コマンドテンプレート（Claude Code にインストールするコマンド）を英語で提供しなければならない

### Key Entities

- **Command**: インストール可能なコマンドテンプレート。名前、説明、コマンド本体（Markdown形式）を持つ。context-forge パッケージに組み込みコマンドとして同梱される
- **Project**: context-forge で管理されるプロジェクト。設定ファイルとインストール済みコマンドの参照を持つ
- **Configuration**: プロジェクト設定。ターゲットAIツール、インストール先パスなどを保持

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 新規ユーザーが3分以内に context-forge をインストールし、hello-world コマンドを Claude Code で実行できる
- **SC-002**: インストールプロセスは5ステップ以内で完了する
- **SC-003**: エラー発生時、ユーザーが次に取るべきアクションが明確に示される
- **SC-004**: インストールしたコマンドが Claude Code で認識され、スラッシュコマンドとして利用可能になる
- **SC-005**: コマンドのインストール操作が10秒以内に完了する

## Assumptions

- ユーザーは Python 3.11 以上がインストールされた開発環境を持っている
- ユーザーは Claude Code が既にインストールされており、基本的な使用方法を理解している
- インターネット接続は初回のツールインストール時のみ必要で、コマンドのローカルインストールには不要
- `.claude/commands/` ディレクトリは Claude Code の標準的なスラッシュコマンド配置場所である
- spec-kit の技術スタック（Python、uv）を踏襲する
