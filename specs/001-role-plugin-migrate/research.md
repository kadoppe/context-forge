# Research: Role Plugin Migration Command

**Date**: 2025-11-30
**Feature**: 001-role-plugin-migrate

## Research Topics

### 1. Claude Code Slash Command 構造

**決定**: Markdown ファイルベースの slash command として実装

**根拠**:
- 既存の `add-role-knowledge.md` と同じパターンを踏襲
- YAML frontmatter で description を定義
- コマンド本体は Markdown で LLM への指示を記述
- Claude Code が自動的にコマンドを認識・実行

**検討した代替案**:
- Python スクリプトによる直接実装 → Claude Code の slash command 仕組みに合わない
- JSON 形式のコマンド定義 → Markdown の方が LLM 指示に適している

### 2. プラグインバージョン判定方式

**決定**: plugin.json の version フィールドで判定

**根拠**:
- plugin.json は Claude Code プラグインの標準的なメタデータファイル
- セマンティックバージョニングで将来の互換性管理が容易
- 既存プラグインは version "1.0.0" を使用している（context-forge 生成時のデフォルト）
- 最新バージョン "0.0.1" より古いものが更新対象

**検討した代替案**:
- ファイル構造の有無で判定 → バージョン間の差分が不明確
- ファイル内容のパターンマッチ → 脆弱で誤検出のリスク

### 3. バックアップ戦略

**決定**: `.claude/plugins/.backup/{timestamp}_{plugin-name}/` 形式

**根拠**:
- タイムスタンプにより複数回のマイグレーションでも衝突しない
- プラグイン単位でバックアップすることで復元が容易
- .backup ディレクトリは .gitignore に追加推奨

**検討した代替案**:
- Git stash 使用 → Git リポジトリ前提が必要、非 Git 環境で使えない
- ファイル名に .bak 追加 → 複数バージョンの管理が困難

### 4. マイグレーション対象コンポーネント

**決定**: 全コンポーネント（plugin.json, agents/, skills/, commands/, hooks/）を対象

**根拠**:
- 一貫性のある最新状態を保証
- 部分的な更新は不整合のリスク
- Claude が各コンポーネントの最新仕様を理解して変換

**マイグレーション内容**:
1. **plugin.json**: version を "0.0.1" に更新
2. **agents/*.md**: description に 3つ以上のトリガー表現を追加（未設定の場合）
3. **skills/*/SKILL.md**: description に 3つ以上のトリガー表現を追加（未設定の場合）
4. **commands/*.md**: frontmatter 形式の確認・修正
5. **hooks/hooks.json**: 構造の検証（変更は通常不要）

### 5. init コマンドのコマンドファイル配置

**決定**: context-forge.* の全コマンドを配置（既存ファイルは上書き）

**根拠**:
- 新規ユーザーは全機能を利用可能にしたい
- 既存ユーザーはコマンドの更新を受け取りたい
- 上書きにより常に最新版が配置される

**配置されるコマンド**:
1. `context-forge.add-role-knowledge.md` - ロール知見プラグイン生成
2. `context-forge.migrate.md` - プラグインマイグレーション（新規）

### 6. エラーハンドリングと復元

**決定**: バックアップからの手動復元をガイド

**根拠**:
- LLM 実行のため自動復元は複雑
- バックアップパスを明示することでユーザーが復元可能
- エラー発生時は変更を中断し、部分的な更新を防ぐ

## 技術的決定事項

| 項目 | 決定 | 理由 |
|------|------|------|
| コマンド形式 | Markdown slash command | 既存パターン踏襲 |
| バージョン管理 | plugin.json version フィールド | 標準的・明確 |
| バックアップ | タイムスタンプ付きディレクトリ | 衝突回避・復元容易 |
| 対象範囲 | 全コンポーネント | 一貫性保証 |
| init 動作 | 全コマンド上書きインストール | 最新版保証 |

## 未解決事項

なし - すべての NEEDS CLARIFICATION は /speckit.clarify で解決済み
