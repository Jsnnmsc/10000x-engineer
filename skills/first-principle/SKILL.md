---
name: first-principle
description: |
  Find the actual problem — take a question, a symptom, or a current approach down to what's provably true (numbers, limits, measurements you can check), separate that from inherited practice, and name what's really wrong plus what any fix has to satisfy.

  Trigger when the user says "first principle", "第一性原理", "本質是什麼", "實際問題是什麼", "問題點在哪", "從根本分析", "這問題的根源", "我們是不是搞錯問題了", "這個設計合理嗎", "why are we doing it this way", or brings a problem that keeps being solved the way it has always been solved.

  Different from tradeoff and decision: those work inside the problem as stated, with the options already on the table. This one starts from what's true and hands back the actual problem plus the conditions any option has to meet.

  Output: what's wanted, the ground truths with their numbers, which parts of the current approach are convention, the actual problem, and what any solution must satisfy. Max 12 lines.
disable-model-invocation: true
---

# First Principle

Goal: the user stops optimizing the stated problem and sees the actual one — with enough ground
under it that the next move is obvious.

Not "ask why five times". The move: find what is provably true about the situation, throw out
what is only current practice, and read the problem off what's left. Reason up from the facts,
not down from the approach that happens to exist.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms (CI, JWT, Redis, API…) stay in English.
- Max 12 lines. Hard limit. Blank lines between sections and the single closing line don't count — everything else does.
- **The user does not have to bring a read of the problem.** A bare question, a symptom, a plan, or a chunk of code is the normal input, and any of them is enough to start. If they do state their own read, it's one more claim to test — not the subject of the answer.
- **Every fact carries what makes it a fact, on the line itself** — the number, measurement, log line, or hard limit behind it. What the tools in front of you can check, check before writing it: the measured number beats a sentence telling the user where to look. A line that is reasoning rather than measurement — arithmetic, a definition, a constraint you're inferring from how the system works — is marked `reasoning`. A claim you'd have to look up and can't reach from here is marked `未查 / unverified`, naming the file or number that settles it. An unchecked claim written in a fact's clothes is the one thing this skill cannot ship.
- **The test for convention is mechanical: remove it and see what breaks.** Nothing breaks → convention. Something breaks → fact, and say what breaks.
- **Provenance is evidence, or it's `untraced` (查不到).** `from:` names something reachable — the request's own wording, a `git log -S` hit, a code comment, a config value. "Common practice", "big repos do this", and "we've always done it" are not origins; say so and move on. An invented origin is worse than an admitted gap — that's the guess-wearing-a-label this skill exists to kill.
- **Audit the approach, not the user's head.** The conventions are what the current approach silently takes for granted, read out of the code, the plan, or the request. Never guess at what the user is thinking.
- **A fact survives only if it can't be decomposed further and violating it definitely breaks something.** "The team prefers Go" is a preference. "It's all just CPU instructions" decomposes and helps nobody — stop at the last layer where removing it changes the answer.
- **Look past the technical.** Business (is that deadline a requirement or a habit?), resource (is that constraint real, or assumed?), historical (why was this decided, and does that condition still hold?). A list of only technical facts means you stopped early.
- **The actual problem is the point of the skill.** One line, and it has to explain why the current approach can't fix the symptom. Different from the stated problem — or, if the framing was already right, the same problem with the reason it survived spelled out. A reframe that has to be manufactured is worse than none.
- **Then say what any solution must satisfy.** One to three conditions, each testable against a concrete option. Don't pick the option — `decision` and `tradeoff` do that. If the facts allow only one direction, say so and name the fact that forces it: that's a verdict the facts made, not one you picked.
- **One closing line is allowed, and only one — and it has a shape:** `[what you couldn't check] — [the file or number that settles it]`. Option costs, trade-offs, and "do this next" belong to `tradeoff` and `decision`; the moment this line starts weighing options, the skill has handed over a recommendation it wasn't asked for.
- No tables, no diagrams, no analogies. No emoji.

## Output format

```
**Wanted:** [the outcome actually wanted, one line — quoted or read out of the request or the code; if you inferred it, say so]

**Ground truths**
- [fact] — [the number, measurement, or hard limit that makes it a fact]

**Convention in the current approach**
- [what it takes for granted] — from: [where it came from] · remove it and: [what breaks, usually nothing]

**The actual problem:** [one line — what's really wrong, in a form that explains why the current approach doesn't fix it]

**Any solution must:** [one to three conditions an option can be tested against]
```

At most one closing line after that, in the shape `[what you couldn't check] — [what settles
it]`. Nothing else.

## Example

`/first-principle CI 每次要跑 40 分鐘，工程師都在等，是不是該加 runner 平行化`

```
**要的是：**壞掉的 commit 在開發者還記得自己改了什麼之前就被知道。

**底層事實**
- 過去 30 天 main 每小時進 12 個 commit，平均碰 3 個檔案（git log）
- 合併前必須全綠，沒有例外（CI required check 只有這一個）
- 4972 個 test 裡 3800 個共用同一個 DB fixture（grep setup 呼叫點）→ 平行度上限約 4 倍

**現行做法裡的慣例**
- 每次 commit 跑完整套 — 來自三年前 200 個 test 時的規則 · 拿掉會怎樣：不會壞，required check 還在
- 把 CI 當算力問題 — 來自「機器不夠」這個直覺 · 拿掉會怎樣：40 分鐘裡絕大多數是等待，不是運算

**實際的問題點：**不是 CI 太慢，是「你壞了沒」的答案 40 分鐘後才到——而在 12 commit/小時的節奏下，他早就換任務了。

**任何解法必須：**① 從 push 到壞掉訊號 ≤5 分鐘；② 只跑受影響的 test（3800 個共用 fixture 的 test 平行不到夠快）；③ 全綠仍然是最終關卡，只是不必每次 push 都付這個成本。
```

## Anti-examples

Don't guess at what the user thinks. If a convention can't be read out of the code, the plan, or
the request, it isn't one you found — it's one you invented, and the user will spend the rest of
the answer distrusting you.

Don't write a fact without its number — or, if what you have is reasoning rather than measurement,
without saying so. "Requests are slow" is an observation. "p95 is 400ms and 380ms of it is one
query" is a fact you can act on.

Don't list only technical conventions. If nothing about the deadline, the resource limit, or the
history made it into the list, you stopped at the first layer that came to mind.

Don't manufacture a reframe. If the stated problem is the real one, that's the answer — write it
on the actual-problem line with the reason it survived, and leave out any section that has nothing
to put in it.

Don't pick the solution. "所以應該做 X" is `decision`'s job — the last required line is the
conditions X has to satisfy, which is what makes it checkable instead of persuasive.

Don't produce a report. A page of analysis with a table is a document nobody reads; twelve lines
that change what the user does next is the deliverable.

If no request was supplied, ask: "First principles on what?"
