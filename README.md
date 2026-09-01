# 10000x Engineer

A [Claude Code](https://claude.ai/code) plugin that gives software engineers a set of focused, no-fluff tools for sizing up a change before you make it — in your language.

## Skills

| Skill | Invoke | Use when |
|---|---|---|
| **one-line** | `/10000x-engineer:one-line JWT` | You want one sentence and nothing else |
| **tldr** | `/10000x-engineer:tldr JWT` | You need the point in 10 seconds |
| **scope** | `/10000x-engineer:scope` + paste requirement | You need to know how big a change is before starting |
| **3w** | `/10000x-engineer:3w` + describe the tweak | You want where/what/why for a possible adjustment |
| **impact** | `/10000x-engineer:impact` + describe the change | You want to know what breaks or gets touched downstream |
| **tradeoff** | `/10000x-engineer:tradeoff X vs Y` | You're picking between two options and want the real cost of each |
| **decision** | `/10000x-engineer:decision` + describe the task | You want the open decision points before diving in |
| **catchup** | `/10000x-engineer:catchup` | You're returning to a task/repo and want to know what changed and what's next |
| **clear-view** | `/10000x-engineer:clear-view` | You've lost the thread mid-investigation and need the situation plus the decision |
| **first-principle** | `/10000x-engineer:first-principle` + describe the approach | You want to know whether you're solving the right problem before you solve it |

## Examples

**`one-line`** — one sentence, then it stops:
```
/10000x-engineer:one-line JWT

**A signed token the client carries so the server can verify who they are without storing a session.**
```

**`tldr`** — the point plus the two facts that matter:
```
/10000x-engineer:tldr JWT

**JWT**
A signed token the client carries so the server can verify who they are without storing a session.

- Use it when: stateless auth across services
- Skip it when: you need instant server-side revocation
- **Bottom line:** use it, keep expiry at 15min
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

**Complexity:** S — standard auth flow, no novel logic, one new table column
```

**`3w`** — where/what/why for a possible adjustment:
```
**Where**
`auth/session.ts`, token refresh middleware

**What**
Shorten access token expiry from 24h to 15min, add silent refresh

**Why**
Stolen tokens currently stay valid for a full day — shrinking the window limits exposure

**Bottom line:** do it, but ship silent refresh in the same deploy or every user gets logged out hourly
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

**Bottom line:** tell the data team before you start, not after — their nightly load is the one thing that breaks silently
```

**`tradeoff`** — A vs B, no hedging:
```
**Postgres**
Gain: joins, transactions, and one query language for everything
Cost: scaling past one big box means sharding work you own forever

**DynamoDB**
Gain: horizontal scale with near-zero ops
Cost: every access pattern must be designed up front into the keys

**Pick:** Postgres — your data is relational and you're nowhere near the scale that justifies DynamoDB's design tax
```

**`decision`** — the open choices before you start:
```
**1. Where does the retry logic live?**
client vs middleware vs queue consumer → default: middleware, the one place all callers pass through

**2. How many retries, and spaced how?**
fixed count vs exponential backoff → default: exponential backoff capped at 3, failures are likely transient

**Bottom line:** decide #1 first — it determines whether #2 is even yours to make
```

**`catchup`** — resume a task without digging through git yourself:
```
**Since last time**
- `47d4b6c` Rework skill set: remove error/risk/why, add 3w, decision, impact, tradeoff
- Uncommitted: `skills/catchup/SKILL.md` (new, untracked)

**Current state**
Mid-change — new skill written, not yet committed or added to README

**Next step:** review the new SKILL.md, then commit
```

**`clear-view`** — the situation told plainly, then the decision:
```
The eval numbers we've been trusting were measuring the wrong thing. Those accuracy
reports look like 4972 cases, but only 34 of them ever reached the real classifier —
everything else short-circuited on a cache hit. So the "accuracy drop" isn't the model
getting worse, it's the cache hit rate going up and squeezing the scored sample down to
almost nothing. The regression we chased for two days doesn't exist, and the model itself
was never touched. What the real accuracy is with the cache off, we don't know yet.

**Rerun with the cache disabled before touching the model — full 4972, or a 500-case
sample first?**
```

**`first-principle`** — the problem restated as it actually is:
```
**Stated problem:** CI takes 40 minutes, so let's parallelize across more machines.

**Assumptions removed**
- Every commit runs the full suite — convention: a rule set three years ago at 200 tests, never revisited
- More machines means faster — convention: treats CI as a compute problem, but total time doesn't drop and that isn't what developers wait on
- The suite splits cleanly — unverified: check how many tests share one DB fixture; past a third it won't parallelize

**Facts that survive**
- A commit touches 3 files on average
- Developers want "did I break it", not "did everything finish"
- Everything must be green before it merges to trunk

**Essence:** the problem isn't that CI is slow, it's that a breakage takes 40 minutes to surface — those two have different fixes.
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
