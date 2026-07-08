---
name: decision
description: |
  Surface the actual decision points in a task, plan, or problem — the specific choices that need to be made, the options for each, and a default recommendation.

  Trigger when the user wants decision points before diving in, or says "decision points", "what do I need to decide", "give me the decision points".

  Output: numbered decision points, each with options and a recommendation. Under 10 lines.
disable-model-invocation: true
---

# Decision Point

Goal: engineer sees exactly which choices are still open, what the options are, and which one to default to — without re-deriving the whole problem.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms stay in English.
- Only list decisions that are actually open — skip anything already implied or settled by context.
- Each decision point needs: the choice, 2-3 concrete options (not "it depends"), and a recommended default with a one-phrase reason.
- Order by impact: the decision that most constrains everything else comes first.
- Max 10 lines total. If there's only one real decision, just give that one.

## Output format

```
**Decision points**
1. [Choice to make] → [option A] vs [option B] (vs [option C]) → default: [X] because [reason]
2. [Choice to make] → [option A] vs [option B] → default: [X] because [reason]
```

If `$ARGUMENTS` is empty, ask: "Decision points for what?"
