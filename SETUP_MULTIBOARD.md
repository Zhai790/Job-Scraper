# Multi-Board Setup Guide

## Quick Setup (5 minutes)

### Step 1: Configure Job Boards

Edit **[config.py](config.py)**:

```python
# Add Greenhouse companies (most Canadian tech companies)
GREENHOUSE_COMPANIES = [
    "shopify",
    "wealthsimple",
    "faire",
    "thinkific",
    # Add more from the list below
]

# Add Lever companies (fewer Canadian companies)
LEVER_COMPANIES = [
    "magnetforensics",
    # Add more if you find them
]

# Optional: Add Adzuna API (free 1000 calls/month)
# Sign up at: https://developer.adzuna.com/
```

### Step 2: Push to GitHub

```bash
cd /d/job-board-monitor
git add -A
git commit -m "Configure multi-board monitoring"
git push origin main
```

### Step 3: Add GitHub Secrets

**Settings → Secrets → Actions → New repository secret**

**Email (Required):**
| Name | Value | Example |
|------|-------|---------|
| `SMTP_SERVER` | SMTP server | `smtp.gmail.com` |
| `SMTP_PORT` | Port number | `587` |
| `SMTP_USER` | Your email | `you@gmail.com` |
| `SMTP_PASSWORD` | App password | Get from [here](https://myaccount.google.com/apppasswords) |
| `RECIPIENT_EMAIL` | Alert email | `you@gmail.com` |

**Adzuna API (Optional but recommended):**
| Name | Value | Get from |
|------|-------|----------|
| `ADZUNA_APP_ID` | Your App ID | [developer.adzuna.com](https://developer.adzuna.com/) |
| `ADZUNA_APP_KEY` | Your App Key | [developer.adzuna.com](https://developer.adzuna.com/) |

### Step 4: Enable Workflow Permissions

**Settings → Actions → General**
- Scroll to "Workflow permissions"
- Select **"Read and write permissions"**
- Save

### Step 5: Run It!

**Actions → Multi-Board Job Monitor → Run workflow**

Check the logs to see jobs being fetched!

---

## Popular Canadian Companies by Job Board

### Greenhouse (Best Coverage)

```python
GREENHOUSE_COMPANIES = [
    # Big Tech
    "shopify",
    "wealthsimple",
    
    # Scale-ups
    "faire",
    "thinkific",
    "league",
    "ritual",
    "koho",
    "clearco",
    
    # Fintech
    "neofinancial",
    "borrowell",
    "mogo",
    
    # Others
    "benchaccounting",
    "tulipretail",
    "freshbooks",
]
```

**How to find more:**
1. Go to company careers page
2. Look for URL: `https://boards.greenhouse.io/{company}/jobs`
3. Add `{company}` to the list

### Lever (Limited Coverage)

```python
LEVER_COMPANIES = [
    "magnetforensics",
    # Most Canadian companies don't use Lever
]
```

### Adzuna (Aggregator - Best Coverage Overall)

Sign up for free API: https://developer.adzuna.com/

```python
ADZUNA_QUERIES = [
    "junior software engineer Canada",
    "new grad developer Toronto",
    "entry level programmer Vancouver",
    "software intern Montreal",
]
```

---

## Workflow Options

You have two workflows now:

### Option A: Use Both Workflows

Keep both `job-monitor.yml` (Lever-only) and `job-monitor-multi.yml` running. They share the same `seen_jobs.json` file, so you won't get duplicate notifications.

### Option B: Use Only Multi-Board (Recommended)

1. Delete `.github/workflows/job-monitor.yml`
2. Rename `job-monitor-multi.yml` to `job-monitor.yml`

```bash
cd /d/job-board-monitor
rm .github/workflows/job-monitor.yml
mv .github/workflows/job-monitor-multi.yml .github/workflows/job-monitor.yml
git add -A
git commit -m "Switch to multi-board monitoring"
git push origin main
```

---

## Testing Locally

```bash
cd /d/job-board-monitor

# Windows (PowerShell)
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SMTP_USER="your-email@gmail.com"
$env:SMTP_PASSWORD="your-app-password"
$env:RECIPIENT_EMAIL="your-email@gmail.com"

# Run test
python monitor_multiboard.py
```

---

## Troubleshooting

### No jobs found?

**Check enabled scrapers in config.py:**
```python
ENABLE_LEVER = True
ENABLE_GREENHOUSE = True
ENABLE_INDEED = False  # May be blocked
ENABLE_ADZUNA = True   # Requires API key
```

**Verify company names:**
- Visit the company's careers page
- Check the job board URL
- Use the exact identifier from the URL

### Indeed returns 403 Forbidden?

Indeed actively blocks scrapers. This is expected. Options:
1. Use Adzuna instead (free API, more reliable)
2. Keep Indeed disabled: `ENABLE_INDEED = False`

### Greenhouse returns "Not found"?

The company doesn't use Greenhouse. Try:
- Visiting their careers page to see what platform they use
- Searching for them on Adzuna instead

### No keywords matching?

Your keywords might be too restrictive. Try broader terms:
```python
KEYWORDS = [
    "software",        # Broader
    "developer",       # Broader
    "engineer",        # Broader
    "junior",
    "new grad",
]
```

Then filter the email results manually.

---

## Advanced: Add More Job Boards

Want to add Workday, Ashby, or other platforms? Create a new scraper in `scrapers/`:

```python
# scrapers/workday.py

def fetch_jobs(companies, location):
    """Fetch jobs from Workday"""
    # Implementation here
    return []
```

Then add it to `config.py` and `monitor_multiboard.py`.

---

## Cost

Everything is **FREE**:
- ✅ GitHub Actions: 2000 minutes/month free
- ✅ Lever API: Free public access
- ✅ Greenhouse API: Free public access
- ✅ Adzuna API: 1000 calls/month free
- ⚠️ Indeed: Blocked (no reliable free access)

---

## Support

- Read [README_MULTIBOARD.md](README_MULTIBOARD.md) for full documentation
- Check GitHub Actions logs for detailed error messages
- Open an issue if you find a bug

---

**You're all set!** 🎉

The monitor will run daily and email you when new junior/entry-level positions are posted.
