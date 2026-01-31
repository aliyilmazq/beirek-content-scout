"""
BEIREK Content Scout - Logger Module
====================================

Centralized logging configuration.

Usage:
    from modules.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Message")
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


_configured = False


def setup_logging(
    level: str = "INFO",
    log_path: Optional[str] = None,
    max_file_size_mb: int = 10,
    backup_count: int = 5
) -> None:
    """
    Setup application-wide logging configuration.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_path: Directory for log files (None for console only)
        max_file_size_mb: Max size of each log file in MB
        backup_count: Number of backup files to keep
    """
    global _configured
    if _configured:
        return

    # Get log level
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (if path provided)
    if log_path:
        log_dir = Path(log_path)
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / "content_scout.log"

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_file_size_mb * 1024 * 1024,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Suppress noisy loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('feedparser').setLevel(logging.WARNING)

    _configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    # Ensure logging is configured
    if not _configured:
        setup_logging()

    return logging.getLogger(name)


# Setup with defaults on import
def init_from_config():
    """Initialize logging from config file."""
    try:
        from .config_manager import config
        setup_logging(
            level=config.get('logging.level', 'INFO'),
            log_path=str(config.base_path / config.get('logging.path', 'logs')),
            max_file_size_mb=config.get('logging.max_file_size_mb', 10),
            backup_count=config.get('logging.backup_count', 5)
        )
    except Exception:
        # Fallback to defaults
        setup_logging()


if __name__ == "__main__":
    setup_logging(level="DEBUG", log_path="./logs")
    logger = get_logger(__name__)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
