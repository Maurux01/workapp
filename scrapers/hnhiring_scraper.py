"""Hacker News 'Who is hiring?' scraper via the public Algolia API.

Monthly freelance/remote-heavy thread. No key, CORS-open (works in browser too).
"""
import re
from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class HnhiringScraper(BaseScraper):
    source_name = "hnhiring"
    SEARCH = "https://hn.algolia.com/api/v1/search"
    ITEM = "https://hn.algolia.com/api/v1/items/{hid}"

    def search(self, keyword: str, location: str = "", max_results: int = 20,
               filters: dict | None = None) -> list:
        thread_id = self._latest_hiring_thread()
        if not thread_id:
            return []
        data = self.get_json(self.ITEM.format(hid=thread_id))
        if not data:
            return []
        kw = (keyword or "").lower().strip()
        jobs = []
        for comment in data.get("children", []):
            text = re.sub(r"<[^>]+>", " ", comment.get("text") or "")
            if kw and kw not in text.lower():
                continue
            title = text.strip().split("\n")[0][:150] or "HN hiring post"
            jobs.append({
                "title": title,
                "company_name": comment.get("author", ""),
                "location": "Remote",
                "description": text[:2000] or title,
                "url": f"https://news.ycombinator.com/item?id={comment.get('id')}",
                "source": self.source_name,
                "job_type": "freelance",
                "modality": "remote",
                "posted_at": comment.get("created_at", ""),
            })
            if len(jobs) >= max_results:
                break
        logger.info(f"[{self.source_name}] found {len(jobs)} jobs for '{keyword}'")
        return jobs

    def _latest_hiring_thread(self) -> int | None:
        data = self.get_json(self.SEARCH, params={
            "query": "Who is hiring", "tags": "story", "hitsPerPage": 10})
        if not data:
            return None
        for hit in data.get("hits", []):
            title = hit.get("title", "") or ""
            if "Who is hiring" in title and hit.get("objectID"):
                try:
                    return int(hit["objectID"])
                except (TypeError, ValueError):
                    continue
        return None
