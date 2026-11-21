#!/usr/bin/env bash
# Validate every skill and build one ZIP per skill in skills-pack/dist/ for Claude.ai upload.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
rm -rf "$HERE/dist" && mkdir -p "$HERE/dist"
python3 "$HERE/plugins/cc-dev/skills/skill-factory/scripts/validate_skill.py" "$HERE/plugins" --zip "$HERE/dist"
