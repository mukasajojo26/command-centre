---
name: humanizer
description: Rewrite text so it reads like a capable person wrote it, removing the tell-tale patterns of AI writing (buzzwords, em dashes, rule-of-three lists, hype, stacked hedges, stock openers and closers) without changing meaning or inventing facts. Includes a lint script that flags patterns. Use when the user asks to humanize, de-AI, make natural, tighten, or edit the tone of a draft, email, post, report or bio, or asks "does this sound like AI".
---

# Humanizer

> Paths: `$SKILL_DIR` means the folder that contains this SKILL.md (Claude Code shows it as the skill base directory). Set it first, e.g. `SKILL_DIR=~/.claude/skills/<skill-name>`.

Edit for a natural, direct voice. Keep every fact. Add nothing that is not in the source.

## Procedure

1. **Lint first.** Save the draft to a file and run:
   ```bash
   python3 "$SKILL_DIR/scripts/ai_lint.py" draft.txt
   ```
   (No shell? Apply the pattern list below by hand.)
2. **Identify the core point.** Write it in one sentence. That sentence, or a version of it, opens the rewrite.
3. **Rewrite** using the rules below.
4. **Re-lint** the rewrite. Target: zero HIGH findings.
5. **Return** the rewrite, then a short list of the main changes (max 5 bullets). If the user asked for "just the text", return only the text.

## Rules

Voice
- Plain words. Short sentences, varied length. Fragments allowed.
- Active voice. Contractions in emails and posts, none in formal reports or SOPs.
- State the conclusion. A clear recommendation beats a neutral summary.

Structure
- Answer first. No warm-up, no restating the question.
- Specific beats vague: real names, numbers, dates, examples from the source.
- Cut any sentence that adds nothing. Do not summarize at the end unless the format needs it.
- Lists only for procedures, comparisons and reports. Paragraphs for conversation.

Punctuation
- No em dashes, en dashes, or spaced hyphens used as pauses. Use commas, periods, colons or parentheses.
- Avoid semicolons. Straight quotes only.

## Pattern catalogue (what the linter flags)

| Pattern | Example | Fix |
|---|---|---|
| Buzzwords | leverage, seamless, robust, holistic, empower, elevate, unlock, delve, landscape, game-changer, cutting-edge, synergy, streamline | Use the plain verb: use, smooth, strong, full, let, raise, open, explore, field |
| Stock openers | "Great question!", "In today's fast-paced world", "Let's dive in", "Here's the thing" | Delete. Start with the point. |
| Stock closers | "In conclusion", "At the end of the day", "I hope this helps", "Feel free to reach out" | Delete or replace with a concrete next step. |
| Contrast formula | "It's not just X, it's Y" | Say Y. |
| Rhetorical opener | "Ever wondered why...?" | State the answer. |
| Rule of three | "fast, reliable, and scalable" everywhere | Keep the one or two that are true and specific. |
| Filler adverbs | very, really, truly, extremely, highly, significantly, incredibly | Delete, or use a number. |
| Stacked hedges | "may potentially be somewhat" | Commit or cut. One hedge maximum. |
| Significance inflation | "pivotal", "testament to", "plays a vital role", "underscores" | Say what it does. |
| Vague attribution | "experts say", "studies show" | Name the source or remove. |
| Signposting | "It's important to note that", "When it comes to" | Delete the frame, keep the content. |
| Em/en dashes | "results - and more" | Comma, period, or parentheses. |
| Emoji and bold overload | 🚀 **Key insight** | Remove unless the user's own style uses them. |

## Keep (do not over-correct)

- Technical terms the audience uses (CCTV, SOP, MTTR, ISO 45001).
- Legal or regulatory wording that must stay exact. Flag it rather than rewrite.
- The author's own phrasing that is already specific and plain.
- Quoted material. Never edit inside quotes.

## Example

Before:
> In today's rapidly evolving security landscape, it's important to note that leveraging cutting-edge CCTV analytics can truly empower teams to seamlessly elevate their incident response — unlocking unprecedented efficiency.

After:
> CCTV analytics cut our average incident response time from 9 minutes to 4. The system flags loitering and tailgating, so guards respond before a complaint comes in.

(The numbers came from the user's source notes. If the source has no numbers, the rewrite says "faster" and asks the user for the figure. Never invent one.)
