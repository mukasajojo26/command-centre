#!/usr/bin/env bash
# Copy all 16 skills into a Claude Code skills folder.
#   bash install-local.sh            -> ~/.claude/skills (personal, all projects)
#   bash install-local.sh --project  -> ./.claude/skills (current project only)
# Existing skills with the same name are backed up to <name>.bak-<timestamp>.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.claude/skills"
[ "${1:-}" = "--project" ] && DEST="$PWD/.claude/skills"
mkdir -p "$DEST"
ts=$(date +%Y%m%d%H%M%S)
n=0
for skill in "$HERE"/plugins/*/skills/*/; do
  name=$(basename "$skill")
  if [ -e "$DEST/$name" ]; then mv "$DEST/$name" "$DEST/$name.bak-$ts"; echo "backed up existing $name"; fi
  cp -R "$skill" "$DEST/$name"
  n=$((n+1))
done
echo "Installed $n skills into $DEST. Restart Claude Code to load them."
