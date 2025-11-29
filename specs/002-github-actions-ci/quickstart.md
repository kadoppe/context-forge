# Quickstart: GitHub Actions CI Setup

## Overview

このドキュメントでは、GitHub Actions CIワークフローのセットアップと使用方法を説明します。

## Prerequisites

- GitHubリポジトリへのアクセス権
- Python 3.11以上がローカルにインストールされていること
- 開発依存パッケージがインストールされていること

## Setup

### 1. ワークフローファイルの配置

`.github/workflows/ci.yml` にワークフローファイルを配置します。

### 2. ローカルでの事前確認

CIと同じチェックをローカルで実行できます：

```bash
# 開発依存パッケージのインストール
uv sync --dev

# リンティング
uv run ruff check .

# 型チェック
uv run mypy src

# テスト
uv run pytest
```

## Usage

### プルリクエスト作成時

1. 新しいブランチを作成
2. 変更をコミット
3. プルリクエストを作成
4. CIが自動的に実行される
5. GitHub PRページでチェック結果を確認

### チェック結果の確認

- **Actions タブ**: 詳細なログを確認
- **PR Checks セクション**: 各ジョブの成功/失敗を確認
- **失敗時**: ログから具体的なエラー内容を確認

## CI Jobs

| ジョブ | 説明 | 実行コマンド |
|--------|------|-------------|
| lint | Ruffによるコードスタイルチェック | `ruff check .` |
| type-check | Mypyによる型チェック | `mypy src` |
| test | Pytestによるテスト実行 | `pytest` |

## Troubleshooting

### よくある問題

1. **依存パッケージのインストール失敗**
   - pyproject.tomlの構文を確認
   - 依存バージョンの互換性を確認

2. **Ruff エラー**
   - `uv run ruff check . --fix` で自動修正可能なエラーを修正
   - pyproject.tomlのruff設定を確認

3. **Mypy エラー**
   - 型アノテーションを追加・修正
   - types-* パッケージが必要な場合はdev依存に追加

4. **テスト失敗**
   - ローカルで `uv run pytest -v` を実行して詳細を確認
   - 環境依存のテストがないか確認

## Branch Protection Setup

CIチェックをマージの必須条件にするには、以下の手順でブランチ保護ルールを設定します：

### 設定手順

1. GitHubリポジトリの **Settings** タブを開く
2. 左メニューから **Branches** を選択
3. **Branch protection rules** セクションで **Add rule** をクリック
4. **Branch name pattern** に `main` を入力
5. 以下のオプションを有効化：
   - ✅ **Require a pull request before merging**
   - ✅ **Require status checks to pass before merging**
6. **Status checks that are required** で以下を選択：
   - `Lint`
   - `Type Check`
   - `Test`
7. **Create** または **Save changes** をクリック

### 確認方法

設定完了後：
- CIが失敗しているPRでは、マージボタンが無効化される
- すべてのCIチェックが成功した場合のみ、マージが可能になる

## Related Files

- `.github/workflows/ci.yml`: CIワークフロー定義
- `pyproject.toml`: プロジェクト設定・依存パッケージ定義
- `specs/002-github-actions-ci/spec.md`: 機能仕様
