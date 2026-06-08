#!/usr/bin/env python3
"""
Job Board Monitor - Checks Lever job board for junior/entry-level positions
Runs daily via GitHub Actions and sends email notifications for new jobs
"""

import json
import os
import re
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Dict, Set
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Configuration
# You can monitor multiple companies by adding them to this list
# Find company names from their Lever job board URL
COMPANIES = [
    "magnetforensics",  # Example - replace with your target company
]

LOCATION = "Canada"  # Filter by location
SEEN_JOBS_FILE = Path(__file__).parent / "seen_jobs.json"

# Keywords to match (case-insensitive)
KEYWORDS = [
    "junior",
    "new grad",
    "entry level",
    "associate",
    "graduate",
    "early career",
]


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


def fetch_jobs_from_api(company: str) -> List[Dict[str, str]]:
    """Fetch jobs from Lever's public API for a specific company"""
    url = f"https://api.lever.co/v0/postings/{company}"
    if LOCATION:
        url += f"?location={LOCATION}"

    try:
        req = Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))

        if not isinstance(data, list):
            print(f"Warning: Unexpected response format for {company}")
            return []

        jobs = []
        for job_data in data:
            # Extract location from categories
            categories = job_data.get('categories', {})
            location = categories.get('location', 'Remote')
            commitment = categories.get('commitment', 'Full-time')

            jobs.append({
                'id': job_data.get('id', ''),
                'title': job_data.get('text', 'Unknown'),
                'url': job_data.get('hostedUrl', ''),
                'location': location,
                'commitment': commitment,
                'company': company
            })

        return jobs

    except (HTTPError, URLError) as e:
        print(f"Error fetching jobs for {company}: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON for {company}: {e}")
        return []


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

    # Build email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🎯 {len(new_jobs)} New Job{'s' if len(new_jobs) > 1 else ''} Found on Lever"
    msg['From'] = smtp_user
    msg['To'] = recipient

    # Plain text version
    text_body = f"Found {len(new_jobs)} new job posting(s):\n\n"
    for job in new_jobs:
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
        <p>New opportunities matching your keywords on the Lever job board:</p>
        <hr style="border: 1px solid #ddd;">
    """

    for job in new_jobs:
        company = job.get('company', 'Unknown Company')
        html_body += f"""
        <div style="margin-bottom: 20px; padding: 15px; background-color: #f5f5f5; border-radius: 5px;">
          <h3 style="margin-top: 0; color: #2c3e50;">
            <a href="{job['url']}" style="color: #3498db; text-decoration: none;">{job['title']}</a>
          </h3>
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
          Automated by Job Monitor
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
    print(f"[{datetime.now().isoformat()}] Starting job monitor...")
    print(f"Companies: {', '.join(COMPANIES)}")
    print(f"Location: {LOCATION}")
    print(f"Keywords: {', '.join(KEYWORDS)}")

    # Load seen jobs
    seen_jobs = load_seen_jobs()
    print(f"Previously seen jobs: {len(seen_jobs)}")

    # Fetch jobs from all companies
    print("\nFetching jobs...")
    all_jobs = []
    for company in COMPANIES:
        print(f"  Checking {company}...")
        company_jobs = fetch_jobs_from_api(company)
        print(f"    Found {len(company_jobs)} jobs")
        all_jobs.extend(company_jobs)

    print(f"\nTotal jobs found: {len(all_jobs)}")

    # Filter matching jobs
    matching_jobs = filter_matching_jobs(all_jobs)
    print(f"Matching jobs: {len(matching_jobs)}")

    # Find new jobs
    new_jobs = [job for job in matching_jobs if job['id'] not in seen_jobs]
    print(f"New jobs: {len(new_jobs)}")

    if new_jobs:
        print("\nNew job postings:")
        for job in new_jobs:
            print(f"  • {job['title']} at {job.get('company', 'Unknown')} ({job['matched_keyword']})")
            print(f"    {job['url']}")

        # Send notification
        send_email_notification(new_jobs)

        # Update seen jobs
        for job in new_jobs:
            seen_jobs.add(job['id'])
        save_seen_jobs(seen_jobs)
        print(f"\n✓ Updated seen jobs file ({len(seen_jobs)} total)")
    else:
        print("No new jobs found.")

    print("Done!")


if __name__ == '__main__':
    main()
