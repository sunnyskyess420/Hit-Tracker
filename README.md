# Sunnys Hit Tracker

A private, single-file marijuana usage tracker. All data stays in your browser — no account, no server, nothing leaves your device. Works fully offline, including on first load.

Built for someone who smokes flower (pipe, mostly) and buys by the ounce, with a partner who occasionally gifts 7g. Tracks **grams**, not just hit counts — because that's what you actually measure.

---

## Features

### Core tracking
- **One-tap logging** — the big button logs a hit instantly with your last-used device, strain and gram estimate
- **Quick buttons** — pre-set for your actual methods: Pipe hit (0.02g), Vape pen (0.01g), Dab (0.01g), Joint (0.1g)
- **Optional details** — mood before/after, stress, energy, sleep quality, who you were with, strain, tags, exact grams, cost override
- **Undo last** — and every delete (hit, stash entry, bust-up) now offers **Undo** in a toast instead of vanishing
- **Notes are only recorded when you move them** — sliders sit at 3 but stay empty in the data until you actually touch them, so the mood/sleep comparisons aren't padded with defaults

### Gram-based daily limit
- Set a daily limit in **grams** (default 1g/day) or hits
- Progress ring fills as you log: green → amber at 80% → red at 100%
- **Logging is never blocked** — you can always record accurately
- Neutral notices, no shame messaging
- **Goal bank** — optionally carry unused allowance forward (capped at 2× the daily limit)

### Stash tracker (does the math for you)
- Add each purchase: your oz (28g), your partner's 7g gift, anything — with **strain** and price
- Add giveaways/sold — reduces supply, recalculates effective price
- **Reup days marked with » on the calendar**
- Auto-calculates grams on hand, effective $/g, **$/g for each purchase**, hits remaining, per-hit cost
- Quick-adjust stepper for grams-per-hit on the main screen

### Bust-up markers (your • on the calendar)
- One-tap **• Bust up** button marks today at your **configured amount** — 2g by default, change it any time in **Settings → Bust-up** (½g / 1g / 2g / 3g / 7g presets, or type any amount)
- Any single day can use a different amount from that day's detail modal
- **Ground-low nudge** — when you have whole nugs but nothing ground, the stash card offers the bust-up with your amount prefilled
- Tracks average days between bust-ups (your natural rhythm)
- Separate from the stash/limit — no double-counting

