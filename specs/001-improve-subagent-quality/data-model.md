# Data Model: SubAgent品質向上のためのプロンプト改善

**Date**: 2025-11-30
**Feature**: 001-improve-subagent-quality

## 概要

この機能はMarkdownプロンプトの改善であり、データベースやAPIは使用しない。
以下は、プロンプト内で使用される概念エンティティの定義である。

## エンティティ定義

### 1. SubAgentテンプレート

SubAgent生成時に使用されるベーステンプレート。

```yaml
SubAgentTemplate:
  structure:
    frontmatter:
      - name: string (required, kebab-case)
      - description: string (required, 1-2文)
      - tools: string (comma-separated, default: "Bash, Read, Write, Edit, Grep, Glob")
      - model: string (default: "sonnet")

    body:
      required_sections:
        - title: "# {Agent Name}"
        - overview: 概要説明
        - execution_steps: "## 実行手順" (numbered subsections)
        - troubleshooting: "## トラブルシューティング"
        - notes: "## 注意事項"

      optional_sections:
        - prerequisites: "## 前提条件"
        - configuration: "## 設定"
```

### 2. 品質チェックリスト

SubAgent生成時に自動適用される品質基準。

```yaml
QualityChecklist:
  checks:
    - id: "QC-001"
      name: "placeholder_detection"
      description: "プレースホルダー構文の検出"
      pattern: "<[^>]+>|\\{[^}]+\\}"
      auto_fix: true
      severity: "error"

    - id: "QC-002"
      name: "variable_quoting"
      description: "変数のクォーティング確認"
      pattern: "\\$[A-Z_]+[^\"']"
      auto_fix: true
      severity: "warning"

    - id: "QC-003"
      name: "dangerous_git_add"
      description: "危険なgit addの検出"
      pattern: "git add (-A|\\.|--all)"
      auto_fix: true
      severity: "error"

    - id: "QC-004"
      name: "troubleshooting_section"
      description: "トラブルシューティングセクションの存在"
      pattern: "## トラブルシューティング"
      auto_fix: true
      severity: "warning"

    - id: "QC-005"
      name: "notes_section"
      description: "注意事項セクションの存在"
      pattern: "## 注意事項"
      auto_fix: true
      severity: "warning"

    - id: "QC-006"
      name: "error_handling"
      description: "bashエラーハンドリングの確認"
      pattern: "if \\[|\\|\\||&&"
      auto_fix: false
      severity: "info"
```

### 3. ベストプラクティス集

よくあるパターンの推奨実装例。

```yaml
BestPractices:
  categories:
    - name: "bash_commands"
      patterns:
        - name: "variable_caching"
          description: "変数キャッシュパターン"
          good_example: |
            REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
            gh api "repos/${REPO}/pulls"
          bad_example: |
            gh api repos/$(gh repo view ...)/pulls

        - name: "error_handling"
          description: "エラーハンドリングパターン"
          good_example: |
            if [ -n "$VAR" ]; then
              command "$VAR"
            fi
          bad_example: |
            command $VAR

    - name: "git_operations"
      patterns:
        - name: "safe_staging"
          description: "安全なステージングパターン"
          good_example: "git add path/to/file.md"
          bad_example: "git add -A"

        - name: "pre_commit_check"
          description: "コミット前確認パターン"
          good_example: |
            git pull --rebase
            git diff --staged
            git add specific/file.md
            git commit -m "message"
          bad_example: |
            git add -A
            git commit -m "message"
            git push
```

## 状態遷移

### SubAgent生成フロー

```
[ユーザー入力]
    ↓
[タイプ判定] → Skill / Command / Hook (SubAgent以外)
    ↓ (SubAgent選択)
[テンプレート適用]
    ↓
[品質チェック実行]
    ↓ (問題あり)          ↓ (問題なし)
[自動修正]              [ファイル生成]
    ↓                       ↓
[修正不可] → [警告表示] → [ファイル生成]
```

## 関連性

```
add-role-knowledge.md (コマンド)
    ├── 使用 → SubAgentTemplate
    ├── 適用 → QualityChecklist
    └── 参照 → BestPractices

生成されるSubAgent (agents/*.md)
    └── 準拠 → SubAgentTemplate.structure
```
