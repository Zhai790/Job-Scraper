"""Greenhouse API scraper"""

import json
from typing import List, Dict
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def fetch_jobs(companies: List[str], location: str = "Canada") -> List[Dict[str, str]]:
    """
    Fetch jobs from Greenhouse's public API

    Args:
        companies: List of company board tokens (e.g., ["shopify", "wealthsimple"])
        location: Location filter keyword

    Returns:
        List of job dictionaries with: id, title, url, location, commitment, company, source
    """
    all_jobs = []

    for company in companies:
        url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

        try:
            req = Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            with urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))

            jobs = data.get('jobs', [])
            filtered_jobs = []

            for job_data in jobs:
                job_location = job_data.get('location', {}).get('name', '')

                # Filter by location if specified
                if location and location.lower() not in job_location.lower():
                    continue

                filtered_jobs.append({
                    'id': f"greenhouse_{job_data.get('id', '')}",
                    'title': job_data.get('title', 'Unknown'),
                    'url': job_data.get('absolute_url', ''),
                    'location': job_location,
                    'commitment': 'Full-time',  # Greenhouse doesn't always provide this
                    'company': company,
                    'source': 'Greenhouse'
                })

            all_jobs.extend(filtered_jobs)
            print(f"  [Greenhouse] {company}: {len(filtered_jobs)} jobs (filtered from {len(jobs)} total)")

        except HTTPError as e:
            if e.code == 404:
                print(f"  [Greenhouse] {company}: Not found (may not use Greenhouse)")
            else:
                print(f"  [Greenhouse] Error fetching {company}: {e}")
        except (URLError, json.JSONDecodeError) as e:
            print(f"  [Greenhouse] Error for {company}: {e}")

    return all_jobs
