# Data Model: Skill/SubAgent 発動率向上

**Date**: 2025-11-30
**Feature**: 003-skill-subagent-activation

## Entities

### 1. ContextForgeConfig

context-forge の設定を表すエンティティ。`.claude/context-forge.md` ファイルとして永続化される。

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| roles | list[RoleConfig] | ロールごとの設定リスト | 空リスト可 |

### 2. RoleConfig

ロールごとの Skill/SubAgent 設定を表すエンティティ。

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| name | str | ロール名（例: software-engineer） | `^[a-z0-9-]+$`, max 64 chars |
| description | str | ロールの説明 | 非空 |
| activation_rules | list[ActivationRule] | 発動ルールのリスト | 1つ以上必須 |

### 3. ActivationRule

Skill/SubAgent の発動条件を表すエンティティ。

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| type | Literal["skill", "subagent"] | 知見のタイプ | 必須 |
| name | str | Skill/SubAgent の名前 | 非空 |
| trigger_patterns | list[str] | トリガー表現パターン | 3つ以上必須 |
| tool_type | str | 使用するツール（Skill: 自動参照, SubAgent: Task） | 必須 |

### 4. ClaudeMdReference

CLAUDE.md に追加する参照情報を表すエンティティ。

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| start_marker | str | 開始マーカー | `<!-- context-forge settings -->` |
| reference_path | str | 参照ファイルパス | `@.claude/context-forge.md` |
| end_marker | str | 終了マーカー | `<!-- end context-forge settings -->` |

## Relationships

```
CLAUDE.md
    │
    │ @reference
    ▼
ContextForgeConfig (.claude/context-forge.md)
    │
    │ contains 1..*
    ▼
RoleConfig
    │
    │ contains 1..*
    ▼
ActivationRule
    │
    │ references
    ▼
Skill/SubAgent files (.claude/plugins/context-forge.role-{name}/...)
```

## State Transitions

### ContextForgeConfig のライフサイクル

```
[Not Exists] ──init──> [Created] ──add-role-knowledge──> [Updated]
                           │                                  │
                           └──────────delete──────────────────┘
                                        ▼
                                  [Not Exists]
```

### CLAUDE.md Reference のライフサイクル

```
[No Reference] ──init──> [Has Reference]
      ▲                        │
      │                        │
      └────────remove──────────┘
```

## File Format Examples

### .claude/context-forge.md

```markdown
# context-forge 設定

このファイルは context-forge によって自動生成されます。
手動で編集した内容は、`add-role-knowledge` コマンド実行時に上書きされる可能性があります。

## Skill/SubAgent 発動ルール

以下のルールに従って、適切な Skill または SubAgent を使用してください。

### software-engineer ロール

- ユーザーが「PRをレビューして」「プルリクを確認して」「レビューコメントを見て」と言った場合、
  必ず Task ツールで `pr-review-assistant` SubAgent を使用すること

### frontend-engineer ロール

- ユーザーが「Reactのベストプラクティス」「コンポーネントの書き方」「フロントエンドの設計」について質問した場合、
  `react-best-practices` Skill を参照すること
```

### CLAUDE.md への追加内容

```markdown
<!-- context-forge settings -->
@.claude/context-forge.md
<!-- end context-forge settings -->
```

## Validation Rules

1. **ロール名**: 小文字英数字とハイフンのみ、最大64文字
2. **トリガーパターン**: 最低3つ必須（発動率向上のため）
3. **参照パス**: `.claude/` ディレクトリ内のファイルのみ許可
4. **マーカー**: 開始・終了マーカーは必ずペアで存在
