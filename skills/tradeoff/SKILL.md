---
name: tradeoff
description: |
  Quick A-vs-B comparison for a technical choice — what each option costs, what it buys, and which one to pick.

  Trigger when the user asks "X vs Y", "should I use X or Y", "which is better here", "what's the tradeoff between X and Y".

  Output: gain/cost for each option + pick. Max 10 lines.
disable-model-invocation: true
---

# Tradeoff

Goal: engineer picks between two options in seconds, knowing exactly what each one costs.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms (JWT, Redis, API…) stay in English.
- Max 10 lines. Hard limit.
- Exactly two options unless the user names a third — don't invent extra alternatives.
- Each option gets one gain and one cost — not a full pros/cons list. Pick the gain and cost that would actually change the decision.
- `Gain:` and `Cost:` stay unbolded. The option name is the only bold thing in each block.
- The cost must be a real cost, not a disguised gain ("Cost: requires learning it" is filler).
- Pick = a real recommendation, not "it depends". If context is genuinely missing, name what's missing and pick anyway under a stated assumption.
- No emoji.

## Output format

```
**[Option A]**
Gain: [what you get]
Cost: [what you give up]

**[Option B]**
Gain: [what you get]
Cost: [what you give up]

**Pick:** [A or B] — [one-line reason]
```

## Example

`/tradeoff Postgres vs DynamoDB`

```
**Postgres**
Gain: joins, transactions, and one query language for everything
Cost: scaling past one big box means sharding work you own forever

**DynamoDB**
Gain: horizontal scale with near-zero ops
Cost: every access pattern must be designed up front into the keys

**Pick:** Postgres — your data is relational and you're nowhere near the scale that justifies DynamoDB's design tax
```

## Anti-examples

Don't list three gains and three costs per option. Six facts don't make a decision easier —
they make the reader do the ranking you were supposed to do.

Don't write a symmetric non-answer ("both are solid, depends on your needs"). If the two
options are genuinely tied, say what would break the tie and pick the reversible one.

Don't compare on dimensions the user can't act on. Benchmark numbers nobody will hit are
not a cost.

If `$ARGUMENTS` is empty, ask: "Which two options am I comparing?"
