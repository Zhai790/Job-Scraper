"""
Configuration for multi-board job monitor
Edit this file to customize your job search
"""

import os

# ============================================================================
# SEARCH CONFIGURATION
# ============================================================================

# Location filter (applied to all scrapers)
LOCATION = "Canada"

# Keywords to match in job titles (case-insensitive)
KEYWORDS = [
    "junior",
    "new grad",
    "entry level",
    "associate",
    "intern",
    "internship",
    "co-op",
    "coop",
    "graduate",
    "early career",
]

# ============================================================================
# LEVER - Companies using Lever (https://jobs.lever.co/{company})
# ============================================================================
LEVER_COMPANIES = [
    "magnetforensics",
    # Add more: Find company name from their Lever careers URL
]

# ============================================================================
# GREENHOUSE - Companies using Greenhouse (https://boards.greenhouse.io/{company})
# ============================================================================
GREENHOUSE_COMPANIES = [
    "shopify",
    "wealthsimple",
    "faire",
    "benchaccounting",
    "thinkific",
    # Add more: Find board token from their Greenhouse careers URL
]

# ============================================================================
# INDEED - Search queries (will search Indeed.ca with these terms)
# ============================================================================
# WARNING: Indeed actively blocks scrapers. This may not work reliably.
# Consider using Adzuna API instead for more reliable results.
INDEED_QUERIES = [
    "junior software engineer",
    "new grad developer",
    "entry level programmer",
    # Add more search queries
]

# ============================================================================
# ADZUNA - Free API (requires sign-up at https://developer.adzuna.com/)
# ============================================================================
# Free tier: 1000 API calls/month
# Get credentials: https://developer.adzuna.com/
ADZUNA_APP_ID = os.environ.get('ADZUNA_APP_ID')
ADZUNA_APP_KEY = os.environ.get('ADZUNA_APP_KEY')

ADZUNA_QUERIES = [
    "junior software",
    "new grad developer",
    # Add more search queries
]

# ============================================================================
# SCRAPER CONTROL - Enable/disable specific scrapers
# ============================================================================
ENABLE_LEVER = True
ENABLE_GREENHOUSE = True
ENABLE_INDEED = False  # Disabled by default - Indeed blocks scrapers (use Adzuna instead)
ENABLE_ADZUNA = bool(ADZUNA_APP_ID and ADZUNA_APP_KEY)  # Auto-enable if credentials present
