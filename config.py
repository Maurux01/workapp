"""Workapp global configuration. Bilingual (ES/EN)."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CV_DIR = DATA_DIR / "CVs"
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CV_DIR.mkdir(parents=True, exist_ok=True)

APP_NAME = "Workapp"
DEFAULT_LANG = os.getenv("WORKAPP_LANG", "es")
DEFAULT_LOCATION = os.getenv("WORKAPP_LOCATION", "Colombia")
CACHE_TTL_HOURS = int(os.getenv("CACHE_TTL_HOURS", "24"))

FAKE_DETECTION_CONFIG = {
    "risk_threshold": 5,
    "suspicious_keywords": [
        "get rich quick", "hazte rico", "sin experiencia",
        "no experience needed", "earn $$$", "gana $$$",
        "crypto", "mlm", "multinivel", "whatsapp only",
        "solo whatsapp", "pay for training", "paga por capacitacion",
        "paga por capacitación", "fee required", "depósito",
        "deposito", "giro", "money mule", "forex",
    ],
    "free_email_domains": [
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
        "live.com", "proton.me", "aol.com",
    ],
}

SCRAPER_CONFIG = {
    "timeout": 15,
    "user_agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "max_results_per_source": 20,
}

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Companies that never hire (ghost posts / spam). Case-insensitive substring
# match against company_name. Extend via BLOCKED_COMPANIES env (comma list).
_BLOCKED_EXTRA = [c.strip() for c in os.getenv("BLOCKED_COMPANIES", "").split(",") if c.strip()]
BLOCKED_COMPANIES = ["varesdev", *_BLOCKED_EXTRA]

# Evergreen / talent-pool bait typical of ghost jobs (both languages).
GHOST_KEYWORDS = [
    "talent pool", "bolsa de talento", "banco de talentos",
    "siempre estamos contratando", "always hiring",
    "unete a nuestra base de datos", "join our database",
    "futuras oportunidades", "future opportunities",
    "registro de candidatos", "candidate pool",
    "reclutamiento continuo", "ongoing recruitment",
]

TRANSLATIONS = {
    "es": {
        "app_tagline": "La forma inteligente de conseguir trabajo",
        "search": "Buscar", "upload_cv": "Subir CV (PDF)",
        "keyword": "Palabra clave", "location": "Ubicación",
        "results": "Resultados", "match": "Compatibilidad",
        "no_spam": "Oferta verificada", "is_spam": "Posible fraude",
        "analyze": "Analizar CV", "settings": "Ajustes",
        "language": "Idioma", "home": "Inicio",
    },
    "en": {
        "app_tagline": "The smart way to get a job",
        "search": "Search", "upload_cv": "Upload CV (PDF)",
        "keyword": "Keyword", "location": "Location",
        "results": "Results", "match": "Match",
        "no_spam": "Verified offer", "is_spam": "Possible scam",
        "analyze": "Analyze CV", "settings": "Settings",
        "language": "Language", "home": "Home",
    },
}


def t(key: str, lang: str = DEFAULT_LANG) -> str:
    return TRANSLATIONS.get(lang, TRANSLATIONS["es"]).get(key, key)
