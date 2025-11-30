# Quality Contract: SubAgent生成品質基準

**Date**: 2025-11-30
**Feature**: 001-improve-subagent-quality

## 概要

この文書は、`add-role-knowledge` コマンドで生成されるSubAgentが満たすべき品質基準を定義する。

## 品質基準

### 1. 構造要件

生成されるSubAgentファイルは以下の構造を持たなければならない。

```yaml
structure:
  frontmatter:
    required:
      - name: "kebab-case, 64文字以内"
      - description: "1-2文の簡潔な説明"
    optional:
      - tools: "カンマ区切りのツール名"
      - model: "sonnet | opus | haiku"

  body:
    required:
      - heading_level_1: "# {Agent Name}"
      - section_execution: "## 実行手順"
      - section_troubleshooting: "## トラブルシューティング"
      - section_notes: "## 注意事項"
```

### 2. コンテンツ要件

#### 2.1 プレースホルダー禁止

以下のパターンは禁止される：

```regex
Forbidden patterns:
  - <[a-zA-Z_-]+>     # 例: <run-id>, <file-path>
  - \{[a-zA-Z_/]+\}   # 例: {owner}/{repo}, {pr_number}
```

許容されるパターン：

```regex
Allowed patterns:
  - ${VAR_NAME}       # シェル変数展開
  - $(command)        # コマンド置換
```

#### 2.2 Bashコマンド要件

```yaml
bash_requirements:
  variable_quoting:
    required: true
    pattern: '"${VAR}"' or '"$VAR"'

  error_handling:
    recommended: true
    patterns:
      - "if [ -n \"$VAR\" ]; then"
      - "command || fallback"

  variable_caching:
    recommended: true
    description: "同じコマンドを複数回実行する代わりに変数にキャッシュ"
```

#### 2.3 Git操作要件

```yaml
git_requirements:
  forbidden_commands:
    - "git add -A"
    - "git add ."
    - "git add --all"

  required_patterns:
    staging:
      pattern: "git add <specific-file-path>"

    pre_commit:
      recommended:
        - "git pull --rebase"
        - "git diff --staged"

    commit_message:
      pattern: "git commit -m \"descriptive message\""
```

### 3. セクション要件

#### 3.1 実行手順セクション

```yaml
execution_steps:
  structure:
    - numbered_subsections: true  # ### 1., ### 2., etc.
    - code_blocks: "各ステップに実行可能なコマンド例"

  content:
    - no_placeholders: true
    - executable_commands: true
    - comments_in_code: "推奨"
```

#### 3.2 トラブルシューティングセクション

```yaml
troubleshooting:
  required: true
  min_items: 1
  structure:
    - problem_subsection: "### {問題タイトル}"
    - solution: "対処法の説明"
    - optional_code: "修正コマンド例"
```

#### 3.3 注意事項セクション

```yaml
notes:
  required: true
  min_items: 1
  recommended_items:
    - "ユーザー確認の必要性"
    - "禁止事項（git add -A など）"
    - "確認手順（git diff --staged など）"
```

## 検証方法

### 自動検証

以下の項目は自動的に検証・修正される：

| # | 項目 | 検証方法 | 修正方法 |
|---|------|---------|---------|
| 1 | プレースホルダー | 正規表現マッチ | 動的コマンドに置換 |
| 2 | 変数クォーティング | 正規表現マッチ | ダブルクォート追加 |
| 3 | 危険なgit操作 | 正規表現マッチ | 個別ファイル指定に変更 |
| 4 | 必須セクション | 見出し検索 | テンプレートから追加 |

### 手動検証

以下の項目は警告のみで手動確認が必要：

| # | 項目 | 検証観点 |
|---|------|---------|
| 1 | エラーハンドリング | 適切な条件分岐があるか |
| 2 | コマンドの正確性 | 実際に実行可能か |
| 3 | 説明の明確さ | ユーザーが理解できるか |

## 準拠レベル

```yaml
compliance_levels:
  MUST:
    - 構造要件を満たす
    - プレースホルダーがない
    - 危険なgit操作がない
    - 必須セクションがある

  SHOULD:
    - 変数がクォートされている
    - エラーハンドリングがある
    - 変数がキャッシュされている

  MAY:
    - 追加のセクションがある
    - 詳細なコメントがある
```
