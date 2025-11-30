# Data Model: Role Plugin Migration Command

**Date**: 2025-11-30
**Feature**: 001-role-plugin-migrate

## Entities

### 1. RolePlugin

context-forge で生成された職能別知見プラグイン。

**属性**:
| フィールド | 型 | 説明 |
|-----------|-----|------|
| name | string | プラグイン名（`context-forge.role-{role-name}` 形式） |
| path | Path | プラグインディレクトリのパス |
| version | string | plugin.json 内の version フィールド（セマンティックバージョン） |
| description | string | プラグインの説明 |
| components | PluginComponents | プラグイン内のコンポーネント群 |

**関連**:
- 1つの RolePlugin は 1つの PluginComponents を持つ
- 1つの RolePlugin は 0..n の Backup を持つ

### 2. PluginComponents

プラグイン内のコンポーネント構成。

**属性**:
| フィールド | 型 | 説明 |
|-----------|-----|------|
| plugin_json | Path | plugin.json ファイルパス |
| agents | list[Path] | agents/ 内の .md ファイル群 |
| skills | list[Path] | skills/ 内の SKILL.md ファイル群 |
| commands | list[Path] | commands/ 内の .md ファイル群 |
| hooks_json | Path | None | hooks/hooks.json（存在する場合） |

### 3. PluginVersion

プラグインのバージョン情報。

**属性**:
| フィールド | 型 | 説明 |
|-----------|-----|------|
| current | string | 現在のバージョン（plugin.json から取得） |
| target | string | 目標バージョン（context-forge の現在バージョン） |
| needs_migration | bool | current < target かどうか |

**状態遷移**:
```
[Unknown] --parse--> [Detected] --compare--> [UpToDate | NeedsMigration]
```

### 4. Backup

マイグレーション前の状態を保存したバックアップ。

**属性**:
| フィールド | 型 | 説明 |
|-----------|-----|------|
| timestamp | datetime | バックアップ作成日時 |
| plugin_name | string | 元プラグイン名 |
| path | Path | バックアップディレクトリパス |
| original_version | string | バックアップ時のバージョン |

**パス形式**: `.claude/plugins/.backup/{YYYYMMDD_HHMMSS}_{plugin-name}/`

### 5. MigrationReport

マイグレーション結果のサマリー。

**属性**:
| フィールド | 型 | 説明 |
|-----------|-----|------|
| total_plugins | int | 検出されたプラグイン総数 |
| migrated | list[string] | 更新されたプラグイン名 |
| skipped | list[string] | スキップされたプラグイン名（既に最新） |
| errors | list[MigrationError] | エラーが発生したプラグイン |

### 6. MigrationError

マイグレーションエラー情報。

**属性**:
| フィールド | 型 | 説明 |
|-----------|-----|------|
| plugin_name | string | エラーが発生したプラグイン名 |
| error_type | string | エラー種別（parse_error, write_error, etc） |
| message | string | エラーメッセージ |
| backup_path | Path | None | バックアップパス（復元用） |

### 7. SlashCommandFile

Claude Code で実行可能なコマンド定義ファイル。

**属性**:
| フィールド | 型 | 説明 |
|-----------|-----|------|
| name | string | コマンド名（例: "migrate"） |
| description | string | コマンドの説明（frontmatter から） |
| content | string | コマンド本体（Markdown） |
| source_path | Path | テンプレートファイルのパス |
| target_path | Path | インストール先のパス |

## Entity Relationships

```
RolePlugin (1) -----> (1) PluginComponents
    |
    | has version
    v
PluginVersion
    |
    | determines
    v
MigrationReport (1) -----> (0..n) MigrationError
    ^
    | created from
    |
Backup (0..n) <----- (1) RolePlugin

SlashCommandFile (独立 - init コマンドで管理)
```

## Validation Rules

### RolePlugin
- name は `context-forge.role-` で始まること
- path は存在するディレクトリであること
- plugin.json が存在すること

### PluginVersion
- セマンティックバージョン形式（x.y.z）であること
- 比較可能であること

### Backup
- timestamp は ISO 8601 形式
- path は書き込み可能なディレクトリ

### SlashCommandFile
- name は英数字、ハイフン、アンダースコアのみ
- 最大64文字
- YAML frontmatter に description が必須
