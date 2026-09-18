"""OCCMundial scraper (MX). Best-effort HTML parsing of public search results."""
from urllib.parse import quote_plus
from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class OccScraper(BaseScraper):
    source_name = "occ"
    BASE = "https://www.occ.com.mx"

    def search(self, keyword: str, location: str = "", max_results: int = 20,
               filters: dict | None = None) -> list:
        q = quote_plus(keyword.strip().replace(" ", "-").lower())
        url = f"{self.BASE}/empleos/de-{q}/"
        soup = self.get_soup(url)
        if soup is None:
            return []
        jobs = []
        cards = soup.select("div.job-card, div.Card, article, div[data-testid='job-card']")
        for card in cards[:max_results]:
            link_el = card.select_one("a[href*='/empleo'], a[href*='/oferta'], h2 a, a")
            title_el = card.select_one("h2, h3, div.job-title")
            title = (title_el.get_text(strip=True) if title_el else "") or \
                    (link_el.get_text(strip=True) if link_el else "")
            if not title or len(title) < 3:
                continue
            link = link_el.get("href", "") if link_el else ""
            if link and link.startswith("/"):
                link = self.BASE + link
            company = card.select_one("span.company, div.company, p.company")
            loc = card.select_one("span.location, div.location")
            desc = card.select_one("p.description, div.description")
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
