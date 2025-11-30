# CLI Interface Contract: Skill/SubAgent 発動率向上

**Date**: 2025-11-30
**Feature**: 003-skill-subagent-activation

## Overview

この機能は API を提供しないため、CLI コマンドのインターフェース契約を定義する。

## Commands

### context-forge init

既存コマンドに以下の機能を追加:

#### 新規動作

1. `.claude/context-forge.md` が存在しない場合、テンプレートから作成
2. `CLAUDE.md` に `@.claude/context-forge.md` 参照を追加（存在しない場合）
3. 既存の context-forge 関連設定が CLAUDE.md にある場合、移行を提案

#### Input

```
context-forge init [--force] [--skip-install]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| --force | bool | false | 既存ファイルを上書き |
| --skip-install | bool | false | コマンドのインストールをスキップ |

#### Output

```
Success! Initialized context-forge project.
Created directories:
  - .claude
  - .claude/commands

Created files:
  - .claude/context-forge.md

Updated files:
  - CLAUDE.md (added @.claude/context-forge.md reference)

Installing commands...
Installed 'add-role-knowledge'
```

#### Error Cases

| Condition | Exit Code | Message |
|-----------|-----------|---------|
| Permission denied | 2 | Cannot write file: {path} |
| CLAUDE.md parse error | 1 | Failed to parse CLAUDE.md |

### /context-forge.add-role-knowledge (Slash Command)

Claude Code のスラッシュコマンドとして実行される。

#### 更新内容

Phase 7（完了とプラグイン有効化）に以下を追加:

1. `.claude/context-forge.md` に発動ルールを追記
2. 発動ルールには 3 つ以上のトリガー表現パターンを含める

#### 生成される発動ルール形式

```markdown
### {role-name} ロール

- ユーザーが「{pattern1}」「{pattern2}」「{pattern3}」と言った場合、
  必ず {tool_type} ツールで `{knowledge-name}` {type} を使用すること
```

## File Contracts

### .claude/context-forge.md

```yaml
# Template structure
type: markdown
required_sections:
  - "# context-forge 設定"
  - "## Skill/SubAgent 発動ルール"
optional_sections:
  - "### {role-name} ロール"  # 動的生成
encoding: utf-8
```

### CLAUDE.md Reference Block

```yaml
# Inserted content
start_marker: "<!-- context-forge settings -->"
content: "@.claude/context-forge.md"
end_marker: "<!-- end context-forge settings -->"
location: end_of_file  # または既存の context-forge セクションの位置
```

## Migration Contract

### 検出パターン

CLAUDE.md 内の以下のパターンを検出:

1. `context-forge` を含むコメントブロック
2. `@.claude/plugins/context-forge.role-` を含む行
3. `Skill/SubAgent 発動` を含むセクション

### 移行フロー

```
1. CLAUDE.md をスキャン
2. 検出されたコンテンツを抽出
3. 確認メッセージを表示:
   "既存の context-forge 設定を .claude/context-forge.md に移行しますか？ (y/N)"
4. 承認された場合:
   a. .claude/context-forge.md に追記
   b. CLAUDE.md から該当セクションを削除
   c. @ 参照を追加
5. 拒否された場合:
   a. 警告を表示して続行
```
