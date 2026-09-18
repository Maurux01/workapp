"""Arbeitnow scraper via its public JSON API (no key needed).

https://www.arbeitnow.com/api/job-board-api returns all recent jobs;
we filter by keyword client-side. Only remote jobs are kept so
location-based searches (e.g. Colombia) don't get EU onsite noise.
"""
import re
from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ArbeitnowScraper(BaseScraper):
    source_name = "arbeitnow"
    API = "https://www.arbeitnow.com/api/job-board-api"

    def search(self, keyword: str, location: str = "", max_results: int = 20,
               filters: dict | None = None) -> list:
        modalities = (filters or {}).get("modalities") or []
        if modalities and "remote" not in modalities:
            return []  # we only surface remote roles from this board
        data = self.get_json(self.API)
        if not data:
            return []
        kw = (keyword or "").lower().strip()
        jobs = []
        for item in data.get("data", []):
            if not item.get("remote"):
                continue
            title = item.get("title", "")
            tags = " ".join(item.get("tags", []) or [])
            blob = f"{title} {tags} {item.get('company_name','')}".lower()
            if kw and kw not in blob:
                continue
            desc = re.sub(r"<[^>]+>", " ", item.get("description") or "")[:2000]
            jobs.append({
                "title": title,
                "company_name": item.get("company_name", ""),
                "location": item.get("location") or "Remote",
                "description": desc or title,
                "url": item.get("url", ""),
                "source": self.source_name,
                "modality": "remote",
                "posted_at": str(item.get("created_at", "")),
            })
            if len(jobs) >= max_results:
                break
        logger.info(f"[{self.source_name}] found {len(jobs)} jobs for '{keyword}'")
        return jobs
