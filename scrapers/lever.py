"""Lever API scraper"""

import json
from typing import List, Dict
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def fetch_jobs(companies: List[str], location: str = "Canada") -> List[Dict[str, str]]:
    """
    Fetch jobs from Lever's public API

    Args:
        companies: List of company identifiers (e.g., ["magnetforensics", "shopify"])
        location: Location filter (e.g., "Canada", "Remote")

    Returns:
        List of job dictionaries with: id, title, url, location, commitment, company, source
    """
    all_jobs = []

    for company in companies:
        url = f"https://api.lever.co/v0/postings/{company}"
        if location:
            url += f"?location={location}"

        try:
            req = Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            with urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))

            if not isinstance(data, list):
                print(f"  [Lever] Warning: Unexpected response for {company}")
                continue

            for job_data in data:
                categories = job_data.get('categories', {})
                all_jobs.append({
                    'id': f"lever_{job_data.get('id', '')}",
                    'title': job_data.get('text', 'Unknown'),
                    'url': job_data.get('hostedUrl', ''),
                    'location': categories.get('location', 'Remote'),
                    'commitment': categories.get('commitment', 'Full-time'),
                    'company': company,
                    'source': 'Lever'
                })

            print(f"  [Lever] {company}: {len(data)} jobs")

        except (HTTPError, URLError) as e:
            print(f"  [Lever] Error fetching {company}: {e}")
        except json.JSONDecodeError as e:
            print(f"  [Lever] JSON error for {company}: {e}")

    return all_jobs
