"""Run all scrapers, normalize, filter by type/modality, dedupe, cache."""
from config import SCRAPER_CONFIG
from parsers.job_parser import normalize_job, is_valid_job, matches_filters
from scrapers.computrabajo_scraper import ComputrabajoScraper
from scrapers.arbeitnow_scraper import ArbeitnowScraper
from scrapers.indeed_scraper import IndeedScraper
from scrapers.jooble_scraper import JoobleScraper
from scrapers.linkedin_scraper import LinkedinScraper
from scrapers.remoteok_scraper import RemoteokScraper
from scrapers.remotive_scraper import RemotiveScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)

SAMPLE_JOBS = [
    {
        "title": "Python Developer",
        "company_name": "TechCorp Demo",
        "location": "Remote",
        "description": "Python developer with 2+ years in Django, SQL and Docker. Full-time, remote.",
        "url": "https://example.com/jobs/python-dev",
        "source": "sample",
        "job_type": "full_time",
        "modality": "remote",
    },
    {
        "title": "Data Analyst Junior",
        "company_name": "DataDemo",
        "location": "Bogotá",
        "description": "Excel, SQL, Power BI, Python pandas. Intermediate English. Full-time, on-site.",
        "url": "https://example.com/jobs/data-analyst",
        "source": "sample",
        "job_type": "full_time",
        "modality": "onsite",
    },
]


class ScraperManager:
    SOURCES = ("linkedin", "jooble", "remoteok", "remotive", "arbeitnow",
                 "indeed", "computrabajo")

    def __init__(self, use_cache: bool = True):
        # NOTE: occ scraper kept as best-effort module but out of the default
        # pool (bot-wall + JS-rendered results). Re-add when stable.
        self.scrapers = [
            LinkedinScraper(), JoobleScraper(), RemoteokScraper(),
            RemotiveScraper(), ArbeitnowScraper(),
            IndeedScraper(), ComputrabajoScraper(),
        ]
        self.use_cache = use_cache
        self._cache = None
        if use_cache:
            try:
                from storage.local_cache import LocalCache
                self._cache = LocalCache()
            except Exception:  # noqa: BLE001
                self._cache = None

    def search_all(self, keyword: str, location: str = "",
                   max_per_source: int | None = None,
                   job_types: list | None = None,
                   modalities: list | None = None,
                   sources: list | None = None) -> list:
        max_per_source = max_per_source or SCRAPER_CONFIG["max_results_per_source"]
        job_types = job_types or []
        modalities = modalities or []
        filters = {"job_types": job_types, "modalities": modalities}
        cache_key = f"{keyword}|{location}|{','.join(sorted(job_types))}|{','.join(sorted(modalities))}"
        if self._cache:
            cached = self._cache.get(cache_key)
            if cached:
                logger.info(f"Cache hit for '{cache_key}' ({len(cached)} jobs)")
                return cached

        wanted = set(sources) if sources else set(self.SOURCES)
        all_jobs: list = []
        for scraper in self.scrapers:
            if scraper.source_name not in wanted:
                continue
            try:
                raw = scraper.search(keyword, location, max_per_source, filters)
                for r in raw:
                    job = normalize_job({**r, "source": scraper.source_name})
                    if is_valid_job(job) and matches_filters(job, job_types, modalities):
                        all_jobs.append(job)
            except Exception as exc:  # noqa: BLE001
                logger.warning(f"Scraper {scraper.source_name} failed: {exc}")

        jobs = self._dedupe(all_jobs)
        if not jobs:
            logger.warning("All scrapers returned 0 jobs — using sample data.")
            jobs = [j for j in (normalize_job(x) for x in SAMPLE_JOBS)
                    if matches_filters(j, job_types, modalities)] or \
                   [normalize_job(x) for x in SAMPLE_JOBS]

        if self._cache:
            self._cache.set(cache_key, jobs)
        self._persist_supabase(jobs)
        return jobs

    @staticmethod
    def _persist_supabase(jobs: list) -> None:
        """Best-effort: save fresh results to Supabase if configured. Never breaks search."""
        try:
            from storage.supabase_client import SupabaseStore
            store = SupabaseStore()
            if store.enabled:
                store.save_jobs(jobs)
        except Exception:  # noqa: BLE001
            pass

    @staticmethod
    def _dedupe(jobs: list) -> list:
        seen, out = set(), []
        for j in jobs:
            key = (j["title"].lower(), j["company_name"].lower(), j["url"].lower())
            if key not in seen:
                seen.add(key)
                out.append(j)
        return out


if __name__ == "__main__":
    m = ScraperManager(use_cache=False)
    results = m.search_all("python", "Colombia")
    print(f"Found {len(results)} jobs")
    for j in results[:8]:
        print("-", j["source"], "|", j["title"][:60], "|", j["company_name"][:30],
              "|", j["job_type"], "|", j["modality"])
