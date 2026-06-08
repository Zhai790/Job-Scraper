#!/usr/bin/env python3
"""
Multi-Board Job Monitor - Checks multiple job boards for junior/entry-level positions
Supports: Lever, Greenhouse, Indeed, Adzuna
Runs daily via GitHub Actions and sends email notifications for new jobs
"""

import json
import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Dict, Set

# Import configuration
from config import (
    LOCATION, KEYWORDS,
    LEVER_COMPANIES, GREENHOUSE_COMPANIES, INDEED_QUERIES, ADZUNA_QUERIES,
    ADZUNA_APP_ID, ADZUNA_APP_KEY,
    ENABLE_LEVER, ENABLE_GREENHOUSE, ENABLE_INDEED, ENABLE_ADZUNA
)

# Import scrapers
from scrapers import lever, greenhouse, indeed, adzuna

SEEN_JOBS_FILE = Path(__file__).parent / "seen_jobs.json"


def load_seen_jobs() -> Set[str]:
    """Load previously seen job IDs from JSON file"""
    if not SEEN_JOBS_FILE.exists():
        return set()

    try:
        with open(SEEN_JOBS_FILE, 'r') as f:
            data = json.load(f)
            return set(data.get('seen_job_ids', []))
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load seen jobs file: {e}")
        return set()


