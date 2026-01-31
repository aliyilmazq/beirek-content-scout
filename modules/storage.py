"""
BEIREK Content Scout - Storage Module
=====================================

Database operations and file storage management.

Tables:
- sources: News sources
- articles: Scanned articles
- generated_content: Produced content
- scan_history: Scan logs
- glossary: Term glossary (7000+ terms)
- daily_concepts: Daily concept records
- content_requests: Request pool
- content_proposals: Content framing proposals
"""

import sqlite3
from pathlib import Path
from datetime import datetime, date
from typing import Optional, List, Dict, Any
import yaml
import re

from .logger import get_logger
from .config_manager import Constants, config

# Module logger
logger = get_logger(__name__)

# Database path - use config with fallback
DB_PATH = config.base_path / config.get('database.path', 'data/scout.db')


class DatabaseConnection:
    """
    Context manager for database connections.

    Ensures connections are properly closed even if exceptions occur.

    Usage:
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(...)
            conn.commit()
    """

    def __init__(self):
        self.conn = None

    def __enter__(self) -> sqlite3.Connection:
        self.conn = sqlite3.connect(str(DB_PATH))
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            self.conn.close()
        return False  # Don't suppress exceptions


def get_db_connection() -> sqlite3.Connection:
    """
    Get database connection with row factory.

    Returns:
        sqlite3.Connection with dict row factory

    Note:
        Prefer using DatabaseConnection context manager instead:
        with DatabaseConnection() as conn:
            ...
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_database() -> None:
    """
    Initialize database with all tables.

    Creates all necessary tables if they don't exist.
    """
    # Ensure data directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Sources table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            rss_url TEXT,
            category TEXT,
            priority INTEGER DEFAULT 2,
            last_checked DATETIME,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Articles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            summary TEXT,
            full_content TEXT,
            published_at DATETIME,
            scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            relevance_score REAL,
            relevance_reason TEXT,
            is_relevant BOOLEAN,
            is_selected BOOLEAN DEFAULT 0,
            is_processed BOOLEAN DEFAULT 0,
            beirek_area TEXT,
            beirek_subarea TEXT,
            FOREIGN KEY (source_id) REFERENCES sources(id)
        )
    """)

    # Generated content table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generated_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER,
            concept_id INTEGER,
            request_id INTEGER,
            content_type TEXT NOT NULL,
            title TEXT,
            content TEXT,
            word_count INTEGER,
            file_path TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_published BOOLEAN DEFAULT 0,
            published_at DATETIME,
            FOREIGN KEY (article_id) REFERENCES articles(id),
            FOREIGN KEY (concept_id) REFERENCES daily_concepts(id),
            FOREIGN KEY (request_id) REFERENCES content_requests(id)
        )
    """)

    # Scan history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at DATETIME,
            completed_at DATETIME,
            sources_scanned INTEGER DEFAULT 0,
            articles_found INTEGER DEFAULT 0,
            articles_relevant INTEGER DEFAULT 0,
            status TEXT DEFAULT 'running',
            error_message TEXT
        )
    """)

    # Glossary table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS glossary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            term_en TEXT NOT NULL,
            term_tr TEXT,
            category TEXT,
            source_line INTEGER,
            is_used BOOLEAN DEFAULT 0,
            used_date DATE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Daily concepts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_concepts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            glossary_id INTEGER,
            concept_en TEXT NOT NULL,
            concept_tr TEXT,
            beirek_area TEXT NOT NULL,
            beirek_subarea TEXT,
            selection_reason TEXT,
            published_date DATE,
            content_path TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (glossary_id) REFERENCES glossary(id)
        )
    """)

    # Content requests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_name TEXT NOT NULL,
            topic TEXT,
            brief TEXT,
            beirek_area TEXT,
            beirek_subarea TEXT,
            status TEXT DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            completed_at DATETIME,
            content_path TEXT
        )
    """)

    # Content proposals table (new workflow)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content_proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER,
            proposal_number INTEGER,
            beirek_area TEXT NOT NULL,
            beirek_subarea TEXT,
            suggested_title TEXT NOT NULL,
            content_angle TEXT NOT NULL,
            brief_description TEXT,
            target_audience TEXT,
            key_talking_points TEXT,
            status TEXT DEFAULT 'suggested',
            confidence_score REAL,
            folder_path TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            accepted_at DATETIME,
            FOREIGN KEY (article_id) REFERENCES articles(id)
        )
    """)

    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_url ON articles(url)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_relevant ON articles(is_relevant)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_selected ON articles(is_selected)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_glossary_used ON glossary(is_used)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_daily_concepts_date ON daily_concepts(published_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_proposals_status ON content_proposals(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_proposals_article ON content_proposals(article_id)")

    conn.commit()
    conn.close()


# =============================================================================
# SOURCES OPERATIONS
# =============================================================================

def add_source(name: str, url: str, rss_url: str = None,
               category: str = None, priority: int = 2) -> int:
    """
    Add a new source.

    Args:
        name: Source name
        url: Website URL
        rss_url: RSS feed URL (optional)
        category: Category (energy, solar, wind, etc.)
        priority: 1=high, 2=medium, 3=low

    Returns:
        New source ID or -1 if already exists
    """
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO sources (name, url, rss_url, category, priority)
                VALUES (?, ?, ?, ?, ?)
            """, (name, url, rss_url, category, priority))

            source_id = cursor.lastrowid
            logger.debug(f"Added source: {name} (ID: {source_id})")
        except sqlite3.IntegrityError:
            source_id = Constants.DB_DUPLICATE
            logger.debug(f"Source already exists: {url}")

    return source_id


