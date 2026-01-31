"""
BEIREK Content Scout Modules
============================

This package contains all the core modules for the content scout application.

Modules:
- scanner: RSS scanning and NewsData.io integration
- filter: Claude-powered article filtering
- generator: Content generation (article, linkedin, twitter)
- framer: Content framing and proposal creation
- storage: Folder-based storage (replaced SQLite)
- ui: Terminal user interface
- newsdata_client: NewsData.io API client
- claude_session: Claude CLI session management
- config_manager: Singleton configuration management
- logger: Centralized logging
- cache: Simple file-based caching
"""

from .storage import init_database, get_storage, FolderStorage
from .config_manager import (
    config, Constants,
    check_claude_cli, ensure_paths_exist, safe_json_parse, retry
)
from .logger import get_logger, setup_logging
from .cache import SimpleCache, get_cache, cached

__all__ = [
    # Storage
    'init_database',
    'get_storage',
    'FolderStorage',
    # Config
    'config',
    'Constants',
    'check_claude_cli',
    'ensure_paths_exist',
    'safe_json_parse',
    'retry',
    # Logging
    'get_logger',
    'setup_logging',
    # Cache
    'SimpleCache',
    'get_cache',
    'cached',
]
