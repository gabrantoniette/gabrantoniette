# Hosting your own stats cards

## Why

The cards in this README depend on free instances maintained by other people. They go down. In August 2026, two went down at the same time:

| Service | What happened |
| --- | --- |
| `github-readme-stats.vercel.app` | Returns `503 DEPLOYMENT_PAUSED` — the official public instance was paused on Vercel. |
| `github-readme-streak-stats.herokuapp.com` | No response — Heroku ended its free dynos and the project moved hosts (it now lives at `streak-stats.demolab.com`). |

The README currently uses `github-profile-summary-cards`, `streak-stats.demolab.com` and `github-readme-activity-graph`, which are up. All three are still shared third-party instances — same risk, just postponed.

Run your own instance of [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) and the only way it goes down is if you take it down. As a bonus you get back three cards that beat the current substitutes: the official stats card, the top languages card, and the repository pin.

## Step by step

Takes about 10 minutes, all free.

### 1. Fork the repository

```bash
gh repo fork anuraghazra/github-readme-stats --clone=false
```

(Or use the **Fork** button at github.com/anuraghazra/github-readme-stats.)

### 2. Create a GitHub token

Go to **Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic)**:

- **Note:** `readme-stats`
- **Expiration:** no expiration, or put a renewal reminder in your calendar
- **Scopes:** **none**. Don't check anything — the token only needs to read public data, and a token with no scopes is the safest one there is. Check `repo` only if you want commits from private repositories to be counted.

Copy the token. It's shown only once.

### 3. Deploy on Vercel

1. Sign in to [vercel.com](https://vercel.com) with your GitHub account.
2. **Add New → Project → Import** your `github-readme-stats` fork.
3. Before clicking Deploy, open **Environment Variables** and add:
   - **Name:** `PAT_1`
   - **Value:** the token from step 2
4. **Deploy**.

You'll end up with a domain like `https://github-readme-stats-yourname.vercel.app`.

> The variable really is called `PAT_1`, with the underscore and the number. Without it the card renders an SVG that reads *"Maximum retries exceeded"* instead of your stats — that's how you know the token never arrived.

### 4. Point the README at your instance

```bash
python scripts/use-self-hosted-stats.py github-readme-stats-yourname.vercel.app
```

The script swaps the blocks between `<!-- cards:start -->` / `<!-- cards:end -->` and `<!-- pin:start -->` / `<!-- pin:end -->` for cards from your instance, already using the profile's palette (`#1F3864` / `#4A7DBF`) and wrapped in `<picture>` for light and dark themes. It writes `README.bak.md` before touching anything.

Review the result and commit:

```bash
git diff README.md
git add README.md && git commit -m "stats: point cards at own instance"
```

### 5. Verify

```bash
python scripts/check-readme-links.py
```

Walks every image in the README and fails if any responds with something other than 200 or returns an error SVG. Worth running now and then — this is exactly the check that would have caught both outages above on the day they happened.

## Rolling back

`README.bak.md` holds the previous version. To undo without the backup, `git checkout README.md`.

## Maintenance

- **An expired token** breaks the cards just like a service outage does. If you set an expiration date, set a reminder too.
- **The fork doesn't need updating** for the cards to work. Sync with upstream only if you want new themes or parameters.
- Vercel idles free projects with no traffic; the first request after a quiet spell can take a few seconds. That's slowness, not an outage.