def get_active_sources(priority: int = None) -> List[Dict]:
    """
    Get all active sources.

    Args:
        priority: Filter by priority (optional)

    Returns:
        List of source dicts
    """
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        if priority:
            cursor.execute("""
                SELECT * FROM sources
                WHERE is_active = 1 AND priority = ?
                ORDER BY priority, name
            """, (priority,))
        else:
            cursor.execute("""
                SELECT * FROM sources
                WHERE is_active = 1
                ORDER BY priority, name
            """)

        sources = [dict(row) for row in cursor.fetchall()]

    return sources


def update_source_last_checked(source_id: int) -> None:
    """Update source last checked timestamp."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sources
            SET last_checked = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (source_id,))


def deactivate_source(source_id: int) -> None:
    """Deactivate a source."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sources SET is_active = 0 WHERE id = ?
        """, (source_id,))
        logger.info(f"Deactivated source ID: {source_id}")


def get_source_count() -> int:
    """Get total source count."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sources WHERE is_active = 1")
        count = cursor.fetchone()[0]

    return count


# =============================================================================
# ARTICLES OPERATIONS
# =============================================================================

def add_article(source_id: int, title: str, url: str,
                summary: str = None, published_at: datetime = None) -> int:
    """
    Add a new article.

    Args:
        source_id: Source ID
        title: Article title
        url: Article URL
        summary: Article summary
        published_at: Publication date

    Returns:
        New article ID, -1 if already exists, -2 if validation failed
    """
    # Validate title - reject empty or whitespace-only titles
    if not title or not title.strip():
        logger.warning(f"Empty title rejected for URL: {url}")
        return Constants.DB_VALIDATION_ERROR

    title = title.strip()

    # Validate title length
    if len(title) < Constants.MIN_TITLE_LENGTH:
        logger.warning(f"Title too short ({len(title)} chars): {title[:50]}")
        return Constants.DB_VALIDATION_ERROR

    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO articles (source_id, title, url, summary, published_at)
                VALUES (?, ?, ?, ?, ?)
            """, (source_id, title, url, summary, published_at))

            article_id = cursor.lastrowid
            logger.debug(f"Added article: {title[:50]}... (ID: {article_id})")
        except sqlite3.IntegrityError:
            article_id = Constants.DB_DUPLICATE
            logger.debug(f"Article already exists: {url}")

    return article_id


def article_exists(url: str) -> bool:
    """Check if article URL already exists."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM articles WHERE url = ?", (url,))
        exists = cursor.fetchone() is not None

    return exists


def update_article_relevance(article_id: int, score: float,
                            is_relevant: bool, reason: str = None) -> None:
    """Update article relevance score."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE articles
            SET relevance_score = ?, is_relevant = ?, relevance_reason = ?
            WHERE id = ?
        """, (score, is_relevant, reason, article_id))


def update_article_beirek_area(article_id: int, beirek_area: str,
                               beirek_subarea: str = None) -> None:
    """Update article BEIREK area assignment."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE articles
            SET beirek_area = ?, beirek_subarea = ?
            WHERE id = ?
        """, (beirek_area, beirek_subarea, article_id))


def get_unfiltered_articles(limit: int = 100) -> List[Dict]:
    """Get articles that haven't been filtered yet."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, s.name as source_name
            FROM articles a
            LEFT JOIN sources s ON a.source_id = s.id
            WHERE a.relevance_score IS NULL
            ORDER BY a.scraped_at DESC
            LIMIT ?
        """, (limit,))

        articles = [dict(row) for row in cursor.fetchall()]

    return articles


