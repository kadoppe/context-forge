# Research: GitHub Actions CI Setup

**Date**: 2025-11-29
**Feature**: 002-github-actions-ci

## Research Topics

### 1. GitHub Actions Workflow Best Practices for Python

**Decision**: 標準的なGitHub Actionsワークフロー構造を採用

**Rationale**:
- `actions/checkout@v4` でリポジトリをチェックアウト
- `actions/setup-python@v5` でPython環境をセットアップ
- マトリックス戦略でPython 3.11と3.12を並列テスト
- `pip install -e ".[dev]"` で開発依存パッケージをインストール

**Alternatives Considered**:
- Poetry/PDM: pyproject.tomlがhatchを使用しているため不採用
- Docker: オーバーヘッドが大きく、シンプルなCIには不要
- tox: 追加の複雑さなしにマトリックス戦略で同等の機能を実現可能

### 2. 並列ジョブ実行戦略

**Decision**: 3つの独立したジョブ（lint, type-check, test）を定義し、すべて並列実行

**Rationale**:
- 仕様で「並列実行・全完了待機」が決定済み
- GitHub Actionsのデフォルト動作（`fail-fast: false`設定）と合致
- 各ジョブが独立しているため、1つの失敗が他に影響しない
- 全エラーを一度に確認でき、修正効率が向上

**Alternatives Considered**:
- 単一ジョブ内での逐次実行: 失敗時に後続チェックがスキップされる
- 依存関係付きジョブ: lintが成功しないとtestを実行しない方式は、エラー発見が遅れる

### 3. Pythonバージョン

**Decision**: Python 3.11のみでテスト実行

**Rationale**:
- pyproject.tomlで `requires-python = ">=3.11"` と宣言
- シンプルな構成を優先し、まずは3.11のみで開始
- 将来的に3.12を追加することは容易

**Alternatives Considered**:
- 3.11と3.12のマトリックス: 将来的に追加可能だが、初期段階では不要
- 3.12のみ: 3.11ユーザーへの互換性確認ができない

### 4. 依存パッケージのキャッシュ

**Decision**: `actions/setup-python@v5` の組み込みキャッシュ機能を使用

**Rationale**:
- `cache: 'pip'` オプションで自動的にpipキャッシュを有効化
- 設定がシンプルで保守が容易
- ビルド時間の短縮に貢献

**Alternatives Considered**:
- `actions/cache` の手動設定: より細かい制御が可能だが複雑
- キャッシュなし: ビルド時間が長くなる

### 5. ワークフロートリガー

**Decision**: `pull_request` と `push` (mainブランチのみ) でトリガー

**Rationale**:
- PRでのチェックにより、マージ前に問題を検出
- main直接プッシュ時もチェックを実行し、品質を維持
- 無駄な実行を避けるため、mainブランチへのpushのみをトリガー

**Alternatives Considered**:
- すべてのブランチへのpush: 不要な実行が増加
- PRのみ: main直接プッシュ時にチェックが実行されない

### 6. タイムアウト設定

**Decision**: ジョブレベルで10分のタイムアウトを設定

**Rationale**:
- 仕様で「10分以内で完了」が成功基準
- 無限ループやハングアップからの保護
- リソースの効率的な使用

**Alternatives Considered**:
- デフォルト（6時間）: 問題発生時の検出が遅れる
- ステップごとのタイムアウト: 管理が複雑

## Summary

GitHub Actions CIのセットアップにおいて、すべての技術的決定が明確になった。標準的なベストプラクティスに従い、シンプルで保守しやすいワークフローを実装する。
