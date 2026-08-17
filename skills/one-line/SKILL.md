---
name: one-line
description: |
  Explain it in exactly one sentence — nothing else.

  Trigger when the user says "one line", "one sentence", "in a sentence", "一句話", "explain in one line", or asks what something is and clearly wants no more than that.

  Different from tldr: tldr gets 5 lines and can add key facts or a verdict. one-line gets one sentence and stops.

  Output: one bold sentence. No bullets, no heading, no follow-up offer.
disable-model-invocation: true
---

# One Line

Goal: user reads one sentence and has the right mental model.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms (JWT, Redis, API…) stay in English.
- **Max 1 sentence. Hard limit.** No second sentence, no bullets, no heading, no code block, no "let me know if you want more".
- The sentence is **bold** — wrap the whole thing in `**`, punctuation included. Nothing sits outside the bold.
- Under 25 words. If it doesn't fit, you haven't found the core yet — cut the qualifiers, not the meaning.
- No section headers and no closing verdict line — the sentence *is* the verdict.
- Say what it *does* or *is for*, not what category it belongs to. "A tamper-proof token that proves who you are" beats "an open standard for representing claims".
- No analogies unless the analogy *is* the shortest true explanation.
- No hedging ("generally", "basically", "essentially", "kind of"). Commit.
- No emoji.

## Output format

```
**[One sentence.]**
```

That's the whole output.

## Examples

`/one-line JWT`
```
**A signed token the client carries so the server can verify who they are without storing a session.**
```

`/one-line 為什麼要用 Redis`
```
**把讀取頻繁但變動不多的資料放在記憶體裡，避免每次都打 database。**
```

`/one-line this function`
```
**Retries the payment call with exponential backoff, giving up after three failures.**
```

## Anti-examples

Don't write "JWT is a JSON Web Token. It's used for auth." — that's two sentences and the
first one says nothing.

Don't write "A signed token for auth — see the docs for details." Pointing elsewhere is not
an explanation.

If `$ARGUMENTS` is empty, ask: "One line on what?"
