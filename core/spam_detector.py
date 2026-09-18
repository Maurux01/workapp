# core/spam_detector.py
from config import FAKE_DETECTION_CONFIG
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SpamDetector:
    def __init__(self):
        self.config = FAKE_DETECTION_CONFIG
        self.risk_threshold = self.config["risk_threshold"]
        self.suspicious_keywords = self.config["suspicious_keywords"]
        self.free_email_domains = self.config["free_email_domains"]

    def detect(self, job_data: dict) -> dict:
        risk_score = 0
        reasons = []

        email = job_data.get("email", "")
        if self._is_free_email(email):
            risk_score += 2
            reasons.append(f"Uses free email domain: {email}")

        description = job_data.get("description", "").lower()
        keyword_matches = self._find_suspicious_keywords(description)
        if keyword_matches:
            risk_score += len(keyword_matches) * 2
            reasons.append(f"Suspicious keywords found: {', '.join(keyword_matches)}")

        if not job_data.get("company_name"):
            risk_score += 3
            reasons.append("No company name provided")

        if not job_data.get("company_website"):
            risk_score += 2
            reasons.append("No company website provided")

        word_count = len(description.split())
        if word_count < 50:
            risk_score += 2
            reasons.append(f"Description too short ({word_count} words)")
    
        if self._has_excessive_uppercase(description):
            risk_score += 2
            reasons.append("Excessive uppercase text (possible scam)")

        is_spam = risk_score >= self.risk_threshold

        result = {
            "is_spam": is_spam,
            "risk_score": risk_score,
            "threshold": self.risk_threshold,
            "reasons": reasons,
        }

        if is_spam:
            logger.warning(f"Job flagged as SPAM. Score: {risk_score}. Reasons: {reasons}")
        else:
            logger.info(f"Job passed spam check. Score: {risk_score}")

        return result

    def _is_free_email(self, email: str) -> bool:
        if not email:
            return False
        for domain in self.free_email_domains:
            if email.lower().endswith(f"@{domain}"):
                return True
        return False

    def _find_suspicious_keywords(self, text: str) -> list:
        found = []
        for keyword in self.suspicious_keywords:
            if keyword.lower() in text:
                found.append(keyword)
        return found

    def _has_excessive_uppercase(self, text: str) -> bool:
        if not text:
            return False
        words = text.split()
        if not words:
            return False
        uppercase_words = [w for w in words if w.isupper() and len(w) > 3]
        return len(uppercase_words) > len(words) * 0.3


if __name__ == "__main__":
    detector = SpamDetector()

    test_job_real = {
        "title": "Python Developer",
        "company_name": "TechCorp",
        "company_website": "https://techcorp.com",
        "email": "jobs@techcorp.com",
        "description": "We are looking for an experienced Python developer with 3+ years of experience in Django and REST APIs. Must know SQL and Docker.",
    }

    test_job_spam = {
        "title": "EARN $5000 WEEKLY",
        "company_name": "",
        "company_website": "",
        "email": "opportunity@gmail.com",
        "description": "NO EXPERIENCE NEEDED! Get rich quick with crypto and MLM. WhatsApp only. Pay for training required.",
    }

    print("Testing REAL job:")
    result_real = detector.detect(test_job_real)
    print(f"Is spam: {result_real['is_spam']}")
    print(f"Risk score: {result_real['risk_score']}")
    print(f"Reasons: {result_real['reasons']}\n")

    print("Testing SPAM job:")
    result_spam = detector.detect(test_job_spam)
    print(f"Is spam: {result_spam['is_spam']}")
    print(f"Risk score: {result_spam['risk_score']}")
    print(f"Reasons: {result_spam['reasons']}")
