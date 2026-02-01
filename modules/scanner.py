"""
BEIREK Content Scout - Scanner Module
=====================================

RSS feed scanning for news collection.

Features:
- RSS feed parsing
- Full article content extraction
- Duplicate detection
- Error handling with retries
- NewsData.io API integration (via NewsDataClient)
"""

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Callable
from pathlib import Path
import time
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urljoin

from .storage import (
    add_article, article_exists, get_active_sources,
    add_source, update_source_last_checked, get_source_count,
    start_scan, complete_scan, is_duplicate_title
)
from .logger import get_logger
from .config_manager import config, Constants
from .newsdata_client import NewsDataClient, NewsDataError

# Module logger
logger = get_logger(__name__)


class ScanError(Exception):
    """Base exception for scanning errors."""
    pass


class RSSParseError(ScanError):
    """RSS parsing error."""
    pass


class RequestTimeoutError(ScanError):
    """Request timeout error."""
    pass


class RateLimiter:
    """
    Domain-based rate limiter.

    Ensures minimum interval between requests to the same domain.
    """

    def __init__(self, requests_per_second: float = 2.0):
        """
        Initialize rate limiter.

        Args:
            requests_per_second: Maximum requests per second per domain
        """
        self.min_interval = 1.0 / requests_per_second
        self.last_request: Dict[str, float] = {}
        self._lock = threading.Lock()

    def wait(self, url: str) -> None:
        """
        Wait if necessary to respect rate limit for domain.

        Args:
            url: URL to rate limit
        """
        domain = urlparse(url).netloc

        with self._lock:
            now = time.time()
            last = self.last_request.get(domain, 0)
            wait_time = self.min_interval - (now - last)

            if wait_time > 0:
                time.sleep(wait_time)

            self.last_request[domain] = time.time()


