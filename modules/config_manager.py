"""
BEIREK Content Scout - Config Manager
=====================================

Singleton configuration manager for centralized config access.

Usage:
    from modules.config_manager import config
    timeout = config.get('scanning.timeout_seconds')
"""

import yaml
import logging
import subprocess
import re
import json
from pathlib import Path
from typing import Any, Optional, Dict
from functools import lru_cache

# Configure module logger
logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Singleton configuration manager.

    Loads config once and provides cached access to all settings.
    """

    _instance: Optional['ConfigManager'] = None
    _config: dict = {}
    _loaded: bool = False

    def __new__(cls) -> 'ConfigManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not ConfigManager._loaded:
            self._load_config()
            ConfigManager._loaded = True

    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        base_path = Path(__file__).parent.parent
        config_file = base_path / "config.yaml"

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                ConfigManager._config = yaml.safe_load(f)
            logger.info(f"Config loaded from {config_file}")
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_file}")
            ConfigManager._config = self._get_default_config()
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in config file: {e}")
            ConfigManager._config = self._get_default_config()

    def _get_default_config(self) -> dict:
        """Return default configuration."""
        return {
            'app': {'name': 'BEIREK Content Scout', 'version': '1.0.0'},
            'database': {'path': 'data/scout.db'},
            'scanning': {
                'max_articles_per_source': 10,
                'timeout_seconds': 30,
                'max_retries': 3
            },
            'filtering': {
                'min_relevance_score': 7,
                'batch_size': 10
            },
            'content': {
                'output_base_path': '../content',
                'article_min_words': 1500,
                'article_max_words': 2500,
                'linkedin_min_words': 150,
                'linkedin_max_words': 300,
                'twitter_min_tweets': 5,
                'twitter_max_tweets': 10
            },
            'claude': {
                'timeout_seconds': 180,
                'max_retries': 3
            },
            'logging': {
                'level': 'INFO',
                'path': 'logs/'
            },
            'beirek_areas': {}
        }

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get config value using dot notation.

        Args:
            key: Config key in dot notation (e.g., 'scanning.timeout_seconds')
            default: Default value if key not found

        Returns:
            Config value or default
        """
        keys = key.split('.')
        value = ConfigManager._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_section(self, section: str) -> dict:
        """
        Get entire config section.

        Args:
            section: Section name (e.g., 'scanning')

        Returns:
            Section dict or empty dict
        """
        return ConfigManager._config.get(section, {})

    @property
    def scanning(self) -> dict:
        """Get scanning configuration."""
        return self.get_section('scanning')

    @property
    def filtering(self) -> dict:
        """Get filtering configuration."""
        return self.get_section('filtering')

    @property
    def content(self) -> dict:
        """Get content configuration."""
        return self.get_section('content')

    @property
    def claude(self) -> dict:
        """Get Claude CLI configuration."""
        return self.get_section('claude')

    @property
    def beirek_areas(self) -> dict:
        """Get BEIREK areas mapping."""
        return self.get_section('beirek_areas')

    @property
    def base_path(self) -> Path:
        """Get application base path."""
        return Path(__file__).parent.parent

    def reload(self) -> None:
        """Force reload configuration."""
        ConfigManager._loaded = False
        self._load_config()
        ConfigManager._loaded = True


