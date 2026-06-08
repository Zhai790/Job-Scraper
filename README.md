# Job Board Monitor 🎯

Automated job notification system that checks the [Lever job board](https://hire.lever.co/jobs/internal?location=Canada) daily and sends email alerts when junior/entry-level positions are posted.

## Features

- 🔍 Monitors job postings for specific keywords
- 📧 Sends formatted email notifications for new jobs
- 🤖 Runs automatically via GitHub Actions (daily at 9 AM UTC)
- 💾 Tracks seen jobs to avoid duplicate notifications
- 🎨 Beautiful HTML email format with direct apply links

## Keywords Monitored

The system matches job titles containing any of these keywords (case-insensitive):

- Junior
- New Grad
- Entry Level
- Associate
- Intern / Internship
- Co-op / Coop
- Graduate
- Early Career

## Setup Instructions

### 1. Fork/Clone this Repository

```bash
git clone https://github.com/YOUR_USERNAME/job-board-monitor.git
cd job-board-monitor
```

### 2. Configure GitHub Secrets

Go to your repository's **Settings → Secrets and variables → Actions** and add these secrets:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `SMTP_SERVER` | SMTP server address | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port (usually 587) | `587` |
| `SMTP_USER` | Your email address | `your-email@gmail.com` |
| `SMTP_PASSWORD` | Email app password | `your-app-password` |
| `RECIPIENT_EMAIL` | Where to send notifications | `your-email@gmail.com` |

#### Gmail Setup (Recommended)

1. Enable 2-factor authentication on your Google account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. Use `smtp.gmail.com` as the server and `587` as the port
4. Use your full Gmail address as `SMTP_USER`
5. Use the generated app password (16 characters) as `SMTP_PASSWORD`

### 3. Enable GitHub Actions

- Go to **Actions** tab in your repository
- Click "I understand my workflows, go ahead and enable them"

### 4. Test the Workflow

You can manually trigger the workflow to test:

1. Go to **Actions** tab
2. Click **Job Board Monitor** workflow
3. Click **Run workflow** → **Run workflow**
4. Check the logs and your email inbox

## How It Works

1. **GitHub Actions** runs the workflow daily at 9 AM UTC (configurable in `.github/workflows/job-monitor.yml`)
2. **Python script** (`monitor.py`) fetches the Lever job board
3. **Parses** job postings and filters by keywords
4. **Compares** with previously seen jobs (`seen_jobs.json`)
5. **Sends email** notification if new matching jobs are found
6. **Commits** updated `seen_jobs.json` back to the repository

## Customization

### Change Keywords

Edit the `KEYWORDS` list in `monitor.py`:

```python
KEYWORDS = [
    "junior",
    "new grad",
    "your-keyword-here",
]
```

### Change Schedule

Edit the cron expression in `.github/workflows/job-monitor.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Daily at 9 AM UTC
```

Common schedules:
- `'0 9 * * *'` - Daily at 9 AM UTC
- `'0 9 * * 1-5'` - Weekdays at 9 AM UTC
- `'0 */6 * * *'` - Every 6 hours
- `'0 9,17 * * *'` - Twice daily (9 AM and 5 PM UTC)

Use [crontab.guru](https://crontab.guru/) to generate cron expressions.

### Change Job Board URL

Edit the `JOB_BOARD_URL` in `monitor.py`:

```python
JOB_BOARD_URL = "https://hire.lever.co/jobs/internal?location=Your-Location"
```

## Local Testing

Test the script locally before pushing:

```bash
# Set environment variables
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="your-email@gmail.com"

# Run the script
python monitor.py
```

## Troubleshooting

### No Email Received

1. Check GitHub Actions logs for errors
2. Verify all secrets are set correctly
3. Check spam/junk folder
4. Test with a different email provider

### Parsing Errors

The job board HTML structure might change. If parsing fails:

1. Check the Actions logs for the error
2. Visit the job board URL manually to see if it's accessible
3. Update the regex pattern in `parse_jobs()` if needed

### Permission Errors

If the workflow can't commit `seen_jobs.json`:

1. Go to **Settings → Actions → General**
2. Under "Workflow permissions", select "Read and write permissions"
3. Click Save

## File Structure

```
job-board-monitor/
├── .github/
│   └── workflows/
│       └── job-monitor.yml    # GitHub Actions workflow
├── monitor.py                  # Main Python script
├── seen_jobs.json             # Tracked jobs (auto-generated)
└── README.md                  # This file
```

## License

MIT License - feel free to use and modify as needed!

## Contributing

Found a bug or want to add a feature? Pull requests are welcome!
