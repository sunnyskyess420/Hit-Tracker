# Sunnys Hit Tracker

A private, single-file marijuana usage tracker. All data stays in your browser's localStorage — no account, no server, nothing leaves your device unless you explicitly enable cloud sync.

Built for someone who smokes flower (pipe, mostly) and buys by the ounce, with a partner who occasionally gifts 7g. Tracks **grams**, not just hit counts — because that's what you actually measure.

---

## Features

### Core tracking
- **One-tap logging** — big green button logs a hit instantly with your last-used device and a sensible gram estimate
- **Quick buttons** — pre-set for your actual methods: Pipe hit (0.02g), Vape pen (0.01g), Dab (0.01g), Joint (0.1g)
- **Optional details** — mood before/after, stress, energy, sleep quality, who you were with, custom tags, exact gram amount, cost override
- **Undo last** — quick correction

### Gram-based daily limit
- Set a daily limit in **grams** (defaults to 1g/day) or hits
- Progress ring fills as you log: green → amber at 80% → red at 100%
- **Logging is never blocked** — you can always record accurately
- Neutral notices ("You're near your daily goal"), no shame messaging

### Stash tracker (does the math for you)
- Add each purchase: your oz (28g), your partner's 7g gift, anything
- Add giveaways/sold — reduces supply, recalculates effective price
- **Reup days marked with ↻ on the calendar** — see at a glance when you restocked
- Auto-calculates:
  - **Grams on hand** = acquired − given away − used
  - **Effective $/g** = total spent ÷ net grams acquired
  - **Hits remaining** = grams on hand ÷ grams-per-hit
  - **Per-hit cost** = effective $/g × grams per hit
- Quick-adjust stepper for grams-per-hit right on the main screen

### Bust-up markers (your X on the calendar)
- One-tap "✕ Bust up 2g" button marks today
- Bold ✕ appears on calendar days you ground a batch
- Backfill any past day from its detail modal
- Tracks avg days between bust-ups (your natural rhythm)
- Separate from the stash/limit — no double-counting

### Calendar heatmap
- Monthly GitHub-style heatmap colored by daily usage (grams or hits)
- **Sunday-first** week layout
- **✕ marker** for bust-up days (when you grind a batch)
- **↻ marker** for reup days (when you restock — from stash entries)
- Tap any day → modal with hits, grams, bust-ups, reups, cost, mood/sleep ratings, and full entry list
- Month navigation + monthly totals (includes bust-up and reup counts)

### Charts & trends
- Daily usage (14 days) and 30-day trend
- Weekly totals (last 12 weeks)
- By hour of day, by weekday, by device, by hit size
- Neutral weekly report: "You used 15% less this week (0.7g) versus last week (0.9g)"

### Mood, sleep & context
- Optional mood/stress/energy/sleep sliders on every hit
- End-of-day check-in (sleep, mood, productivity, well-being, 1–5)
- Correlation summary: average mood/sleep on higher-use vs lower-use days
- Clearly labeled as personal awareness, not medical claims

### Privacy & security
- **Optional 4–6 digit PIN** (SHA-256 hashed locally)
- Blur content until unlocked
- **Panic hide** button — instant black screen
- Clearly labeled as basic privacy, not encryption
- All data local by default

### Optional cloud sync (off by default)
- Sync to a private URL you control (your own server, a private bin, etc.)
- Manual "Sync now" / "Pull from cloud" buttons
- Shows last sync time
- Explicit warning about what data leaves the device before you enable it

### Data portability
- **CSV export** (with all fields including grams, mood, tags)
- **JSON backup** (full backup: log + check-ins + stash + bust-ups + settings)
- **JSON import** (merges by ID, no duplicates)
- **Search & filter** entries by note, tag, device, or size

---

## Quick start

1. **Download** `hit-tracker.html`
2. **Open it** in any modern browser (Chrome, Firefox, Edge, Safari)
3. That's it — the app runs entirely offline after first load

### On mobile (optional)
- Open the file in your mobile browser
- **Add to Home Screen** — it'll work like a native app, fully offline

