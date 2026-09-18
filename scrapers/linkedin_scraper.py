"""LinkedIn public guest API scraper (no login required).

Uses https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search
which returns HTML cards and is the standard public endpoint.
"""
from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LinkedinScraper(BaseScraper):
    source_name = "linkedin"
    API = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

    # LinkedIn guest API codes
    JT_CODES = {"full_time": "F", "part_time": "P", "freelance": "C", "internship": "I"}
    WT_CODES = {"onsite": "1", "remote": "2", "hybrid": "3"}

    def search(self, keyword: str, location: str = "", max_results: int = 20,
               filters: dict | None = None) -> list:
        params = {"keywords": keyword, "location": location or "Colombia", "start": 0}
        filters = filters or {}
        jt = [self.JT_CODES[j] for j in (filters.get("job_types") or []) if j in self.JT_CODES]
        wt = [self.WT_CODES[m] for m in (filters.get("modalities") or []) if m in self.WT_CODES]
        if jt:
            params["f_JT"] = ",".join(jt)
        if wt:
            params["f_WT"] = ",".join(wt)
        soup = self.get_soup(self.API, params=params)
        if soup is None:
            return []
        jobs = []
        for li in soup.select("li")[:max_results]:
            title_el = li.select_one("h3.base-search-card__title")
            company_el = li.select_one("h4.base-search-card__subtitle")
            loc_el = li.select_one("span.job-search-card__location")
            link_el = li.select_one("a.base-card__full-link")
            title = title_el.get_text(strip=True) if title_el else ""
            if not title:
                continue
            jobs.append({
                "title": title,
                "company_name": company_el.get_text(strip=True) if company_el else "",
                "location": loc_el.get_text(strip=True) if loc_el else location,
                "description": title,  # list view has no full desc; detail fetch optional
                "url": (link_el.get("href", "").split("?")[0] if link_el else ""),
                "source": self.source_name,
            })
        logger.info(f"[{self.source_name}] found {len(jobs)} jobs for '{keyword}'")
        return jobs