def save_seen_jobs(job_ids: Set[str]):
    """Save seen job IDs to JSON file"""
    try:
        with open(SEEN_JOBS_FILE, 'w') as f:
            json.dump({
                'seen_job_ids': sorted(list(job_ids)),
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)
    except IOError as e:
        print(f"Error: Could not save seen jobs file: {e}")


def filter_matching_jobs(jobs: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Filter jobs matching keywords in title"""
    matching = []

    for job in jobs:
        title_lower = job['title'].lower()

        for keyword in KEYWORDS:
            if keyword.lower() in title_lower:
                job['matched_keyword'] = keyword
                matching.append(job)
                break

    return matching


def send_email_notification(new_jobs: List[Dict[str, str]]):
    """Send email notification for new jobs"""
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    recipient = os.environ.get('RECIPIENT_EMAIL')

    if not all([smtp_user, smtp_password, recipient]):
        print("Error: Email credentials not configured (SMTP_USER, SMTP_PASSWORD, RECIPIENT_EMAIL)")
        return

    # Group jobs by source
    by_source = {}
    for job in new_jobs:
        source = job.get('source', 'Unknown')
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(job)

    # Build email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🎯 {len(new_jobs)} New Job{'s' if len(new_jobs) > 1 else ''} Found"
    msg['From'] = smtp_user
    msg['To'] = recipient

    # Plain text version
    text_body = f"Found {len(new_jobs)} new job posting(s) across {len(by_source)} job board(s):\n\n"

    for source, jobs in by_source.items():
        text_body += f"\n--- {source} ({len(jobs)} jobs) ---\n"
        for job in jobs:
            company = job.get('company', 'Unknown Company')
            text_body += f"• {job['title']}\n"
            text_body += f"  Company: {company.title()}\n"
            text_body += f"  Location: {job['location']} | {job['commitment']}\n"
            text_body += f"  Matched: {job['matched_keyword']}\n"
            text_body += f"  Apply: {job['url']}\n\n"

    # HTML version
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2>🎯 Found {len(new_jobs)} New Job Posting{'s' if len(new_jobs) > 1 else ''}</h2>
        <p>New opportunities from <strong>{len(by_source)} job board{'s' if len(by_source) > 1 else ''}</strong> matching your keywords:</p>
        <hr style="border: 1px solid #ddd;">
    """

    for source, jobs in by_source.items():
        html_body += f"""
        <h3 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px;">
          {source} ({len(jobs)} job{'s' if len(jobs) > 1 else ''})
        </h3>
        """

        for job in jobs:
            company = job.get('company', 'Unknown Company')
            html_body += f"""
            <div style="margin-bottom: 20px; padding: 15px; background-color: #f5f5f5; border-radius: 5px;">
              <h4 style="margin-top: 0; color: #2c3e50;">
                <a href="{job['url']}" style="color: #3498db; text-decoration: none;">{job['title']}</a>
              </h4>
              <p style="margin: 5px 0;">
                <strong>Company:</strong> {company.title()} |
                <strong>Location:</strong> {job['location']} |
                <strong>Type:</strong> {job['commitment']}
              </p>
              <p style="margin: 5px 0; color: #7f8c8d;">
                <em>Matched keyword: "{job['matched_keyword']}"</em>
              </p>
              <p style="margin: 10px 0 0 0;">
                <a href="{job['url']}" style="background-color: #3498db; color: white; padding: 8px 16px; text-decoration: none; border-radius: 3px; display: inline-block;">
                  Apply Now →
                </a>
              </p>
            </div>
            """

    html_body += """
        <hr style="border: 1px solid #ddd;">
        <p style="color: #7f8c8d; font-size: 12px;">
          Automated by Multi-Board Job Monitor
        </p>
      </body>
    </html>
    """

    msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    # Send email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        print(f"✓ Email sent to {recipient}")
    except Exception as e:
        print(f"Error sending email: {e}")


def main():
    """Main execution flow"""
    print(f"[{datetime.now().isoformat()}] Starting multi-board job monitor...")
    print(f"Location: {LOCATION}")
    print(f"Keywords: {', '.join(KEYWORDS)}\n")

    # Load seen jobs
    seen_jobs = load_seen_jobs()
    print(f"Previously seen jobs: {len(seen_jobs)}\n")

    # Fetch jobs from all enabled sources
    print("Fetching jobs from multiple boards...")
    all_jobs = []

    if ENABLE_LEVER and LEVER_COMPANIES:
        print(f"\n[LEVER] Checking {len(LEVER_COMPANIES)} companies...")
        all_jobs.extend(lever.fetch_jobs(LEVER_COMPANIES, LOCATION))

    if ENABLE_GREENHOUSE and GREENHOUSE_COMPANIES:
        print(f"\n[GREENHOUSE] Checking {len(GREENHOUSE_COMPANIES)} companies...")
        all_jobs.extend(greenhouse.fetch_jobs(GREENHOUSE_COMPANIES, LOCATION))

    if ENABLE_INDEED and INDEED_QUERIES:
        print(f"\n[INDEED] Searching {len(INDEED_QUERIES)} queries...")
        all_jobs.extend(indeed.fetch_jobs(INDEED_QUERIES, LOCATION))

    if ENABLE_ADZUNA and ADZUNA_QUERIES and ADZUNA_APP_ID and ADZUNA_APP_KEY:
        print(f"\n[ADZUNA] Searching {len(ADZUNA_QUERIES)} queries...")
        all_jobs.extend(adzuna.fetch_jobs(ADZUNA_QUERIES, LOCATION, ADZUNA_APP_ID, ADZUNA_APP_KEY))

    print(f"\n{'='*70}")
    print(f"Total jobs fetched: {len(all_jobs)}")

    # Filter matching jobs
    matching_jobs = filter_matching_jobs(all_jobs)
    print(f"Jobs matching keywords: {len(matching_jobs)}")

    # Find new jobs
    new_jobs = [job for job in matching_jobs if job['id'] not in seen_jobs]
    print(f"New jobs (not seen before): {len(new_jobs)}")

    if new_jobs:
        print(f"\n{'='*70}")
        print("NEW JOB POSTINGS:")
        print('='*70)

        for job in new_jobs:
            print(f"• {job['title']}")
            print(f"  Company: {job.get('company', 'Unknown')} | Source: {job.get('source', 'Unknown')}")
            print(f"  Keyword: {job['matched_keyword']}")
            print(f"  URL: {job['url']}\n")

        # Send notification
        send_email_notification(new_jobs)

        # Update seen jobs
        for job in new_jobs:
            seen_jobs.add(job['id'])
        save_seen_jobs(seen_jobs)
        print(f"✓ Updated seen jobs file ({len(seen_jobs)} total tracked)")
    else:
        print("\nNo new jobs found.")

    print(f"\n{'='*70}")
    print("Done!")


if __name__ == '__main__':
    main()
