# Handoff — Sunnys Hit Tracker

Written so another engineer/agent can pick this up cold. Read this, then `README.md`.

## What this is

A private, **single-file PWA** marijuana tracker. One `index.html` (~270 KB) holds markup, CSS and all JS. No build step, no framework, no npm install. Data lives in the user's browser only.

- Repo: `github.com/sunnyskyess420/Hit-Tracker` (branch `main`)
- Live: `https://sunnyskyess420.github.io/Hit-Tracker/` (GitHub Pages, deploy from `main` / root)
- Files: `index.html`, `chart.umd.min.js` (Chart.js 4.4.6, bundled), `sw.js`, `manifest.json`, icons (+ `icon-512-maskable.png`), `weed-bg.png`, `lighting-weed.mp3`, `tools/check.js`, `.github/workflows/check.yml`, `README.md`.

## Architecture in 60 seconds

- JS is one classic script, split into numbered sections (`===== N =====`). Grep those headers to navigate.
- Global state: `log` (hits), `checkins`, `stash`, `bustups`, `settings`. All persisted to `localStorage` + mirrored to IndexedDB.
- Keys: `hitTrackerLogV2`, `hitTrackerSettingsV2`, `hitTrackerCheckinsV2`, `hitTrackerStashV2`, `hitTrackerBustupsV2`, plus `hitTrackerVaultV1` (only when encryption is on) and `hitTrackerLockV1`.
- `settings` is the god object (limit, currency, costs, quick buttons, tags, theme, sleep window, counts…). Every new field needs: a default in `defaultSettings()`, normalization in `loadAll()` **and** `applyState()` (encrypted path), and sanitizing in `sanitizeImportedSettings()`.
- Rendering is a full redraw: `renderAll()` rebuilds stats, calendar, entries and charts. It runs on every hit. Fine on desktop, noticeable on old phones.
- Encryption: optional, opt-in. PBKDF2-SHA256 (210k) → AES-256-GCM. No PIN hash stored; a wrong PIN fails the GCM tag. `forgotPin()` **erases everything** (typed `ERASE`), by design.

## Verify before you ship

```powershell
node tools/check.js          # syntax, duplicate ids, getElementById targets, assets
```
Then open `index.html?selftest=1` — the tab title prints `SELFTEST PASS n/n`; console has the table. Currently **48 tests**. State is restored after; nothing is saved.

CI (`.github/workflows/check.yml`) runs `node tools/check.js` on every push. It does **not** run the in-app suite — do that manually in a browser.

Pages deploy takes **1–3 minutes** after a push. `raw.githubusercontent.com` updates instantly, the `github.io` URL lags. Don't conclude a push failed from the live site; check `https://api.github.com/repos/sunnyskyess420/Hit-Tracker/actions/runs`.

## Environment traps (learned the hard way)

1. **Files are UTF-8 with CRLF.** Do not edit with PowerShell `Set-Content -Encoding utf8` — it writes a BOM and, worse, `Get-Content -Raw` without `-Encoding UTF8` decodes as ANSI and double-encodes the whole file (all `•`, `—`, emoji turn to mojibake). Use Python with `newline=""` and preserve CRLF, or the `edit`/`apply_patch` tools which handle it.
2. **Emoji in source are real characters**, not escapes. Anchoring a patch on `"\u2014"` won't match a literal `—`.
3. **`<body>` appears twice** (app + print report template). Anchor on something unique.
4. Git identity is already configured in this working copy; pushes work without prompting. Build commits on top of `origin/main` — no force-push.
5. Screenshots in some browser panes fail intermittently (`browser_capture_busy`); retry on a second tab.

## Current feature set (do not regress)

One-tap logging; editable/deletable quick buttons; per-hit details (mood/stress/energy/sleep/social/tags/strain/grams/cost); per-device grams remembered from the last typed amount; daily limit in grams or hits with carry-over ("Carried over" stat, `computeGoalBank()`); stash with **chronological ground replay** (`stashBreakdown()`); **Count it** (physical count overrides history via `settings.inventoryFix`) + calibration prompt; bust-ups with configurable amount and **real timestamps**; calendar heatmap; charts; patterns; strain tracking; monthly budget; T-break; check-in nudge; **sleep window** (excludes overnight hours from gap maths); three themes (neon/earthy/groovy); PIN + panic + optional encryption; verified backups; CSV/JSON; print report; PWA shortcuts; undo toasts.

## Rules the product follows

- **Never block logging.** Limit messages are informational.
- **No shame language**, no "goal" wording — it's a *limit*.
- **Estimates must be correctable**: the app guesses grams per hit; Count it and calibration exist so the user can overrule it.
- **Never touch stored data** during a code change. Migrations are additive; `loadAll()` must tolerate any older shape.

## Known rough edges / next steps

- `renderAll()` redraws everything on every hit; splitting it (only stats + calendar cell) would help low-end phones.
- `avgDaysBetweenBustups` still uses calendar dates, not the sleep window.
- No strain list screen or per-strain stats; no filter-by-strain dropdown.
- Print report still uses `•`/`»` glyphs in its legend (correct for paper, but inconsistent with the app's icons).
- `hit-tracker-backup.json` in the repo is an empty placeholder; `.gitignore` excludes real backups.
- The app is English-only, and copy is deliberately plain.

## Quick local start

Open `index.html` directly (file://). Phone: *Add to Home Screen*. Data is per-origin — `file://` and the hosted URL are **separate stores**; move data with Backup JSON → Import JSON.
