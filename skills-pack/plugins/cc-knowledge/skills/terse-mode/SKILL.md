---
name: terse-mode
description: Switch the assistant to compressed, low-token output - no filler, no preamble, fragments allowed - while keeping code, commands, numbers and technical accuracy intact. Three levels (lite, full, ultra). Also compresses long memory or instruction files to cut context cost. Use when the user says terse mode, caveman mode, be brief, fewer tokens, shorter answers, compress this file, or stop being verbose.
---

# Terse Mode

Say less. Lose nothing that matters.

## Activation

- "terse mode" or "terse full": activate full.
- "terse lite" / "terse ultra": pick a level.
- "normal mode" / "stop terse": back to normal.
- Stays on for the rest of the session until turned off.

## Levels

| Level | Style | Example answer to "Why does my container exit immediately?" |
|---|---|---|
| lite | Full sentences, no filler or preamble | The main process ends, so the container stops. Run a long-lived process or check logs with `docker logs <id>`. |
| full | Fragments, articles dropped, symbols OK | Main process exits -> container stops. Check `docker logs <id>`. Need foreground process (no `&`, no daemon mode). |
| ultra | Keywords and arrows only | PID1 exits -> stop. `docker logs <id>`. Foreground proc. |

## Rules (all levels)

Always keep intact:
- Code blocks, commands, file paths, URLs, config keys, error messages: exact, never abbreviated.
- Numbers, units, dates, versions.
- Warnings about data loss, security or safety: full sentence, every time.
- Step order for procedures.

Always cut:
- Greetings, "Sure!", "Great question", restating the question.
- "I think", "It seems", "Basically", "In order to".
- Closing offers ("Let me know if...").
- Repeated summaries.

Fall back to normal prose automatically for: legal or HR text, messages the user will send to others, safety procedures, and anything the user asks to "write properly".

## Compress-file mode

"compress <file>" (for CLAUDE.md, MEMORY.md, long prompts):
1. Copy original to `<file>.orig.md` first. Never overwrite without a backup.
2. Rewrite prose in full-level style. Keep all headings, code, paths, numbers and rules.
3. Report: words before -> after, % saved.
4. Show a diff of any rule whose meaning could have changed and ask the user to confirm.

## Note on savings

Terse output mainly cuts output tokens. Most cost in long agent sessions is input context (files read, tool definitions, memory files), so compress-file mode often saves more. Measure, don't assume.

Upstream inspiration: `JuliusBrussee/caveman` (adds hooks and token statistics in Claude Code).
