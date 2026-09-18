"""Jooble scraper (MX). Best-effort HTML parsing of public search results."""
from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class JoobleScraper(BaseScraper):
    source_name = "jooble"
    BASE = "https://co.jooble.org"

    def search(self, keyword: str, location: str = "", max_results: int = 20,
               filters: dict | None = None) -> list:
        params = {"ukw": keyword, "rgns": location or "Colombia"}
        soup = self.get_soup(f"{self.BASE}/SearchResult", params=params)
        if soup is None:
            return []
        jobs = []
        cards = soup.select("article._0653c0, div.vacancy-card, article[data-test='vacancy'], td.result")
        if not cards:
            # generic fallback: any article with a link + heading
            cards = soup.select("article")
        for card in cards[:max_results]:
            link_el = card.select_one("a[href*='/vacancy'], a.job-link, h2 a, a")
            title_el = card.select_one("h2, span._0d4589, div.caption")
            title = (title_el.get_text(strip=True) if title_el else "") or \
                    (link_el.get_text(strip=True) if link_el else "")
            if not title or len(title) < 3:
                continue
            link = link_el.get("href", "") if link_el else ""
            if link and link.startswith("/"):
                link = self.BASE + link
            company = card.select_one("span._786d9c, div.company, p.company")
            loc = card.select_one("span.caption, div.location, span.location")
            desc = card.select_one("div._5b9d9a, p.description, div.description")
            jobs.append({
                "title": title[:150],
                "company_name": company.get_text(strip=True) if company else "",
                "location": loc.get_text(strip=True) if loc else location,
                "description": desc.get_text(" ", strip=True) if desc else title,
                "url": link,
                "source": self.source_name,
            })
        logger.info(f"[{self.source_name}] found {len(jobs)} jobs for '{keyword}'")
        return jobs
