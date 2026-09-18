"""JSON file cache with TTL for job search results."""
import hashlib
import json
import time
from pathlib import Path
from config import CACHE_DIR, CACHE_TTL_HOURS
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LocalCache:
    def __init__(self, cache_dir: Path | str = CACHE_DIR, ttl_hours: int = CACHE_TTL_HOURS):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl_hours * 3600

    def _path(self, key: str) -> Path:
        h = hashlib.md5(key.encode("utf-8")).hexdigest()
        return self.cache_dir / f"{h}.json"

    def get(self, key: str) -> list | None:
        p = self._path(key)
        if not p.is_file():
            return None
        if time.time() - p.stat().st_mtime > self.ttl:
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"Cache read failed: {exc}")
            return None

    def set(self, key: str, data: list) -> None:
        try:
            self._path(key).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"Cache write failed: {exc}")

    def clear(self) -> int:
        n = 0
        for f in self.cache_dir.glob("*.json"):
            try:
                f.unlink()
                n += 1
            except OSError:
                pass
        return n
