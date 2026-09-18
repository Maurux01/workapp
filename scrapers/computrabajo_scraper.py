"""Computrabajo scraper (MX/CO/ES generic). Best-effort HTML parsing."""
from urllib.parse import quote_plus
from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ComputrabajoScraper(BaseScraper):
    source_name = "computrabajo"
    BASE = "https://www.computrabajo.com.co"

    def search(self, keyword: str, location: str = "", max_results: int = 20,
               filters: dict | None = None) -> list:
        q = quote_plus(keyword.strip())
        url = f"{self.BASE}/trabajo-de-{q}/"
        params = {"q": keyword}
        if location:
            params["prov"] = location
        soup = self.get_soup(url, params=params if location else None)
        if soup is None:
            return []
        jobs = []
        # Computrabajo uses article.box_offer
        for art in soup.select("article.box_offer, article.js-offer")[:max_results]:
            a = art.select_one("a.js-o-link, a.o-link")
            title = (a.get_text(strip=True) if a else "") or (art.select_one("h2,h3").get_text(strip=True) if art.select_one("h2,h3") else "")
            link = a.get("href", "") if a else ""
            if link and link.startswith("/"):
                link = self.BASE + link
            company = art.select_one(".o-card_company, span.fs13, p.fs13")
            loc = art.select_one(".o-card_location, span.fs16")
            desc = art.select_one("p.o-card_description, p.fs13")
            jobs.append({
                "title": title,
                "company_name": company.get_text(strip=True) if company else "",
                "location": loc.get_text(strip=True) if loc else location,
                "description": desc.get_text(strip=True) if desc else title,
                "url": link,
                "source": self.source_name,
            })
        logger.info(f"[{self.source_name}] found {len(jobs)} jobs for '{keyword}'")
        return [j for j in jobs if j["title"]]
