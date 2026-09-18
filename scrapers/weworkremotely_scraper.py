"""We Work Remotely scraper via its public RSS feeds (CORS-open too).

Main feed covers all categories; keyword filtering is client-side.
"""
import xml.etree.ElementTree as ET
from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class WeworkremotelyScraper(BaseScraper):
    source_name = "weworkremotely"
    FEED = "https://weworkremotely.com/remote-jobs.rss"

    def search(self, keyword: str, location: str = "", max_results: int = 20,
               filters: dict | None = None) -> list:
        modalities = (filters or {}).get("modalities") or []
        if modalities and "remote" not in modalities:
            return []  # WWR is remote-only
        try:
            resp = self.session.get(self.FEED, timeout=self.timeout)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"[{self.source_name}] feed failed: {exc}")
            return []
        kw = (keyword or "").lower().strip()
        jobs = []
        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            desc = (item.findtext("description") or "").strip()
            blob = f"{title} {desc}".lower()
            if kw and kw not in blob:
                continue
            jobs.append({
                "title": title,
                "company_name": "",
                "location": "Remote",
                "description": desc[:2000] or title,
                "url": link,
                "source": self.source_name,
                "modality": "remote",
                "posted_at": (item.findtext("pubDate") or "").strip(),
            })
            if len(jobs) >= max_results:
                break
        logger.info(f"[{self.source_name}] found {len(jobs)} jobs for '{keyword}'")
        return jobs
