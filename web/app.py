"""Flask web app: bilingual job search + CV upload + match + spam badges."""
import os
from flask import Flask, render_template, request, session, redirect, url_for
from config import APP_NAME, TRANSLATIONS, DEFAULT_LANG, DEFAULT_LOCATION
from core.cv_analyzer import CVAnalyzer
from core.job_matcher import JobMatcher
from core.spam_detector import SpamDetector
from scrapers.scraper_manager import ScraperManager
from utils.helpers import truncate
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "workapp-dev-secret")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

manager = ScraperManager()
matcher = JobMatcher()
spam_detector = SpamDetector()
analyzer = CVAnalyzer()


def get_lang() -> str:
    lang = request.args.get("lang") or session.get("lang") or DEFAULT_LANG
    if lang not in ("es", "en"):
        lang = "es"
    session["lang"] = lang
    return lang


@app.context_processor
def inject_globals():
    lang = session.get("lang", DEFAULT_LANG)
    return {"T": TRANSLATIONS.get(lang, TRANSLATIONS["es"]), "lang": lang, "app_name": APP_NAME}


@app.route("/", methods=["GET"])
def index():
    get_lang()
    return render_template("index.html", cv=session.get("cv"))


@app.route("/lang/<lang>")
def set_lang(lang):
    session["lang"] = "en" if lang == "en" else "es"
    return redirect(request.referrer or url_for("index"))


@app.route("/upload", methods=["POST"])
def upload():
    lang = get_lang()
    f = request.files.get("cv")
    if not f or not f.filename.lower().endswith(".pdf"):
        return render_template("index.html", cv=None, error="Sube un PDF válido / Upload a valid PDF" if True else "")
    os.makedirs("data/CVs", exist_ok=True)
    path = os.path.join("data", "CVs", secure_filename(f.filename))
    f.save(path)
    cv = analyzer.analyze(path)
    if "error" in cv:
        return render_template("index.html", cv=None, error=cv["error"])
    session["cv"] = {"skills": cv["skills"], "clean_text": cv["clean_text"][:4000],
                     "email": cv["email"], "experience_years": cv["experience_years"]}
    return redirect(url_for("index"))


@app.route("/jobs", methods=["GET"])
def jobs():
    lang = get_lang()
    keyword = request.args.get("q", "python").strip()
    location = request.args.get("loc", DEFAULT_LOCATION).strip()
    hide_spam = request.args.get("hide_spam", "1") == "1"
    results = manager.search_all(keyword, location)
    for j in results:
        j["spam"] = spam_detector.detect(j)
    if hide_spam:
        results = [j for j in results if not j["spam"].get("is_spam")]
    cv = session.get("cv")
    if cv:
        results = matcher.rank(cv, results)
    for j in results:
        j["short"] = truncate(j.get("description", ""), 280)
    return render_template("jobs.html", jobs=results, q=keyword, loc=location,
                           hide_spam=hide_spam, cv=cv)


def run():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)


if __name__ == "__main__":
    run()
