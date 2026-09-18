"""Match a parsed CV against job offers using skill overlap + keywords."""
import re
from parsers.text_cleaner import TextCleaner
from utils.logger import setup_logger

logger = setup_logger(__name__)


class JobMatcher:
    def __init__(self):
        self.cleaner = TextCleaner()

    def match(self, cv_data: dict, job: dict) -> dict:
        cv_skills = set(s.lower() for s in (cv_data.get("skills") or []))
        cv_text = (cv_data.get("clean_text") or cv_data.get("raw_text") or "").lower()
        job_text = f"{job.get('title','')} {job.get('description','')}".lower()

        job_skills = self._extract_job_skills(job_text)
        if job_skills:
            overlap = cv_skills & job_skills
            score = round(100 * len(overlap) / len(job_skills), 1)
        else:
            overlap = {s for s in cv_skills if re.search(r"\b" + re.escape(s) + r"\b", job_text)}
            score = round(min(100.0, len(overlap) * 15.0), 1)

        # Bonus if job title words appear in CV
        title_words = [w for w in re.findall(r"[a-záéíóúñ+#.]{3,}", job.get("title", "").lower())]
        title_hits = sum(1 for w in title_words if w in cv_text)
        if title_words:
            score = round(min(100.0, score + 10 * title_hits / len(title_words)), 1)

        return {
            "score": score,
            "matched_skills": sorted(overlap),
            "required_skills": sorted(job_skills),
            "missing_skills": sorted(job_skills - cv_skills),
        }

    def rank(self, cv_data: dict, jobs: list) -> list:
        ranked = []
        for job in jobs:
            m = self.match(cv_data, job)
            ranked.append({**job, **m})
        ranked.sort(key=lambda j: j["score"], reverse=True)
        return ranked

    def _extract_job_skills(self, job_text: str) -> set:
        known = [
            "python", "javascript", "java", "c++", "c#", "typescript", "php",
            "html", "css", "sql", "mongodb", "postgresql", "mysql", "redis",
            "docker", "kubernetes", "aws", "azure", "gcp", "linux", "git",
            "react", "angular", "vue", "django", "flask", "fastapi",
            "node.js", "express", "pandas", "numpy", "tensorflow", "pytorch",
            "machine learning", "data analysis", "excel", "power bi", "tableau",
        ]
        found = set()
        for skill in known:
            if re.search(r"\b" + re.escape(skill) + r"\b", job_text):
                found.add(skill)
        return found


if __name__ == "__main__":
    matcher = JobMatcher()
    cv = {"skills": ["python", "sql", "docker"], "clean_text": "python developer with sql and docker"}
    job = {"title": "Python Developer", "description": "Looking for python, sql, aws, docker"}
    print(matcher.match(cv, job))
