---
name: catchup
description: |
  Quick status brief so the user can pick up where things left off — what changed, what state it's in, what's next.

  Trigger when the user says "catch up", "catch me up", "where were we", "what's the status", "what's going on", or returns to a task/repo after a gap and wants an overview.

  Output: since last time / current state / next step. Under 12 lines. Grounded in actual git status/log/diff, not guesses.
disable-model-invocation: true
---

# Catch Up

Goal: user reads this once and knows exactly what happened, what state things are in, and what to do next — no need to dig through `git log` themselves.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms stay in English.
- Ground every line in evidence: check `git status`, `git log` (recent commits, last ~5-10 or since $ARGUMENTS if given a branch/date/commit), and `git diff` for uncommitted work before writing anything. Never guess at what changed.
- "Since last time" = what actually landed: commits, files changed, uncommitted work in progress. Cite specifics (file names, commit subjects), not vague summaries like "some fixes were made".
- "Current state" = is it clean, mid-change, broken, blocked? Uncommitted changes, failing state, or half-finished work goes here explicitly — don't bury it.
- "Next step" = the single most obvious next action, not a full plan. If there's an open blocker (merge conflict, failing test, unclear decision), say that instead.
- If there's no git repo or no meaningful history, say so directly rather than padding the response.
- Max 12 lines total.

## Output format

```
**Since last time**
- [commit or change, specific]
- [uncommitted work in progress, if any]

**Current state**
[clean / mid-change / blocked — one line, concrete]

**Next step**
[the one obvious next action, or the blocker in the way]
```

If `$ARGUMENTS` is given (e.g. a branch, date, or "since <commit>"), scope the git history to that instead of just recent commits.
