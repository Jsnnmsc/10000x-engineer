---
name: impact
description: |
  Surface the blast radius of a change — which modules, services, users, or data get touched, directly or downstream.

  Trigger when the user asks "what does this affect", "blast radius", "who gets touched by this", "impact of this change", or pastes a change and wants to know what depends on it.

  Output: directly affected + downstream affected + who notices. Under 10 lines.
disable-model-invocation: true
---

# Impact

Goal: engineer knows who and what gets touched by a change before it ships — not what could break, just what's connected.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, reply in Chinese. Technical terms stay in English.
- Directly affected = code/data/config that the change literally touches.
- Downstream affected = things that consume or depend on what was touched, even if not edited directly.
- Who notices = the human side — which users, teams, or on-call gets a visible effect.
- If a dependency is uncertain, mark it "uncertain — verify" rather than guessing.
- Max 10 lines total.

## Output format

```
**Directly affected**
- [module/file/service]

**Downstream affected**
- [what depends on it, and how]

**Who notices**
- [users / team / on-call — what they'd see]
```

If `$ARGUMENTS` is empty, ask: "Impact of what change?"
