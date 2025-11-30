# Quickstart: Skill/SubAgent 発動率向上

**Date**: 2025-11-30
**Feature**: 003-skill-subagent-activation

## 概要

この機能により、context-forge で追加した Skill/SubAgent が Claude Code で確実に発動するようになります。

## 前提条件

- context-forge CLI がインストール済み
- Claude Code が使用可能
- プロジェクトが git 管理されている（推奨）

## セットアップ手順

### 1. プロジェクトの初期化（新規または更新）

```bash
context-forge init
```

以下のファイルが作成/更新されます:
- `.claude/context-forge.md` - 発動ルールの設定ファイル
- `CLAUDE.md` に `@.claude/context-forge.md` 参照が追加

### 2. ロール知見の追加

Claude Code 内で:

```
/context-forge.add-role-knowledge
```

対話形式で以下を設定:
1. ロール名（例: software-engineer）
2. 知見の内容
3. 知見タイプ（Skill / SubAgent / Command / Hook）

追加完了時、`.claude/context-forge.md` に発動ルールが自動追記されます。

### 3. 発動確認

Claude Code を再起動し、関連するタスクを依頼:

```
PRをレビューして
```

対応する SubAgent が自動的に呼び出されれば成功です。

## 既存ユーザー向け移行

既に CLAUDE.md に context-forge の設定がある場合:

```bash
context-forge init
```

実行時に移行の確認メッセージが表示されます。「y」を選択すると、設定が `.claude/context-forge.md` に移動します。

## ファイル構造

```
.claude/
├── context-forge.md          # 発動ルール設定（新規）
├── commands/
│   └── context-forge.add-role-knowledge.md
├── plugins/
│   └── context-forge.role-{role-name}/
│       ├── agents/
│       └── skills/
└── settings.json

CLAUDE.md                      # @.claude/context-forge.md 参照のみ
```

## 発動ルールのカスタマイズ

`.claude/context-forge.md` を直接編集することで、発動条件をカスタマイズできます:

```markdown
### software-engineer ロール

- ユーザーが「PRをレビューして」「プルリクを確認」「コードレビュー」「差分を見て」と言った場合、
  必ず Task ツールで `pr-review-assistant` SubAgent を使用すること
```

**ポイント**:
- トリガー表現パターンは 3 つ以上含める
- 「必ず〇〇ツールで△△を使用すること」形式で記述
- 曖昧な表現より具体的なフレーズを使用

## トラブルシューティング

### 発動しない場合

1. Claude Code を再起動
2. `/memory` コマンドで `.claude/context-forge.md` が読み込まれているか確認
3. 発動ルールの記述形式を確認（「必ず...使用すること」形式）

### 参照エラーの場合

1. `.claude/context-forge.md` ファイルが存在するか確認
2. CLAUDE.md の `@.claude/context-forge.md` 参照がコードブロック外にあるか確認
3. ファイルパスの typo を確認

## 次のステップ

- 複数のロールに知見を追加
- 発動率をモニタリングし、トリガー表現を調整
- チームで知見を共有（`.claude/` ディレクトリを git 管理）
