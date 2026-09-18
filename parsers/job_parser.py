"""Normalize raw scraped jobs into a common schema + infer job_type/modality."""
from parsers.text_cleaner import TextCleaner

cleaner = TextCleaner()

REQUIRED_FIELDS = ("title", "company_name", "location", "description", "url", "source")

JOB_TYPES = ("full_time", "part_time", "freelance", "internship", "unknown")
MODALITIES = ("remote", "onsite", "hybrid", "unknown")

_TYPE_RULES = [
    ("freelance", ["freelance", "freelancer", "autónomo", "autonomo", "por proyecto",
                   "por hora", "contract", "contrato por", "independiente"]),
    ("part_time", ["part-time", "part time", "medio tiempo", "media jornada", "por horas"]),
    ("internship", ["intern", "internship", "pasant", "practicante", "prácticas",
                    "practicas", "becario", "trainee"]),
    ("full_time", ["full-time", "full time", "tiempo completo", "jornada completa",
                   "indefinido", "permanent"]),
]

_MODALITY_RULES = [
    ("remote", ["remot", "home office", "work from home", "trabajo desde casa",
                "teletrabajo", "100% remoto"]),
    ("hybrid", ["híbri", "hibri", "hybrid", "mixto"]),
    ("onsite", ["presencial", "on-site", "on site", "oficina", "in office"]),
]


def infer_job_type(text: str) -> str:
    low = (text or "").lower()
    for jtype, keywords in _TYPE_RULES:
        if any(k in low for k in keywords):
            return jtype
    return "unknown"


def infer_modality(text: str) -> str:
    low = (text or "").lower()
    for mod, keywords in _MODALITY_RULES:
        if any(k in low for k in keywords):
            return mod
    return "unknown"


def normalize_job(raw: dict) -> dict:
    title = (raw.get("title") or "").strip()
    company = (raw.get("company_name") or raw.get("company") or "").strip()
    location = (raw.get("location") or "").strip()
    description = cleaner.clean_job_description(raw.get("description") or "")
    blob = f"{title} {description} {location}"
    job = {
        "title": title,
        "company_name": company,
        "location": location,
        "description": description,
        "url": (raw.get("url") or raw.get("link") or "").strip(),
        "source": (raw.get("source") or "unknown").strip().lower(),
        "salary": (raw.get("salary") or "").strip(),
        "posted_at": (raw.get("posted_at") or raw.get("date") or "").strip(),
        "email": (raw.get("email") or "").strip(),
        "company_website": (raw.get("company_website") or "").strip(),
        "job_type": (raw.get("job_type") or "").strip().lower() or infer_job_type(blob),
        "modality": (raw.get("modality") or "").strip().lower() or infer_modality(blob),
    }
    if job["job_type"] not in JOB_TYPES:
        job["job_type"] = "unknown"
    if job["modality"] not in MODALITIES:
        job["modality"] = "unknown"
    return job


def matches_filters(job: dict, job_types: list, modalities: list) -> bool:
    """Empty filter list = no filtering on that axis. 'unknown' values always pass."""
    if job_types and job.get("job_type") not in ("unknown", *job_types):
        return False
    if modalities and job.get("modality") not in ("unknown", *modalities):
        return False
    return True


def is_valid_job(job: dict) -> bool:
    return bool(job.get("title") and job.get("description"))
