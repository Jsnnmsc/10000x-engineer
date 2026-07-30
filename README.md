# 10000x Engineer

A [Claude Code](https://claude.ai/code) plugin that gives software engineers a set of focused, no-fluff tools for sizing up a change before you make it — in your language.

## Skills

| Skill | Invoke | Use when |
|---|---|---|
| **tldr** | `/10000x-engineer:tldr JWT` | You need the point in 10 seconds |
| **scope** | `/10000x-engineer:scope` + paste requirement | You need to know how big a change is before starting |
| **3w** | `/10000x-engineer:3w` + describe the tweak | You want where/what/why for a possible adjustment |
| **impact** | `/10000x-engineer:impact` + describe the change | You want to know what breaks or gets touched downstream |
| **tradeoff** | `/10000x-engineer:tradeoff X vs Y` | You're picking between two options and want the real cost of each |
| **decision** | `/10000x-engineer:decision` + describe the task | You want the open decision points before diving in |
| **catchup** | `/10000x-engineer:catchup` | You're returning to a task/repo and want to know what changed and what's next |
| **clear-view** | `/10000x-engineer:clear-view` | You've lost the thread mid-investigation and need the situation plus the decision |
| **doubt** | `/10000x-engineer:doubt` + describe the requirement | You suspect a requirement or design isn't actually needed and want it challenged |

## Examples

**`tldr`** — adapts to whether you need a definition or a decision:
```
/10000x-engineer:tldr JWT

**JWT**
A tamper-proof token that proves who you are — server signs it, client carries it.

- Use it when: stateless auth across services
- Skip it when: you need server-side session revocation
- Bottom line: use it, keep expiry short (15min)
```

**`scope`** — clear boundaries before work starts:
```
**In scope**
- User can reset password via email link
- Link expires after 1 hour

**Out of scope**
- SMS reset, OAuth re-auth
- Admin-triggered resets

**Unknowns**
- Does the link invalidate after first use?
- Which email service?

**Complexity:** S — straightforward auth flow, no novel logic
```

**`3w`** — where/what/why for a possible adjustment:
```
**Where**
`auth/session.ts`, token refresh middleware

**What**
Shorten access token expiry from 24h to 15min, add silent refresh

**Why**
Stolen tokens currently stay valid for a full day — shrinking the window limits exposure
```

**`impact`** — what a change actually touches:
```
**Directly affected**
- `users` table — column type change (int → bigint)

**Downstream affected**
- Any service joining on `users.id` — must handle wider type
- Analytics pipeline reading raw `users` table dumps

**Who notices**
- On-call, during migration window — brief write lock
- Data team — schema change breaks existing dashboards until updated
```

**`tradeoff`** — A vs B, no hedging:
```
**Postgres**
Gain: strong consistency, mature tooling
Cost: vertical scaling gets expensive past a point

**DynamoDB**
Gain: scales horizontally with near-zero ops
Cost: query flexibility is limited, no joins

**Pick:** Postgres — team's data has relational structure and scale isn't there yet
```

**`decision`** — the open choices before you start:
```
**Decision points**
1. Where does the retry logic live? → client vs middleware vs queue consumer → default: middleware because it's the one place all callers pass through
2. How many retries? → fixed count vs exponential backoff → default: exponential backoff because failures are likely transient
```

**`catchup`** — resume a task without digging through git yourself:
```
**Since last time**
- `47d4b6c` Rework skill set: remove error/risk/why, add 3w, decision, impact, tradeoff
- Uncommitted: `skills/catchup/SKILL.md` (new, untracked)

**Current state**
Mid-change — new skill written, not yet committed or added to README

**Next step**
Review the new SKILL.md, then commit
```

**`clear-view`** — the situation and the decision, nothing else:
```
**The eval numbers we've been trusting were measuring the wrong thing.**

- Facts: 4972 cases scored, but only 34 ever hit the real classifier — the rest short-circuited on a cache hit
- Scope: every accuracy number since the caching change; the model itself is untouched
- Surprise: the regression we chased for two days doesn't exist
- Bottom line: rerun the eval with cache disabled before touching the model — do you want the full 4972 or a 500 sample first?
```

**`doubt`** — one fewer thing to build, or a reason it survives:
```
**"Add a plugin system" — the claimed problem is that users need to extend the importer.**

- Real?: two users asked, both wanted the same CSV variant — nobody has asked for a second extension point
- Do nothing: those two stay blocked; everyone else is unaffected
- Smallest version: support that CSV variant directly, ~40 lines, no API to maintain
- Verdict: defer the plugin system until a third distinct extension request lands — ship the CSV variant now
```

## Agents

Cheaper-model subagents for delegating mechanical work out of an orchestrator's context — invoke via `@10000x-engineer:scout` / `@10000x-engineer:executor` / `@10000x-engineer:grunt` / `@10000x-engineer:reviewer`, or let Claude pick them up automatically.

| Agent | Model | Use when |
|---|---|---|
| **scout** | haiku | You need to know where something is before deciding what to do about it — finds files, symbols, call sites, patterns (read-only) |
| **executor** | sonnet | A step is already decided (what/where/how) and just needs implementing + verifying — writes/edits code to spec, runs build/tests |
| **grunt** | haiku | Pure mechanical legwork with one obviously-correct outcome — running commands, grepping/reading, mass find-replace, renaming |
| **reviewer** | sonnet | You want a cheap sanity pass on a diff — the few things that actually bite, explained in seconds, fix-or-ignore left to you |

They stop and report back rather than guessing when a step turns out to need a judgment call.

**`reviewer`** — findings you can act on without re-reading the diff:
```
**[api/orders.ts:88] Refund amount is read before the currency conversion runs.**
- Breaks when: any non-USD order refunds — customer gets the raw foreign-currency number
- Fix: move the `convert()` call above line 88
- Call: must fix — wrong money leaves the system

**[api/orders.ts:140] Retry loop has no cap.**
- Breaks when: the payment provider 500s persistently — the request hangs until timeout
- Fix: cap at 3 attempts
- Call: your call — provider rarely stays down

Start with the currency one; the retry can ride along later.
```

## Installation

Run these three commands inside Claude Code:

```
/plugin marketplace add Jsnnmsc/10000x-engineer
/plugin install 10000x-engineer@10000x-engineer
/reload-plugins
```

## License

[MIT](./LICENSE)
