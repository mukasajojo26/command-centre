---
name: legal-review
description: Review contracts and legal documents against a saved playbook - service and security contracts, NDAs, vendor agreements, SLAs, employment offer letters, policies - producing an issues list with risk ratings, clause-by-clause redlines, and negotiation positions. Flags UAE-specific points (PDPL, labour law, onshore vs DIFC/ADGM jurisdiction). Use when the user asks to review a contract, check an NDA, compare terms to their standard, draft a redline, summarise obligations, or build a contract playbook. Not a substitute for a licensed lawyer.
---

# Legal Review

Find the risk, rate it, propose the fix. Final decisions belong to a qualified lawyer.

## Step 0: Playbook (once per organisation)

Look for `legal-playbook.md`. If missing, interview the user and create it:

```markdown
# Contract playbook
Our role usually: <customer / supplier>
Governing law preferred: <UAE onshore / ADGM / DIFC / other>; disputes: <courts / arbitration (ADGM-AC, DIAC)>
Liability cap: <e.g. 1x annual fees>; exclusions we refuse: <...>
Indemnities we accept / refuse:
Payment terms: <e.g. 60 days>
Termination for convenience: <notice period>
Insurance we require from suppliers: <public liability AED x, workers comp, professional indemnity>
Data protection: <UAE PDPL Federal Decree-Law 45/2021; DPA required when personal data processed>
Confidentiality term: <years>
Approval matrix: <who signs what value>
```

## Step 1: Intake

Confirm: document type, our party, counterparty, value, term, what the user cares about most, deadline. Extract text with clause numbers preserved.

## Step 2: Review checklist

| Area | Check |
|---|---|
| Parties | Correct legal entities, trade licence names, signatory authority |
| Scope / SLA | Measurable deliverables, KPIs, service credits, acceptance |
| Price / payment | Fixed vs variable, escalation, VAT (5%), late interest |
| Term / termination | Renewal (auto?), convenience, cause, cure periods, exit assistance |
| Liability | Cap, carve-outs (fraud, wilful misconduct, data breach, IP, death/injury), consequential loss |
| Indemnity | Mutual? Triggered by what? Defence control? |
| Insurance | Types and limits match risk; certificates required |
| Confidentiality | Definition, term, permitted disclosures, return/destruction |
| Data protection | PDPL roles (controller/processor), DPA, cross-border transfer, breach notice timeline |
| IP | Ownership of deliverables, licence back, pre-existing IP |
| Staff (security services) | Licensing of guards (e.g. SIRA Dubai / relevant Abu Dhabi authority), vetting, replacement, non-solicit, labour law compliance, WPS payroll |
| Health and safety | Compliance with ADOSH-SF / site rules, incident reporting, PPE, permits |
| Subcontracting | Consent required, flow-down |
| Law / disputes | Governing law and forum consistent with each other and the playbook |
| Boilerplate | Assignment, change of control, force majeure (what counts), notices, entire agreement, language (Arabic prevails?) |

## Step 3: Output

```
Contract: <name>  Our role: <...>  Reviewed: <date>
Overall risk: High / Medium / Low   Sign as is? Yes / After changes / No

Issues (highest risk first)
| # | Clause | Issue | Risk (H/M/L) | Playbook position | Proposed redline | Fallback |

Obligations summary (what WE must do, with dates)
Missing clauses
Questions for the counterparty
Items needing a lawyer: <list>
```

Redline format: quote the original clause, then the proposed text, then one line of rationale.

## Modes

- **NDA quick check**: 10-point triage, verdict in under a page.
- **Compare to template**: diff the counterparty draft against our standard, list every deviation.
- **Obligations register**: table of every "shall" for our side with owner and due date (feed into a tracker).

## Guardrails

- Start formal outputs with: "This review is not legal advice. Have a qualified lawyer approve before signing."
- Quote clauses exactly. Never claim a clause says something it does not.
- If the governing law is outside the user's knowledge or the doc is in Arabic only, flag it and recommend a translation check (Arabic text typically prevails in UAE onshore courts).
- Do not upload confidential contracts to external tools beyond what the user approved.
- Upstream: Anthropic's `anthropics/claude-for-legal` marketplace offers practice-area plugins (commercial, employment, litigation, privacy) with a cold-start playbook interview.
