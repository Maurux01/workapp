"""Flask web app: job search + CV match + spam badges. Fully ES/EN via utils.i18n."""
import os
import uuid
from flask import Flask, render_template, request, session, redirect, url_for
from config import APP_NAME, DEFAULT_LANG, DEFAULT_LOCATION
from core.cv_analyzer import CVAnalyzer
from core.job_matcher import JobMatcher
from core.spam_detector import SpamDetector
from scrapers.scraper_manager import ScraperManager
from utils.helpers import truncate
from utils.i18n import t, STRINGS, JOB_TYPE_KEYS, MODALITY_KEYS
from utils.logger import setup_logger
from werkzeug.utils import secure_filename

logger = setup_logger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "workapp-dev-secret")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

manager = ScraperManager()
matcher = JobMatcher()
spam_detector = SpamDetector()
analyzer = CVAnalyzer()

# Server-side CV store: session cookie only keeps an id (fixes cookie overflow).
_CV_STORE: dict[str, dict] = {}


def get_lang() -> str:
    lang = request.args.get("lang") or session.get("lang") or DEFAULT_LANG
    if lang not in ("es", "en"):
        lang = "es"
    session["lang"] = lang
    return lang


def get_cv() -> dict | None:
    cv_id = session.get("cv_id")
    return _CV_STORE.get(cv_id) if cv_id else None


@app.context_processor
def inject_globals():
    lang = session.get("lang", DEFAULT_LANG)
    if lang not in ("es", "en"):
        lang = "es"
    return {"T": STRINGS[lang], "lang": lang, "app_name": APP_NAME,
            "JOB_TYPES": JOB_TYPE_KEYS, "MODALITIES": MODALITY_KEYS}


@app.route("/", methods=["GET"])
def index():
    get_lang()
    cv = get_cv()
    return render_template("index.html", cv=_cv_summary(cv) if cv else None,
                           error=request.args.get("error"))


@app.route("/lang/<lang>")
def set_lang(lang):
    session["lang"] = "en" if lang == "en" else "es"
    dest = request.referrer or url_for("index")
    return redirect(dest)


@app.route("/upload", methods=["POST"])
def upload():
    lang = get_lang()
    f = request.files.get("cv")
    if not f or not f.filename or not f.filename.lower().endswith(".pdf"):
        return redirect(url_for("index", error=t("invalid_pdf", lang)))
    try:
        os.makedirs("data/CVs", exist_ok=True)
        path = os.path.join("data", "CVs", secure_filename(f.filename))
        f.save(path)
        cv = analyzer.analyze(path)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"upload failed: {exc}")
        return redirect(url_for("index", error=t("could_not_read_cv", lang)))
    if "error" in cv:
        return redirect(url_for("index", error=t("could_not_read_cv", lang)))
    cv_id = uuid.uuid4().hex
    _CV_STORE[cv_id] = {"skills": cv.get("skills", []),
                        "clean_text": cv.get("clean_text", "")[:6000],
                        "email": cv.get("email", ""),
                        "experience_years": cv.get("experience_years", "")}
    session["cv_id"] = cv_id
    return redirect(url_for("index"))


@app.route("/jobs", methods=["GET"])
def jobs():
    lang = get_lang()
    keyword = request.args.get("q", "python").strip()
    location = request.args.get("loc", DEFAULT_LOCATION).strip() or DEFAULT_LOCATION
    hide_spam = request.args.get("hide_spam", "1") == "1"
    job_types = [v for v in request.args.getlist("jt") if v in JOB_TYPE_KEYS]
    modalities = [v for v in request.args.getlist("mod") if v in MODALITY_KEYS]
    if not keyword:
        return redirect(url_for("index", error=t("type_keyword", lang)))
    try:
        results = manager.search_all(keyword, location,
                                     job_types=job_types, modalities=modalities)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"search failed: {exc}")
        return render_template("jobs.html", jobs=[], q=keyword, loc=location,
                               hide_spam=hide_spam, job_types=job_types,
                               modalities=modalities, cv=_cv_summary(get_cv()),
                               error=str(exc))
    for j in results:
        j["spam"] = spam_detector.detect(j)
    if hide_spam:
        results = [j for j in results if not j["spam"].get("is_spam")]
    cv = get_cv()
    if cv:
        results = matcher.rank(cv, results)
    for j in results:
        j["short"] = truncate(j.get("description", ""), 280)
    return render_template("jobs.html", jobs=results, q=keyword, loc=location,
                           hide_spam=hide_spam, job_types=job_types,
                           modalities=modalities, cv=_cv_summary(cv), error=None)


def _cv_summary(cv: dict | None) -> dict | None:
    if not cv:
        return None
    return {"email": cv.get("email", ""),
            "experience_years": cv.get("experience_years", ""),
            "skills": (cv.get("skills", []) or [])[:10]}


def run():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)


if __name__ == "__main__":
    run()
