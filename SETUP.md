# Quick Setup Guide

## Step 1: Push to GitHub

```bash
cd /d/job-board-monitor

# Create a new repository on GitHub (https://github.com/new)
# Then run these commands:

git remote add origin https://github.com/YOUR_USERNAME/job-board-monitor.git
git branch -M main
git push -u origin main
```

## Step 2: Configure Companies to Monitor

Edit `monitor.py` and update the `COMPANIES` list:

```python
COMPANIES = [
    "magnetforensics",  # Replace with your target companies
    "shopify",
    "1password",
]
```

**How to find a company's Lever name:**
1. Go to the company's careers page
2. If they use Lever, the URL will be: `https://jobs.lever.co/{company-name}`
3. Use that `{company-name}` in the COMPANIES list

**Common Canadian tech companies on Lever:**
- `magnetforensics`
- `shopify`
- `1password`
- `wealthsimple`
- `ritual`
- `clearbanc`

## Step 3: Configure Email (GitHub Secrets)

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**

Add these 5 secrets:

### For Gmail Users (Recommended):

1. **SMTP_SERVER**: `smtp.gmail.com`
2. **SMTP_PORT**: `587`
3. **SMTP_USER**: Your Gmail address (e.g., `you@gmail.com`)
4. **SMTP_PASSWORD**: 
   - Go to https://myaccount.google.com/apppasswords
   - Enable 2FA first if not enabled
   - Generate an "App Password" (16 characters)
   - Use that password here
5. **RECIPIENT_EMAIL**: Email where you want notifications (e.g., `you@gmail.com`)

### For Other Email Providers:

| Provider | SMTP_SERVER | SMTP_PORT |
|----------|-------------|-----------|
| **Outlook/Hotmail** | `smtp-mail.outlook.com` | `587` |
| **Yahoo** | `smtp.mail.yahoo.com` | `587` |
| **ProtonMail** | `smtp.protonmail.ch` | `587` |

## Step 4: Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. Enable "Read and write permissions":
   - Go to **Settings** → **Actions** → **General**
   - Scroll to "Workflow permissions"
   - Select **"Read and write permissions"**
   - Click Save

## Step 5: Test It!

Manually trigger the workflow to test:

1. Go to **Actions** tab
2. Click **"Job Board Monitor"** workflow
3. Click **"Run workflow"** button (top right)
4. Click green **"Run workflow"** button
5. Wait ~30 seconds, then refresh
6. Click on the workflow run to see logs
7. Check your email inbox

## Step 6: Configure Schedule (Optional)

The workflow runs daily at 9 AM UTC by default.

To change it, edit `.github/workflows/job-monitor.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Modify this line
```

**Common schedules:**
- `'0 9 * * *'` - Daily at 9 AM UTC
- `'0 9 * * 1-5'` - Weekdays only at 9 AM UTC
- `'0 */6 * * *'` - Every 6 hours
- `'0 9,17 * * *'` - Twice daily (9 AM and 5 PM UTC)

Use https://crontab.guru to create custom schedules.

## Troubleshooting

### No email received?
1. Check GitHub Actions logs for errors
2. Verify all 5 secrets are set correctly
3. Check your spam/junk folder
4. Try running the workflow manually

### "Workflow permissions" error?
- Enable "Read and write permissions" in Settings → Actions → General

### Want to add more keywords?
Edit the `KEYWORDS` list in `monitor.py`:
```python
KEYWORDS = [
    "junior",
    "your custom keyword",
]
```

### Want to change location filter?
Edit `LOCATION` in `monitor.py`:
```python
LOCATION = "Canada"  # or "Remote", "Toronto", etc.
```

## What Happens Next?

- The workflow runs automatically based on the schedule
- When new matching jobs are found, you'll get an email
- The workflow commits `seen_jobs.json` to track what's been sent
- You'll only get notified once per job posting

## Example Email

You'll receive a nicely formatted email like:

```
🎯 2 New Jobs Found on Lever

• Junior Software Engineer
  Company: Magnetforensics
  Location: Waterloo, ON | Full-time
  Matched: "junior"
  [Apply Now →]

• New Grad - Backend Developer
  Company: Shopify
  Location: Toronto, ON | Full-time  
  Matched: "new grad"
  [Apply Now →]
```

---

**Questions?** Open an issue in the repository!
