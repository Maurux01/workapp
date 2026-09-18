"""Base class for all scrapers."""
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from config import SCRAPER_CONFIG
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseScraper(ABC):
    source_name = "base"

    def __init__(self, timeout: int | None = None):
        self.timeout = timeout or SCRAPER_CONFIG["timeout"]
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": SCRAPER_CONFIG["user_agent"]})

    def get_soup(self, url: str, params: dict | None = None) -> BeautifulSoup | None:
        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "lxml")
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"[{self.source_name}] request failed {url}: {exc}")
            return None

    def get_json(self, url: str, params: dict | None = None):
        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"[{self.source_name}] JSON request failed {url}: {exc}")
            return None

    @abstractmethod
    def search(self, keyword: str, location: str = "", max_results: int = 20,
               filters: dict | None = None) -> list:
        """filters: {'job_types': [...], 'modalities': [...]}. Sites apply what they support."""
        raise NotImplementedError
