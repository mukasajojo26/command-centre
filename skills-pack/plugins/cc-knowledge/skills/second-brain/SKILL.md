---
name: second-brain
description: Set up and run a plain-Markdown "second brain" (works with Obsidian or any folder) - capture inbox, daily notes, projects, areas, resources, decision log, weekly review - and a persistent assistant memory file. Also designs a personalised build plan (PRD) for a more automated AI second brain. Use when the user wants to organise notes, capture ideas, plan their week, do a weekly review, find something they wrote before, or build a personal knowledge system.
---

# Second Brain

A folder of Markdown files the assistant can read and write. No database, no lock-in.

## Structure (PARA + logs)

```
brain/
  00-inbox/            raw captures, process weekly
  01-daily/            YYYY-MM-DD.md
  02-projects/         has a deadline and an outcome
  03-areas/            ongoing responsibility (e.g. fire safety, team, career)
  04-resources/        reference material by topic
  05-archive/          finished or inactive
  decisions.md         decision log
  people.md            who's who (work context only, no sensitive personal data)
  MEMORY.md            what the assistant should always know about the user
```

Setup command: create the folders and seed files with the templates below. Ask before creating anything outside the current directory.

## Templates

**Daily note** (`01-daily/YYYY-MM-DD.md`)
```markdown
# YYYY-MM-DD
## Top 3
- [ ]
## Log
- HH:MM
## Captured
## Done
```

**Project** (`02-projects/<name>.md`)
```markdown
# <Project>
Outcome: <what done looks like>   Due: <date>   Owner: <name>   Status: active
## Next actions
- [ ]
## Notes
## Links
```

**Decision log entry** (append to `decisions.md`)
```markdown
## YYYY-MM-DD: <decision>
Context: | Options: | Chosen: | Why: | Review on: <date>
```

**MEMORY.md**
```markdown
# Memory
## Preferences
## Current focus
## Standing facts
## Updated: YYYY-MM-DD
```

## Daily operations

| User says | Do |
|---|---|
| "capture: ..." | Append to `00-inbox/inbox.md` with timestamp. No sorting yet. |
| "start my day" | Create today's daily note. Pull open next actions from active projects and items due within 7 days. Propose Top 3. |
| "log: ..." | Append to today's Log with time. |
| "what did I decide about X" | Search `decisions.md`, then daily notes. Quote the entry with its date. |
| "find ..." | `grep -ril` across the vault; return file paths and the matching lines. |
| "remember ..." | Update MEMORY.md. Confirm what changed. |
| "weekly review" | See below. |

## Weekly review (30 minutes)

1. Process inbox to zero: each item becomes a next action in a project, a resource note, a calendar item, or deleted.
2. For each active project: status, next action, blocked? Flag projects with no next action.
3. Areas: anything slipping? (e.g. certifications expiring, overdue audits.)
4. Review last 7 daily notes. Extract wins, lessons, and open loops.
5. Write `01-daily/YYYY-Www-review.md` with: wins, misses, lessons, Top 3 for next week.

## Build-plan mode (AI second brain PRD)

If the user wants an always-on automated assistant (scheduled briefings, email/calendar integration, Slack capture), interview them on: tools they use, what to automate, privacy limits, budget, technical skill. Produce a phased PRD:
- Phase 1: vault + MEMORY.md + manual commands (this skill).
- Phase 2: integrations (calendar, email, task app) via connectors or MCP servers.
- Phase 3: scheduled jobs (morning brief, weekly review prompt) and a capture channel.
- For each phase: components, tools, setup steps, cost, risks, success measure.
Upstream reference: `coleam00/second-brain-starter` provides a PRD-generator skill of this kind.

## Guardrails
- Never delete notes. Move to `05-archive/`.
- Do not store passwords, ID numbers, health or financial account data in the vault.
- Work notes may be confidential: keep the vault in a location your employer permits.
