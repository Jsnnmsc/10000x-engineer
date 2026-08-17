---
name: doubt
description: |
  Challenge whether a requirement, feature, or design is needed at all — before any effort goes into how to build it.

  Trigger when the user says "doubt", "do we actually need this", "is this necessary", "push back on this", "am I overbuilding", or is drowning in options and wants the list cut down instead of expanded.

  Different from tradeoff and decision: those help you pick between options, this one questions whether the thing should exist and kills options rather than adding them.

  Output: the claimed problem, a plain-language paragraph on whether it's real, then do-nothing / smallest-version / one verdict. Max 10 lines.
disable-model-invocation: true
---

# Doubt

Goal: user walks away with one fewer thing to build, or a clear reason why this one survives.

Your default posture is skeptical. Most requirements are a proposed solution wearing the
costume of a problem — your job is to find the problem underneath and check whether it's
actually hurting anyone today.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms (JWT, Redis, API…) stay in English.
- Max 10 lines. Hard limit.
- **Attack the requirement, not the user.** Skepticism is about the idea; be blunt, not snide.
- The headline restates the requirement as the problem it claims to solve — in quotes, so the
  user sees their own words held up for inspection.
- **The "is it real" part is a paragraph, not a bullet.** Plain spoken language: what was
  asked for, what the people asking actually wanted, and what evidence is missing. This is
  where the context lives, so tell it as a short story.
- **Do nothing and Smallest version stay as bold headers.** They're the two things a reader
  skips when they've already decided to build it, so they get their own visual stop.
- Always state the do-nothing cost explicitly. If nothing bad happens when you skip it, say so plainly.
- **Never end on a menu.** This skill removes options, it doesn't produce them. Exactly one verdict.
- If the requirement survives, say so directly — doubt that can never clear the thing is theater.
- Distinguish "not needed" from "not needed yet". A trigger condition ("revisit when X") is a valid verdict.
- No diagrams, no analogies. No emoji.

## Output format

```
**["The requirement"] — the claimed problem is [what it says it solves].**

[One paragraph, 2-3 sentences. Who asked, what they actually wanted, what evidence is
missing. Plain spoken language.]

**Do nothing**
[What breaks if this never gets built. "Nothing" is a valid answer — say it plainly.]

**Smallest version**
[The cheapest thing that covers the real case, with a rough size. Or "none" if there isn't one.]

**Verdict:** [kill / defer until [trigger] / build the smallest version / build it as specified — one line, no alternatives]
```

## Example

`/doubt 幫 importer 加一個 plugin system`

```
**「加一個 plugin system」——聲稱要解決的問題是使用者需要擴充 importer。**

有兩個人提過這件事，但去看他們真正想要的，兩次都是同一件事：多支援一種 CSV 格式。沒有人
提出第二種擴充需求，所以「使用者需要擴充性」這個說法，證據撐不起來。

**什麼都不做**
那兩個人繼續卡在 CSV 上，產品裡沒有其他東西在等這個。

**最小版本**
直接在 importer 裡支援那個 CSV 格式，大約 40 行，不用對外 API，之後沒有維護成本。

**Verdict:** 先把 CSV 格式做掉，plugin system 等第三個不同的擴充需求出現再談。
```

## Anti-examples

Don't write "there are a few approaches, depending on your priorities" — that's the option
flood this skill exists to stop.

Don't manufacture doubt about something clearly load-bearing. If it's needed, the answer is
"build it as specified" plus the one sentence that settles it.

Don't turn the opening paragraph back into bullets. It's the story of who asked and what they
really wanted; a fragment list loses exactly the part that changes the reader's mind.

Don't soften "Do nothing" into a risk hedge ("there may be some user friction"). Name who
stays blocked, or say nobody does.

If `$ARGUMENTS` is empty, ask: "Doubt what — which requirement or design?"
