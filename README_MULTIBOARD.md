# Multi-Board Job Monitor 🎯

Automated job notification system that checks **multiple job boards** daily and sends email alerts when junior/entry-level positions are posted.

## Supported Job Boards

| Board | Type | Setup Required | Canadian Jobs |
|-------|------|----------------|---------------|
| **Lever** | API | ✅ No | ⭐⭐ Limited |
| **Greenhouse** | API | ✅ No | ⭐⭐⭐⭐ Excellent (Shopify, Wealthsimple, etc.) |
| **Indeed** | Scraping | ✅ No | ⭐⭐⭐⭐⭐ Best coverage |
| **Adzuna** | API | ⚠️ Free API key required | ⭐⭐⭐⭐ Very good |

## Quick Start

### 1. Configure Job Boards

Edit **[config.py](config.py)** to customize your search:

```python
# Location filter
LOCATION = "Canada"

# Keywords to match in job titles
KEYWORDS = [
    "junior",
    "new grad",
    "entry level",
    # ... add more
]

# Lever companies (e.g., Magnet Forensics)
LEVER_COMPANIES = [
    "magnetforensics",
]

# Greenhouse companies (Shopify, Wealthsimple, etc.)
GREENHOUSE_COMPANIES = [
    "shopify",
    "wealthsimple",
    "faire",
]

# Indeed search queries
INDEED_QUERIES = [
    "junior software engineer",
    "new grad developer",
]

# Enable/disable specific scrapers
ENABLE_LEVER = True
ENABLE_GREENHOUSE = True
ENABLE_INDEED = True
ENABLE_ADZUNA = False  # Requires API key
```

### 2. Push to GitHub

```bash
git add -A
git commit -m "Configure job boards"
git push origin main
```

### 3. Add GitHub Secrets

Go to **Settings → Secrets → Actions** and add:

