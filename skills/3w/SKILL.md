---
name: 3w
description: |
  Break a possible adjustment or change down into Where, What, Why — where it applies, what actually changes, why it matters.

  Trigger when the user describes a possible tweak/adjustment and wants a quick breakdown, or says "3w", "where what why", "give me the 3w".

  Output: Where + What + Why. Under 8 lines.
disable-model-invocation: true
---

# 3W

Goal: engineer sees exactly where a change lands, what it does, and why it's worth doing — in one glance.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms stay in English.
- Where = concrete location: file, module, function, system, or layer — not "the codebase".
- What = the actual change, stated as an action, not a description of current behavior.
- Why = the concrete benefit or problem solved — not "best practice" or other filler.
- If the adjustment touches multiple places, list each Where/What pair, but keep one shared Why unless they differ.
- Max 8 lines total.

## Output format

```
**Where**
[file/module/function/system]

**What**
[the concrete change, one action]

**Why**
[the concrete reason — problem solved or benefit gained]
```

If `$ARGUMENTS` is empty, ask: "3W of what adjustment?"
