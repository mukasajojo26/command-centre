---
name: dev-discipline
description: A disciplined software workflow - brainstorm, written plan, test-driven development, systematic debugging, and verification before claiming done. Use for any non-trivial coding task, new feature, bug fix, refactor, or when a previous attempt failed, tests are flaky, or the user says "do it properly".
---

# Dev Discipline

Five gates. Do not skip a gate because the task "looks simple". Trivial one-line edits may compress gates 1 and 2 into one sentence each.

## Gate 1: Brainstorm (understand before building)

- Restate the goal in one sentence and the definition of done in testable terms.
- Read the relevant code first. List the files you will touch.
- Ask at most 3 questions, and only if the answer changes the design. Otherwise choose a default and state it.
- Offer 2 approaches when there is a real trade-off. Recommend one with the reason.

## Gate 2: Plan

Write a numbered plan where each step is small (2 to 10 minutes of work) and independently verifiable:

```
1. Add failing test: parseShift() rejects end time before start time  -> verify: test fails for the right reason
2. Implement validation in src/shift.ts                               -> verify: test passes
3. Add test for overnight shifts (22:00 to 06:00)                     -> verify: fails, then passes
4. Update API docs                                                    -> verify: docs build
```

For multi-file work, save the plan to `docs/plans/YYYY-MM-DD-<topic>.md` so it survives context loss.

## Gate 3: Test-driven development

Red, green, refactor, every time:
1. **Red**: write one failing test. Run it. Confirm it fails *for the expected reason* (not an import error).
2. **Green**: write the minimum code to pass. Run it.
3. **Refactor**: clean up with tests green. Run the full suite.

Rules:
- No production code without a failing test first, unless the user opts out or no test harness exists (then say so and add one if cheap).
- Test behaviour, not implementation details.
- One assertion concept per test. Name tests as sentences: `rejects shift when end precedes start`.

## Gate 4: Systematic debugging (when something breaks)

Never guess-and-patch. Follow the loop:
1. **Reproduce**: smallest command that shows the failure. Record exact output.
2. **Locate**: bisect (git bisect, comment out halves, add logging at boundaries). Trace data backward from the symptom to the source.
3. **Hypothesize**: one written hypothesis at a time: "X fails because Y, which predicts Z".
4. **Test the hypothesis**: check prediction Z. If wrong, discard and form a new one.
5. **Fix the root cause**, not the symptom. Add a regression test that failed before the fix.
6. After 3 failed fix attempts, stop and question the architecture. Report to the user.

## Gate 5: Verification before completion

Never say "done", "fixed" or "working" without evidence from this session:
- Run the tests, typecheck, lint, and build. Paste the summary line.
- For UI: load the page and check the changed behaviour.
- Re-read the original request. Tick each requirement.
- State plainly anything not verified and why.

## Report format

```
Done: <one line>
Evidence: <test count passed / command output summary>
Changed files: <list>
Not verified: <list or "none">
Follow-ups: <optional>
```

## Red flags (stop and reset)

- "This should work" without running it.
- Editing tests to make them pass.
- A fix that adds a special case for the exact failing input.
- Growing diff with no new tests.
