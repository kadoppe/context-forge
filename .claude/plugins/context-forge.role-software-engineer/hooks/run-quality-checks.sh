#!/bin/bash
# Quality checks hook script for software-engineer role
# Runs ruff, mypy, and pytest on Stop event

set -e

echo "=== Running Quality Checks ==="

# Run ruff (linter)
echo ""
echo ">>> Running ruff check..."
if uv run ruff check . 2>/dev/null; then
    echo "✓ ruff: No issues found"
else
    echo "✗ ruff: Issues found (see above)"
fi

# Run mypy (type checker)
echo ""
echo ">>> Running mypy..."
if uv run mypy src 2>/dev/null; then
    echo "✓ mypy: No type errors"
else
    echo "✗ mypy: Type errors found (see above)"
fi

# Run pytest
echo ""
echo ">>> Running pytest..."
if uv run pytest 2>/dev/null; then
    echo "✓ pytest: All tests passed"
else
    echo "✗ pytest: Some tests failed (see above)"
fi

echo ""
echo "=== Quality Checks Complete ==="
