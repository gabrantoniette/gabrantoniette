# Keeping the profile README current, automatically

**Date:** 2026-09-22
**Status:** approved, not yet implemented

## The problem

Two sections of the README go stale by hand.

**"What I'm building"** lists Halcyon Goods, LinkedIn Growth and Transcriptone.
By last commit on the default branch the real order is
`students-categorization` (22/09), `linkedin-growth-agents` (21/09),
`halcyon-goods-product-control` (18/08). The newest project is absent, the
oldest is first, and Transcriptone has no repository to click through to.

**"Stack"** is a hand-written list of badges. A project can introduce a
language or a tool and the section never hears about it. JavaScript and
TensorFlow.js are in the newest repository and in neither badge group.

## Goals

1. The projects section always shows the three most recently worked-on
   public projects, each clickable, each with a description.
2. The stack section notices languages and tools that show up in new work,
   without being told.
3. Neither section churns. A commit to an existing project must not produce
   a commit here.
4. The current design survives exactly: same card shape, same badge style,
   same narrative voice.

## Non-goals

- Private repositories. They 404 for a visitor, so they never appear.
- Replacing the hand-written prose with generated text.
- Touching anything outside the two generated blocks.

## Ordering and eligibility

A repository is eligible when it is public, not a fork, not archived, and
not this profile repository itself. The self-exclusion is load-bearing: the
workflow commits here, which would pin this repo to first place forever.

Eligible repositories rank by the date of the last commit on the default
branch. Not by `pushedAt` — `halcyon` has a `pushedAt` of 01/09 from a push
to a side branch while its `main` last moved on 18/08. The default-branch
date is also what the `last-commit` badge renders, so the prose and the
badge can never disagree.

## Content model

Two TOML files, read with stdlib `tomllib`. No third-party dependency, which
is the property the existing scripts already have.

### `content/projects.toml`

One table per repository, holding what no API can produce: the title, the
headline after the colon, the narrative body, the list of decisions behind
the `<details>` fold, and the curated technology chips.

Every field is optional. A repository with no entry still renders: the
title falls back to the repository name, the body to the GitHub
description, and the chips to the repository topics that resolve to a known
technology. A project is never missing and never broken — it is either rich
or plain.

### `content/stack.toml`

The badge catalog: group order, the technologies pinned to each group, the
aliases, the denylist, and the language threshold.

A group may be marked frozen, which means detection may neither add to nor
remove from it. That exists for "From the data years" — Databricks, Azure,
PySpark, Power BI — which describes professional experience that leaves no
trace in any public repository.

Entries may override colour and logo. `Agno`, `SQLModel`, `Alembic` and
`pytest` have no brand icon of their own and already borrow the Python logo
in the current README; the catalog records that as-is.

## Detection

Two sources, one resolver.

**Languages** come from the repository languages endpoint, which returns
byte counts. A language counts when it holds at least 5% of that
repository's bytes. The threshold exists because `Mako` (an Alembic
template), `Jinja` and a 491-byte `JavaScript` file are noise, not stack.

**Topics** come from the repository metadata.

Both feed one resolver against the simple-icons catalog, 3461 entries, which
doubles as the noise filter. Resolution is ordered:

1. exact slug match — `docker`, `fastapi`, `langgraph`
2. explicit alias from the catalog — `Dockerfile` to `Docker`
3. known suffix stripped (`js`, `node`, `py`, `cli`, `api`, `sdk`) —
   `tensorflowjs` to `TensorFlow`
4. text before the first `-` or `_` — `docker-compose` to `Docker`
5. unresolved: dropped, and reported

Step 5 is why `one-hot-encoding`, `portfolio`, `monorepo`, `rest-api`,
`machine-learning` and `server-side-rendering` never reach the README. They
are concepts, and no brand ships an icon for a concept.

A resolved technology already in the catalog renders in its group. A
resolved technology not in the catalog renders in **"Recently picked up"**,
with colour and logo taken from simple-icons, and the run reports it so it
can be promoted to a real group with one line of TOML.

## Change policy

The generator computes the desired set of three repositories and the
desired set of technologies, then compares them against what the README
currently renders.

**When the sets are unchanged, the run exits without writing.** This is the
requirement that no ordinary commit disturbs this repository. Dates are not
part of the comparison because dates live in live badges, which refresh on
their own without a commit.

When a set does change, the affected block is regenerated whole — fresh
order included — and the run opens a pull request describing what moved.
Ordering inside the block is therefore frozen between membership changes,
which is the intended reading of "the last three projects, not a feed".

## Blocks

`<!-- projects:start -->` / `<!-- projects:end -->` and
`<!-- stack:start -->` / `<!-- stack:end -->`. Replacement is anchored on
the markers; everything outside is hand-written and untouched.

The existing `<!-- pin:start -->` / `<!-- pin:end -->` markers are removed.
They sit inside the region that is now generated, and
`scripts/use-self-hosted-stats.py` rewrites them from a hard-coded
`PIN_REPO`. That script keeps its cards behaviour and loses its pin
behaviour; `docs/self-host-stats.md` is updated to match.

Transcriptone has no repository and cannot survive a rule that ranks by
commit date. It moves to a short static "Earlier work" line below the
generated block rather than being deleted.

## Module layout

```
content/projects.toml
content/stack.toml
scripts/profilegen/github.py    # API access, eligibility, ranking
scripts/profilegen/icons.py     # simple-icons fetch, cache, resolver
scripts/profilegen/projects.py  # renders the projects block
scripts/profilegen/stack.py     # renders the stack block
scripts/profilegen/readme.py    # marker-anchored replacement, set comparison
scripts/update-profile.py    # CLI: --check, --write, --report
tests/                       # pytest against fixtures, no network
```

Every renderer takes plain data and returns a string, so the tests need no
network and no token.

## Workflow

`.github/workflows/update-profile.yml`, on a daily cron and on manual
dispatch. Python 3.12, with write permission on contents and pull requests.
It runs the check, stops when nothing moved, and otherwise writes and opens
a pull request whose body is the report.

Creating that pull request requires "Allow GitHub Actions to create and
approve pull requests" under Settings, Actions, General. It is enabled.

## Testing

Renderers are tested against fixtures: a repository with a full entry, one
with no entry at all, a language set below the threshold, a topic that
resolves only by suffix, a topic that resolves to nothing, and a frozen
group that detection tries to modify. The set comparison is tested for the
case that matters most: identical sets produce no write.

## Risks

The stats cards depend on `github-profile-summary-cards.vercel.app` and
`streak-stats.demolab.com`. All 47 images currently respond;
`docs/self-host-stats.md` documents the fallback.

simple-icons is fetched at run time. A failed fetch must leave the README
alone rather than render a stack with no colours, so a fetch error aborts
the run.
