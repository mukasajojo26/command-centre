#!/usr/bin/env bash
# Reports which independent reviewers are available. Read-only, no network calls.
set -u
echo "== Second opinion reviewer check =="
if command -v codex >/dev/null 2>&1; then
  echo "codex CLI: installed ($(codex --version 2>/dev/null | head -1))"
  if [ -f "$HOME/.codex/auth.json" ] || [ -n "${OPENAI_API_KEY:-}" ]; then
    echo "codex auth: credentials found"
    echo "RECOMMENDED: codex exec --sandbox read-only \"<review prompt>\""
  else
    echo "codex auth: not found. Run: codex login"
    echo "RECOMMENDED: fresh subagent (until codex is logged in)"
  fi
else
  echo "codex CLI: not installed (optional: npm install -g @openai/codex)"
  echo "RECOMMENDED: fresh subagent with only the review packet"
fi
if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  base=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null || echo main)
  echo "git: repo detected, suggested diff: git diff ${base}...HEAD"
  echo "changed files: $(git diff --name-only "${base}"...HEAD 2>/dev/null | wc -l | tr -d ' ')"
fi
