"""Remotive scraper via its public JSON API (no key needed).

Docs: https://remotive.com/api — supports ?search= and ?limit=.
Strong for remote + freelance roles, many LATAM-friendly.
"""
from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)

_JT_MAP = {"full_time": "full_time", "part_time": "part_time",
           "contract": "freelance", "freelance": "freelance"}


class RemotiveScraper(BaseScraper):
    source_name = "remotive"
    API = "https://remotive.com/api/remote-jobs"

    def search(self, keyword: str, location: str = "", max_results: int = 20,
               filters: dict | None = None) -> list:
        modalities = (filters or {}).get("modalities") or []
        if modalities and "remote" not in modalities:
            return []  # remotive is remote-only
        data = self.get_json(self.API, params={"search": keyword,
                                               "limit": max_results})
        if not data:
            return []
        jobs = []
        for item in data.get("jobs", [])[:max_results]:
            title = item.get("title", "")
            if not title:
                continue
            jt = _JT_MAP.get((item.get("job_type") or "").lower(), "unknown")
            jobs.append({
                "title": title,
                "company_name": item.get("company_name", ""),
                "location": item.get("candidate_required_location") or "Remote",
                "description": (item.get("description") or title)[:2000],
                "url": item.get("url", ""),
                "source": self.source_name,
                "job_type": jt,
                "modality": "remote",
                "salary": item.get("salary") or "",
                "posted_at": item.get("publication_date", ""),
            })
        logger.info(f"[{self.source_name}] found {len(jobs)} jobs for '{keyword}'")
        return jobs
