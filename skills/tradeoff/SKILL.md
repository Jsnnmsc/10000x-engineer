---
name: tradeoff
description: |
  Quick A-vs-B comparison for a technical choice — what each option costs, what it buys, and which one to pick.

  Trigger when the user asks "X vs Y", "should I use X or Y", "which is better here", "what's the tradeoff between X and Y".

  Output: cost/benefit for each option + pick. Under 10 lines.
disable-model-invocation: true
---

# Tradeoff

Goal: engineer picks between two options in seconds, knowing exactly what each one costs.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms stay in English.
- Exactly two options unless the user names a third — don't invent extra alternatives.
- Each option gets one gain and one cost — not a full pros/cons list.
- The pick must be a real recommendation, not "it depends" — if context is genuinely missing, say what's missing instead.
- Max 10 lines total.

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

If `$ARGUMENTS` is empty, ask: "Which two options am I comparing?"