def get_relevant_articles(limit: int = 50) -> List[Dict]:
    """Get relevant articles that haven't been selected."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, s.name as source_name
            FROM articles a
            LEFT JOIN sources s ON a.source_id = s.id
            WHERE a.is_relevant = 1 AND a.is_selected = 0
            ORDER BY a.relevance_score DESC, a.scraped_at DESC
            LIMIT ?
        """, (limit,))

        articles = [dict(row) for row in cursor.fetchall()]

    return articles


def mark_article_selected(article_id: int) -> None:
    """Mark article as selected for processing."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE articles SET is_selected = 1 WHERE id = ?
        """, (article_id,))


def mark_article_processed(article_id: int) -> None:
    """Mark article as processed."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE articles SET is_processed = 1 WHERE id = ?
        """, (article_id,))
        logger.debug(f"Article {article_id} marked as processed")


def get_pending_articles() -> List[Dict]:
    """Get selected but not processed articles."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, s.name as source_name
            FROM articles a
            LEFT JOIN sources s ON a.source_id = s.id
            WHERE a.is_selected = 1 AND a.is_processed = 0
            ORDER BY a.relevance_score DESC
        """)

        articles = [dict(row) for row in cursor.fetchall()]

    return articles


def get_article_by_id(article_id: int) -> Optional[Dict]:
    """Get article by ID."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, s.name as source_name
            FROM articles a
            LEFT JOIN sources s ON a.source_id = s.id
            WHERE a.id = ?
        """, (article_id,))

        row = cursor.fetchone()
        article = dict(row) if row else None

    return article


def update_article_full_content(article_id: int, full_content: str) -> None:
    """Update article with full content."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE articles SET full_content = ? WHERE id = ?
        """, (full_content, article_id))


def get_recent_article_titles(days: int = 7) -> List[str]:
    """
    Get recent article titles for duplicate detection.

    Args:
        days: Number of days to look back

    Returns:
        List of article titles
    """
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title FROM articles
            WHERE scraped_at >= datetime('now', ?)
            AND title IS NOT NULL AND title != ''
        """, (f'-{days} days',))

        titles = [row[0] for row in cursor.fetchall()]

    return titles


def is_duplicate_title(new_title: str, threshold: float = 0.85, days: int = 7) -> bool:
    """
    Check if a title is a duplicate of recent articles.

    Uses SequenceMatcher for fuzzy matching.

    Args:
        new_title: Title to check
        threshold: Similarity threshold (0-1)
        days: Number of days to look back

    Returns:
        True if duplicate found
    """
    from difflib import SequenceMatcher

    if not new_title:
        return False

    recent_titles = get_recent_article_titles(days=days)
    new_title_lower = new_title.lower().strip()

    for title in recent_titles:
        if not title:
            continue
        ratio = SequenceMatcher(None, new_title_lower, title.lower().strip()).ratio()
        if ratio > threshold:
            logger.debug(f"Duplicate title detected: '{new_title[:50]}' similar to '{title[:50]}' (ratio={ratio:.2f})")
            return True

    return False


# =============================================================================
# GENERATED CONTENT OPERATIONS
# =============================================================================

def save_generated_content(content_type: str, title: str, content: str,
                          file_path: str, article_id: int = None,
                          concept_id: int = None, request_id: int = None) -> int:
    """
    Save generated content.

    Args:
        content_type: 'article', 'linkedin', or 'twitter'
        title: Content title
        content: Content text
        file_path: Saved file path
        article_id: Related article ID (optional)
        concept_id: Related concept ID (optional)
        request_id: Related request ID (optional)

    Returns:
        New content ID
    """
    # Calculate word count
    word_count = len(content.split())

    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO generated_content
            (article_id, concept_id, request_id, content_type, title, content, word_count, file_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (article_id, concept_id, request_id, content_type, title, content, word_count, file_path))

        content_id = cursor.lastrowid
        logger.info(f"Saved {content_type} content: {title[:50]}... ({word_count} words)")

    return content_id


def get_content_by_article(article_id: int) -> List[Dict]:
    """Get all content generated for an article."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM generated_content WHERE article_id = ?
        """, (article_id,))

        content = [dict(row) for row in cursor.fetchall()]

    return content


def mark_content_published(content_id: int) -> None:
    """Mark content as published."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE generated_content
            SET is_published = 1, published_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (content_id,))
        logger.info(f"Content {content_id} marked as published")


