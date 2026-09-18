"""Indeed scraper (MX). Best-effort HTML parsing."""
from urllib.parse import quote_plus
from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class IndeedScraper(BaseScraper):
    source_name = "indeed"
    BASE = "https://co.indeed.com"

    JT_MAP = {"full_time": "fulltime", "part_time": "parttime",
              "freelance": "contract", "internship": "internship"}

    def search(self, keyword: str, location: str = "", max_results: int = 20,
               filters: dict | None = None) -> list:
        params = {"q": keyword, "l": location, "limit": max_results}
        filters = filters or {}
        jt = (filters.get("job_types") or [])
        if len(jt) == 1 and jt[0] in self.JT_MAP:
            params["jt"] = self.JT_MAP[jt[0]]
        if (filters.get("modalities") or []) == ["remote"]:
            params["q"] += " remote"
        soup = self.get_soup(f"{self.BASE}/jobs", params=params)
        if soup is None:
            return []
        jobs = []
        for card in soup.select("div.job_seen_beacon, div.jobsearch-ResultsList > div")[:max_results]:
            title_el = card.select_one("h2.jobTitle a, h2.jobTitle span")
            title = title_el.get_text(strip=True).replace("new", "") if title_el else ""
            link_el = card.select_one("h2.jobTitle a")
            link = link_el.get("href", "") if link_el else ""
            if link and link.startswith("/"):
                link = self.BASE + link
            company = card.select_one("span.companyName, [data-testid='company-name']")
            loc = card.select_one("div.companyLocation, [data-testid='text-location']")
            snippet = card.select_one("div.job-snippet, ul.job-snippet")
            if not title:
                continue
            jobs.append({
                "title": title,
                "company_name": company.get_text(strip=True) if company else "",
                "location": loc.get_text(strip=True) if loc else location,
                "description": snippet.get_text(" ", strip=True) if snippet else title,
                "url": link,
                "source": self.source_name,
            })
        logger.info(f"[{self.source_name}] found {len(jobs)} jobs for '{keyword}'")
        return jobs
