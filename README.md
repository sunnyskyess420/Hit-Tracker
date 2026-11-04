# Sunnys Hit Tracker

A private, single-file marijuana usage tracker. All data stays in your browser — no account, no server, nothing leaves your device. Works fully offline, including on first load.

Built for someone who smokes flower (pipe, mostly) and buys by the ounce, with a partner who occasionally gifts 7g. Tracks **grams**, not just hit counts — because that's what you actually measure.

---

## Features

### Core tracking
- **One-tap logging** — the big button logs a hit with your last-used device, strain and grams
- **Quick buttons** — pre-set for real methods (Pipe 0.02g, Vape pen 0.01g, Dab 0.01g, Joint 0.1g). Edit or delete them all; the app remembers an empty list
- **Optional details** — mood before/after, stress, energy, sleep quality, who you were with, strain, tags, exact grams, cost override
- **Habits stick, moments don't** — device, size and strain carry to the next hit; notes, moods and tags are cleared after each log so they never bleed into the next session
- **Remembered grams per device** — type `0.08g` once for Joint and every later Joint hit defaults to it. Not retroactive: past entries keep what they had
- **Undo everywhere** — every delete (hit, stash entry, bust-up, count) offers Undo in a toast
- **Sliders only count when touched** — leaving a rating alone stores nothing, so the mood/sleep comparisons aren't padded with fake 3s

### Gram-based daily limit
- Set a daily limit in **grams** (default 1g/day) or hits
- Progress ring fills as you log: green → amber at 80% → red at 100%
- **Logging is never blocked** — you can always record accurately
- **Carry over unused allowance** — grams you don't use are added to tomorrow (capped at 2× the limit). The Today card spells it out: *"1.1g left today — 0.21g of 1.31g used (1g limit + 0.31g carried over)"*
- Neutral wording throughout: no "goal" language, no shame

### Stash tracker (two-stage: nugs → ground → smoked)
- Add each purchase: your oz (28g), your partner's 7g gift, anything — with **strain** and price
- Add giveaways/sold — reduces supply, recalculates effective price
- **Ground is replayed chronologically**, not subtracted as a lifetime total: a hit draws from ground first, then whole nugs, and only from weed that existed at that moment. Smoking before you grind can't eat into the next batch
- **Last-batch line** — "2g batch from Nov 3 — 1g left", so "how much of that 2g is left" is always answerable
- Auto-calculates grams on hand, effective $/g, **$/g per purchase**, hits remaining, per-hit cost

### Count it — the app can be corrected
- **Count it** takes a real weighing: total on hand and how much is ground
- That count becomes the truth from that moment; later hits replay from it, so the card matches the jar even if old estimates drifted
- **Calibration** — after a count, if the batch's real consumption implies a different grams-per-hit (say 0.025g instead of 0.02g), the app offers to update the estimate
- **Weigh-in nudge** if your last count is older than two weeks

### Bust-up markers
- One-tap **Bust up** at your **configured amount** — 2g by default, change it in **Settings → Logging** (½ / 1 / 2 / 3 / 7g presets, or any amount)
- Any single day can use a different amount from its detail modal
- Bust-ups are **timestamped**, so one ground after a count is added on top of it rather than being wiped by it
- **Ground-low nudge** when you have whole nugs but nothing ground
- Tracks average days between bust-ups

