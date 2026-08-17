---
name: catchup
description: |
  Quick status brief so the user can pick up where things left off — what changed, what state it's in, what's next.

  Trigger when the user says "catch up", "catch me up", "where were we", "what's the status", "what's going on", or returns to a task/repo after a gap and wants an overview.

  Output: since last time / current state / next step. Max 12 lines. Grounded in actual git status/log/diff, not guesses.
disable-model-invocation: true
---

# Catch Up

Goal: user reads this once and knows exactly what happened, what state things are in, and what to do next — no need to dig through `git log` themselves.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms (JWT, Redis, API…) stay in English.
- Max 12 lines. Hard limit.
- Ground every line in evidence: check `git status`, `git log` (recent commits, last ~5-10 or since `$ARGUMENTS` if given a branch/date/commit), and `git diff` for uncommitted work before writing anything. Never guess at what changed.
- "Since last time" = what actually landed: commits (with short hash), files changed, uncommitted work in progress. Cite specifics, not "some fixes were made".
- "Current state" = is it clean, mid-change, broken, blocked? Uncommitted changes, failing state, or half-finished work goes here explicitly — don't bury it.
- "Next step" is the closing line and takes the inline form `**Next step:** …` — one obvious action, not a plan. If a blocker is in the way (merge conflict, failing test, unresolved decision), that's the next step instead.
- If there's no git repo or no meaningful history, say so directly rather than padding the response.
- No emoji.

## Output format

```
**Since last time**
- `[hash]` [commit subject]
- Uncommitted: [file] ([new / +N lines / deleted])

**Current state**
[clean / mid-change / blocked — one line, concrete]

**Next step:** [the one obvious action, or the blocker in the way]
```

## Example

`/catchup`

```
**Since last time**
- `6efbe87` Add clear-view and doubt skills, reviewer agent
- `e6fd00f` Bump version to 1.4.0
- Uncommitted: `skills/one-line/SKILL.md` (new, untracked), `README.md` (+12 lines)

**Current state**
Mid-change — new skill written and documented, nothing committed yet; no tests in this repo to run

**Next step:** commit the one-line skill plus the README and version bump as one change
```

## Anti-examples

Don't summarize commits into a theme ("various skill improvements"). The subject lines are
already short — quote them.

Don't report "Current state: clean" when there's untracked work sitting there. Untracked
counts.

Don't turn the next step into a roadmap. One action. If the user needs the plan, they'll ask
for it.

If `$ARGUMENTS` is given (e.g. a branch, date, or "since <commit>"), scope the git history to that instead of just recent commits.
