---
name: second-opinion-review
description: Get an independent second opinion on code, a plan, or a decision - either from the OpenAI Codex CLI when installed, or from a fresh reviewer subagent with no shared context. Includes an adversarial mode that tries to break the design. Use when the user asks for a second opinion, a cross-model review, an adversarial review, "poke holes in this", or wants a check before merging something risky.
---

# Second Opinion Review

> Paths: `$SKILL_DIR` means the folder that contains this SKILL.md (Claude Code shows it as the skill base directory). Set it first, e.g. `SKILL_DIR=~/.claude/skills/<skill-name>`.

An independent reviewer catches what the author misses. Independence matters more than which model does it.

## Step 1: Pick the reviewer

Run the check script:

```bash
bash "$SKILL_DIR/scripts/check-reviewers.sh"
```

It reports which of these are available:

| Reviewer | When to use | How |
|---|---|---|
| Codex CLI (`codex`) | Installed and logged in, user wants a different model family | `codex exec --sandbox read-only "<prompt>"` |
| Fresh subagent | Codex missing, or the user prefers Claude only | Spawn a general-purpose subagent with ONLY the review prompt and file paths, no conversation history |
| Self-review (last resort) | No subagents available | Re-read as a hostile reviewer, say clearly it is not independent |

The official OpenAI plugin (`/plugin marketplace add openai/codex-plugin-cc`, then `/plugin install codex@openai-codex`) adds `/codex:review` and `/codex:adversarial-review`. If the user has it, prefer it.

## Step 2: Build the review packet

The reviewer gets nothing else, so the packet must stand alone:
- Goal of the change in 2 sentences.
- The diff (`git diff main...HEAD`) or file paths, or the plan text.
- Constraints (performance budget, compatibility, regulatory).
- What NOT to comment on (formatting, naming nits).
- Output format (below).

Never include secrets, `.env` contents, customer data or personal details in a packet sent to an external CLI or API. Strip them first.

## Step 3: Review modes

**Standard review prompt**
```
Review this change for correctness bugs, security issues and missing tests.
For each finding: severity (Blocker/Major/Minor), file:line, what breaks,
a concrete input or sequence that triggers it, and the fix.
Report only findings you can justify from the code. Say "no findings" if none.
```

**Adversarial prompt**
```
Assume this design is wrong. Your job is to find the strongest reasons it will
fail in production: wrong assumptions, race conditions, scale limits, abuse
cases, operational blind spots, and simpler alternatives that were missed.
Rank the top 5 by likelihood x impact. Be specific. No praise.
```

**Decision review prompt** (non-code)
```
Here is a decision and its reasoning. Identify the weakest assumption,
the most likely way it goes wrong, the information that would change the
decision, and one alternative the author did not consider.
```

## Step 4: Reconcile

Do not paste the second opinion raw. For each finding:
1. Verify it against the code yourself.
2. Mark it Confirmed, Plausible, or Rejected (with reason).
3. Fix Confirmed Blockers and Majors if the user asked for fixes.

Output:
```
Reviewer: codex | subagent | self (not independent)
Confirmed: n   Plausible: n   Rejected: n
<table of findings with status>
Recommendation: merge / fix first / rethink
```
