"""
BEIREK Content Scout - NewsData.io Client Module
=================================================

NewsData.io API integration for fetching news articles.

Features:
- Keyword-based article search
- Category filtering
- Country/language filtering
- Rate limiting
- Response caching
"""

import requests
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import hashlib
import json
from pathlib import Path

from .logger import get_logger
from .config_manager import config

# Module logger
logger = get_logger(__name__)


class NewsDataError(Exception):
    """Base exception for NewsData API errors."""
    pass


class NewsDataRateLimitError(NewsDataError):
    """Rate limit exceeded error."""
    pass


class NewsDataClient:
    """
    NewsData.io API client.

    Fetches articles using keywords and categories relevant to BEIREK.
    """

    def __init__(self):
        """Initialize NewsData client with config."""
        self.api_key = config.get('newsdata.api_key', '')
        self.base_url = config.get('newsdata.base_url', 'https://newsdata.io/api/1')
        self.keywords = config.get('newsdata.keywords', [])
        self.categories = config.get('newsdata.categories', ['energy', 'business'])
        self.language = config.get('newsdata.language', 'en')
        self.countries = config.get('newsdata.countries', ['us', 'gb'])
        self.max_results = config.get('newsdata.max_results', 50)

        # Rate limiting (NewsData free tier: 200 credits/day)
        self.min_request_interval = 1.0  # seconds between requests
        self.last_request_time = 0

        # Cache for deduplication
        self.cache_path = config.base_path / 'data' / 'newsdata_cache.json'
        self._cache = self._load_cache()

        if not self.api_key:
            logger.warning("NewsData API key not configured")
        else:
            logger.info(f"NewsData client initialized: {len(self.keywords)} keywords, {len(self.categories)} categories")

    def _load_cache(self) -> Dict:
        """Load URL cache from file."""
        try:
            if self.cache_path.exists():
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load NewsData cache: {e}")
        return {'seen_urls': [], 'last_fetch': None}

    def _save_cache(self):
        """Save URL cache to file."""
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(self._cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"Could not save NewsData cache: {e}")

    def _rate_limit_wait(self):
        """Wait if necessary to respect rate limit."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """
        Make API request with rate limiting.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            API response as dict
        """
        if not self.api_key:
            raise NewsDataError("NewsData API key not configured")

        self._rate_limit_wait()

        url = f"{self.base_url}/{endpoint}"
        params['apikey'] = self.api_key

        try:
            response = requests.get(url, params=params, timeout=30)

            if response.status_code == 429:
                raise NewsDataRateLimitError("API rate limit exceeded")

            response.raise_for_status()
            return response.json()

        except requests.Timeout:
            raise NewsDataError("API request timed out")
        except requests.RequestException as e:
            raise NewsDataError(f"API request failed: {e}")

    def fetch_by_keyword(self, keyword: str, max_results: int = None) -> List[Dict]:
        """
        Fetch articles by keyword.

        Args:
            keyword: Search keyword
            max_results: Maximum results to return

        Returns:
            List of article dicts
        """
        max_results = max_results or self.max_results

        params = {
            'q': keyword,
            'language': self.language,
            'size': min(max_results, 50)  # NewsData max per request
        }

        if self.countries:
            params['country'] = ','.join(self.countries)

        try:
            response = self._make_request('news', params)
            return self._parse_response(response)
        except NewsDataError as e:
            logger.error(f"Error fetching keyword '{keyword}': {e}")
            return []

    def fetch_by_category(self, category: str, max_results: int = None) -> List[Dict]:
        """
        Fetch articles by category.

        Args:
            category: Category name (energy, business, technology, etc.)
            max_results: Maximum results to return

        Returns:
            List of article dicts
        """
        max_results = max_results or self.max_results

        params = {
            'category': category,
            'language': self.language,
            'size': min(max_results, 50)
        }

        if self.countries:
            params['country'] = ','.join(self.countries)

        try:
            response = self._make_request('news', params)
            return self._parse_response(response)
        except NewsDataError as e:
            logger.error(f"Error fetching category '{category}': {e}")
            return []

    def _parse_response(self, response: Dict) -> List[Dict]:
        """
        Parse NewsData API response.

        Args:
            response: API response dict

        Returns:
            List of normalized article dicts
        """
        articles = []

        if response.get('status') != 'success':
            logger.warning(f"NewsData API error: {response.get('message', 'Unknown error')}")
            return articles

        for item in response.get('results', []):
            # Skip if URL already seen
            url = item.get('link', '')
            if not url or url in self._cache.get('seen_urls', []):
                continue

            # Normalize to scanner format
            article = {
                'title': item.get('title', '').strip(),
                'url': url,
                'summary': item.get('description', '') or item.get('content', '')[:500],
                'published_at': self._parse_date(item.get('pubDate')),
                'source_name': item.get('source_id', 'NewsData'),
                'category': item.get('category', []),
                'keywords': item.get('keywords', []),
                'image_url': item.get('image_url'),
                'country': item.get('country', [])
            }

            # Only add if we have title and URL
            if article['title'] and article['url']:
                articles.append(article)

        return articles

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime."""
        if not date_str:
            return None

        # NewsData format: 2026-01-31 10:30:00
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d'
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue

        return None

    def fetch_all_articles(self, progress_callback=None) -> List[Dict]:
        """
        Fetch articles using a SINGLE API call to conserve credits.

        Searches for: energy, ebrd, epc, epc management, epcm
        Returns max 10 results.

        Args:
            progress_callback: Optional callback(current, total)

        Returns:
            List of unique article dicts (max 10)
        """
        all_articles = []
        seen_urls = set(self._cache.get('seen_urls', []))

        if progress_callback:
            progress_callback(1, 1)

        # SINGLE API call - combined keywords
        # Includes: energy, development banks (EBRD, World Bank, IFC, ADB), EPC
        combined_query = "energy OR ebrd OR \"world bank\" OR ifc OR adb OR epc OR epcm OR infrastructure OR \"project finance\""

        params = {
            'q': combined_query,
            'language': self.language,
            'size': 10  # Only 10 results
        }

        if self.countries:
            params['country'] = ','.join(self.countries)

        try:
            response = self._make_request('news', params)
            articles = self._parse_response(response)

            for article in articles:
                if article['url'] not in seen_urls:
                    seen_urls.add(article['url'])
                    all_articles.append(article)

        except NewsDataError as e:
            logger.error(f"NewsData API error: {e}")

        # Update cache
        self._cache['seen_urls'] = list(seen_urls)[-1000:]
        self._cache['last_fetch'] = datetime.now().isoformat()
        self._save_cache()

        logger.info(f"NewsData fetched {len(all_articles)} articles (1 API call, max 10)")
        return all_articles[:10]  # Ensure max 10

    def fetch_all_articles_full(self, progress_callback=None) -> List[Dict]:
        """
        DEPRECATED: Full fetch using all keywords and categories.
        Uses many API credits - use fetch_all_articles() instead.
        """
        all_articles = []
        seen_urls = set(self._cache.get('seen_urls', []))

        total_requests = len(self.keywords) + len(self.categories)
        current = 0

        for keyword in self.keywords:
            if progress_callback:
                current += 1
                progress_callback(current, total_requests)

            articles = self.fetch_by_keyword(keyword)
            for article in articles:
                if article['url'] not in seen_urls:
                    seen_urls.add(article['url'])
                    all_articles.append(article)

        for category in self.categories:
            if progress_callback:
                current += 1
                progress_callback(current, total_requests)

            articles = self.fetch_by_category(category)
            for article in articles:
                if article['url'] not in seen_urls:
                    seen_urls.add(article['url'])
                    all_articles.append(article)

        self._cache['seen_urls'] = list(seen_urls)[-1000:]
        self._cache['last_fetch'] = datetime.now().isoformat()
        self._save_cache()

        logger.info(f"NewsData fetched {len(all_articles)} unique articles (full mode)")
        return all_articles

    def is_configured(self) -> bool:
        """Check if NewsData client is properly configured."""
        return bool(self.api_key)


if __name__ == "__main__":
    print("Testing NewsDataClient...")

    client = NewsDataClient()

    if not client.is_configured():
        print("NewsData API key not configured!")
    else:
        print(f"Configured keywords: {client.keywords[:3]}...")
        print(f"Configured categories: {client.categories}")

        # Test fetch
        print("\nFetching articles...")
        articles = client.fetch_all_articles()
        print(f"Fetched {len(articles)} articles")

        if articles:
            print(f"\nSample article: {articles[0]['title'][:60]}...")

    print("\nNewsData client test complete!")