**Required (Email):**
- `SMTP_SERVER` - e.g., `smtp.gmail.com`
- `SMTP_PORT` - e.g., `587`
- `SMTP_USER` - Your email address
- `SMTP_PASSWORD` - Gmail app password ([get it here](https://myaccount.google.com/apppasswords))
- `RECIPIENT_EMAIL` - Where to send alerts

**Optional (Adzuna API):**
- `ADZUNA_APP_ID` - Sign up at [developer.adzuna.com](https://developer.adzuna.com/)
- `ADZUNA_APP_KEY` - Free tier: 1000 calls/month

### 4. Enable Workflow

1. Go to **Actions** tab
2. Click **"I understand my workflows"**
3. **Settings → Actions → General** → Enable "Read and write permissions"

### 5. Test It

**Actions → Multi-Board Job Monitor → Run workflow**

Check logs and your email!

---

## Finding Company Identifiers

### Greenhouse

Visit the company's careers page. If they use Greenhouse, the URL will be:
```
https://boards.greenhouse.io/{company-token}/jobs
```

**Examples:**
- Shopify: `https://boards.greenhouse.io/shopify/jobs` → Use `"shopify"`
- Wealthsimple: `https://boards.greenhouse.io/wealthsimple/jobs` → Use `"wealthsimple"`

**Popular Canadian companies on Greenhouse:**
```python
GREENHOUSE_COMPANIES = [
    "shopify",          # Shopify
    "wealthsimple",     # Wealthsimple
    "faire",            # Faire
    "benchaccounting",  # Bench
    "thinkific",        # Thinkific
    "clearco",          # Clearco
    "league",           # League
    "ritual",           # Ritual
    "koho",             # KOHO
    "neofinancial",     # Neo Financial
    "borrowell",        # Borrowell
]
```

### Lever

Visit the company's careers page. If they use Lever, the URL will be:
```
https://jobs.lever.co/{company-name}
```

**Examples:**
- Magnet Forensics: `https://jobs.lever.co/magnetforensics` → Use `"magnetforensics"`

Lever is less popular in Canada. Most companies use Greenhouse or Indeed.

### Indeed

No configuration needed! Just add search queries:

```python
INDEED_QUERIES = [
    "junior software engineer Toronto",
    "new grad developer Vancouver",
    "entry level programmer Montreal",
    "software engineer intern",
]
```

### Adzuna

Requires free API key (1000 calls/month):
1. Sign up at https://developer.adzuna.com/
2. Get your App ID and App Key
3. Add as GitHub secrets: `ADZUNA_APP_ID` and `ADZUNA_APP_KEY`

---

## Email Notification Format

You'll receive grouped notifications:

```
🎯 Found 5 New Jobs

--- Greenhouse (3 jobs) ---
• Junior Software Engineer
  Company: Shopify | Location: Toronto, ON
  Matched: "junior"
  [Apply Now →]

--- Indeed (2 jobs) ---
• New Grad Developer
  Company: Wealthsimple | Location: Remote
  Matched: "new grad"
  [Apply Now →]
```

---

## Customization

### Change Schedule

Edit `.github/workflows/job-monitor-multi.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Daily at 9 AM UTC
  # - cron: '0 */6 * * *'  # Every 6 hours
  # - cron: '0 9 * * 1-5'  # Weekdays only
```

Use [crontab.guru](https://crontab.guru) to generate schedules.

### Add More Keywords

Edit `config.py`:

```python
KEYWORDS = [
    "junior",
    "graduate program",
    "rotational",
    "your custom keyword",
]
```

### Disable a Scraper

Edit `config.py`:

```python
ENABLE_INDEED = False  # Disable Indeed scraping
```

### Change Location

Edit `config.py`:

```python
LOCATION = "Toronto"  # Specific city
LOCATION = "Remote"   # Remote jobs
LOCATION = "Canada"   # Anywhere in Canada
```

---

## Local Testing

Test the monitor locally before deploying:

```bash
# Set environment variables
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="your-email@gmail.com"

# Optional: Adzuna API
export ADZUNA_APP_ID="your-app-id"
export ADZUNA_APP_KEY="your-app-key"

# Run the monitor
cd /d/job-board-monitor
python monitor_multiboard.py
```

---

## Troubleshooting

### Indeed not returning results?

Indeed actively fights scraping. The scraper may break if they change their HTML structure. Consider:
- Using Adzuna instead (more reliable API)
- Adjusting search queries to be more specific
- Reducing the number of queries to avoid rate limiting

### Greenhouse returning 404?

The company doesn't use Greenhouse. Check their careers page to see what platform they use.

### No email received?

1. Check GitHub Actions logs for errors
2. Verify all 5 email secrets are set correctly
3. Check spam/junk folder
4. Test locally with your credentials

### Want more job boards?

You can add more scrapers in the `scrapers/` directory. Common ones:
- **Workday** (used by large enterprises)
- **Ashby** (newer startups)
- **BambooHR**
- **JazzHR**

---

## File Structure

```
job-board-monitor/
├── .github/workflows/
│   ├── job-monitor.yml           # Original Lever-only workflow
│   └── job-monitor-multi.yml     # New multi-board workflow ✨
├── scrapers/
│   ├── __init__.py
│   ├── lever.py                  # Lever API scraper
│   ├── greenhouse.py             # Greenhouse API scraper
│   ├── indeed.py                 # Indeed HTML scraper
│   └── adzuna.py                 # Adzuna API scraper
├── config.py                     # Configuration (edit this!)
├── monitor.py                    # Original Lever-only script
├── monitor_multiboard.py         # New multi-board script ✨
├── seen_jobs.json                # Tracked jobs (auto-generated)
└── README_MULTIBOARD.md          # This file
```

---

## Migration from Original Script

If you're using the original `monitor.py` (Lever-only):

1. Keep both workflows active, or
2. Disable the old workflow:
   - Delete `.github/workflows/job-monitor.yml`
   - Rename `job-monitor-multi.yml` to `job-monitor.yml`

The `seen_jobs.json` file is shared between both scripts.

---

## License

MIT License - Use freely!

## Contributing

Found a bug or want to add a new scraper? Pull requests welcome!
