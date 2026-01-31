"""
BEIREK Content Scout - Cache Module
====================================

Simple file-based cache for reducing redundant requests.

Features:
- TTL-based expiration
- File-based persistence
- Thread-safe operations
"""

import hashlib
import json
import os
import time
import threading
from pathlib import Path
from typing import Optional, Any
from datetime import datetime

from .logger import get_logger
from .config_manager import config

# Module logger
logger = get_logger(__name__)


class SimpleCache:
    """
    Simple file-based cache with TTL support.

    Thread-safe and persistent across restarts.
    """

    def __init__(self, cache_dir: str = None, ttl_hours: int = 24):
        """
        Initialize cache.

        Args:
            cache_dir: Cache directory path (default: data/cache)
            ttl_hours: Time-to-live in hours (default: 24)
        """
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = config.base_path / "data" / "cache"

        self.ttl = ttl_hours * 3600  # Convert to seconds
        self._lock = threading.Lock()

        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        logger.debug(f"Cache initialized: {self.cache_dir}, TTL={ttl_hours}h")

    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path for a key."""
        # Hash the key to create a safe filename
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        cache_path = self._get_cache_path(key)

        with self._lock:
            if not cache_path.exists():
                return None

            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Check TTL
                cached_at = data.get('cached_at', 0)
                if time.time() - cached_at > self.ttl:
                    # Expired
                    cache_path.unlink(missing_ok=True)
                    logger.debug(f"Cache expired for key: {key[:50]}")
                    return None

                logger.debug(f"Cache hit for key: {key[:50]}")
                return data.get('value')

            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Cache read error: {e}")
                return None

    def set(self, key: str, value: Any) -> bool:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)

        Returns:
            True if successful
        """
        cache_path = self._get_cache_path(key)

        with self._lock:
            try:
                data = {
                    'key': key,
                    'value': value,
                    'cached_at': time.time(),
                    'expires_at': time.time() + self.ttl
                }

                with open(cache_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)

                logger.debug(f"Cache set for key: {key[:50]}")
                return True

            except (TypeError, IOError) as e:
                logger.warning(f"Cache write error: {e}")
                return False

    def delete(self, key: str) -> bool:
        """
        Delete value from cache.

        Args:
            key: Cache key

        Returns:
            True if deleted
        """
        cache_path = self._get_cache_path(key)

        with self._lock:
            if cache_path.exists():
                cache_path.unlink()
                logger.debug(f"Cache deleted for key: {key[:50]}")
                return True
            return False

    def clear(self) -> int:
        """
        Clear all cache entries.

        Returns:
            Number of entries cleared
        """
        count = 0

        with self._lock:
            for cache_file in self.cache_dir.glob("*.cache"):
                try:
                    cache_file.unlink()
                    count += 1
                except IOError:
                    pass

        logger.info(f"Cache cleared: {count} entries")
        return count

    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries.

        Returns:
            Number of entries removed
        """
        count = 0
        now = time.time()

        with self._lock:
            for cache_file in self.cache_dir.glob("*.cache"):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    cached_at = data.get('cached_at', 0)
                    if now - cached_at > self.ttl:
                        cache_file.unlink()
                        count += 1

                except (json.JSONDecodeError, IOError):
                    # Remove corrupted cache files
                    try:
                        cache_file.unlink()
                        count += 1
                    except IOError:
                        pass

        if count > 0:
            logger.info(f"Cache cleanup: {count} expired entries removed")

        return count

    def stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dict with cache stats
        """
        total = 0
        expired = 0
        size_bytes = 0
        now = time.time()

        with self._lock:
            for cache_file in self.cache_dir.glob("*.cache"):
                total += 1
                size_bytes += cache_file.stat().st_size

                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    cached_at = data.get('cached_at', 0)
                    if now - cached_at > self.ttl:
                        expired += 1
                except (json.JSONDecodeError, IOError):
                    expired += 1

        return {
            'total_entries': total,
            'expired_entries': expired,
            'valid_entries': total - expired,
            'size_bytes': size_bytes,
            'size_mb': round(size_bytes / (1024 * 1024), 2),
            'cache_dir': str(self.cache_dir),
            'ttl_hours': self.ttl / 3600
        }


# Global cache instance
_cache = None


def get_cache(ttl_hours: int = 24) -> SimpleCache:
    """
    Get global cache instance.

    Args:
        ttl_hours: TTL for new cache (ignored if already initialized)

    Returns:
        SimpleCache instance
    """
    global _cache
    if _cache is None:
        _cache = SimpleCache(ttl_hours=ttl_hours)
    return _cache


# Decorator for caching function results
def cached(ttl_hours: int = 24, key_prefix: str = ''):
    """
    Decorator to cache function results.

    Args:
        ttl_hours: Cache TTL in hours
        key_prefix: Prefix for cache keys

    Usage:
        @cached(ttl_hours=1, key_prefix='fetch_')
        def fetch_data(url):
            return requests.get(url).text
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Build cache key from function name and arguments
            key_parts = [key_prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ':'.join(key_parts)

            cache = get_cache(ttl_hours)

            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Call function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result)

            return result

        return wrapper
    return decorator


if __name__ == "__main__":
    # Test cache
    print("Testing SimpleCache...")

    cache = SimpleCache(ttl_hours=1)

    # Test set/get
    cache.set("test_key", {"data": "test value", "count": 42})
    result = cache.get("test_key")
    print(f"Get test_key: {result}")

    # Test stats
    stats = cache.stats()
    print(f"Cache stats: {stats}")

    # Test cleanup
    cache.cleanup_expired()

    print("\nCache module ready!")
