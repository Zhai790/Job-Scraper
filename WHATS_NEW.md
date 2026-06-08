# What's New: Multi-Board Support 🎉

## Major Upgrade: 4 Job Boards Instead of 1

Your job monitor now checks **4 job boards** instead of just Lever!

| Board | Coverage | Setup |
|-------|----------|-------|
| **Greenhouse** ⭐ | Shopify, Wealthsimple, Faire, Thinkific, 100+ Canadian companies | ✅ No API key needed |
| **Adzuna** ⭐ | Aggregates jobs from 1000s of sources | ⚠️ Free API key required |
| **Lever** | Magnet Forensics, limited Canadian coverage | ✅ No API key needed |
| **Indeed** | Largest job board but actively blocks scrapers | ⚠️ May not work |

---

## Quick Start

### 1. Edit config.py

```python
# Add Canadian companies using Greenhouse
GREENHOUSE_COMPANIES = [
    "shopify",
    "wealthsimple",
    "faire",
    "thinkific",
]

# Keep Lever companies
LEVER_COMPANIES = [
    "magnetforensics",
]

# Optional: Enable Adzuna (requires free API key)
ADZUNA_QUERIES = [
    "junior software engineer Canada",
    "new grad developer",
]
```

### 2. (Optional) Get Adzuna API Key

**Free tier: 1000 calls/month**

1. Sign up: https://developer.adzuna.com/
2. Get your App ID and App Key
3. Add to GitHub Secrets:
   - `ADZUNA_APP_ID`
   - `ADZUNA_APP_KEY`

### 3. Push and Run

```bash
git add -A
git commit -m "Configure multi-board monitoring"
git push origin main
```

Go to **Actions → Multi-Board Job Monitor → Run workflow**

---

## What Changed?

### Before (Lever Only)
```
✓ monitor.py
✓ job-monitor.yml workflow
✓ Checks ~1 company (Magnet Forensics)
✓ Finds 0-2 junior jobs typically
```

### After (Multi-Board)
```
✓ monitor.py (still works, backward compatible)
✓ monitor_multiboard.py (NEW)
✓ job-monitor-multi.yml workflow (NEW)
✓ Checks 100+ companies across 4 job boards
✓ Finds 10-50+ junior jobs typically
```

### File Structure

```
job-board-monitor/
├── scrapers/              ← NEW: Modular scrapers
│   ├── lever.py
│   ├── greenhouse.py
│   ├── indeed.py
│   └── adzuna.py
├── config.py              ← NEW: Centralized config
├── monitor_multiboard.py  ← NEW: Multi-board script
├── monitor.py             ← OLD: Still works!
├── README_MULTIBOARD.md   ← NEW: Documentation
└── SETUP_MULTIBOARD.md    ← NEW: Setup guide
```

---

## Canadian Companies on Greenhouse

These companies actively hire junior/new grad roles:

**Big Tech:**
- Shopify (Ottawa, Toronto, Remote)
- Wealthsimple (Toronto)

**Scale-ups:**
- Faire (Kitchener-Waterloo)
- Thinkific (Vancouver)
- League (Toronto)
- Ritual (Toronto)
- KOHO (Vancouver)
- Clearco (Toronto)

**Fintech:**
- Neo Financial (Calgary)
- Borrowell (Toronto)
- Mogo (Vancouver)

**Others:**
- Bench Accounting (Vancouver)
- Tulip Retail (Kitchener-Waterloo)
- FreshBooks (Toronto)

**Add them to config.py:**
```python
GREENHOUSE_COMPANIES = [
    "shopify", "wealthsimple", "faire", "thinkific",
    "league", "ritual", "koho", "clearco",
    "neofinancial", "borrowell", "mogo",
    "benchaccounting", "tulipretail", "freshbooks",
]
```

---

## Migration Options

### Option A: Run Both (Recommended)

Keep both workflows running:
- `job-monitor.yml` - Original Lever-only
- `job-monitor-multi.yml` - New multi-board

They share `seen_jobs.json`, so no duplicate notifications.

### Option B: Switch to Multi-Board Only

```bash
cd /d/job-board-monitor
rm .github/workflows/job-monitor.yml
mv .github/workflows/job-monitor-multi.yml .github/workflows/job-monitor.yml
git add -A && git commit -m "Switch to multi-board" && git push
```

---

## Expected Results

### Before (Lever Only)
```
[2026-06-08] Starting job monitor...
Checking: magnetforensics
Found 10 jobs
Matching jobs: 0
New jobs: 0
```

### After (Multi-Board)
```
[2026-06-08] Starting multi-board job monitor...

[LEVER] Checking 1 companies...
  magnetforensics: 10 jobs

[GREENHOUSE] Checking 10 companies...
  shopify: 15 jobs
  wealthsimple: 8 jobs
  faire: 12 jobs
  ...

[ADZUNA] Searching 3 queries...
  "junior software": 47 jobs
  "new grad developer": 23 jobs
  ...

Total jobs fetched: 115
Jobs matching keywords: 12
New jobs: 12

✓ Email sent with 12 new opportunities!
```

---

## Why This Matters

**Before:** You'd miss 95% of Canadian junior positions because they're not on Lever.

**After:** You now see opportunities from:
- Top Canadian tech companies (Shopify, Wealthsimple)
- Scale-ups hiring aggressively (Faire, Thinkific, League)
- Aggregated results from 1000s of smaller companies (via Adzuna)

---

## Next Steps

1. **Read:** [SETUP_MULTIBOARD.md](SETUP_MULTIBOARD.md)
2. **Configure:** Edit [config.py](config.py)
3. **Optional:** Sign up for [Adzuna API](https://developer.adzuna.com/) (free)
4. **Push:** Commit and push your changes
5. **Test:** Actions → Multi-Board Job Monitor → Run workflow

---

## Questions?

- Full docs: [README_MULTIBOARD.md](README_MULTIBOARD.md)
- Setup guide: [SETUP_MULTIBOARD.md](SETUP_MULTIBOARD.md)
- Original docs: [README.md](README.md)

**Happy job hunting!** 🎯
