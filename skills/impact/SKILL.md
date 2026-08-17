---
name: impact
description: |
  Surface the blast radius of a change — which modules, services, users, or data get touched, directly or downstream — plus what to do about it.

  Trigger when the user asks "what does this affect", "blast radius", "who gets touched by this", "impact of this change", or pastes a change and wants to know what depends on it.

  Output: directly affected + downstream affected + who notices + bottom line. Max 10 lines.
disable-model-invocation: true
---

# Impact

Goal: engineer knows who and what gets touched by a change before it ships — not what could break, just what's connected.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms (JWT, Redis, API…) stay in English.
- Max 10 lines. Hard limit.
- Directly affected = code/data/config that the change literally touches.
- Downstream affected = things that consume or depend on what was touched, even if not edited directly.
- Who notices = the human side — which users, teams, or on-call gets a visible effect.
- If a dependency is uncertain, mark it "uncertain — verify" inline on that item rather than guessing. Don't give it its own section.
- Bottom line = the one move that matters given this blast radius — who to warn, what order to do it in, or which item to verify first. Not a summary of the sections above.
- No emoji.

## Output format

```
**Directly affected**
- [module/file/service — what changes about it]

**Downstream affected**
- [what depends on it, and how]

**Who notices**
- [users / team / on-call — what they'd see, and when]

**Bottom line:** [the one move that matters — who to warn, what order, what to verify first]
```

## Example

`/impact users.id 從 int 改成 bigint`

```
**Directly affected**
- `users` table — column type change (int → bigint)
- `models/user.py` — ORM column type must match or writes fail silently

**Downstream affected**
- Any service joining on `users.id` — 4 services, all must handle the wider type
- Analytics pipeline reading raw `users` dumps — schema mismatch breaks nightly load
- Uncertain — verify: the legacy PHP admin panel may hardcode int parsing

**Who notices**
- On-call, during the migration window — brief write lock on `users`
- Data team, next morning — dashboards break until the pipeline schema is updated

**Bottom line:** tell the data team before you start, not after — their nightly load is the one thing that breaks silently
```

## Anti-examples

Don't list what *could* break in theory. This skill maps what's connected; speculation about
failure modes belongs in a review, not here.

Don't write "Who notices: users" with nothing after it. Name what they'd actually see and
when — a visible effect or nothing.

Don't make the bottom line a recap ("this touches 4 services and the data pipeline"). They
just read that. Give them the move.

If `$ARGUMENTS` is empty, ask: "Impact of what change?"