# =============================================================================
# SCAN HISTORY OPERATIONS
# =============================================================================

def start_scan() -> int:
    """Start a new scan record."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO scan_history (started_at, status)
            VALUES (CURRENT_TIMESTAMP, 'running')
        """)

        scan_id = cursor.lastrowid
        logger.info(f"Scan started (ID: {scan_id})")

    return scan_id


def complete_scan(scan_id: int, sources_scanned: int,
                 articles_found: int, articles_relevant: int,
                 status: str = 'completed', error_message: str = None) -> None:
    """Complete a scan record."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE scan_history
            SET completed_at = CURRENT_TIMESTAMP,
                sources_scanned = ?,
                articles_found = ?,
                articles_relevant = ?,
                status = ?,
                error_message = ?
            WHERE id = ?
        """, (sources_scanned, articles_found, articles_relevant, status, error_message, scan_id))

    logger.info(f"Scan {scan_id} completed: {sources_scanned} sources, {articles_found} articles, status={status}")


def get_last_scan() -> Optional[Dict]:
    """Get the most recent scan."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM scan_history
            ORDER BY started_at DESC LIMIT 1
        """)

        row = cursor.fetchone()
        scan = dict(row) if row else None

    return scan


# =============================================================================
# GLOSSARY OPERATIONS
# =============================================================================

def import_glossary_from_file(file_path: str) -> int:
    """
    Import glossary from markdown file.

    Expected format:
    | # | Kavram (EN) | Kavram (TR) | Kategori |

    Returns:
        Number of terms imported
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    count = 0

    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        # Parse markdown table
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('|---'):
                continue
            if '|' not in line:
                continue

            parts = [p.strip() for p in line.split('|')]
            parts = [p for p in parts if p]  # Remove empty parts

            if len(parts) >= 2:
                # Skip header row
                if parts[0].lower() in ['#', 'no', 'sıra']:
                    continue

                term_en = parts[1] if len(parts) > 1 else ''
                term_tr = parts[2] if len(parts) > 2 else ''
                category = parts[3] if len(parts) > 3 else ''

                if term_en:
                    try:
                        cursor.execute("""
                            INSERT INTO glossary (term_en, term_tr, category, source_line)
                            VALUES (?, ?, ?, ?)
                        """, (term_en, term_tr, category, i + 1))
                        count += 1
                    except sqlite3.IntegrityError:
                        pass  # Term already exists

    logger.info(f"Imported {count} glossary terms from {file_path}")
    return count


def get_unused_terms(category: str = None, limit: int = 100) -> List[Dict]:
    """Get unused glossary terms."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        if category:
            cursor.execute("""
                SELECT * FROM glossary
                WHERE is_used = 0 AND category = ?
                ORDER BY RANDOM()
                LIMIT ?
            """, (category, limit))
        else:
            cursor.execute("""
                SELECT * FROM glossary
                WHERE is_used = 0
                ORDER BY RANDOM()
                LIMIT ?
            """, (limit,))

        terms = [dict(row) for row in cursor.fetchall()]

    return terms


def mark_term_used(term_id: int) -> None:
    """Mark a glossary term as used."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE glossary
            SET is_used = 1, used_date = DATE('now')
            WHERE id = ?
        """, (term_id,))
        logger.debug(f"Term {term_id} marked as used")


def get_term_by_id(term_id: int) -> Optional[Dict]:
    """Get glossary term by ID."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM glossary WHERE id = ?", (term_id,))

        row = cursor.fetchone()
        term = dict(row) if row else None

    return term


def search_terms(query: str) -> List[Dict]:
    """Search glossary terms."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM glossary
            WHERE term_en LIKE ? OR term_tr LIKE ?
            ORDER BY term_en
            LIMIT 50
        """, (f'%{query}%', f'%{query}%'))

        terms = [dict(row) for row in cursor.fetchall()]

    return terms


def get_glossary_stats() -> Dict:
    """Get glossary statistics."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM glossary")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM glossary WHERE is_used = 1")
        used = cursor.fetchone()[0]

    return {
        'total': total,
        'used': used,
        'remaining': total - used
    }


# =============================================================================
# DAILY CONCEPTS OPERATIONS
# =============================================================================

