import logging


def get_logger(name: str = "mirna_toolkit", level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger for toolkit modules."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
