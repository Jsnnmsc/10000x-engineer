---
name: decision
description: |
  Surface the actual decision points in a task, plan, or problem — the specific choices that need to be made, the options for each, and a default recommendation.

  Trigger when the user wants decision points before diving in, or says "decision points", "what do I need to decide", "give me the decision points".

  Output: numbered decision points, each with options and a default + bottom line. Max 10 lines.
disable-model-invocation: true
---

# Decision Point

Goal: engineer sees exactly which choices are still open, what the options are, and which one to default to — without re-deriving the whole problem.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms (JWT, Redis, API…) stay in English.
- Max 10 lines. Hard limit. That's 3 decision points at most.
- Only list decisions that are actually open — skip anything already implied or settled by context.
- Each decision point is a **bold numbered question**, with its options and default on the line below.
- Each one needs 2-3 concrete options (not "it depends") and a default with a short reason.
- Order by impact: the decision that most constrains everything else is #1.
- Bottom line = which one to settle first, or which one can be deferred. Not a recap of the defaults.
- If there's only one real decision, give that one and say so.
- No emoji.

## Output format

```
**1. [The choice, as a question]**
[option A] vs [option B] (vs [option C]) → default: [X], [short reason]

**2. [The choice, as a question]**
[option A] vs [option B] → default: [X], [short reason]

**Bottom line:** [which to settle first, or which can wait]
```

## Example

`/decision 幫 payment API 加上 retry`

```
**1. Where does the retry logic live?**
client vs middleware vs queue consumer → default: middleware, the one place all callers pass through

**2. How many retries, and spaced how?**
fixed count vs exponential backoff → default: exponential backoff capped at 3, failures are likely transient

**Bottom line:** decide #1 first — it determines whether #2 is even yours to make
```

## Anti-examples

Don't list a decision that context already settles. If the repo has one HTTP client and no
appetite for a second, "which HTTP client" is not an open decision.

Don't write "default: depends on your latency budget". That's the question again. Pick one
and name the assumption you picked it under.

Don't pad to three points. One real decision stated cleanly beats three where two are
theater.

If `$ARGUMENTS` is empty, ask: "Decision points for what?"
