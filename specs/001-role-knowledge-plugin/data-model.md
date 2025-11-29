# Data Model: Role Knowledge Plugin Generator

**Feature**: 001-role-knowledge-plugin
**Date**: 2025-11-29

## Entity Relationship Diagram

```
┌─────────────────────┐
│       Role          │
│─────────────────────│
│ name: str           │
│ description: str    │
│ created_at: datetime│
└─────────┬───────────┘
          │ 1
          │
          │ generates
          │
          ▼ 1
┌─────────────────────┐
│    RolePlugin       │
│─────────────────────│
│ name: str           │
│ version: str        │
│ author: str         │
│ path: Path          │
└─────────┬───────────┘
          │ 1
          │
          │ contains
          │
          ▼ *
┌─────────────────────┐
│   KnowledgeItem     │
│─────────────────────│
│ name: str           │
│ description: str    │
│ type: KnowledgeType │
│ content: str        │
└─────────────────────┘
```

## Entities

### Role（職能）

チーム内の専門職能を表すエンティティ。

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | str | Yes | ロール名（例: "frontend-engineer"）|
| description | str | Yes | ロールの説明文 |
| created_at | datetime | Yes | 作成日時 |

**Validation Rules**:
- `name`: 小文字英数字とハイフンのみ、最大64文字
- `description`: 最大1024文字

**State Transitions**: なし（イミュータブル）

---

### KnowledgeItem（知見項目）

各ロールが持つ個別の知見やスキル。

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | str | Yes | 知見の名前（例: "code-review-checklist"）|
| description | str | Yes | 知見の説明（トリガー条件を含む）|
| type | KnowledgeType | Yes | 実装形式（Sub Agent/Command/Skill/Hook）|
| content | str | Yes | 知見の本文内容 |

**Validation Rules**:
- `name`: 小文字英数字とハイフンのみ、最大64文字
- `description`: 最大1024文字（Skillの場合はトリガー条件必須）
- `type`: Enum値のいずれか

---

### KnowledgeType（知見タイプ）

知見の実装形式を表すEnum。

```python
class KnowledgeType(Enum):
    SKILL = "skill"           # 参照情報、チェックリスト
    COMMAND = "command"       # ワークフロー自動化
    SUB_AGENT = "sub_agent"   # 自律的タスク遂行
    HOOK = "hook"             # イベントトリガー処理
```

**Type Selection**: LLMが知見の内容を分析し、最適なタイプを判定。ユーザーが最終確認。

---

### RolePlugin（ロールプラグイン）

生成されるClaude Codeプラグインの構成。

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | str | Yes | プラグイン名（ロール名と同一）|
| version | str | Yes | セマンティックバージョン（例: "1.0.0"）|
| author | str | Yes | 作成者名 |
| path | Path | Yes | プラグインディレクトリのパス |

**Generated Structure**:
```
.claude/plugins/{role-name}/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── {knowledge-item}.md
├── agents/
│   └── {knowledge-item}.md
├── skills/
│   └── {knowledge-item}/
│       └── SKILL.md
└── hooks/
    └── hooks.json
```

---

### PluginMetadata（プラグインメタデータ）

plugin.json の内容を表す。

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | str | Yes | プラグイン識別子 |
| description | str | Yes | プラグインの説明 |
| version | str | Yes | バージョン番号 |
| author | AuthorInfo | Yes | 作成者情報 |

**Example**:
```json
{
  "name": "frontend-engineer",
  "description": "フロントエンドエンジニアの知見とベストプラクティス",
  "version": "1.0.0",
  "author": {
    "name": "Team Lead"
  }
}
```

---

### DocumentCache（ドキュメントキャッシュ）

公式ドキュメントのキャッシュ情報。

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| url | str | Yes | ドキュメントURL |
| content | str | Yes | キャッシュされた内容 |
| fetched_at | datetime | Yes | 取得日時 |

**Cache Location**: `~/.cache/context-forge/docs/`

---

## File Formats

### Command File (.md)

```markdown
---
name: {knowledge-name}
description: {description}
arguments:
  - name: input
    description: User input for the command
    required: false
---

{content}
```

### Agent File (.md)

```markdown
---
name: {knowledge-name}
description: {description}
tools: Read, Write, Grep, Glob
model: sonnet
---

{content}
```

### Skill File (SKILL.md)

```markdown
---
name: {knowledge-name}
description: {description}. Use when {trigger condition}.
---

{content}
```

### Hook Configuration (hooks.json)

```json
{
  "hooks": {
    "{event-type}": [
      {
        "matcher": "{tool-name}",
        "hooks": [
          {
            "type": "command",
            "command": "{script-path}"
          }
        ]
      }
    ]
  }
}
```

---

## Relationships

| From | To | Cardinality | Description |
|------|-----|-------------|-------------|
| Role | RolePlugin | 1:1 | 1つのロールは1つのプラグインを生成 |
| RolePlugin | KnowledgeItem | 1:N | 1つのプラグインは複数の知見を含む |

---

## Indexes / Lookups

| Entity | Lookup Key | Use Case |
|--------|-----------|----------|
| Role | name | 既存ロールの検索・更新 |
| RolePlugin | path | プラグイン存在確認 |
| DocumentCache | url | キャッシュヒット判定 |
