# Research: Skill/SubAgent 発動率向上

**Date**: 2025-11-30
**Feature**: 003-skill-subagent-activation

## Research Topics

### 1. Claude Code の @ 記法によるファイル参照

**Decision**: `@path/to/file` 形式で CLAUDE.md から他ファイルを参照

**Rationale**:
- Claude Code 公式ドキュメント（https://code.claude.com/docs/en/memory）で確認済み
- 相対パス・絶対パス・ホームディレクトリパス（`@~/.claude/...`）すべてサポート
- マークダウンのコードブロック内では機能しない（処理されない）
- 再帰的インポート対応（最大5階層まで）
- `/memory` コマンドで読み込まれたファイルを確認可能

**Alternatives considered**:
- `Contents of` 形式 → 非公式、動作保証なし
- 単純な説明テキスト → 読み込みを保証しない
- 両方を併用 → 冗長、@ 記法のみで十分

### 2. Skill/SubAgent の発動率向上手法

**Decision**: CLAUDE.md に明示的なルール形式で発動条件を記述

**Rationale**:
- 参考記事（https://zenn.dev/oligin/articles/7691926a83936a）の検証結果
  - CLAUDE.md なしの発動率: 約 25%
  - CLAUDE.md に発動条件を明記: 100%
- 「ユーザーが〇〇と言った場合、必ず Task ツールで△△を使用すること」形式が効果的
- description に複数のトリガー表現パターンを含めることも有効

**Alternatives considered**:
- description のみで改善 → 効果限定的（25%程度）
- 一覧表形式 → ルール形式ほど明確でない
- Hook で強制発動 → 過剰発動のリスク、柔軟性低下

### 3. context-forge.md のファイル構造

**Decision**: 以下の構造を採用

```markdown
# context-forge 設定

## Skill/SubAgent 発動ルール

以下のルールに従って、適切な Skill または SubAgent を使用してください。

### software-engineer ロール

- ユーザーが「PRをレビューして」「プルリクを確認」「レビューコメント」と言った場合、
  必ず Task ツールで `pr-review-assistant` SubAgent を使用すること

### [other-role] ロール

- [発動条件] の場合、必ず [タイプ] ツールで `[name]` を使用すること
```

**Rationale**:
- ロールごとに整理することで管理しやすい
- 発動条件を明示的に列挙することで Claude Code が認識しやすい
- 既存の Skill/SubAgent 一覧としても機能

**Alternatives considered**:
- フラットなリスト → ロールが増えると管理困難
- YAML 形式 → Claude Code は Markdown の方が認識しやすい

### 4. CLAUDE.md への追加内容

**Decision**: 最小限の参照のみ追加（10行以下）

```markdown
<!-- context-forge settings -->
@.claude/context-forge.md
<!-- end context-forge settings -->
```

**Rationale**:
- コメントでマーカーを付けることで、更新・削除が容易
- 既存の CLAUDE.md 内容を汚染しない
- 参照のみなので CLAUDE.md の可読性を維持

**Alternatives considered**:
- マーカーなし → 更新時に既存内容との区別が困難
- 説明文追加 → 冗長、@ 参照だけで十分

### 5. 既存設定の移行処理

**Decision**: `context-forge init` 時に自動検出・移行

**Rationale**:
- ユーザーが明示的に init を実行したタイミングで移行
- 確認メッセージを表示してユーザーに認識させる
- 移行前のバックアップは作成しない（git で管理されている前提）

**Implementation approach**:
1. CLAUDE.md を読み込み
2. `<!-- context-forge` マーカーまたは context-forge 関連コンテンツを検索
3. 見つかった場合、確認メッセージを表示
4. ユーザーが承認したら `.claude/context-forge.md` に移動
5. CLAUDE.md を @ 参照形式に置換

**Alternatives considered**:
- 別コマンド `migrate` を用意 → ユーザーの手間が増える
- add-role-knowledge 時に移行 → 予期しないタイミングで変更される

## Summary

| トピック | 決定事項 |
|---------|---------|
| ファイル参照方式 | `@.claude/context-forge.md` 形式 |
| 発動率向上手法 | 明示的ルール形式を CLAUDE.md（経由で専用ファイル）に記述 |
| 専用ファイル構造 | ロールごとにセクション分け、ルール形式で発動条件記述 |
| CLAUDE.md への追加 | マーカー付きの @ 参照のみ（10行以下） |
| 既存設定の移行 | init 時に自動検出・確認メッセージ付きで移行 |

すべての NEEDS CLARIFICATION が解決されました。Phase 1 に進む準備が整いました。