---

## Setup walkthrough for your first session

1. **Open the file** — you'll see an empty tracker with a 1g/day limit
2. **Tap ⚙️ Settings** → set your daily limit (default 1g is fine for ~1g/day)
3. **Tap "Manage stash"** → add your oz:
   - Source: "My oz deal" (auto-fills 28g)
   - Price: what you paid (e.g. $180)
   - Add entry
4. Add your partner's gift:
   - Source: "Partner's gift" (auto-fills 7g, price $0)
5. **Tap "✕ Bust up 2g"** whenever you grind a batch — an ✕ appears on today's calendar cell
6. **Tap "Log a hit"** each time you smoke — the ring fills based on your grams-per-hit estimate
7. If the ring fills too fast or slow, use the **+/− stepper** on the stash card to adjust grams-per-hit

---

## How the data is stored

All data lives in your browser's `localStorage` under these keys:

| Key | Contents |
|-----|----------|
| `hitTrackerLogV2` | Hit entries (preserved from v1) |
| `hitTrackerSettingsV2` | App settings (limit, currency, costs, PIN, quick buttons, tags, sync) |
| `hitTrackerCheckinsV2` | End-of-day check-ins |
| `hitTrackerStashV2` | Stash entries (purchases + giveaways) |
| `hitTrackerBustupsV2` | Bust-up markers |

**Each browser has separate storage.** If you open the file in Chrome, your data won't appear in Firefox. Use **Backup JSON** / **Import JSON** to move data between browsers or devices.

---

## Backward compatibility

The app preserves existing data from earlier versions:
- v1 entries (just `id, time, size, device, note`) are migrated additively — new optional fields are filled as null/empty
- v4 settings with 0.1g/hit default are auto-updated to 0.02g/hit (unless you customized it)
- Old JSON backups (v1 bare arrays, or v3/v4 objects) still import correctly

---

## Tech

- **Single HTML file** (~216 KB, includes embedded background image) — no build step, no dependencies to install
- **Vanilla JavaScript** — no framework, no bundler
- **Chart.js** via CDN (cached after first load; charts hidden with a notice if offline on first load)
- **Embedded cannabis leaf background** — AI-generated, base64-encoded, subtle dark overlay for readability
- **localStorage** — primary data store, always
- **Responsive** — mobile-first, dark-themed, works one-handed
- **Haptic feedback** on supported devices (`navigator.vibrate`)
- **SHA-256 PIN hashing** via Web Crypto API

---

## Privacy

- **No account, no server** by default
- **No analytics, no tracking, no cookies**
- **No external requests** except the Chart.js CDN on first load (cached after)
- **PIN is hashed locally** with SHA-256 + salt — but localStorage itself is not encrypted, so this is basic privacy against casual viewing, not a security measure
- **Cloud sync is off by default** and only activates when you provide a URL and tap "Sync now"

---

## Customizing

The code is heavily commented and organized into numbered sections (search for `===== N` to jump around):

1. Constants & defaults
2. State
3. Persistence & migration
4. Utilities
5. Logging a hit
6. Limit & reminders
7. Cost calculations (+ stash math)
7b. Bust-ups
8. Mood/context & check-ins
9. Calendar heatmap
10. Charts
11. Weekly report
12. Patterns/correlations
13. Entries (search/filter)
14. Settings UI
15. PIN lock & panic
16. Export/import
17. Cloud sync
18. Render all + init

### Common tweaks
- **Change default devices**: edit `DEFAULT_DEVICES` in section 1
- **Change default quick buttons**: edit `settings.quickButtons` in `defaultSettings()`
- **Change calendar tier thresholds**: edit `calTier()` in section 9
- **Change default grams-per-hit**: edit `defaultGramsPerHit` in `defaultSettings()`

---

## No medical advice

This app is a personal tracking tool. It does not provide medical advice, diagnosis, or treatment recommendations. All messaging is neutral and factual. If you have questions about your usage, consult a healthcare professional.

---

## License

MIT — do whatever you want with it. Attribution appreciated but not required.
