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

## Installation

Run these three commands inside Claude Code:

```
/plugin marketplace add Jsnnmsc/10000x-engineer
/plugin install 10000x-engineer@10000x-engineer
/reload-plugins
```

## License

[MIT](./LICENSE)
