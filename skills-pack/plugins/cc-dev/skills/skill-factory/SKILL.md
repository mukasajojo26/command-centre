---
name: skill-factory
description: Create, improve, validate and package Claude Agent Skills (SKILL.md folders) for Claude.ai, Claude Code and the API. Use when the user wants to turn a repeatable workflow into a skill, fix a skill that does not trigger, check a skill folder for errors, or zip skills for upload to Claude.ai.
---

# Skill Factory

> Paths: `$SKILL_DIR` means the folder that contains this SKILL.md (Claude Code shows it as the skill base directory). Set it first, e.g. `SKILL_DIR=~/.claude/skills/<skill-name>`.

Turn a repeatable task into a skill that triggers reliably and does the job the same way every time.

## Anatomy

```
my-skill/
  SKILL.md            required: YAML frontmatter + instructions
  scripts/            optional: deterministic code the skill runs
  references/         optional: long docs loaded only when needed
  assets/             optional: templates, images, sample files
```

Frontmatter rules (checked by the validator):
- `name`: lowercase letters, digits, hyphens. Max 64 characters. Must match the folder name. Must not contain the reserved words "claude" or "anthropic".
- `description`: max 1024 characters, no XML tags. Says WHAT it does AND WHEN to use it, with trigger phrases the user would actually type.

## Step 1: Interview (5 questions)

1. What task, start to finish? Ask for one real example input and the ideal output.
2. What triggers it? Collect 5 phrases a user would type.
3. What must never happen? (Inventing data, sending externally, overwriting files.)
4. What is deterministic and better done by a script? (Calculations, file checks, formatting.)
5. Where does it run? Claude.ai (upload ZIP), Claude Code (folder or plugin), or API.

## Step 2: Write SKILL.md

Structure:
1. One-line purpose.
2. Inputs required, and what to ask if missing.
3. Numbered procedure. Each step has a verifiable outcome.
4. Output format, with a filled example.
5. Guardrails and failure handling.

Writing rules:
- Under 500 lines. Move long material to `references/` and link it ("Read references/x.md when Y").
- Imperative voice. Specific numbers over adjectives.
- Put the trigger phrases in the description, not only in the body. The description is all Claude sees when deciding to load the skill.

## Step 3: Validate

```bash
python3 "$SKILL_DIR/scripts/validate_skill.py" path/to/skill-or-parent-folder
```

The validator checks frontmatter, name rules, description length, line count, broken relative links, and executable scripts. Fix every ERROR. Review every WARN.

## Step 4: Test triggering

Write 5 should-trigger prompts and 3 should-not-trigger prompts. Run them in a fresh session. If a should-trigger prompt misses, add its key phrase to the description. If a should-not prompt fires, narrow the description.

## Step 5: Package

```bash
python3 "$SKILL_DIR/scripts/validate_skill.py" path/to/skill --zip dist/
```

Produces `dist/<name>.zip` with the folder at the archive root, ready for Claude.ai: Settings > Capabilities > Skills > Upload skill.

## Security review before installing any third-party skill

Skills can run code with your permissions. Before installing one you did not write:
- Read every file in `scripts/` and any install script. Never pipe `curl | bash` unread.
- Search for network calls (`curl`, `wget`, `requests`, `fetch`), credential paths (`~/.ssh`, `~/.aws`, `.env`), and `eval`/`exec`.
- Check hooks in plugins (`hooks/hooks.json`): they run automatically on events.
- Pin to a commit SHA you reviewed. Re-review on update.
