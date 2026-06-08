"""Adzuna API scraper - Free tier: 1000 calls/month"""

import json
from typing import List, Dict
from urllib.request import Request, urlopen
from urllib.parse import quote_plus
from urllib.error import URLError, HTTPError


def fetch_jobs(keywords: List[str], location: str = "Canada", app_id: str = None, app_key: str = None) -> List[Dict[str, str]]:
    """
    Fetch jobs from Adzuna API (requires free API key)

    Args:
        keywords: Search keywords
        location: Country code (ca for Canada, us for USA, uk for UK)
        app_id: Adzuna API application ID (get from https://developer.adzuna.com/)
        app_key: Adzuna API key

    Returns:
        List of job dictionaries with: id, title, url, location, commitment, company, source

    Note: Sign up at https://developer.adzuna.com/ for free API credentials
    Free tier: 1000 calls/month
    """
    if not app_id or not app_key:
        print("  [Adzuna] Skipped - requires API credentials (ADZUNA_APP_ID, ADZUNA_APP_KEY)")
        print("  [Adzuna] Sign up at https://developer.adzuna.com/ for free tier (1000 calls/month)")
        return []

    all_jobs = []
    country_code = "ca" if location.lower() == "canada" else "us"

    for keyword in keywords:
        query = quote_plus(keyword)
        url = (
            f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"
            f"?app_id={app_id}&app_key={app_key}"
            f"&what={query}"
            f"&results_per_page=50"
            f"&content-type=application/json"
        )

        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))

            results = data.get('results', [])

            for job_data in results:
                all_jobs.append({
                    'id': f"adzuna_{job_data.get('id', '')}",
                    'title': job_data.get('title', 'Unknown'),
                    'url': job_data.get('redirect_url', ''),
                    'location': job_data.get('location', {}).get('display_name', location),
                    'commitment': job_data.get('contract_type', 'Full-time'),
                    'company': job_data.get('company', {}).get('display_name', 'Unknown'),
                    'source': 'Adzuna'
                })

            print(f"  [Adzuna] '{keyword}': {len(results)} jobs")

        except (HTTPError, URLError) as e:
            print(f"  [Adzuna] Error fetching '{keyword}': {e}")
        except json.JSONDecodeError as e:
            print(f"  [Adzuna] JSON error for '{keyword}': {e}")

    return all_jobs