class NewsScanner:
    """
    News scanner for RSS and web scraping.

    Handles:
    - Loading sources from YAML
    - Fetching RSS feeds
    - Web scraping for non-RSS sources
    - Article content extraction
    """

    def __init__(self, config_path: str = None):
        """
        Initialize scanner.

        Args:
            config_path: Path to config.yaml (optional, uses singleton config if not provided)
        """
        self.base_path = config.base_path

        # Use singleton config
        self.config = {
            'scanning': config.scanning,
            'content': config.content
        }

        # Load sources from YAML file
        sources_file = self.base_path / "sources.yaml"
        try:
            import yaml
            with open(sources_file, 'r', encoding='utf-8') as f:
                self.sources_config = yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Sources file not found: {sources_file}")
            self.sources_config = {'sources': {}}

        # Settings from config
        self.max_articles_per_source = config.get('scanning.max_articles_per_source', 10)
        self.timeout = config.get('scanning.timeout_seconds', 30)
        self.max_retries = config.get('scanning.max_retries', 3)

        # Parallel scanning settings
        self.max_workers = config.get('scanning.max_workers', 5)

        # Rate limiter
        self.rate_limiter = RateLimiter(requests_per_second=2.0)

        # User agent rotation
        self.user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
        ]
        self._ua_index = 0
        self._ua_lock = threading.Lock()

        # HTTP session with headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self._get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        })

        # Duplicate detection
        self.check_duplicates = config.get('scanning.check_duplicates', True)
        self.duplicate_threshold = config.get('scanning.duplicate_threshold', 0.85)

        logger.info(f"Scanner initialized: timeout={self.timeout}s, max_retries={self.max_retries}, max_workers={self.max_workers}")

    def _get_user_agent(self) -> str:
        """Get next user agent in rotation (thread-safe)."""
        with self._ua_lock:
            ua = self.user_agents[self._ua_index % len(self.user_agents)]
            self._ua_index += 1
            return ua

    def load_sources_to_db(self) -> int:
        """
        Load sources from YAML to database.

        Returns:
            Number of sources added
        """
        count = 0
        errors = 0

        for priority_level in ['primary', 'secondary', 'tertiary']:
            sources = self.sources_config.get('sources', {}).get(priority_level, [])

            for source in sources:
                try:
                    source_id = add_source(
                        name=source['name'],
                        url=source['url'],
                        rss_url=source.get('rss_url'),
                        category=source.get('category'),
                        priority=source.get('priority', 2)
                    )
                    if source_id > 0:
                        count += 1
                except KeyError as e:
                    logger.warning(f"Source missing required field {e}: {source}")
                    errors += 1
                except Exception as e:
                    logger.warning(f"Could not add source {source.get('name', 'unknown')}: {e}")
                    errors += 1

        if errors > 0:
            logger.info(f"Loaded {count} sources with {errors} errors")
        else:
            logger.info(f"Loaded {count} sources successfully")

        return count

    def fetch_rss_feed(self, rss_url: str, source_name: str = None,
                      max_items: int = None) -> List[Dict]:
        """
        Fetch articles from RSS feed.

        Uses requests for timeout control, then feedparser for parsing.

        Args:
            rss_url: RSS feed URL
            source_name: Source name for logging
            max_items: Maximum articles to fetch

        Returns:
            List of article dicts with title, url, summary, published_at
        """
        max_items = max_items or self.max_articles_per_source
        articles = []

        try:
            # Apply rate limiting
            self.rate_limiter.wait(rss_url)

            # Fetch RSS with timeout using requests
            response = self.session.get(
                rss_url,
                timeout=self.timeout,
                headers={'User-Agent': self._get_user_agent()}
            )
            response.raise_for_status()

            # Parse feed content
            feed = feedparser.parse(response.content)

            if feed.bozo and feed.bozo_exception:
                # Log but don't fail - feedparser can still work
                logger.debug(f"RSS parse warning for {source_name}: {feed.bozo_exception}")

            for entry in feed.entries[:max_items]:
                # Extract title with fallbacks
                title = entry.get('title', '').strip()

                # Fallback 1: Try to get title from content/description
                if not title:
                    summary_text = entry.get('summary', entry.get('description', ''))
                    if summary_text:
                        # Extract first sentence or first N characters as title
                        clean_text = self._clean_html(summary_text)
                        if clean_text:
                            # Take first sentence (up to first period, question mark, or exclamation)
                            import re
                            match = re.match(r'^(.+?[.!?])', clean_text)
                            if match:
                                title = match.group(1).strip()
                            else:
                                # Take first 100 characters
                                title = clean_text[:100].strip()
                                if len(clean_text) > 100:
                                    title += '...'

                article = {
                    'title': title,
                    'url': entry.get('link', ''),
                    'summary': self._clean_html(entry.get('summary', entry.get('description', ''))),
                    'published_at': self._parse_date(entry.get('published', entry.get('updated'))),
                    'source_name': source_name
                }

                # Skip if no title or URL (title must be non-empty string)
                if article['title'] and article['url']:
                    articles.append(article)

        except requests.Timeout:
            logger.warning(f"RSS timeout after {self.timeout}s: {source_name or rss_url}")
            return []
        except requests.RequestException as e:
            logger.warning(f"RSS request error for {source_name or rss_url}: {e}")
            return []
        except Exception as e:
            raise RSSParseError(f"Failed to fetch RSS from {rss_url}: {e}")

        return articles

    def extract_article_content(self, url: str) -> Dict:
        """
        Extract full article content from URL.

        Args:
            url: Article URL

        Returns:
            Dict with title, content, author, date
        """
        try:
            response = self._make_request(url)
            soup = BeautifulSoup(response.text, 'lxml')

            # Extract metadata
            title = self._extract_title(soup)
            content = self._extract_content(soup)
            author = self._extract_author(soup)
            date = self._extract_date(soup)

            return {
                'title': title,
                'content': content,
                'author': author,
                'date': date,
                'url': url
            }

        except Exception as e:
            return {
                'title': '',
                'content': '',
                'author': '',
                'date': None,
                'url': url,
                'error': str(e)
            }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract article title with comprehensive fallback strategies."""

        # Strategy 1: Try JSON-LD structured data first (most reliable)
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                import json
                data = json.loads(script.string or '')
                # Handle both single object and array formats
                if isinstance(data, list):
                    data = data[0] if data else {}
                if isinstance(data, dict):
                    # Check for headline in various schema types
                    title = data.get('headline') or data.get('name')
                    if title and isinstance(title, str) and title.strip():
                        return title.strip()
            except (json.JSONDecodeError, TypeError, AttributeError):
                continue

        # Strategy 2: Meta tags (very reliable for modern sites)
        meta_selectors = [
            ('meta[property="og:title"]', 'content'),
            ('meta[name="twitter:title"]', 'content'),
            ('meta[property="article:title"]', 'content'),
            ('meta[name="title"]', 'content'),
            ('meta[itemprop="headline"]', 'content'),
            ('meta[name="sailthru.title"]', 'content'),
            ('meta[name="parsely-title"]', 'content'),
        ]

        for selector, attr in meta_selectors:
            elem = soup.select_one(selector)
            if elem and elem.get(attr):
                title = elem[attr].strip()
                if title:
                    return title

        # Strategy 3: HTML heading selectors (expanded list)
        heading_selectors = [
            # Specific article title classes
            'h1.article-title', 'h1.post-title', 'h1.entry-title',
            'h1.headline', 'h1.story-title', 'h1.news-title',
            'h1.page-title', 'h1.content-title', 'h1.title',
            # Article container h1
            'article h1', '.article h1', '.post h1', '.story h1',
            '.article-header h1', '.post-header h1', '.entry-header h1',
            # Semantic markup
            'h1[itemprop="headline"]', 'h1[itemprop="name"]',
            '[itemprop="headline"] h1', '[itemprop="headline"]',
            # Data attributes (modern sites)
            'h1[data-testid="headline"]', 'h1[data-headline]',
            '[data-headline]', '[data-title]',
            # Common class patterns
            '.headline h1', '.entry-title', '.post-title',
            '.article-headline', '.story-headline',
            # Generic h1 (last resort for headings)
            'main h1', '#content h1', '#main h1', 'h1'
        ]

        for selector in heading_selectors:
            try:
                elem = soup.select_one(selector)
                if elem:
                    title = elem.get_text(strip=True)
                    if title and len(title) > 5:  # Avoid very short titles
                        return title
            except Exception:
                continue

        # Strategy 4: HTML title tag (fallback)
        if soup.title:
            title_text = soup.title.string or soup.title.get_text(strip=True)
            if title_text:
                # Clean up title (remove site name suffix if present)
                title = title_text.strip()
                # Common patterns: "Article Title | Site Name" or "Article Title - Site Name"
                for separator in [' | ', ' - ', ' — ', ' · ', ' :: ']:
                    if separator in title:
                        parts = title.split(separator)
                        # Usually the article title is the first/longest part
                        if len(parts[0]) > len(parts[-1]):
                            title = parts[0].strip()
                        break
                if title:
                    return title

        # Strategy 5: First significant heading on page
        for tag in ['h1', 'h2']:
            elem = soup.find(tag)
            if elem:
                title = elem.get_text(strip=True)
                if title and len(title) > 10:
                    return title

        return ''

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract article main content."""
        # Remove unwanted elements
        for tag in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']):
            tag.decompose()

        # Try various content selectors
        selectors = [
            'article .content', 'article .entry-content', 'article .post-content',
            '.article-body', '.article-content', '.post-body', '.entry-content',
            '[itemprop="articleBody"]', '.story-content', '.news-content',
            'article'
        ]

        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                # Get text with paragraph separation
                paragraphs = elem.find_all('p')
                if paragraphs:
                    return '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        # Fallback: get all paragraphs
        paragraphs = soup.find_all('p')
        content_paragraphs = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50]
        return '\n\n'.join(content_paragraphs[:20])  # Limit to first 20 paragraphs

    def _extract_author(self, soup: BeautifulSoup) -> str:
        """Extract article author."""
        selectors = [
            '[rel="author"]', '.author-name', '.byline', '.author',
            '[itemprop="author"]', 'meta[name="author"]'
        ]

        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                if selector.startswith('meta'):
                    return elem.get('content', '').strip()
                return elem.get_text(strip=True)

        return ''

    def _extract_date(self, soup: BeautifulSoup) -> Optional[datetime]:
        """Extract article publication date."""
        selectors = [
            'time[datetime]', '[itemprop="datePublished"]',
            'meta[property="article:published_time"]',
            '.publish-date', '.post-date', '.article-date'
        ]

        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                date_str = elem.get('datetime') or elem.get('content') or elem.get_text(strip=True)
                if date_str:
                    return self._parse_date(date_str)

        return None

    def scan_source(self, source: Dict) -> List[Dict]:
        """
        Scan a single source (RSS only).

        Args:
            source: Source dict from database

        Returns:
            List of new articles found
        """
        articles = []

        try:
            # Only process sources with RSS feeds
            if source.get('rss_url'):
                articles = self.fetch_rss_feed(
                    source['rss_url'],
                    source['name']
                )
            else:
                # Skip non-RSS sources (web scraping removed)
                logger.debug(f"Skipping non-RSS source: {source['name']}")
                return []

            # Filter out already scanned articles
            new_articles = [a for a in articles if not article_exists(a['url'])]

            # Update last checked
            update_source_last_checked(source['id'])

            return new_articles

        except Exception as e:
            logger.error(f"Error scanning {source['name']}: {e}")
            return []

    def scan_all_sources(self, priority: int = None,
                        progress_callback: Callable = None,
                        parallel: bool = True) -> Dict:
        """
        Scan all active sources.

        Args:
            priority: Filter by priority (optional)
            progress_callback: Callback for progress updates (current, total, source_name)
            parallel: Use parallel scanning (default: True)

        Returns:
            Scan result dict
        """
        # Start scan record
        scan_id = start_scan()

        # Get sources
        sources = get_active_sources(priority)
        total_sources = len(sources)

        results = {
            'scan_id': scan_id,
            'sources_scanned': 0,
            'articles_found': 0,
            'new_articles': 0,
            'duplicates_skipped': 0,
            'errors': [],
            'articles': []  # List of new articles for filtering
        }

        # Thread-safe counter for progress
        progress_lock = threading.Lock()
        progress_counter = [0]  # Use list for mutability in closure
        all_new_articles = []  # Thread-safe list for new articles

        def process_source(source: Dict) -> Dict:
            """Process a single source (thread-safe)."""
            source_result = {
                'source_name': source['name'],
                'articles_found': 0,
                'new_articles': 0,
                'duplicates': 0,
                'error': None,
                'articles': []  # Articles added from this source
            }

            try:
                # Scan source
                new_articles = self.scan_source(source)
                source_result['articles_found'] = len(new_articles)

                # Save to database
                for article in new_articles:
                    # Check for duplicate titles if enabled
                    if self.check_duplicates and is_duplicate_title(
                        article['title'],
                        threshold=self.duplicate_threshold
                    ):
                        source_result['duplicates'] += 1
                        continue

                    article_id = add_article(
                        source_id=source['id'],
                        title=article['title'],
                        url=article['url'],
                        summary=article.get('summary'),
                        published_at=article.get('published_at')
                    )

                    if article_id > 0:
                        source_result['new_articles'] += 1
                        # Add to articles list for filtering
                        article['id'] = article_id
                        article['source_name'] = source['name']
                        source_result['articles'].append(article)

            except Exception as e:
                source_result['error'] = str(e)
                logger.error(f"Error scanning {source['name']}: {e}")

            # Update progress
            with progress_lock:
                progress_counter[0] += 1
                if progress_callback:
                    progress_callback(progress_counter[0], total_sources, source['name'])

            return source_result

        # Process sources (parallel or sequential)
        if parallel and self.max_workers > 1:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(process_source, s): s for s in sources}

                for future in as_completed(futures):
                    source_result = future.result()
                    results['sources_scanned'] += 1
                    results['articles_found'] += source_result['articles_found']
                    results['new_articles'] += source_result['new_articles']
                    results['duplicates_skipped'] += source_result['duplicates']
                    results['articles'].extend(source_result.get('articles', []))
                    if source_result['error']:
                        results['errors'].append(f"{source_result['source_name']}: {source_result['error']}")
        else:
            # Sequential processing
            for source in sources:
                source_result = process_source(source)
                results['sources_scanned'] += 1
                results['articles_found'] += source_result['articles_found']
                results['new_articles'] += source_result['new_articles']
                results['duplicates_skipped'] += source_result['duplicates']
                results['articles'].extend(source_result.get('articles', []))
                if source_result['error']:
                    results['errors'].append(f"{source_result['source_name']}: {source_result['error']}")

        # Fetch from NewsData.io API
        newsdata_articles = self._fetch_newsdata_articles()
        if newsdata_articles:
            for article in newsdata_articles:
                # Check for duplicate titles if enabled
                if self.check_duplicates and is_duplicate_title(
                    article['title'],
                    threshold=self.duplicate_threshold
                ):
                    results['duplicates_skipped'] += 1
                    continue

                # Check if URL already exists
                if article_exists(article['url']):
                    continue

                article_id = add_article(
                    source_id=None,  # NewsData articles don't have a source_id
                    title=article['title'],
                    url=article['url'],
                    summary=article.get('summary'),
                    published_at=article.get('published_at')
                )

                if article_id > 0:
                    results['new_articles'] += 1
                    results['articles_found'] += 1
                    # Add to articles list for filtering
                    article['id'] = article_id
                    if not article.get('source_name'):
                        article['source_name'] = 'NewsData.io'
                    results['articles'].append(article)

            logger.info(f"NewsData.io: Added {len(newsdata_articles)} potential articles")

        # Complete scan record
        complete_scan(
            scan_id=scan_id,
            sources_scanned=results['sources_scanned'],
            articles_found=results['articles_found'],
            articles_relevant=0,  # Will be updated after filtering
            status='completed' if not results['errors'] else 'partial'
        )

        return results

    def _fetch_newsdata_articles(self) -> List[Dict]:
        """
        Fetch articles from NewsData.io API.

        Returns:
            List of article dicts
        """
        try:
            newsdata_client = NewsDataClient()
            if not newsdata_client.is_configured():
                logger.debug("NewsData API not configured, skipping")
                return []

            articles = newsdata_client.fetch_all_articles()
            return articles

        except NewsDataError as e:
            logger.warning(f"NewsData API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching NewsData articles: {e}")
            return []

    def _make_request(self, url: str, retries: int = None) -> requests.Response:
        """
        Make HTTP request with retries and rate limiting.

        Args:
            url: URL to fetch
            retries: Number of retries

        Returns:
            Response object
        """
        retries = retries or self.max_retries

        for attempt in range(retries):
            try:
                # Apply rate limiting
                self.rate_limiter.wait(url)

                # Rotate user agent
                headers = {'User-Agent': self._get_user_agent()}

                response = self.session.get(url, timeout=self.timeout, headers=headers)
                response.raise_for_status()
                return response

            except requests.Timeout:
                wait_time = 2 ** attempt
                logger.warning(f"Request timeout (attempt {attempt + 1}/{retries}): {url}")
                if attempt == retries - 1:
                    raise RequestTimeoutError(f"Timeout after {retries} attempts: {url}")
                time.sleep(wait_time)

            except requests.RequestException as e:
                wait_time = 2 ** attempt
                logger.warning(f"Request error (attempt {attempt + 1}/{retries}): {url} - {e}")
                if attempt == retries - 1:
                    raise ScanError(f"Request failed: {e}")
                time.sleep(wait_time)

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime."""
        if not date_str:
            return None

        # Common date formats
        formats = [
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%a, %d %b %Y %H:%M:%S %z',
            '%a, %d %b %Y %H:%M:%S GMT',
            '%d %b %Y',
            '%B %d, %Y',
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue

        return None

    def _clean_html(self, html: str) -> str:
        """Remove HTML tags from string."""
        if not html:
            return ''

        soup = BeautifulSoup(html, 'lxml')
        return soup.get_text(strip=True)

    def is_recent(self, published_at: datetime, hours: int = 48) -> bool:
        """Check if article is recent."""
        if not published_at:
            return True  # Assume recent if no date

        cutoff = datetime.now() - timedelta(hours=hours)
        return published_at > cutoff


if __name__ == "__main__":
    # Test scanner
    print("Testing NewsScanner...")

    scanner = NewsScanner()

    # Load sources to DB
    count = scanner.load_sources_to_db()
    print(f"Loaded {count} sources to database")

    # Test RSS fetch
    print("\nTesting RSS fetch (PV Magazine)...")
    try:
        articles = scanner.fetch_rss_feed(
            "https://www.pv-magazine.com/feed/",
            "PV Magazine"
        )
        print(f"Found {len(articles)} articles")
        if articles:
            print(f"Sample: {articles[0]['title'][:60]}...")
    except Exception as e:
        print(f"RSS test failed: {e}")

    print("\nScanner test complete!")
