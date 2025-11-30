# context-forge Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-11-29

## Active Technologies
- Python 3.11, 3.12（マトリックスビルド） + GitHub Actions, pip, hatch (002-github-actions-ci)
- Python 3.11+ + Typer (CLI), Rich (terminal UI), PyYAML (001-role-knowledge-plugin)
- ファイルシステム（.claude/plugins/, ~/.cache/context-forge/docs/） (001-role-knowledge-plugin)
- Markdown (Claude Code プロンプト形式) + Claude Code Plugin System (commands, agents) (001-improve-subagent-quality)
- N/A (ファイルベースのMarkdownプロンプト) (001-improve-subagent-quality)
- Python 3.11+ / Markdown (Claude Code プロンプト形式) + Typer (CLI), Rich (terminal UI), PyYAML (003-skill-subagent-activation)
- ファイルシステム（`.claude/` ディレクトリ） (003-skill-subagent-activation)

- Python 3.11+ + Typer (CLI), Rich (terminal UI) (001-context-forge-cli)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.11+: Follow standard conventions

## Recent Changes
- 003-skill-subagent-activation: Added Python 3.11+ / Markdown (Claude Code プロンプト形式) + Typer (CLI), Rich (terminal UI), PyYAML
- 001-improve-subagent-quality: Added Markdown (Claude Code プロンプト形式) + Claude Code Plugin System (commands, agents)
- 001-role-knowledge-plugin: Added Python 3.11+ + Typer (CLI), Rich (terminal UI), PyYAML


<!-- MANUAL ADDITIONS START -->
## Package Management

- Use `uv` instead of `pip` for all package operations
- Install dependencies: `uv sync --dev`
- Run commands: `uv run <command>` (e.g., `uv run pytest`, `uv run ruff check .`, `uv run mypy src`)
<!-- MANUAL ADDITIONS END -->

<!-- context-forge settings -->
@.claude/context-forge.md
<!-- end context-forge settings -->
