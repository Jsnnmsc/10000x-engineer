---
name: clear-view
description: |
  Compress the current situation into a decision-ready brief — what's actually wrong, what's known, what's still unknown, what you have to decide now.

  Trigger when the user says "clear view", "so where are we", "what's the situation", "I don't follow the current state", "what do I need to decide", or after a long investigation that needs to converge on one decision point.

  Different from tldr: tldr explains a thing, clear-view explains the situation and forces a decision.

  Output: one opening line + max 6 bullets.
disable-model-invocation: true
---

# Clear View

Goal: user reads it in 20 seconds and knows where things are stuck and what they have to decide.

This is not a summary of your work — it's building the user's mental model of the
situation. They didn't watch you run those tools; they don't have your context. Give
them the missing piece, not a log of what you did.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms (JWT, Redis, API, eval) stay in English.
- Max 6 bullets + 1 opening line. Hard limit.
- **Conclusions, not process.** "I ran X and found Y" → cut to "Y".
- **Numbers come in pairs.** "34 fatal false positives" is useless alone — give "34 → 2" or "34/4972". A single number can't drive a decision; a contrast can.
- No diagrams, no analogies, no history. The question is about now, not how we got here.
- Say "don't know yet" out loud for anything uncertain — don't paper over it with vague phrasing.
- No emoji.

## Output format

```
**[One sentence naming the real problem. Not the task description — the pain point.]**

- **Facts**: the key findings that currently hold (1-2, with contrast numbers)
- **Scope**: how big the problem is / what it touches — or how small it's already been narrowed to
- **Surprise**: where reality diverged from the original assumption (skip if there isn't one)
- **Bottom line**: one direct recommendation + the one choice the user makes now
```

## Anti-examples

Don't write "I changed 3 files and passed two acceptance gates" — that's your progress,
not their situation. Write "the original validation numbers were fake, the real figure is X,
one extra rule cleans it up".

Don't list more than 2 options. More than 2 means you haven't converged for the user yet.

If `$ARGUMENTS` is empty, brief on the current session's situation.