def add_daily_concept(glossary_id: int, concept_en: str, concept_tr: str,
                     beirek_area: str, beirek_subarea: str = None,
                     selection_reason: str = None) -> int:
    """Add a daily concept record."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO daily_concepts
            (glossary_id, concept_en, concept_tr, beirek_area, beirek_subarea,
             selection_reason, published_date)
            VALUES (?, ?, ?, ?, ?, ?, DATE('now'))
        """, (glossary_id, concept_en, concept_tr, beirek_area, beirek_subarea, selection_reason))

        concept_id = cursor.lastrowid
        logger.info(f"Added daily concept: {concept_en} (ID: {concept_id})")

    return concept_id


def get_today_concept() -> Optional[Dict]:
    """Get today's concept if exists."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dc.*, g.category as term_category
            FROM daily_concepts dc
            LEFT JOIN glossary g ON dc.glossary_id = g.id
            WHERE dc.published_date = DATE('now')
            ORDER BY dc.created_at DESC
            LIMIT 1
        """)

        row = cursor.fetchone()
        concept = dict(row) if row else None

    return concept


def get_concept_history(days: int = 30) -> List[Dict]:
    """Get concept history for last N days."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dc.*, g.category as term_category
            FROM daily_concepts dc
            LEFT JOIN glossary g ON dc.glossary_id = g.id
            WHERE dc.published_date >= DATE('now', ?)
            ORDER BY dc.published_date DESC
        """, (f'-{days} days',))

        concepts = [dict(row) for row in cursor.fetchall()]

    return concepts


def update_concept_content_path(concept_id: int, content_path: str) -> None:
    """Update concept content path."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE daily_concepts SET content_path = ? WHERE id = ?
        """, (content_path, concept_id))


# =============================================================================
# CONTENT REQUESTS OPERATIONS
# =============================================================================

def add_content_request(folder_name: str, topic: str = None,
                       brief: str = None) -> int:
    """Add a content request."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO content_requests (folder_name, topic, brief)
            VALUES (?, ?, ?)
        """, (folder_name, topic, brief))

        request_id = cursor.lastrowid
        logger.debug(f"Added content request: {folder_name} (ID: {request_id})")

    return request_id


def get_pending_requests() -> List[Dict]:
    """Get pending content requests."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM content_requests
            WHERE status = 'pending'
            ORDER BY created_at
        """)

        requests = [dict(row) for row in cursor.fetchall()]

    return requests


def get_request_by_folder(folder_name: str) -> Optional[Dict]:
    """Get request by folder name."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM content_requests WHERE folder_name = ?
        """, (folder_name,))

        row = cursor.fetchone()
        request = dict(row) if row else None

    return request


def update_request_status(request_id: int, status: str) -> None:
    """Update request status."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE content_requests SET status = ? WHERE id = ?
        """, (status, request_id))


def complete_request(request_id: int, beirek_area: str,
                    beirek_subarea: str, content_path: str) -> None:
    """Complete a content request."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE content_requests
            SET status = 'completed',
                beirek_area = ?,
                beirek_subarea = ?,
                content_path = ?,
                completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (beirek_area, beirek_subarea, content_path, request_id))

    logger.info(f"Request {request_id} completed")


# =============================================================================
# CONTENT PROPOSALS OPERATIONS
# =============================================================================

def add_content_proposal(article_id: int, beirek_area: str, beirek_subarea: str,
                        suggested_title: str, content_angle: str,
                        brief_description: str = None, target_audience: str = None,
                        key_talking_points: str = None,
                        confidence_score: float = None) -> int:
    """
    Add a new content proposal.

    Args:
        article_id: Related article ID
        beirek_area: BEIREK area (e.g., "4")
        beirek_subarea: BEIREK sub-area (e.g., "3")
        suggested_title: Suggested content title
        content_angle: Content perspective/angle
        brief_description: Brief description (2-3 sentences)
        target_audience: Target audience description
        key_talking_points: JSON array of key talking points
        confidence_score: AI confidence score (0-1)

    Returns:
        New proposal ID

    Raises:
        ValueError: If confidence_score is not between 0 and 1
    """
    # Validate confidence_score
    if confidence_score is not None:
        if not isinstance(confidence_score, (int, float)):
            raise ValueError("confidence_score must be a number")
        if not 0 <= confidence_score <= 1:
            raise ValueError("confidence_score must be between 0 and 1")

    max_retries = 3
    for attempt in range(max_retries):
        try:
            with DatabaseConnection() as conn:
                cursor = conn.cursor()

                # Use a single atomic INSERT with subquery to avoid race condition
                # This calculates proposal_number at INSERT time
                cursor.execute("""
                    INSERT INTO content_proposals
                    (article_id, proposal_number, beirek_area, beirek_subarea, suggested_title,
                     content_angle, brief_description, target_audience, key_talking_points,
                     confidence_score, status)
                    VALUES (?,
                            (SELECT COALESCE(MAX(proposal_number), 0) + 1
                             FROM content_proposals
                             WHERE DATE(created_at) = DATE('now')),
                            ?, ?, ?, ?, ?, ?, ?, ?, 'suggested')
                """, (article_id, beirek_area, beirek_subarea, suggested_title,
                      content_angle, brief_description, target_audience, key_talking_points,
                      confidence_score))

                proposal_id = cursor.lastrowid
                logger.info(f"Added proposal: {suggested_title[:50]}... (ID: {proposal_id})")

            return proposal_id

        except sqlite3.IntegrityError as e:
            # If there's a unique constraint violation on proposal_number, retry
            if attempt < max_retries - 1:
                logger.warning(f"Proposal number collision, retrying ({attempt + 1}/{max_retries})")
                continue
            raise

    return -1  # Should not reach here


def get_proposals_by_status(status: str = 'suggested', limit: int = 50) -> List[Dict]:
    """
    Get proposals by status.

    Args:
        status: Status to filter (suggested|accepted|rejected|outline_created|content_generated)
        limit: Maximum number of proposals to return

    Returns:
        List of proposal dicts with article info
    """
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.*, a.title as article_title, a.url as article_url,
                   s.name as source_name
            FROM content_proposals p
            LEFT JOIN articles a ON p.article_id = a.id
            LEFT JOIN sources s ON a.source_id = s.id
            WHERE p.status = ?
            ORDER BY p.confidence_score DESC, p.created_at DESC
            LIMIT ?
        """, (status, limit))

        proposals = [dict(row) for row in cursor.fetchall()]

    return proposals


