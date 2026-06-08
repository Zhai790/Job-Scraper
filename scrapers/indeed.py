"""Indeed scraper (basic HTML parsing)"""

import re
from typing import List, Dict
from urllib.request import Request, urlopen
from urllib.parse import quote_plus
from urllib.error import URLError, HTTPError


def fetch_jobs(keywords: List[str], location: str = "Canada", max_results: int = 50) -> List[Dict[str, str]]:
    """
    Fetch jobs from Indeed (basic scraping - no API)

    Args:
        keywords: Search keywords (e.g., ["junior software engineer", "new grad developer"])
        location: Location (e.g., "Canada", "Toronto")
        max_results: Maximum number of results per keyword

    Returns:
        List of job dictionaries with: id, title, url, location, commitment, company, source

    Note: Indeed actively fights scraping. This is a basic implementation that may break.
    Consider using Indeed Publisher API if available.
    """
    all_jobs = []

    for keyword in keywords:
        query = quote_plus(keyword)
        loc = quote_plus(location)
        url = f"https://ca.indeed.com/jobs?q={query}&l={loc}&limit={min(max_results, 50)}"

        try:
            req = Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            )
            with urlopen(req, timeout=30) as response:
                html = response.read().decode('utf-8')

            # Parse job cards - Indeed's HTML structure (may change frequently)
            # Pattern: data-jk="job_id" ... <h2><a href="..." ...>Title</a></h2>
            job_pattern = re.compile(
                r'data-jk="([^"]+)".*?'
                r'<span[^>]*class="[^"]*companyName[^"]*"[^>]*>([^<]+)</span>.*?'
                r'<h2[^>]*>.*?<span[^>]*title="([^"]+)"',
                re.DOTALL
            )

            matches = job_pattern.findall(html)

            for job_id, company, title in matches[:max_results]:
                all_jobs.append({
                    'id': f"indeed_{job_id}",
                    'title': title.strip(),
                    'url': f"https://ca.indeed.com/viewjob?jk={job_id}",
                    'location': location,
                    'commitment': 'Full-time',
                    'company': company.strip(),
                    'source': 'Indeed'
                })

            print(f"  [Indeed] '{keyword}': {len(matches)} jobs")

        except (HTTPError, URLError) as e:
            print(f"  [Indeed] Error fetching '{keyword}': {e}")
        except Exception as e:
            print(f"  [Indeed] Parse error for '{keyword}': {e}")

    return all_jobs
