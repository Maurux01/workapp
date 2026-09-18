"""Optional Supabase persistence. Works even if supabase is not installed/configured."""
from config import SUPABASE_URL, SUPABASE_KEY
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SupabaseStore:
    def __init__(self, url: str = SUPABASE_URL, key: str = SUPABASE_KEY):
        self.url = url
        self.key = key
        self.client = None
        if url and key:
            try:
                from supabase import create_client
                self.client = create_client(url, key)
            except ImportError:
                logger.warning("supabase package not installed. Run: pip install supabase")
            except Exception as exc:  # noqa: BLE001
                logger.warning(f"Supabase init failed: {exc}")

    @property
    def enabled(self) -> bool:
        return self.client is not None

    def save_jobs(self, jobs: list, table: str = "jobs") -> bool:
        """Upsert by url (see supabase/schema.sql). Falls back to plain insert."""
        if not self.enabled or not jobs:
            return False
        payload = [self._row(j) for j in jobs]
        try:
            self.client.table(table).upsert(payload, on_conflict="url").execute()
            logger.info(f"Supabase: saved {len(payload)} jobs to '{table}'")
            return True
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"Supabase upsert failed, trying insert: {exc}")
        try:
            self.client.table(table).insert(payload).execute()
            return True
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"Supabase save failed: {exc}")
            return False

    def load_jobs(self, table: str = "jobs", limit: int = 100) -> list:
        if not self.enabled:
            return []
        try:
            res = self.client.table(table).select("*").limit(limit).execute()
            return res.data or []
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"Supabase load failed: {exc}")
            return []

    @staticmethod
    def _row(job: dict) -> dict:
        """Trim internal-only keys (spam/match/score) before sending to Supabase."""
        skip = {"spam", "matched_skills", "missing_skills", "required_skills",
                "score", "short"}
        return {k: v for k, v in job.items() if k not in skip}