### Strain tracking
- Add a strain to each stash entry; pick it per hit (with autocomplete from what you've already logged)
- Quick logs reuse the last strain you used
- Insights shows your **top strain by grams**

### Money
- **Monthly budget bar** — set a budget and see spend vs target, green → amber → red
- Effective $/g from real purchases, plus per-purchase $/g in the stash list
- Per-hit cost, today/week/month/all-time totals

### T-break mode
- Start a break with a target length; a banner counts **day N of M** and how many hits were logged since
- Nothing is blocked — it's a counter, not a lock
- Optional **evening check-in nudge** after an hour you choose

### Calendar heatmap
- Monthly GitHub-style heatmap colored by daily usage (grams or hits)
- Sunday-first layout, **•** for bust-up days, **»** for reup days
- Tap any day → hits, grams, bust-ups, reups, cost, mood/sleep, entries, plus backfill for smoking or bust-ups
- Month navigation and monthly totals

### Charts & patterns
- Daily usage (14 days), 30-day trend, weekly totals (12 weeks)
- By hour, weekday, device, size
- Neutral weekly report: "You used 15% less this week (0.7g) versus last week (0.9g)"
- Correlations between check-ins and usage, clearly labeled as awareness, not medical claims

### Privacy & security
- **Optional 4–6 digit PIN**, with escalating lockout after wrong attempts
- **Blur content until unlocked** and a panic-hide button
- **Optional encryption at rest** (Settings → Encryption): the payload is encrypted with **AES-256-GCM**, using a key derived from your PIN with **PBKDF2-SHA256 (210,000 rounds)**. The PIN itself is never stored, and a wrong PIN simply fails the GCM tag. If you forget it, the data is unrecoverable — that's the trade-off
- Without encryption, data sits in storage as plain JSON and the PIN is only a screen lock — the app says so rather than pretending otherwise

### Backups that don't lie
- **Back up now** writes a real file and only stamps "last backup" after the write succeeds
- On Chrome/Edge it reuses the file you picked once (File System Access API); elsewhere it downloads
- A **Backup due** banner appears after 7 days — no more silent weekly downloads that browsers quietly blocked
- Encrypted installs back up the **encrypted vault**, so the file is safe to keep anywhere
- JSON import validates every row (dates, grams, costs, ratings) and merges by ID

### Data portability
- **CSV export** with all fields including strain and grams
- **JSON backup / restore** (merges, no duplicates)
- **Search & filter** by note, strain, tag, device or size
- **Print report** — a clean light-mode PDF with inline SVG charts

### PWA
- Installable, offline-first, with long-press **shortcuts**: Log a hit · Bust up · Check-in

---

## Quick start

1. Open `index.html` in any modern browser
2. **⚙️ Settings** → set your daily limit and currency
3. **Manage stash** → add your oz (source, grams, price, strain)
4. Tap **• Bust up** when you grind a batch, **Log a hit** when you smoke
5. Adjust grams-per-hit with the +/− stepper so the ring matches reality

**On mobile:** open it, then *Add to Home Screen* — it runs like a native app, fully offline.

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | The whole app (~220 KB, no build step) |
| `hit-tracker.html` | Redirect to `index.html` (kept so old links still work) |
| `chart.umd.min.js` | Chart.js 4.4.6, bundled locally — no CDN, works offline |
| `sw.js` | Service worker (offline cache) |
| `manifest.json` | PWA manifest + launch shortcuts |
| `weed-bg.png`, `lighting-weed.mp3`, `icon-*.png` | Assets |
| `backup/` | Local pre-upgrade snapshot — git-ignored, not part of the release |

---

## How the data is stored

All data lives in your browser's storage:

| Key | Contents |
|-----|----------|
| `hitTrackerLogV2` | Hit entries |
| `hitTrackerSettingsV2` | Settings (limit, currency, costs, PIN, quick buttons, tags, budget, T-break…) |
| `hitTrackerCheckinsV2` | End-of-day check-ins |
| `hitTrackerStashV2` | Stash entries (purchases + giveaways) |
| `hitTrackerBustupsV2` | Bust-up markers |
| `hitTrackerVaultV1` | **Only when encryption is on** — the encrypted payload (replaces the five keys above) |
| `hitTrackerLockV1` | PIN attempt counter / lockout time (no data, no hash) |

Everything is mirrored to IndexedDB as a second copy, and recovered automatically if localStorage is wiped. **Each browser has separate storage** — use Backup/Restore to move between browsers or devices.

---

## Self-tests

Open `index.html?selftest=1` — the title bar reports `SELFTEST PASS n/n` and the console prints a table. It covers gram math, date keys, streak counting, stash breakdown, bust-up clamping, PIN lockout escalation, escaping, and the crypto round-trip (including that a wrong key cannot decrypt). State is restored afterwards; nothing is saved.

---

## Tech

- **Single HTML file + one JS library** — no build step, no framework, no bundler
- **Vanilla JavaScript**, numbered sections (`===== N`) for navigation
- **Chart.js 4.4.6** bundled locally (no external requests at all)
- **Web Crypto** — SHA-256 for the PIN gate, PBKDF2 + AES-GCM for optional encryption
- **localStorage + IndexedDB mirror**, File System Access for backups where available
- Responsive, mobile-first, dark theme, haptic feedback where supported

---

## Customizing

Sections in `index.html`:

1. Constants & defaults
2. State
3. Persistence, migration, **encryption**
4. Utilities
5. Logging a hit
6. Limit & reminders
7. Cost calculations (+ stash math)
7b. Bust-ups
7c. Budget / T-break / nudges
8. Mood/context & check-ins
9. Calendar heatmap
10. Charts
11. Weekly report
12. Patterns/correlations
13. Entries (search/filter)
14. Settings UI
15. PIN lock & panic
16. Export/import
17b. Backup writer + reminder
18. Render all + init
19. Self-tests

Common tweaks: `DEFAULT_DEVICES`, `settings.quickButtons`, `calTier()`, `defaultGramsPerHit`, `BUSTUP_MIN_G` / `BUSTUP_MAX_G`.

---

## No medical advice

This app is a personal tracking tool. It does not provide medical advice, diagnosis, or treatment recommendations. All messaging is neutral and factual. If you have questions about your usage, consult a healthcare professional.

---

## License

MIT — do whatever you want with it. Attribution appreciated but not required.
