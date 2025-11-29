# Research: Role Knowledge Plugin Generator

**Feature**: 001-role-knowledge-plugin
**Date**: 2025-11-29

## Research Summary

### 1. Claude Code Plugin Structure

**Decision**: Claude Codeプラグインは `.claude-plugin/plugin.json` をルートに持つディレクトリ構造を採用

**Rationale**: 公式ドキュメントに準拠し、Claude Codeが自動認識できる標準形式

**Directory Structure**:
```
role-plugin/
├── .claude-plugin/
│   └── plugin.json              # プラグインメタデータ (必須)
├── commands/                     # カスタムスラッシュコマンド
│   └── *.md
├── agents/                       # カスタムエージェント
│   └── *.md
├── skills/                       # エージェントスキル
│   └── skill-name/
│       └── SKILL.md
└── hooks/                        # イベントハンドラ
    └── hooks.json
```

**Alternatives Considered**:
- 単一ファイル形式 → 機能が限定的、拡張性低い
- 独自形式 → Claude Codeとの互換性がない

---

### 2. Command File Format

**Decision**: Markdown + YAML frontmatterでコマンドを定義

**Rationale**:
- spec-kitコマンドと同じ形式を採用し一貫性を保つ
- Claude Codeネイティブ形式
- 人間が読みやすく編集しやすい

**Format**:
```markdown
---
name: add-role-knowledge
description: 職能ごとの知見をプラグインとして追加・更新する
---

[コマンドの本文（プロンプト）]
```

**Reference**: `.claude/commands/speckit.specify.md` の実装パターン

---

### 3. context-forge CLI Integration

**Decision**: 既存の `init` コマンドで全コマンドテンプレートを自動インストール

**Rationale**:
- 既存のCLI構造（Typer + Rich）を活用
- `load_template()` と `InstallTarget` パターンを再利用
- ユーザー体験の一貫性を維持
- `init` コマンド1つで初期化とインストールを完結

**Implementation Approach**:
```python
# init コマンドで全テンプレートをインストール
@app.command()
def init(
    force: bool = ...,  # 既存ファイル上書き
)
```

**Alternatives Considered**:
- 別個の `install` コマンド → コマンドが増えて複雑化
- 別個のCLIツール作成 → 複雑化、ユーザー体験が分断
- Bashスクリプト → 型安全性なし、エラーハンドリング困難

---

### 4. Knowledge Type Detection Logic

**Decision**: LLM判定によるタイプ推論

**Rationale**:
- Claude自身が知見の内容を分析し、最適なタイプを判定
- コンテキストを理解した柔軟な判定が可能
- 最終的にはユーザー確認で精度保証

**Type Guidelines** (LLM判定の参考):

| Knowledge Pattern | Recommended Type | Example |
|-------------------|-----------------|---------|
| 参照情報、ガイドライン、チェックリスト | Skill | コードレビューチェックリスト |
| ワークフロー自動化、ファイル生成 | Command | 設計ドキュメント作成 |
| 自律的なタスク遂行、分析、レビュー | Sub Agent | アーキテクチャレビュー |
| イベントトリガー、検証、ガード処理 | Hook | コミット前セキュリティチェック |

**Fallback**: 判別に自信がない場合はユーザーに選択を促す

---

### 5. Official Documentation Fetching

**Decision**: WebFetch + キャッシュによる公式ドキュメント参照

**Rationale**:
- 仕様変更に追従するため毎回最新を取得
- ネットワーク障害時はキャッシュで継続可能
- Clarificationsで決定済み: 警告表示して前回キャッシュで続行

**URLs to Fetch**:
- https://code.claude.com/docs/en/plugins
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/hooks-guide

**Cache Strategy**:
- キャッシュ場所: `~/.cache/context-forge/docs/`
- キャッシュ有効期限: なし（毎回フェッチ試行、失敗時のみ使用）
- キャッシュ形式: Markdown

---

### 6. Plugin Installation Location

**Decision**: プロジェクトディレクトリの `.claude/plugins/` に生成

**Rationale**:
- Clarificationsで決定済み
- Git経由でチーム共有可能
- プロジェクト固有のロール知見を管理

**Path Structure**:
```
project-root/
└── .claude/
    └── plugins/
        └── {role-name}/
            ├── .claude-plugin/
            │   └── plugin.json
            ├── commands/
            ├── agents/
            ├── skills/
            └── hooks/
```

---

### 7. Existing Pattern Reference: spec-kit Commands

**Key Patterns from spec-kit**:

1. **YAML Frontmatter**: `description`, `handoffs` フィールド
2. **$ARGUMENTS 参照**: ユーザー入力を本文で参照
3. **段階的フロー**: 明確なステップを定義
4. **バリデーション**: チェックリスト生成と検証
5. **外部スクリプト呼び出し**: `.specify/scripts/bash/` 配下のスクリプト実行

**Applicable Patterns for add-role-knowledge**:
- 対話的な情報収集フロー
- 段階的なプラグイン生成
- 生成後の検証ステップ

---

## Technical Decisions Summary

| Decision Area | Choice | Confidence |
|---------------|--------|------------|
| Plugin Structure | Claude Code標準形式 | High |
| Command Format | Markdown + YAML | High |
| CLI Integration | Typer拡張 | High |
| Type Detection | LLM判定 | High |
| Doc Fetching | WebFetch + Cache | High |
| Install Location | `.claude/plugins/` | High (Clarified) |

## Open Questions Resolved

- [x] プラグイン保存場所 → `.claude/plugins/`
- [x] CLIコマンド名 → `context-forge init`（全コマンドを自動インストール）
- [x] スラッシュコマンド名 → `/context-forge.add-role-knowledge`
- [x] 対応OS → macOS + Linux
- [x] ドキュメント取得失敗時 → 警告表示して前回キャッシュで続行

## Next Steps

1. data-model.md でエンティティ定義
2. contracts/ でCLIコマンドインターフェース定義
3. quickstart.md で開発者向けクイックスタート作成