### Strain tracking
- Add a strain to each stash entry; pick it per hit (autocomplete from what you've used)
- Quick logs reuse the last strain; **Patterns** shows your top strain by grams
- The CSV export carries a Strain column

### Money
- **Monthly budget bar** — spend vs target, green → amber → red
- Effective $/g from real purchases, per-purchase $/g in the stash list, per-hit cost, and today/week/month/all-time totals

### T-break mode
- Start a break with a target length; a banner counts **day N of M** and how many hits were logged since
- Nothing is blocked — it's a counter, not a lock
- Optional **evening check-in nudge** after an hour you choose

### Calendar heatmap
- Monthly GitHub-style heatmap coloured by usage (grams or hits)
- Sunday-first, with grinder icons for bust-up days and jar icons for reups
- Tap any day → hits, grams, bust-ups, reups, cost, mood/sleep, entries, plus backfill

### Charts & patterns
- Daily usage (14 days), 30-day trend, weekly totals (12 weeks)
- By hour, weekday, device, size
- Neutral weekly report: *"You used 15% less this week (0.7g) versus last week (0.9g)"*
- Correlations between check-ins and usage, labelled as awareness — not medical claims

### Three looks (Settings → Privacy & data → Appearance)
- **Neon** — near-black, green and violet glow
- **Earthy** — moss, kraft and amber
- **Groovy** — warm amber and burnt orange
- Every surface follows the palette (notices, tabs, action buttons), and your choice is remembered

### Privacy & security
- **Optional 4–6 digit PIN**, with escalating lockout after wrong attempts
- **Blur until unlocked** and a panic button (screen-off icon) that blacks out instantly
- **Forgot PIN erases** — there is no recovery path, so the lock can't be bypassed by tapping a link. It's confirmed by typing `ERASE`
- **Optional encryption at rest** — payload encrypted with **AES-256-GCM**, key derived from your PIN with **PBKDF2-SHA256 (210,000 rounds)**. No PIN hash is stored; a wrong PIN fails the GCM tag. Forget it and the data is unrecoverable
- Without encryption, data is plain JSON and the PIN is only a screen lock — the app says so instead of pretending otherwise

### Backups that don't lie
- **Back up now** writes a real file and stamps "last backup" only after the write succeeds
- On Chrome/Edge it reuses the file you picked once (File System Access API); elsewhere it downloads
- A **Backup due** banner sits at the top of the screen after 7 days, and Settings shows the last backup date
- Encrypted installs back up the **encrypted vault**, safe to keep anywhere
- JSON import validates every row (dates, grams, costs, ratings) and merges by ID

### Data portability
- **CSV export** with every field including strain
- **JSON backup / restore** (merges, no duplicates)
- **Search & filter** by note, strain, tag, device or size
- **Print report** — clean light-mode PDF with inline SVG charts

### PWA
- Installable, offline-first, with long-press **shortcuts**: Log a hit · Bust up · Check-in

---

## Quick start

1. Open `index.html` in any modern browser
2. **Settings → Logging** — set your daily limit, currency and grams per hit
3. **Manage stash** — add your oz (grams, price, strain)
4. Tap **Bust up** when you grind a batch, **Log a hit** when you smoke
5. Once you have a real number on the scale, tap **Count it** — that's what keeps the maths honest

**On mobile:** open it, then *Add to Home Screen* — it runs like a native app, fully offline.

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | The whole app (~270 KB, no build step) |
| `hit-tracker.html` | Redirect to `index.html` (kept so old links keep working) |
| `chart.umd.min.js` | Chart.js 4.4.6, bundled locally — no CDN, works offline |
| `sw.js` | Service worker (offline cache, `sunnys-hit-tracker-v4`) |
| `manifest.json` | PWA manifest, icons and launch shortcuts |
| `icon-192/256/512.png`, `icon-512-maskable.png` | App icons (maskable has its own padding) |
| `weed-bg.png`, `lighting-weed.mp3` | Background texture, hit sound |
| `tools/check.js` | Static checks: script syntax, duplicate ids, missing elements/assets |
| `.github/workflows/check.yml` | Runs those checks on every push |
| `backup/` | Local pre-upgrade snapshot — git-ignored, not part of the release |

---

## How the data is stored

| Key | Contents |
|-----|----------|
| `hitTrackerLogV2` | Hit entries |
| `hitTrackerSettingsV2` | Settings (limit, currency, costs, PIN, quick buttons, tags, budget, T-break, theme, counts…) |
| `hitTrackerCheckinsV2` | End-of-day check-ins |
| `hitTrackerStashV2` | Stash entries (purchases + giveaways) |
| `hitTrackerBustupsV2` | Bust-up markers |
| `hitTrackerVaultV1` | **Only when encryption is on** — the encrypted payload (replaces the five keys above) |
| `hitTrackerLockV1` | PIN attempt counter / lockout time (no data, no hash) |

Everything is mirrored to IndexedDB and recovered automatically if localStorage is wiped. **Each browser has separate storage**, and so does each address — `file://` and a hosted URL keep different data. Use Backup/Restore to move between them.

---

## Checks

- **In the app:** open `index.html?selftest=1` — the title reports `SELFTEST PASS n/n` and the console prints a table. **46 tests** cover gram maths, date keys, streaks, the ground ledger, goal-bank carry-over, bust-up clamping, remembered per-device grams, saved counts, input escaping, PIN lockout and the crypto round-trip. State is restored afterwards; nothing is saved.
- **On every push:** `node tools/check.js` parses both inline scripts, flags duplicate ids, verifies every `getElementById` target exists and that local assets are present. It runs in GitHub Actions, so a typo can't reach the live site unnoticed.

---

## Tech

- **Single HTML file + one JS library** — no framework, no bundler, no build step
- **Vanilla JavaScript**, numbered sections (`===== N`) for navigation
- **Chart.js 4.4.6** bundled locally; the app makes no external requests at all
- **Web Crypto** — SHA-256 for the PIN gate, PBKDF2 + AES-GCM for optional encryption
- **localStorage + IndexedDB mirror**, File System Access for backups where available
- **CSS custom properties** for the three themes; SVG sprite for every icon (no emoji in the interface)
- Responsive, mobile-first, haptic feedback where supported

---

## Customizing

Sections in `index.html`:

1. Constants & defaults
2. State
3. Persistence, migration, **encryption**
4. Utilities (including **theme switching**)
5. Logging a hit
6. Limit, carry-over & reminders
7. Cost calculations, stash maths, **ground replay**, **counts & calibration**
8. Mood/context & check-ins
9. Calendar heatmap
10. Charts
11. Weekly report
12. Patterns/correlations
13. Entries (search/filter)
14. Settings UI (**tabs**, appearance, quick buttons)
15. PIN lock & panic
16. Export/import
17b. Backup writer + reminder
18. Render all + init
19. Self-tests

Common tweaks: `DEFAULT_DEVICES`, `settings.quickButtons`, `calTier()`, `defaultGramsPerHit`, `BUSTUP_MIN_G` / `BUSTUP_MAX_G`, and the palette blocks under `html[data-theme="…"]`.

---

## No medical advice

This app is a personal tracking tool. It does not provide medical advice, diagnosis, or treatment recommendations. All messaging is neutral and factual. If you have questions about your usage, consult a healthcare professional.

---

## License

MIT — do whatever you want with it. Attribution appreciated but not required.
