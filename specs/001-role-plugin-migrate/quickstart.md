# Quickstart: Role Plugin Migration Command

**Date**: 2025-11-30
**Feature**: 001-role-plugin-migrate

## 概要

この機能は以下の2つのコンポーネントで構成されます：

1. **`/context-forge.migrate`** - Claude Code slash command（LLM が実行）
2. **`context-forge init`** - CLI コマンドの拡張（ファイルコピー）

## 使用方法

### 1. init コマンドでコマンドファイルをインストール

```bash
# 新規プロジェクトの初期化（全コマンドをインストール）
context-forge init

# 既存プロジェクトでコマンドを更新（上書き）
context-forge init --force
```

これにより `.claude/commands/` に以下のファイルが配置されます：
- `context-forge.add-role-knowledge.md`
- `context-forge.migrate.md`

### 2. migrate コマンドでプラグインを更新

Claude Code 内で以下を実行：

```
/context-forge.migrate
```

または、特定のプラグインのみを更新：

```
/context-forge.migrate software-engineer
```

### 3. マイグレーション結果の確認

Claude が以下のレポートを表示します：

```
## マイグレーション完了

### 更新されたプラグイン
- context-forge.role-software-engineer (1.0.0 → 0.1.0)

### スキップされたプラグイン
- context-forge.role-frontend-engineer（既に最新）

### バックアップ
- .claude/plugins/.backup/20251130_123456_software-engineer/
```

## ディレクトリ構造

```
.claude/
├── commands/
│   ├── context-forge.add-role-knowledge.md
│   └── context-forge.migrate.md          # 新規追加
├── plugins/
│   ├── context-forge.role-{name}/        # マイグレーション対象
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json               # version フィールドで判定
│   │   ├── agents/
│   │   ├── skills/
│   │   ├── commands/
│   │   └── hooks/
│   └── .backup/                          # バックアップ保存先
│       └── {timestamp}_{plugin-name}/
└── context-forge.md
```

## マイグレーション内容

Claude は以下の更新を行います：

1. **plugin.json**: version を context-forge の最新バージョンに更新
2. **agents/*.md**: description にトリガー表現を追加（3つ以上）
3. **skills/*/SKILL.md**: description にトリガー表現を追加（3つ以上）
4. **commands/*.md**: frontmatter 形式の確認・修正
5. **hooks/hooks.json**: 構造の検証

## エラー時の復元

マイグレーション中にエラーが発生した場合：

1. Claude がエラーメッセージとバックアップパスを表示
2. バックアップからファイルを手動でコピーして復元

```bash
# 復元例
cp -r .claude/plugins/.backup/20251130_123456_software-engineer/* \
      .claude/plugins/context-forge.role-software-engineer/
```

## 開発者向け情報

### テンプレートファイルの場所

```
src/context_forge_cli/templates/commands/
├── add-role-knowledge.md
└── migrate.md              # 新規追加
```

### テスト実行

```bash
uv run pytest tests/
```
