---
name: clear-view
description: |
  Explain the current situation as one short plain-language paragraph — what we thought, what turned out to be true, where that leaves us — then the one decision to make.

  Trigger when the user says "clear view", "so where are we", "what's the situation", "I don't follow the current state", "what do I need to decide", or after a long investigation that needs to converge on one decision point.

  Different from tldr: tldr explains a thing in 5 clipped lines. clear-view tells the story of the situation in plain prose, with the context the user is missing, and ends on a decision.

  Output: one narrative paragraph + one bold decision line. No bullets, no headers. Max 8 lines.
disable-model-invocation: true
---

# Clear View

Goal: user reads one paragraph and understands the situation the way you understand it — then knows the one thing they have to decide.

This is not a summary of your work — it's building the user's mental model. They didn't watch
you run those tools; they don't have your context. Tell them what's going on the way you'd
explain it to a colleague who just walked in: plainly, in order, with the part that actually
matters up front.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms (JWT, Redis, API, eval) stay in English.
- Max 8 lines. Hard limit — one paragraph plus the decision line.
- **Prose, not structure.** No bullets, no section headers, no labels. If you're reaching for a bullet, the sentence wasn't finished.
- **Plain spoken language.** Write it the way you'd say it out loud. Short sentences. No noun stacks, no "additionally", no report voice.
- **Narrative order**: what we believed → what's actually true → what that means now. The context is the point; a bare fact list is what this skill exists to avoid.
- **Conclusions, not process.** "I ran X and found Y" → cut to "Y".
- **Numbers come in pairs.** "34 cases hit the classifier" is useless alone — "34 of 4972" drives a decision, a lone number doesn't.
- Say "we don't know yet" out loud for anything uncertain — don't paper over it with vague phrasing.
- The last line is bold and holds the decision: one recommendation, or one binary question. Never a menu of three.
- No diagrams, no analogies, no history of how we got here beyond what the situation needs.
- No emoji.

## Output format

```
[One paragraph, 3-5 sentences. What was assumed, what's actually true, where that leaves things. Plain spoken language.]

**[One line: the recommendation, or the single choice the user makes now.]**
```

## Example

`/clear-view`

```
我們一直在看的 eval 數字量錯了東西。這三週的準確率報告看起來是跑了 4972 筆案例，但實際上只有 34 筆真的進到 classifier，其他都在 cache 那層就直接回傳了。所以「準確率下降」不是模型變差，是 cache 命中率變高、真正被評分的樣本被壓到只剩一點點——我們追了兩天的 regression 其實不存在，模型本身從頭到尾沒被動過。至於關掉 cache 之後真實準確率是多少，現在還不知道。

**先把 cache 關掉重跑一次才有意義——你要跑完整 4972 筆，還是先抽 500 筆確認？**
```

## Anti-examples

Don't write "I changed 3 files and passed two acceptance gates" — that's your progress, not
their situation.

Don't slip back into structure. A paragraph with "First, … Second, … Third, …" is a bullet
list wearing a coat.

Don't write for a reader who already knows. "The cache short-circuit invalidated the scoring
path" assumes the thing you're supposed to be explaining.

Don't end on a menu of options. More than two means you haven't converged for the user yet.

If `$ARGUMENTS` is empty, brief on the current session's situation.
