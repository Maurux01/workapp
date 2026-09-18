"""Text cleaning + email/phone extraction for CVs and jobs."""
import re
import unicodedata


class TextCleaner:
    EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    PHONE_RE = re.compile(r"\+?\d[\d\s().-]{6,}\d")
    WS_RE = re.compile(r"\s+")

    def clean_cv_text(self, text: str) -> str:
        return self._clean(text, keep_case=False)

    def clean_job_description(self, text: str) -> str:
        return self._clean(text, keep_case=False)

    def _clean(self, text: str, keep_case: bool = False) -> str:
        if not text:
            return ""
        text = unicodedata.normalize("NFKC", text)
        text = text.replace("\x00", " ")
        text = self.WS_RE.sub(" ", text).strip()
        return text if keep_case else text.lower()

    def extract_emails(self, text: str) -> list:
        if not text:
            return []
        seen, out = set(), []
        for m in self.EMAIL_RE.findall(text):
            e = m.strip(".,;)").lower()
            if e not in seen:
                seen.add(e)
                out.append(e)
        return out

    def extract_phone_numbers(self, text: str) -> list:
        if not text:
            return []
        out = []
        for m in self.PHONE_RE.findall(text):
            digits = re.sub(r"\D", "", m)
            if 7 <= len(digits) <= 15:
                out.append(m.strip())
        return out
