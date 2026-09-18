"""Central logging helper."""
import logging
import sys

_configured = False


def setup_logger(name: str = "workapp", level: int = logging.INFO) -> logging.Logger:
    global _configured
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not _configured:
        handler = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        _configured = True
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger
