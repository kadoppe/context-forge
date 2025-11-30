# Research: SubAgent品質向上のためのプロンプト改善

**Date**: 2025-11-30
**Feature**: 001-improve-subagent-quality

## 1. PRレビューで受けた指摘パターンの分析

### Decision
実際に受けた指摘を分類し、汎用的な品質ガイドラインとして整理する。

### Rationale
今回のPR（#6）で受けた指摘は、SubAgent生成全般に適用可能な汎用的な問題点を示している。これらをカテゴリ化することで、再発防止のためのチェックリストを作成できる。

### 指摘カテゴリ

| カテゴリ | 具体的な指摘 | 汎用的な問題 |
|----------|-------------|--------------|
| プレースホルダー | `<run-id>`, `{owner}/{repo}` が残っている | 実行不可能なコマンド例 |
| 変数管理 | API呼び出しが重複、変数キャッシュなし | 非効率・保守性の問題 |
| Git安全性 | `git add -A` が危険 | 意図しない変更のコミット |
| エラーハンドリング | bash失敗時の対処なし | 実行時エラーの放置 |
| セクション不足 | トラブルシューティングがない | ユーザーサポートの欠如 |

### Alternatives Considered
- 指摘ごとに個別対応 → 場当たり的で再発する
- 完全なリンターの実装 → 過剰なエンジニアリング

---

## 2. SubAgentテンプレートのベストプラクティス

### Decision
SubAgentテンプレートに以下のセクションと品質ガイドラインを組み込む。

### Rationale
テンプレート段階で品質を担保することで、生成されるSubAgentの一貫した品質を保証できる。

### 必須セクション構造

```markdown
# {Agent Name}

{概要説明}

## 実行手順

### 1. {ステップ1}
{説明}
{実行可能なコマンド例 - プレースホルダー禁止}

### 2. {ステップ2}
...

## トラブルシューティング

### {問題1}
{対処法}

## 注意事項

- {安全性に関する注意}
- {禁止事項}
```

### Alternatives Considered
- 自由形式のテンプレート → 品質のばらつきが大きい
- より複雑な構造 → 学習コストが高い

---

## 3. Bashコマンドのベストプラクティス

### Decision
SubAgent内のbashコマンドには以下のパターンを適用する。

### Rationale
実際のPRレビューで指摘されたbash関連の問題を防ぐ。

### パターン集

#### 変数キャッシュ
```bash
# 良い例: 変数をキャッシュして再利用
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
PR_NUMBER=$(gh pr view --json number -q '.number')
gh api "repos/${REPO}/pulls/${PR_NUMBER}/reviews"

# 悪い例: 毎回コマンドを実行
gh api repos/$(gh repo view ...)/pulls/$(gh pr view ...)/reviews
```

#### エラーハンドリング
```bash
# 良い例: エラー時の処理を含む
RUN_ID=$(gh run list --limit 1 --json databaseId,conclusion --jq '.[] | select(.conclusion == "failure") | .databaseId')
if [ -n "$RUN_ID" ]; then
  gh run view "$RUN_ID" --log-failed
fi

# 悪い例: エラー時の考慮なし
gh run view <run-id> --log-failed
```

#### クォーティング
```bash
# 良い例: 変数を適切にクォート
git add "$FILE_PATH"
gh api "repos/${REPO}/pulls/${PR_NUMBER}"

# 悪い例: クォートなし（スペース含むパスで失敗）
git add $FILE_PATH
```

### Alternatives Considered
- ShellCheckの実行を必須化 → プロンプト内では実行不可
- bashコマンドを禁止 → 実用性が大幅に低下

---

## 4. Git操作の安全パターン

### Decision
SubAgent内のgit操作には以下の安全パターンを必須とする。

### Rationale
`git add -A` のような危険なコマンドによる意図しない変更のコミットを防ぐ。

### パターン集

#### ファイルのステージング
```bash
# 良い例: 個別ファイル指定
git add path/to/file1.md path/to/file2.md

# 禁止: 全ファイルステージング
git add -A  # 危険
git add .   # 危険
```

#### コミット前の確認
```bash
# 必須: 変更内容の確認
git diff --staged

# 推奨: リモートとの同期
git pull --rebase
```

#### プッシュ前の確認
```bash
# 推奨: ブランチ状態の確認
git status
git log --oneline -3
```

### Alternatives Considered
- git操作を禁止 → SubAgentの有用性が大幅に低下
- 確認プロンプトを必須化 → 自動化の利点が失われる

---

## 5. 品質チェックリストの設計

### Decision
SubAgent生成時に自動適用する品質チェックリストを定義する。

### Rationale
生成段階で問題を検出・自動修正することで、PRレビュー前に品質を担保できる。

### チェック項目

| # | チェック項目 | 自動修正可能 | 対応アクション |
|---|-------------|-------------|---------------|
| 1 | プレースホルダー構文 (`<xxx>`, `{xxx}`) が残っていないか | Yes | 動的コマンドに置換 |
| 2 | 変数が適切にクォートされているか | Yes | ダブルクォート追加 |
| 3 | `git add -A` や `git add .` を使用していないか | Yes | 個別ファイル指定に変更 |
| 4 | トラブルシューティングセクションがあるか | Yes | テンプレートから追加 |
| 5 | 注意事項セクションがあるか | Yes | テンプレートから追加 |
| 6 | bashコマンドにエラーハンドリングがあるか | Partial | 警告表示 |

### Alternatives Considered
- 全項目を警告のみ → ユーザーの手間が増える
- 全項目を自動修正 → 意図しない変更のリスク

---

## 6. プロンプト改善の具体的な変更点

### Decision
`src/context_forge_cli/templates/commands/add-role-knowledge.md`（`context-forge init` でインストールされるテンプレート）に以下の変更を加える。

### 変更内容

1. **Phase 5: ファイル生成** セクションのSubAgentテンプレートを拡充
   - 必須セクション（トラブルシューティング、注意事項）を追加
   - bashコマンドのベストプラクティスを埋め込み
   - git操作の安全パターンを埋め込み

2. **新規Phase: 品質チェック** を追加
   - 生成後の品質チェック実行
   - 自動修正可能な項目は自動修正
   - 自動修正不可能な項目は警告表示

3. **Phase 6: 継続確認** の前に品質チェック結果を表示

### Alternatives Considered
- 別ファイルにベストプラクティスを分離 → 参照の手間が増える
- 品質チェックを別コマンド化 → ワークフローが複雑化
