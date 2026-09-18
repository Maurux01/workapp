"""Extract text from a CV PDF. Tries pypdf, falls back gracefully."""
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger(__name__)


def extract_text_from_pdf(pdf_path: str) -> str:
    path = Path(pdf_path)
    if not path.is_file():
        logger.warning(f"PDF not found: {pdf_path}")
        return ""
    # Try pypdf
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        parts = [(page.extract_text() or "") for page in reader.pages]
        text = "\n".join(parts).strip()
        if text:
            return text
    except ImportError:
        logger.warning("pypdf not installed. Install with: pip install pypdf")
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"pypdf failed for {pdf_path}: {exc}")
    # Try pdfminer as fallback
    try:
        from pdfminer.high_level import extract_text
        return (extract_text(str(path)) or "").strip()
    except ImportError:
        pass
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"pdfminer failed for {pdf_path}: {exc}")
    return ""
