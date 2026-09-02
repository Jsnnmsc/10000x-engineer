---
name: first-principle
description: |
  Strip a problem down to what's actually true underneath — separate inherited convention from real constraint, then restate the problem as it really is.

  Trigger when the user says "first principle", "第一性原理", "本質是什麼", "從頭想一次", "從根本分析", "這問題的根源", "我們是不是搞錯問題了", "這個設計合理嗎", "why are we doing it this way", or is about to solve a problem the way it has always been solved.

  Different from tradeoff and decision: those work inside the problem as stated. This one checks whether the problem is stated right, and hands back a different one if it isn't.

  Output: the stated problem, the assumptions under it split into convention vs unverified, the facts that survive, and one line naming the real problem. Max 12 lines.
disable-model-invocation: true
---

# First Principle

Goal: user walks away solving a different problem than the one they walked in with — or knowing
their original framing survived inspection.

The move is not "ask why five times". It's this: take the current approach apart into separate
claims, and sort each one into **inherited convention** or **fact that can't be removed**. Throw
out the conventions, look at what's left, and see what problem those facts actually describe.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms (CI, JWT, Redis, API…) stay in English.
- Max 12 lines. Hard limit.
- **Every assumption carries one of two labels, never a third:**
  - `慣例 / convention` — say where it came from. Who brought it in, what it was copied from, or when it was decided and under what conditions.
  - `待查 / unverified` — name the one number, log, or metric that settles it. Not "we should investigate" — which thing to go look at.
- If you can't source it and can't say how to check it, don't list it. An assumption without either is a guess wearing a label.
- **The input is usually the user's own read of the problem, not a one-line proposal.** Compress it into one sentence for the stated-problem line. Make that compression faithful and specific — if they'd object to it, that objection is itself the finding, so don't hide behind a generic restatement.
- **Go after what they didn't say.** The assumptions that matter are the ones so obvious to the writer that they never got typed. List those first. If every assumption you list is one they explicitly stated, you audited their text instead of their thinking.
- **Agreement is the default failure here.** A well-argued paragraph reads as correct; that's the trap. Before you write "the framing was already right", confirm you found at least one unstated assumption and that it held. That verdict is for reasoning you attacked and couldn't break, never for reasoning you didn't attack.
- **One load-bearing claim.** If the input carries several, take the one that makes the rest irrelevant if it's wrong. Don't walk the paragraph line by line.
- **Ground truth test.** A fact goes in only if it passes all three: it can't be decomposed further, it's provably true rather than widely believed, and violating it definitely breaks something.
- **Don't over-reduce.** "It's all just CPU instructions" is true and useless. Stop at the last layer where removing the fact would change the answer.
- **Look past technical assumptions.** Check the business ones (is that deadline or requirement actually fixed?), the resource ones (is that constraint real or assumed?), and the historical ones (why was this decided originally, and does that condition still hold?). A list of only technical assumptions means you stopped early.
- Phrases that mark a convention, not a constraint: "we've always done it this way", "it's the industry standard", "everyone uses X", "that's too simple to work", "Company X does it like this".
- For a borrowed pattern, ask what problem the source was actually solving and which of their constraints you don't have. "Netflix does it" is not a fact about your system.
- **Don't give the solution.** Name the real problem and stop — `decision` and `tradeoff` take it from there.
- The 本質 line must say something different from the stated problem. If the framing was already right, say that plainly in one line and give the reason — a reframe that has to be manufactured is worse than none.
- No tables, no diagrams, no analogies. No emoji.

## Output format

```
**[Your read]:** [their understanding compressed to one faithful sentence, in their words]

**[Assumptions removed]**
- [assumption] — 慣例: [where it came from]
- [assumption] — 待查: [the one number or log that settles it]

**[Facts that survive]**
- [fact that passes the ground truth test]
- [fact]

**[Essence]:** [one line — the real problem, different from the stated one]
```

## Example

`/first-principle 我們 CI 要跑 40 分鐘，工程師都在等。我的理解是 test 太多了，機器不夠，所以應該加 runner 平行化，把時間壓到 10 分鐘以內`

```
**你的理解：**CI 慢是因為 test 量超過機器算力，所以加 runner 平行化就能把 40 分鐘壓到 10 分鐘。

**拆掉的假設**
- 每次 commit 都要跑完整套 test — 慣例：三年前只有 200 個 test 時定的規則，之後沒人重新檢討
- 加機器就會變快 — 慣例：把 CI 當算力問題，但總時數沒變少，開發者等的也不是總時數
- test 拆得開 — 待查：去看有多少 test 共用同一個 DB fixture，超過三成就平行不動

**拆不掉的事實**
- 一次 commit 平均只碰 3 個檔案
- 開發者要的是「我壞了沒」，不是「全部跑完了沒」
- 合併進主幹前終究要全綠

**本質：**問題不是 CI 跑太久，是壞掉的訊號要 40 分鐘才到——這兩件事的解法不一樣。
```

## Anti-examples

Don't list an assumption with no origin and no way to check it. "Maybe we don't need strong
consistency" is a thought, not a finding — say where the requirement came from, or which query
pattern proves it.

Don't put a preference in the facts section. "The team prefers Go" fails the ground truth test:
it can be decomposed, it isn't provably true, and violating it breaks nothing.

Don't manufacture a reframe. If the stated problem is the real one, "這題本來就問對了——[one
line why]" is the honest answer and it's allowed to be the whole output.

Don't slide into the fix. "So we should build a test impact analyzer" is `decision`'s job; this
skill stops at naming the problem.

Don't produce a report. Five sections with tables and a reasoning chain is a document nobody
reads — twelve lines that change the reader's mind is the deliverable.

If `$ARGUMENTS` is empty, ask: "要從第一性原理拆哪件事？" (in the user's language)
