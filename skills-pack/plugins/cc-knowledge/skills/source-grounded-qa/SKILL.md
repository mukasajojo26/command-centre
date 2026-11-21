---
name: source-grounded-qa
description: Answer questions strictly from a defined set of sources (uploaded PDFs, standards, SOPs, manuals, regulations, notebooks) with page or section citations for every claim, and say "not in the sources" instead of guessing. Works like a NotebookLM notebook inside Claude. Use when the user asks what a document, standard, code or policy says, wants citations, wants to query a document library, or says "only use my documents".
---

# Source-Grounded Q&A

The sources are the only truth. Every claim gets a citation. Gaps are reported, not filled.

## Step 1: Build the notebook

1. List the sources in scope: file name, title, version/date, page count. Save as `notebook.md` in the working folder:
   ```markdown
   # Notebook: <topic>
   | ID | Title | Version/date | File | Pages |
   | S1 | ADOSH-SF CoP 4.0 First Aid | v3.0 2019 | cop4.pdf | 24 |
   ```
2. Extract text with page markers so citations are exact:
   ```bash
   pdftotext -layout source.pdf - | awk 'BEGIN{p=1} /\f/{p++} {print "[p" p "] " $0}' > source.txt
   ```
   For scanned PDFs, OCR first (`ocrmypdf`) and note OCR in the notebook.
3. If a source cannot be read, list it as UNREAD. Never answer from an unread source.

## Step 2: Answer

1. Search the extracted text for the key terms and synonyms (`grep -n -i`).
2. Read the surrounding section, not just the hit line.
3. Answer in this format:

```
Answer: <direct answer in 1-3 sentences>

Evidence:
- "<short exact quote>" [S1, p.12, clause 5.3]
- "<short exact quote>" [S2, p.4]

Not covered by the sources: <part of the question with no support, or "none">
Conflicts: <where sources disagree, both cited, which is newer>
```

## Rules

- Quote exactly. Keep quotes short (under 40 words each).
- Cite source ID + page (+ clause or section where available).
- If the sources do not answer it, say: "The sources do not cover this." Then, only if useful, add general knowledge in a separate section labelled **Outside the sources**.
- Note the version date. Flag if a source may be superseded (e.g. "check for a newer revision").
- Do not merge two clauses into one paraphrase that neither says.
- For regulations and standards, do not reproduce large copyrighted sections. Summarise and cite.

## Modes

- **Briefing**: a 1-page summary of a source: purpose, scope, key requirements (cited), deadlines, roles.
- **Compliance checklist**: turn "shall" statements into a checklist table: Requirement | Clause | Evidence needed | Status.
- **Compare**: two sources side by side on one topic, with citations, differences highlighted.
- **Quiz**: 10 questions with answers and citations, for training.

## Google NotebookLM option

To query an actual NotebookLM notebook from Claude Code (local only, needs Chrome and a Google login), the community skill `PleasePrompto/notebooklm-skill` uses browser automation. It stores a Google session cookie locally. Review its scripts first and use a dedicated Google account, not a work account holding sensitive data.