def get_proposal_by_id(proposal_id: int) -> Optional[Dict]:
    """Get proposal by ID with article info."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.*, a.title as article_title, a.url as article_url,
                   a.summary as article_summary, a.full_content as article_content,
                   s.name as source_name
            FROM content_proposals p
            LEFT JOIN articles a ON p.article_id = a.id
            LEFT JOIN sources s ON a.source_id = s.id
            WHERE p.id = ?
        """, (proposal_id,))

        row = cursor.fetchone()
        proposal = dict(row) if row else None

    return proposal


def update_proposal_status(proposal_id: int, status: str,
                          folder_path: str = None) -> None:
    """
    Update proposal status.

    Args:
        proposal_id: Proposal ID
        status: New status
        folder_path: Folder path (for outline_created status)
    """
    # Validate status using Constants
    if status not in Constants.VALID_PROPOSAL_STATUSES:
        raise ValueError(f"Invalid status: {status}. Must be one of: {Constants.VALID_PROPOSAL_STATUSES}")

    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        if folder_path:
            cursor.execute("""
                UPDATE content_proposals
                SET status = ?, folder_path = ?
                WHERE id = ?
            """, (status, folder_path, proposal_id))
        else:
            cursor.execute("""
                UPDATE content_proposals
                SET status = ?
                WHERE id = ?
            """, (status, proposal_id))

        logger.debug(f"Proposal {proposal_id} status updated to: {status}")


