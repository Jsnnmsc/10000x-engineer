---
name: 3w
description: |
  Break a possible adjustment or change down into Where, What, Why — where it applies, what actually changes, why it matters — plus what to do about it.

  Trigger when the user describes a possible tweak/adjustment and wants a quick breakdown, or says "3w", "where what why", "give me the 3w".

  Output: Where + What + Why + bottom line. Max 10 lines.
disable-model-invocation: true
---

# 3W

Goal: engineer sees exactly where a change lands, what it does, why it's worth doing, and what to do next — in one glance.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms (JWT, Redis, API…) stay in English.
- Max 10 lines. Hard limit.
- Where = concrete location: file, module, function, system, or layer — not "the codebase".
- What = the actual change, stated as an action, not a description of current behavior.
- Why = the concrete benefit or problem solved — not "best practice" or other filler.
- Bottom line = what to actually do now. It answers a different question than Why: Why is
  "is this worth doing", bottom line is "so what happens next". Use it for the sequencing
  trap, the prerequisite, or the reason to hold off — never to restate Why.
- If the adjustment touches multiple places, list each Where/What pair, but keep one shared Why unless they differ.
- No emoji.

## Output format

```
**Where**
[file/module/function/system]

**What**
[the concrete change, one action]

**Why**
[the concrete reason — problem solved or benefit gained]

**Bottom line:** [what to do now — the sequencing trap, prerequisite, or hold-off reason]
```

## Example

`/3w 把 access token 的有效期從 24 小時縮到 15 分鐘`

```
**Where**
`auth/session.ts`, token refresh middleware

**What**
Shorten access token expiry from 24h to 15min, add silent refresh

**Why**
Stolen tokens currently stay valid for a full day — shrinking the window limits exposure

**Bottom line:** do it, but ship silent refresh in the same deploy or every user gets logged out hourly
```

## Anti-examples

Don't write "Where: the auth system" — that's a restatement of the request. Name the file or
function someone would open.

Don't write "Why: it's a security best practice." Say what the current behavior actually
costs.

Don't let the bottom line echo Why ("Why: limits exposure" → "Bottom line: worth doing for
the security gain"). If you have nothing new to add, the bottom line is the prerequisite or
the order of operations.

If `$ARGUMENTS` is empty, ask: "3W of what adjustment?"