# Singleton instance for easy import
config = ConfigManager()


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def check_claude_cli() -> Dict[str, Any]:
    """
    Check Claude CLI availability and version.

    Returns:
        Dict with 'available' (bool) and 'version' (str or None)
    """
    try:
        result = subprocess.run(
            ['claude', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip() if result.stdout else 'unknown'
            return {'available': True, 'version': version}
        return {'available': False, 'version': None, 'error': result.stderr.strip()}
    except FileNotFoundError:
        return {'available': False, 'version': None, 'error': 'Claude CLI not found'}
    except subprocess.TimeoutExpired:
        return {'available': False, 'version': None, 'error': 'Timeout checking CLI'}
    except Exception as e:
        return {'available': False, 'version': None, 'error': str(e)}


def ensure_paths_exist() -> None:
    """
    Ensure all required application directories exist.

    Creates data, logs, and content directories if they don't exist.
    """
    paths = [
        config.base_path / 'data',
        config.base_path / 'logs',
        config.base_path / config.get('content.output_base_path', 'content')
    ]

    for path in paths:
        try:
            path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured path exists: {path}")
        except Exception as e:
            logger.warning(f"Could not create path {path}: {e}")


def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0,
          exceptions: tuple = (Exception,)):
    """
    Retry decorator with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry

    Usage:
        @retry(max_attempts=3, delay=1, backoff=2)
        def unstable_function():
            # May fail sometimes
            pass
    """
    import time
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = delay * (backoff ** attempt)
                        logger.warning(
                            f"Retry {attempt + 1}/{max_attempts} for {func.__name__} "
                            f"after {wait_time:.1f}s: {e}"
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}: {e}")

            # All retries exhausted
            raise last_exception

        return wrapper
    return decorator


def safe_json_parse(text: str, default: Any = None) -> Any:
    """
    Safely parse JSON from text with fallback strategies.

    Attempts multiple parsing strategies:
    1. Direct JSON parse
    2. Extract JSON object from text (handles markdown code blocks)
    3. Extract JSON array from text
    4. Return default value

    Args:
        text: Text that may contain JSON
        default: Default value if parsing fails (defaults to empty dict)

    Returns:
        Parsed JSON or default value
    """
    if default is None:
        default = {}

    if not text or not isinstance(text, str):
        return default

    text = text.strip()

    # Strategy 1: Direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strategy 2: Remove markdown code blocks and try again
    cleaned = text
    if '```json' in cleaned:
        match = re.search(r'```json\s*([\s\S]*?)\s*```', cleaned)
        if match:
            cleaned = match.group(1).strip()
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass
    elif '```' in cleaned:
        match = re.search(r'```\s*([\s\S]*?)\s*```', cleaned)
        if match:
            cleaned = match.group(1).strip()
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass

    # Strategy 3: Find JSON object in text
    json_obj_match = re.search(r'\{[\s\S]*\}', text)
    if json_obj_match:
        try:
            return json.loads(json_obj_match.group())
        except json.JSONDecodeError:
            pass

    # Strategy 4: Find JSON array in text
    json_arr_match = re.search(r'\[[\s\S]*\]', text)
    if json_arr_match:
        try:
            return json.loads(json_arr_match.group())
        except json.JSONDecodeError:
            pass

    # All strategies failed
    logger.warning(f"JSON parse failed, using default. Text preview: {text[:100]}...")
    return default


# Constants that should not be in config file
class Constants:
    """Application-wide constants."""

    # Twitter limits
    TWITTER_MAX_CHARS = 280
    TWITTER_TRUNCATE_SUFFIX = "..."
    TWITTER_TRUNCATE_LENGTH = TWITTER_MAX_CHARS - len(TWITTER_TRUNCATE_SUFFIX)

    # Content limits
    MAX_ARTICLE_CONTENT_LENGTH = 3000
    MAX_SUMMARY_LENGTH = 500

    # Validation
    MIN_TITLE_LENGTH = 5
    MAX_TITLE_LENGTH = 200

    # Database return codes
    DB_SUCCESS = 1
    DB_DUPLICATE = -1
    DB_VALIDATION_ERROR = -2

    # Proposal statuses
    PROPOSAL_SUGGESTED = 'suggested'
    PROPOSAL_ACCEPTED = 'accepted'
    PROPOSAL_REJECTED = 'rejected'
    PROPOSAL_OUTLINE_CREATED = 'outline_created'
    PROPOSAL_CONTENT_GENERATED = 'content_generated'

    VALID_PROPOSAL_STATUSES = {
        PROPOSAL_SUGGESTED,
        PROPOSAL_ACCEPTED,
        PROPOSAL_REJECTED,
        PROPOSAL_OUTLINE_CREATED,
        PROPOSAL_CONTENT_GENERATED
    }


if __name__ == "__main__":
    # Test config manager
    print(f"App name: {config.get('app.name')}")
    print(f"Timeout: {config.get('scanning.timeout_seconds')}")
    print(f"BEIREK Areas: {len(config.beirek_areas)} areas")
    print(f"Base path: {config.base_path}")
