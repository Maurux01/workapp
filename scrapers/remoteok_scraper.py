"""RemoteOK scraper via its public JSON API (no key needed).

Great for remote/freelance searches. Endpoint: https://remoteok.com/api
"""
from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class RemoteokScraper(BaseScraper):
    source_name = "remoteok"
    API = "https://remoteok.com/api"

    def search(self, keyword: str, location: str = "", max_results: int = 20,
               filters: dict | None = None) -> list:
        # RemoteOK is remote-only; skip unless remote wanted (or no modality filter)
        modalities = (filters or {}).get("modalities") or []
        if modalities and "remote" not in modalities:
            return []
        data = self.get_json(self.API)
        if not data:
            return []
        kw = keyword.lower().strip()
        jobs = []
        for item in data:
            if not isinstance(item, dict) or "position" not in item:
                continue
            title = item.get("position", "")
            tags = " ".join(item.get("tags", []) or [])
            blob = f"{title} {tags} {item.get('description','')}".lower()
            if kw and kw not in blob:
                continue
            jobs.append({
                "title": title,
                "company_name": item.get("company", ""),
                "location": "Remote / Remoto",
                "description": (item.get("description") or title)[:2000],
                "url": item.get("url", ""),
                "source": self.source_name,
                "modality": "remote",
                "salary": f"{item.get('salary_min','')}-{item.get('salary_max','')}" .strip("-"),
                "posted_at": item.get("date", ""),
            })
            if len(jobs) >= max_results:
                break
        logger.info(f"[{self.source_name}] found {len(jobs)} jobs for '{keyword}'")
        return jobs
