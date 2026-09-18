"""Misc helpers: safe filenames, truncation, language."""
import re
from pathlib import Path


def safe_filename(name: str) -> str:
    name = re.sub(r"[^\w\-. ]+", "_", name).strip()
    return name[:120] or "file"


def truncate(text: str, limit: int = 300) -> str:
    text = (text or "").strip()
    return text if len(text) <= limit else text[:limit].rstrip() + "…"


def detect_lang(text: str) -> str:
    """Very naive ES/EN detection based on stopwords."""
    text = (text or "").lower()
    es_hits = sum(w in text for w in [" de ", " la ", " que ", " trabajo ", " experiencia "])
    en_hits = sum(w in text for w in [" the ", " and ", " job ", " experience ", " with "])
    return "es" if es_hits >= en_hits else "en"


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
