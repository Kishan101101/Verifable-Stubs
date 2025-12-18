import logging
import logging.handlers
import os


def configure_logging(log_level: str | int = None, log_dir: str | None = None) -> None:
    """Configure root logger: console + rotating file handler.

    - `log_level` can be a string like 'INFO' or an int from logging module.
    - `log_dir` defaults to a `logs` folder at project root.
    """
    if log_level is None:
        log_level = os.getenv("LOG_LEVEL", "INFO")

    if isinstance(log_level, str):
        log_level = getattr(logging, log_level.upper(), logging.INFO)

    if log_dir is None:
        log_dir = os.path.join(os.getcwd(), "logs")

    os.makedirs(log_dir, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Console handler (stream)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s [%(name)s] %(message)s"))

    # Rotating file handler
    fh = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, "app.log"), maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    fh.setLevel(log_level)
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s [%(name)s] %(message)s"))

    # Clear existing handlers to avoid duplicate logs in some reload scenarios
    if root_logger.handlers:
        for h in list(root_logger.handlers):
            root_logger.removeHandler(h)

    root_logger.addHandler(ch)
    root_logger.addHandler(fh)

    logging.getLogger("alembic").setLevel(logging.WARN)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARN)
