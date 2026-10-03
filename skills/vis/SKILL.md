---
name: vis
description: |
  Draw it instead of describing it — one monospace diagram in the terminal: flow, tree, layers, timeline, table, bar chart, or state machine.

  Trigger when the user says "vis", "visualize this", "draw it", "diagram this", "show me the flow", "畫出來", "畫給我看", "圖解", or wants structure they can see rather than prose they have to read.

  Different from tldr and clear-view: those answer in words. vis answers with a drawing and stops.

  Output: optional bold title + one fenced code block, ≤80 columns, ≤20 rows, Unicode box drawing. Text in the session only — no mermaid, no HTML, no images, no files, no artifacts unless you ask for one.
disable-model-invocation: true
---

# VIS

Goal: the user looks at one drawing and understands the structure. No sentence needed.

Text only, inside the session. No mermaid, no HTML, no SVG, no images, no file written to
disk, no artifact viewer. If the subject can't be drawn in a monospace code block, say so
and ask for the one part of it that is drawable.

## Pick one form

Exactly one. Not a form with a table bolted on, not a hybrid.

| Form | Use when | Shape |
|---|---|---|
| **flow** | Steps, pipeline, cause → effect, data path | `[A] ──▶ [B] ──▶ [C]` |
| **tree** | Nesting, ownership, dir/file structure, decision paths | `root ├── a └── b` |
| **layers** | Stacked planes — architecture, protocol stack, request depth | `┌───┐ │ x │ └───┘` |
| **timeline** | Order over time, who talks to whom, sequence | `t0 ──▶ t1 ──▶ t2` |
| **table** | Options × criteria, before/after, side by side | aligned grid |
| **bar** | Magnitudes from real numbers — counts, latency, share | `████████░░ 8/10` |
| **state** | States and the transitions between them | `(idle) ──start──▶ [running]` |

When two fit, pick the one that answers the question asked: comparison → table, order →
flow or timeline, magnitude → bar, nesting → tree, behavior over time → state.

## Rules

- Respond in the same language the user wrote in. If they write in Chinese, label in Chinese. Technical terms (Redis, JWT, API) stay in English.
- **One fenced code block. That is the answer.** Optional bold title above it, optional single bold bottom line after it — nothing else. No "here's a diagram of…", no bullets describing what it shows.
- **≤80 display columns, ≤20 rows.** Count the widest line in display columns, not characters — a CJK character is 1 character but 2 columns wide, so a Chinese label eats twice the width it looks like. Don't eyeball it; the user can ask for wider or taller.
- **Box drawing only**: `┌ ┐ └ ┘ ─ │ ├ ┤ ┬ ┴ ┼ ▶ ◀ ▲ ▼`, plus `█` `░` for bars. In a box or a vertical flow, branch with `┬`/`┴`/`┼`, never two arrows stacked on separate rows; a tree branches with `├`/`└`.
- **Alignment is the whole point.** The left and right wall of a box sit in the same two columns on every row of that box. An arrow starts and ends on a wall or a line, never in air. A misaligned box is a broken drawing, not a small cosmetic issue.
- Arrow labels are verbs, conditions, or the mechanism on that edge, ≤3 words (`token ok`, `on 5xx`, `HTTPS`). Node labels are nouns, ≤20 chars — break a long one onto two lines inside the box rather than widening the box.
- Numbers carry their scale: `8/10`, `p95 120 ms`, `+34%`. A bar with no value is decoration.
- No emoji, no ANSI colour, no tabs, no mermaid, no ASCII art of pictures, logos, or faces. This draws structure, not illustrations.
- No file written unless the user explicitly asks for one.
- Nothing in the request? Visualize the current session's subject. Truly nothing? Ask `Visualize what?` and stop.

## Self-check before sending

Run this over your own drawing. Fix, then send.

- Widest line is ≤80 display columns — CJK counts as 2 — count it, don't guess.
- Every box's `│` walls line up in the same columns on every row of that box.
- Every connecting `▶ ◀ ▲ ▼` butts against the line it leaves and the wall it points at — no space on either side. Shorthand inside a label (`queue ▶ reconcile ▶ DLQ`) is fine.
- Every branch has a `┬`, `┴`, or `┼` at the junction.
- Bar lengths match the numbers, and the block says what one block is worth (`1 █ ≈ 20 ms`) — on the title line or beside the bars.
- One form, one code block, nothing outside it but the optional title and bottom line.

## Output format

A bold title line (a short noun phrase, optional), then exactly one fenced code block
holding the drawing, then at most one bold bottom line. Nothing else in the message.

## Examples

The outer fence here is just a wrapper. In real output the title and the bottom line sit
**outside** the drawing's code block, where bold actually renders — put them inside it and
the user sees literal `**asterisks**`.

`/vis request 進到 API 之後發生什麼`

```
**Request 進到 API 之後**

┌──────────┐
│  client  │
└────┬─────┘
     │ HTTPS
     ▼
┌──────────┐
│   edge   │
└────┬─────┘
     │
     ▼
┌──────────┐    ┌──────────┐
│   auth   │───▶│ session  │
└────┬─────┘    │ (redis)  │
     │ token ok └──────────┘
     ▼
┌──────────┐    ┌──────────┐
│ handler  │───▶│ postgres │
└──────────┘    └──────────┘
```

`/vis Redis 還是 Postgres 存 session`

```
**Session 存在哪**

┌────────────┬──────────────┬──────────────┐
│            │    redis     │   postgres   │
├────────────┼──────────────┼──────────────┤
│ revocation │ instant      │ instant      │
│ latency    │ <1 ms        │ ~2 ms        │
│ scale out  │ horizontal   │ vertical 1st │
│ ops burden │ high         │ low          │
│ durability │ lossy        │ durable      │
└────────────┴──────────────┴──────────────┘

**Postgres 除非你已經有 redis 在跑**
```

`/vis p95 latency 每個 endpoint`

```
**p95 latency by endpoint**  (1 block ≈ 20 ms)

/search    ████████████████████  412 ms
/checkout  ██████████            207 ms
/login     ███                   61 ms
/health    █                     23 ms
```

## Anti-examples

Don't write "Here's a diagram showing the request flow:" above the block — the block is the
answer, and the sentence makes it two answers.

Don't mix forms. A flow with a comparison table under it is two drawings, and the user asked
for one.

Don't draw a picture with `/\` characters — a cat, a rocket, a logo. This skill draws
structure; illustration is a different skill someone else can write.

Don't emit a mermaid block and note that it renders on GitHub. It doesn't render here.

Don't let one label push a line past 80. It wraps, the wall moves, the box breaks — shorten
the label or put it on two lines.

Don't spend 40 rows. Cut to the 5–7 things that carry the decision; the rest is a second
drawing nobody asked for.

Don't "save it as vis.md for you" or write an SVG. The terminal is the medium.

If no request was supplied, visualize the current session's situation — the same subject
`clear-view` would describe in prose.
