---
name: tldr
description: |
  Quick plain-language brief — skip the explanation, get the point.

  Use when the user says "tldr", "quick version", "what is X", "should I use X", "just tell me", "give me the short version", or is clearly in a hurry.

  Different from one-line: one-line gives one sentence and stops. tldr adds the two facts that matter and a bottom line.

  Output: bold topic + one sentence + 2 adaptive bullets + bottom line. Max 5 lines. No diagrams, no analogies, no history.
disable-model-invocation: true
---

# TL;DR

Goal: user reads this in 10 seconds and knows what to do.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms (JWT, Redis, API…) stay in English.
- Max 5 lines. Hard limit. That is exactly: headline, one sentence, two bullets, bottom line.
- **The headline is the topic, not the question.** Turn whatever the user typed into a short noun phrase — `**JWT**`, `**one-line 的粗體**`. Never echo their raw question back as the heading.
- No section headers — at this length they'd cost more lines than they buy.
- No diagrams, no analogies, no history.
- Every word earns its place.
- No emoji.

## Output format

```
**[Topic as a short noun phrase]**
[One sentence. What it is or does, in plain language.]

- [First of the two things that matter]
- [Second of the two things that matter]
- **Bottom line:** [direct recommendation or verdict]
```

## Pick the two middle bullets from the question

- **Definition** ("what is X", "explain X briefly") → the two key facts a user needs to not misuse it
- **Decision** ("should I use X", "X vs Y", "is X worth it") → `Use it when: [≤8 words]` / `Skip it when: [≤8 words]`
- **State of something** ("is X done", "does X do Y") → the two observations that settle it

The bottom line is never optional. For a definition it's the one practical takeaway, not a
restatement of the sentence above.

## Examples

`/tldr JWT`
```
**JWT**
A signed token the client carries so the server can verify who they are without storing a session.

- Use it when: stateless auth across services
- Skip it when: you need instant server-side revocation
- **Bottom line:** use it, keep expiry at 15min
```

`/tldr Redis 拿來幹嘛`
```
**Redis**
把讀取頻繁但變動不多的資料放在記憶體裡，避免每次都打 database。

- 讀取延遲從幾十 ms 降到 1ms 以下
- 資料會過期、也可能掉，不能當唯一來源
- **Bottom line:** 當 cache 用，永遠假設它是空的也要能跑
```

## Anti-examples

Don't write `**一句話解釋 JWT 是什麼意思**` as the headline — that's the user's question,
not the topic. It should be `**JWT**`.

Don't stretch to four bullets because the topic feels rich. If two facts can't carry it, the
user asked for the wrong skill — answer at this length anyway.

Don't let the bottom line repeat the opening sentence in different words. It has to tell
them what to *do*.

If `$ARGUMENTS` is empty, ask: "Quick brief on what?"
