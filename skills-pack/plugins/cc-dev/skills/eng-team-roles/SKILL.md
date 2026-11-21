---
name: eng-team-roles
description: Run a product and engineering task through specialist roles - product review (office hours), engineering plan review, design review, staff-level code review, QA pass, security review, and release checklist. Use when the user asks to review an idea or plan, review a branch before merge, QA a staging URL, ship a release, or wants "a team" to look at their work. Invoke a single role by name, e.g. "run the QA role".
---

# Engineering Team Roles

One assistant, seven hats. Each role has a mandate, inputs, a checklist, and a fixed output. Run one role or chain them in order.

| # | Role | Trigger phrases | Output |
|---|---|---|---|
| 1 | Product (office hours) | "is this worth building", "review my idea" | Problem statement, user, wedge, 3 risks, go/no-go |
| 2 | Eng plan review | "review my plan", "architecture check" | Data flow, failure modes, test plan, scope cuts |
| 3 | Design review | "review the UI" | Ranked issues with screenshots or selectors |
| 4 | Code review | "review this branch/PR" | Findings by severity with file:line |
| 5 | QA | "QA this", "test staging" | Repro steps per bug, pass/fail matrix |
| 6 | Security review | "security check" | Findings mapped to OWASP/CWE |
| 7 | Release | "ship it", "release" | Checklist result, changelog, rollback plan |

## 1. Product (office hours)

Ask and answer, in this order:
1. Who exactly has this problem? Name the role and situation ("night shift security supervisor at a 400-room hotel").
2. What do they do today instead? What does it cost them (time, money, risk)?
3. What is the narrowest version that someone would use this week?
4. What would make this a 10x improvement rather than 10%?
5. Top 3 risks: demand, feasibility, distribution.
Verdict: build / shrink scope / do not build, with one paragraph of reasoning. Challenge the premise if it is weak.

## 2. Eng plan review

- Draw the data flow as a text diagram (inputs, stores, outputs).
- List failure modes per component: what happens on timeout, bad input, duplicate events, partial failure.
- State boundaries and trust zones.
- Test plan: unit, integration, one end-to-end happy path, the 3 riskiest edge cases.
- Scope: mark each item must / should / later. Cut the "later" items.

## 3. Design review

Check hierarchy, spacing consistency, typography scale, colour use, states (empty, loading, error), responsiveness at 360/768/1280 px, keyboard access, contrast. Rank issues High/Medium/Low with the exact element.

## 4. Code review (staff engineer)

Read the full diff (`git diff main...HEAD`). For each finding give severity (Blocker, Major, Minor, Nit), `file:line`, the problem, a concrete failure scenario, and the fix. Look for:
- Correctness: off-by-one, null paths, race conditions, wrong error handling, timezone bugs.
- Data: N+1 queries, missing indexes, unbounded queries, migrations that lock tables.
- Trust boundaries: unvalidated input, injection, authz checks missing on new endpoints.
- Tests: does a test fail if the change is reverted?
Do not report style issues a linter would catch.

## 5. QA

1. List the user flows touched by the change.
2. For each flow: happy path, invalid input, boundary values, back button, refresh mid-flow, slow network, mobile width.
3. If a browser tool is available, drive the real page and capture console errors and screenshots.
4. Output a matrix: Flow | Case | Result | Evidence. Each bug: steps, expected, actual, severity.

## 6. Security review

Map to OWASP Top 10 and CWE IDs. Check secrets in diff, authn/authz on new routes, input validation, output encoding, SSRF on URL fetches, file upload handling, dependency changes (new packages, install scripts), logging of PII. Rate each finding with likelihood and impact.

## 7. Release

- [ ] CI green on the exact commit being shipped
- [ ] Migrations reviewed, backward compatible, tested on a copy of production data
- [ ] Feature flags default safe
- [ ] Changelog written from commits (user-facing language)
- [ ] Rollback plan: exact command or revert PR, and data rollback if needed
- [ ] Monitoring: which dashboard and alert will show breakage within 15 minutes
- [ ] Version bumped and tagged

## Chaining

"Full review" means roles 2, 4, 6, 5, 7 in that order. Stop the chain at any Blocker and report.
