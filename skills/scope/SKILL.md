---
name: scope
description: |
  Turn a vague feature request or task description into a clear scope — what's in, what's out, what's unknown, and how big it is.

  Trigger when the user pastes a requirement, feature request, ticket description, or says "scope this", "what does this involve", "how big is this", "break this down".

  Output: in scope / out of scope / unknowns / complexity estimate. Max 15 lines.
disable-model-invocation: true
---

# Scope

Goal: turn a fuzzy requirement into a clear boundary so the team can start without guessing.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms (JWT, Redis, API…) stay in English.
- Max 15 lines. Hard limit.
- In scope = what must be built for this to be "done".
- Out of scope = what people might assume is included but isn't. Be explicit.
- Unknowns = questions that must be answered before work starts, not nice-to-know details.
- Complexity uses T-shirt sizing: XS (hours) / S (1-2 days) / M (1 week) / L (2-4 weeks) / XL (month+).
- If the input is too vague to scope, list the clarifying questions instead.
- No emoji.

## Output format

```
**In scope**
- [What must be built]
- [What must be built]

**Out of scope**
- [What to explicitly exclude]
- [What to explicitly exclude]

**Unknowns**
- [Question that blocks starting]
- [Question that blocks starting]

**Complexity:** [XS / S / M / L / XL] — [one-line reason]
```

## Example

`/scope 使用者可以用 email 連結重設密碼`

```
**In scope**
- Request reset → send email with signed link
- Link expires after 1 hour, single use
- New password replaces old, existing sessions revoked

**Out of scope**
- SMS reset, OAuth re-auth
- Admin-triggered resets
- Password strength policy changes

**Unknowns**
- Which email service — existing SES setup or new?
- Should the old password be rejected as the new one?

**Complexity:** S — standard auth flow, no novel logic, one new table column
```

## Anti-examples

Don't put implementation steps in "In scope" — "add a `reset_token` column" is how, not what.
Scope is stated as user-visible outcomes.

Don't fill "Out of scope" with things nobody would have assumed. "Not building a blockchain"
is noise; "no SMS reset" earns its line because someone will ask.

Don't hedge the complexity with a range ("S–M"). Pick one and say what would move it.

If `$ARGUMENTS` is empty, ask: "Paste the requirement or describe the task."