def accept_proposal(proposal_id: int) -> None:
    """Accept a proposal."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE content_proposals
            SET status = 'accepted', accepted_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (proposal_id,))


def reject_proposal(proposal_id: int) -> None:
    """Reject a proposal."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE content_proposals
            SET status = 'rejected'
            WHERE id = ?
        """, (proposal_id,))


def get_proposals_for_outline() -> List[Dict]:
    """Get accepted proposals ready for outline creation."""
    return get_proposals_by_status('accepted')


def get_proposals_for_generation() -> List[Dict]:
    """Get proposals with outlines ready for content generation."""
    return get_proposals_by_status('outline_created')


def get_today_proposals() -> List[Dict]:
    """Get all proposals created today."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.*, a.title as article_title, s.name as source_name
            FROM content_proposals p
            LEFT JOIN articles a ON p.article_id = a.id
            LEFT JOIN sources s ON a.source_id = s.id
            WHERE DATE(p.created_at) = DATE('now')
            ORDER BY p.proposal_number
        """)

        proposals = [dict(row) for row in cursor.fetchall()]

    return proposals


def get_proposal_stats() -> Dict[str, int]:
    """Get proposal statistics."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        stats = {}

        cursor.execute("SELECT COUNT(*) FROM content_proposals WHERE status = 'suggested'")
        stats['suggested'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM content_proposals WHERE status = 'accepted'")
        stats['accepted'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM content_proposals WHERE status = 'rejected'")
        stats['rejected'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM content_proposals WHERE status = 'outline_created'")
        stats['outline_created'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM content_proposals WHERE status = 'content_generated'")
        stats['content_generated'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM content_proposals WHERE DATE(created_at) = DATE('now')")
        stats['today_total'] = cursor.fetchone()[0]

    return stats


# =============================================================================
# STATISTICS
# =============================================================================

def get_stats() -> Dict:
    """Get overall statistics."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        stats = {}

        # Sources
        cursor.execute("SELECT COUNT(*) FROM sources WHERE is_active = 1")
        stats['total_sources'] = cursor.fetchone()[0]

        # Articles
        cursor.execute("SELECT COUNT(*) FROM articles")
        stats['total_articles'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM articles WHERE is_relevant = 1")
        stats['relevant_articles'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM articles WHERE is_processed = 1")
        stats['processed_articles'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM articles WHERE is_selected = 1 AND is_processed = 0")
        stats['pending_articles'] = cursor.fetchone()[0]

        # Content - count unique content pieces (not duplicate by article/concept/request)
        cursor.execute("SELECT COUNT(*) FROM generated_content")
        stats['total_content'] = cursor.fetchone()[0]

        # Today's content - all formats generated today
        cursor.execute("SELECT COUNT(*) FROM generated_content WHERE DATE(created_at) = DATE('now')")
        stats['today_content'] = cursor.fetchone()[0]

        # Today's content by source type
        cursor.execute("""
            SELECT
                COUNT(CASE WHEN article_id IS NOT NULL THEN 1 END) as from_articles,
                COUNT(CASE WHEN concept_id IS NOT NULL THEN 1 END) as from_concepts,
                COUNT(CASE WHEN request_id IS NOT NULL THEN 1 END) as from_requests
            FROM generated_content
            WHERE DATE(created_at) = DATE('now')
        """)
        row = cursor.fetchone()
        stats['today_from_articles'] = row[0] if row else 0
        stats['today_from_concepts'] = row[1] if row else 0
        stats['today_from_requests'] = row[2] if row else 0

        # Concepts
        cursor.execute("SELECT COUNT(*) FROM daily_concepts")
        stats['total_concepts'] = cursor.fetchone()[0]

        # Requests
        cursor.execute("SELECT COUNT(*) FROM content_requests WHERE status = 'pending'")
        stats['pending_requests'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM content_requests WHERE status = 'completed'")
        stats['completed_requests'] = cursor.fetchone()[0]

        # Today's scans
        cursor.execute("SELECT COUNT(*) FROM scan_history WHERE DATE(started_at) = DATE('now')")
        stats['today_scans'] = cursor.fetchone()[0]

        # Last scan info
        cursor.execute("""
            SELECT sources_scanned, articles_found, articles_relevant, status
            FROM scan_history
            ORDER BY started_at DESC LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            stats['last_scan_sources'] = row[0]
            stats['last_scan_articles'] = row[1]
            stats['last_scan_relevant'] = row[2]
            stats['last_scan_status'] = row[3]

        # Proposals
        cursor.execute("SELECT COUNT(*) FROM content_proposals WHERE status = ?", (Constants.PROPOSAL_SUGGESTED,))
        stats['pending_proposals'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM content_proposals WHERE status = ?", (Constants.PROPOSAL_ACCEPTED,))
        stats['accepted_proposals'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM content_proposals WHERE status = ?", (Constants.PROPOSAL_OUTLINE_CREATED,))
        stats['ready_for_generation'] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM content_proposals WHERE status = ?", (Constants.PROPOSAL_CONTENT_GENERATED,))
        stats['generated_proposals'] = cursor.fetchone()[0]

    return stats


# =============================================================================
# FILE OPERATIONS
# =============================================================================

def generate_slug(title: str) -> str:
    """
    Generate URL-friendly slug from title.

    Args:
        title: Original title

    Returns:
        Slugified string
    """
    # Convert to lowercase
    slug = title.lower()

    # Replace Turkish characters
    tr_map = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c'
    }
    for tr_char, en_char in tr_map.items():
        slug = slug.replace(tr_char, en_char)

    # Replace non-alphanumeric with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)

    # Remove leading/trailing hyphens
    slug = slug.strip('-')

    # Limit length
    if len(slug) > 50:
        slug = slug[:50].rsplit('-', 1)[0]

    return slug


def sanitize_path_component(component: str) -> str:
    """
    Sanitize a path component to prevent path traversal attacks.

    Removes or replaces dangerous characters like ../, .., /, \\

    Args:
        component: Path component to sanitize

    Returns:
        Sanitized path component
    """
    if not component:
        return ''

    # Remove path traversal sequences
    sanitized = component.replace('..', '').replace('/', '').replace('\\', '')

    # Remove any remaining dangerous characters
    sanitized = re.sub(r'[<>:"|?*]', '', sanitized)

    # Strip leading/trailing whitespace and dots
    sanitized = sanitized.strip('. \t\n\r')

    return sanitized


def get_content_folder_path(beirek_area: str, beirek_subarea: str = None,
                           content_type: str = 'haber', slug: str = '') -> str:
    """
    Get full path for content folder.

    Args:
        beirek_area: BEIREK area (e.g., "4" or "4-project-development-finance")
        beirek_subarea: Sub-area (e.g., "3" or "3-project-finance-structuring")
        content_type: Content type (haber, kavram)
        slug: Content slug

    Returns:
        Full folder path

    Raises:
        ValueError: If path components contain invalid characters
    """
    # Use singleton config
    base_path = config.base_path / config.get('content.output_base_path', 'content')

    # Convert area number to full path if needed
    beirek_areas = config.beirek_areas

    # Handle both "4" and "4-project-development-finance" formats
    if beirek_area and '-' not in beirek_area and beirek_area in beirek_areas:
        area_info = beirek_areas[beirek_area]
        area_name = area_info['name'] if isinstance(area_info, dict) else area_info
        beirek_area = f"{beirek_area}-{area_name}"

    # Handle subarea conversion
    if beirek_subarea and '-' not in beirek_subarea:
        area_num = beirek_area.split('-')[0] if '-' in beirek_area else beirek_area
        if area_num in beirek_areas:
            area_info = beirek_areas[area_num]
            if isinstance(area_info, dict) and 'subareas' in area_info:
                subarea_name = area_info['subareas'].get(beirek_subarea, '')
                if subarea_name:
                    beirek_subarea = f"{beirek_subarea}-{subarea_name}"

    # Sanitize all path components to prevent path traversal
    beirek_area = sanitize_path_component(beirek_area)
    beirek_subarea = sanitize_path_component(beirek_subarea) if beirek_subarea else None
    content_type = sanitize_path_component(content_type)
    slug = sanitize_path_component(slug)

    # Validate that we have valid components
    if not beirek_area:
        raise ValueError("Invalid beirek_area after sanitization")

    # Validate area is a known BEIREK area (1-8)
    area_num = beirek_area.split('-')[0] if '-' in beirek_area else beirek_area
    if area_num not in beirek_areas and area_num not in ['1', '2', '3', '4', '5', '6', '7', '8']:
        raise ValueError(f"Invalid BEIREK area: {beirek_area}")

    today = date.today().isoformat()
    folder_name = f"{today}_{content_type}_{slug}"

    if beirek_subarea:
        final_path = base_path / beirek_area / beirek_subarea / folder_name
    else:
        final_path = base_path / beirek_area / folder_name

    # Final security check: ensure resolved path is under base_path
    resolved_path = final_path.resolve()
    resolved_base = base_path.resolve()
    if not str(resolved_path).startswith(str(resolved_base)):
        raise ValueError("Path traversal attempt detected")

    return str(final_path)


def save_content_to_file(content: str, file_path: str) -> bool:
    """
    Save content to file.

    Args:
        content: Content to save
        file_path: Full file path

    Returns:
        True if successful
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.debug(f"Saved file: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving file {file_path}: {e}")
        return False


def add_frontmatter(content: str, metadata: Dict) -> str:
    """
    Add YAML frontmatter to content.

    Args:
        content: Original content
        metadata: Metadata dict

    Returns:
        Content with frontmatter
    """
    frontmatter = "---\n"
    for key, value in metadata.items():
        if isinstance(value, (list, dict)):
            frontmatter += f"{key}: {yaml.dump(value, default_flow_style=True).strip()}\n"
        else:
            frontmatter += f'{key}: "{value}"\n'
    frontmatter += "---\n\n"

    return frontmatter + content


if __name__ == "__main__":
    # Initialize database when run directly
    print("Initializing database...")
    init_database()
    print(f"Database created at: {DB_PATH}")

    # Print stats
    stats = get_stats()
    print(f"\nCurrent stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
