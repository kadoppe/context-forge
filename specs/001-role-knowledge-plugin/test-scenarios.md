# Test Scenarios: Role Knowledge Plugin Generator

**Feature**: 001-role-knowledge-plugin
**Date**: 2025-11-29

## Manual Testing Scenarios

### US1: コマンドインストール

#### Scenario 1.1: 初回インストール
1. 新しいプロジェクトディレクトリを作成
2. `context-forge init` を実行
3. **Expected**:
   - `.claude/commands/context-forge.add-role-knowledge.md` が作成される
   - `context-forge.hello-world.md` も作成される

#### Scenario 1.2: 再インストール（上書き確認）
1. 既に `init` 済みのプロジェクトで `context-forge init` を再実行
2. 確認プロンプトで `n` を入力
3. **Expected**: ファイルがスキップされ、既存ファイルが保持される

#### Scenario 1.3: 強制上書き
1. `context-forge init --force` を実行
2. **Expected**: 確認なしで全ファイルが上書きされる

---

### US2: 新規ロールプラグイン作成

#### Scenario 2.1: 新規ロール作成（Skill）
1. Claude Code で `/context-forge.add-role-knowledge` を実行
2. 既存ロールがない場合、新規作成フローが開始される
3. ロール名: `frontend-engineer`
4. 説明: `フロントエンド開発のベストプラクティス`
5. 知見: `コードレビューチェックリスト`
6. タイプ判定で `Skill` が推奨される → `yes` で確定
7. **Expected**:
   - `.claude/plugins/context-forge.role-frontend-engineer/.claude-plugin/plugin.json` が作成される
   - `.claude/plugins/context-forge.role-frontend-engineer/skills/code-review-checklist/SKILL.md` が作成される

#### Scenario 2.2: 新規ロール作成（Command）
1. `/context-forge.add-role-knowledge` を実行
2. ロール名: `backend-engineer`
3. 知見: `APIドキュメントを自動生成する`
4. タイプ判定で `Command` が推奨される
5. **Expected**:
   - `.claude/plugins/context-forge.role-backend-engineer/commands/api-documentation.md` が作成される

#### Scenario 2.3: 新規ロール作成（Sub Agent）
1. `/context-forge.add-role-knowledge` を実行
2. ロール名: `security-engineer`
3. 知見: `セキュリティ観点でコードを自律的にレビューする`
4. タイプ判定で `Sub Agent` が推奨される
5. **Expected**:
   - `.claude/plugins/context-forge.role-security-engineer/agents/security-review.md` が作成される

#### Scenario 2.4: 新規ロール作成（Hook）
1. `/context-forge.add-role-knowledge` を実行
2. ロール名: `devops-engineer`
3. 知見: `コミット前にセキュリティスキャンを実行する`
4. タイプ判定で `Hook` が推奨される
5. **Expected**:
   - `.claude/plugins/context-forge.role-devops-engineer/hooks/hooks.json` が作成される

---

### US3: 既存ロールプラグイン更新

#### Scenario 3.1: 既存ロールに知見追加
1. 既存の `context-forge.role-frontend-engineer` プラグインがある状態で `/context-forge.add-role-knowledge` を実行
2. 既存ロール一覧が表示される
3. `1` を入力して `frontend-engineer` を選択
4. 新しい知見: `パフォーマンス最適化ガイド`
5. **Expected**:
   - 既存の `code-review-checklist` が保持される
   - 新しい `performance-optimization/SKILL.md` が追加される

#### Scenario 3.2: Hook追加時の hooks.json マージ
1. 既存の Hook がある `context-forge.role-devops-engineer` プラグインに新しい Hook を追加
2. **Expected**:
   - 既存の hooks.json エントリが保持される
   - 新しいエントリが追加される

---

### US4: 知見タイプ自動判別

#### Scenario 4.1: Skill 判定テストケース

| 入力 | 期待されるタイプ |
|------|------------------|
| コードレビューチェックリスト | Skill |
| React コンポーネント設計ガイドライン | Skill |
| TypeScript ベストプラクティス | Skill |
| セキュリティ対策の参照情報 | Skill |

#### Scenario 4.2: Command 判定テストケース

| 入力 | 期待されるタイプ |
|------|------------------|
| テストレポートを生成する | Command |
| 設計ドキュメントを自動作成する | Command |
| データベースマイグレーションを実行する | Command |
| API クライアントコードを生成する | Command |

#### Scenario 4.3: Sub Agent 判定テストケース

| 入力 | 期待されるタイプ |
|------|------------------|
| コードの品質を自律的に分析する | Sub Agent |
| アーキテクチャをレビューして改善提案する | Sub Agent |
| バグの根本原因を調査する | Sub Agent |
| パフォーマンスボトルネックを特定する | Sub Agent |

#### Scenario 4.4: Hook 判定テストケース

| 入力 | 期待されるタイプ |
|------|------------------|
| コミット前にリンターを実行する | Hook |
| ファイル保存時に自動フォーマットする | Hook |
| プッシュ前にテストを実行する | Hook |
| 特定のファイル変更時に通知する | Hook |

#### Scenario 4.5: 曖昧なケース
1. 入力: `コードの品質を改善する`
2. **Expected**: 複数のタイプが候補として表示され、ユーザーに選択を促す

---

### エラーケース

#### Error 1: 無効なロール名
1. ロール名に `Frontend Engineer` (スペースあり) を入力
2. **Expected**: バリデーションエラーが表示され、再入力を促される

#### Error 2: ドキュメント取得失敗
1. ネットワーク接続がない状態で実行
2. **Expected**: 警告メッセージが表示され、内蔵仕様で続行

#### Error 3: キャンセル
1. フロー途中で `cancel` を入力
2. **Expected**: 作成中のファイルが削除され、終了

---

## Automated Test Coverage

| Test | Location | Status |
|------|----------|--------|
| init creates add-role-knowledge | `tests/integration/test_cli.py` | ✓ |
| init installs all templates | `tests/integration/test_cli.py` | ✓ |
| init --force overwrites | `tests/integration/test_cli.py` | ✓ |
| init prompts on conflict | `tests/integration/test_cli.py` | ✓ |

---

## Verification Checklist

- [X] `uv run context-forge init` で `add-role-knowledge` がインストールされる
- [ ] Claude Code で `/context-forge.add-role-knowledge` が実行可能
- [ ] 新規ロールプラグインが `.claude/plugins/context-forge.role-{role-name}/` に生成される
- [ ] 既存プラグインへの追加が既存ファイルを破壊しない
- [ ] 各タイプの知見が正しく判定される
