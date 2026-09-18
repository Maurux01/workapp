# core/cv_analyzer.py
import re
from parsers.cv_parser import extract_text_from_pdf
from parsers.text_cleaner import TextCleaner
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CVAnalyzer:
    def __init__(self):
        self.cleaner = TextCleaner()

    def analyze(self, pdf_path: str) -> dict:
        raw_text = extract_text_from_pdf(pdf_path)

        if not raw_text:
            logger.warning(f"Could not extract text from: {pdf_path}")
            return {"error": "Could not read PDF"}

        clean_text = self.cleaner.clean_cv_text(raw_text)

        result = {
            "raw_text": raw_text,
            "clean_text": clean_text,
            "email": self._extract_email(clean_text),
            "phone": self._extract_phone(clean_text),
            "skills": self._extract_skills(clean_text),
            "experience_years": self._estimate_experience(clean_text),
            "word_count": len(clean_text.split()),
        }

        logger.info(f"CV analyzed successfully. Found {len(result['skills'])} skills.")
        return result

    def _extract_email(self, text: str) -> str:
        emails = self.cleaner.extract_emails(text)
        return emails[0] if emails else ""

    def _extract_phone(self, text: str) -> str:
        phones = self.cleaner.extract_phone_numbers(text)
        return phones[0] if phones else ""

    def _extract_skills(self, text: str) -> list:
        known_skills = [
            "python", "javascript", "java", "c++", "c#", "ruby",
            "go", "rust", "typescript", "php", "swift", "kotlin",
            "html", "css", "sql", "nosql", "mongodb", "postgresql",
            "mysql", "redis", "docker", "kubernetes", "aws", "azure",
            "gcp", "linux", "git", "react", "angular", "vue",
            "django", "flask", "fastapi", "node.js", "express",
            "pandas", "numpy", "scipy", "tensorflow", "pytorch",
            "machine learning", "deep learning", "data analysis",
            "excel", "power bi", "tableau", "r", "matlab",
            "agile", "scrum", "jira", "figma", "photoshop",
        ]

        text_lower = text.lower()
        found_skills = []

        for skill in known_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)

        return found_skills

    def _estimate_experience(self, text: str) -> str:
        pattern_years = r'(\d+)\+?\s*years?'
        matches = re.findall(pattern_years, text.lower())

        if matches:
            max_years = max(int(m) for m in matches)
            return f"{max_years}+ years"

        pattern_dates = r'(20\d{2})\s*[-–]\s*(20\d{2})'
        date_matches = re.findall(pattern_dates, text)

        if date_matches:
            total = 0
            for start, end in date_matches:
                total += int(end) - int(start)
            return f"~{total} years"

        return "Unknown"


if __name__ == "__main__":
    analyzer = CVAnalyzer()
    test_path = "data/CVs/test_cv.pdf"

    print("Analyzing CV...")
    result = analyzer.analyze(test_path)

    if "error" not in result:
        print(f"\n✅ Email: {result['email']}")
        print(f"✅ Phone: {result['phone']}")
        print(f"✅ Skills: {result['skills']}")
        print(f"✅ Experience: {result['experience_years']}")
        print(f"✅ Word count: {result['word_count']}")
    else:
        print(f"\n❌ Error: {result['error']}")
