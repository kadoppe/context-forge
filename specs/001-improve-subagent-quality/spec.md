# Feature Specification: SubAgent品質向上のためのプロンプト改善

**Feature Branch**: `001-improve-subagent-quality`
**Created**: 2025-11-30
**Status**: Draft
**Input**: User description: "add_role_knowledge コマンドで追加された SubAgent、実際にPull Request でマージしようとすると、Pull Request でいくつかの指摘をもらってしまった。次回移行SubAgentを作る時に同じような指摘を貰わないように add_role_knowledge のプロンプトを改善できないか。具体的な指摘事項そのものではなく、少し広く捉えて汎用的な改善を施したい"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - SubAgentの高品質な自動生成 (Priority: P1)

ユーザーが `add-role-knowledge` コマンドを使ってSubAgentを追加する際、生成されるSubAgentファイルが最初からレビュー指摘を受けにくい高品質なものになる。

**Why this priority**: SubAgent生成はコマンドの主要機能であり、品質が低いと毎回手動修正が必要になり、コマンドの価値が大幅に低下する。

**Independent Test**: コマンドでSubAgentを生成し、生成されたファイルが品質ガイドラインを満たしているかを確認できる。

**Acceptance Scenarios**:

1. **Given** ユーザーがSubAgentの知見を入力した、**When** コマンドがSubAgentファイルを生成する、**Then** 生成されたファイルにはプレースホルダー（`<xxx>`, `{xxx}`）が含まれない
2. **Given** ユーザーがbashコマンドを含むSubAgentを作成した、**When** コマンドがファイルを生成する、**Then** bashコマンドには適切なエラーハンドリングが含まれる
3. **Given** ユーザーがgit操作を含むSubAgentを作成した、**When** コマンドがファイルを生成する、**Then** 安全なgit操作パターン（個別ファイル指定、diff確認等）が使用される

---

### User Story 2 - 品質チェックリストの自動適用 (Priority: P2)

SubAgent生成時に、コマンド内部で品質チェックリストが自動的に適用され、一般的な問題が事前に検出・修正される。

**Why this priority**: 生成後のレビュー指摘を待つのではなく、生成段階で品質を担保することで、開発サイクルを短縮できる。

**Independent Test**: 意図的に問題のある入力をして、コマンドがその問題を検出・修正できるかを確認できる。

**Acceptance Scenarios**:

1. **Given** SubAgent生成プロセス中、**When** コマンドがファイルを生成する、**Then** 内部品質チェックが自動実行される
2. **Given** 品質チェックで問題が検出された、**When** ファイル生成が完了する、**Then** 問題は自動修正されるか、ユーザーに警告が表示される

---

### User Story 3 - ベストプラクティスの組み込み (Priority: P3)

SubAgentテンプレートに業界標準のベストプラクティスが組み込まれ、ユーザーが特別な知識を持たなくても高品質なSubAgentを作成できる。

**Why this priority**: ユーザーの学習コストを下げ、一貫した品質のSubAgentを組織全体で作成できるようにする。

**Independent Test**: 異なるユーザーが同じ種類のSubAgentを作成した際、一貫した品質レベルになることを確認できる。

**Acceptance Scenarios**:

1. **Given** ユーザーがSubAgentを作成する、**When** テンプレートが適用される、**Then** セキュリティ考慮事項が自動的に含まれる
2. **Given** bashコマンドを含むSubAgentを作成する、**When** テンプレートが適用される、**Then** 変数のクォーティングやエラーハンドリングのパターンが含まれる

---

### Edge Cases

- bashコマンドを一切含まないSubAgent（純粋な分析・判断タスク）の場合、不要なbash関連ガイドラインは省略される
- 非常に複雑なワークフローを持つSubAgentの場合でも、品質チェックは必須項目のみに絞り、過剰な制約を課さない
- ユーザーが意図的にシンプルなSubAgentを望む場合、必須の安全性要件のみを適用し、推奨事項は省略可能とする

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: コマンドは、生成するSubAgentファイル内にプレースホルダー構文（`<xxx>`, `{xxx}`）を残さず、実行可能なコマンド例のみを含めなければならない
- **FR-002**: bashコマンドを含むSubAgentを生成する際、コマンドは変数キャッシュ、エラーハンドリング、適切なクォーティングのパターンを含めなければならない
- **FR-003**: git操作を含むSubAgentを生成する際、コマンドは安全なパターン（`git add`での個別ファイル指定、`git diff --staged`での確認、`git pull --rebase`での競合回避）を含めなければならない
- **FR-004**: 生成されるSubAgentには、注意事項セクションとして安全なコマンド実行のガイドラインを含めなければならない
- **FR-005**: 生成されるSubAgentには、トラブルシューティングセクションとして一般的な問題と対処法を含めなければならない
- **FR-006**: コマンドは、SubAgent生成完了前に内部品質チェックを実行し、基準を満たさない項目があれば自動修正を行い、自動修正できない場合のみ警告を表示しなければならない

### Key Entities

- **SubAgentテンプレート**: SubAgent生成時に使用されるベーステンプレート。品質ガイドライン、ベストプラクティス、必須セクションを含む
- **品質チェックリスト**: SubAgent生成時に自動適用される品質基準のリスト。プレースホルダー検出、セキュリティパターン、エラーハンドリングなどを検証
- **ベストプラクティス集**: bashコマンド、git操作、API呼び出しなど、よくあるパターンの推奨実装例

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 生成されたSubAgentがPRレビューで受ける指摘件数が、改善前と比較して50%以上減少する
- **SC-002**: 生成されたSubAgentの初回PRマージ成功率が80%以上になる（修正なしでマージ可能）
- **SC-003**: ユーザーがSubAgent生成後に手動で行う修正作業の時間が、平均5分以内に収まる
- **SC-004**: 生成されたSubAgentに含まれるbashコマンドの100%が、変数展開時のクォーティングエラーを起こさない

## Clarifications

### Session 2025-11-30

- Q: 品質チェックで問題が検出された際、コマンドはどのように対応すべきか？ → A: 自動修正を優先し、修正できない場合のみ警告

## Assumptions

- PRレビューはClaude Code Reviewまたは同等の自動レビューツールで行われる
- SubAgentが主に使用するツールはBash、Read、Write、Edit、Grep、Globである
- 生成されるSubAgentは主に開発ワークフローの自動化に使用される（CI/CD、コードレビュー、ドキュメント生成など）
- ユーザーはbashやgitの基本的な知識を持っているが、ベストプラクティスについては詳しくない可能性がある
- **改善対象は `context-forge init` でインストールされるテンプレート（`src/context_forge_cli/templates/commands/add-role-knowledge.md`）であり、プロジェクトにインストール済みの `.claude/commands/` 配下のファイルではない**
