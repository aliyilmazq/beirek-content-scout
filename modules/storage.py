"""
BEIREK Content Scout - Storage Module
=====================================

Folder-based storage management for articles and content.

Directory Structure:
- content/{beirek_area}/{beirek_subarea}/girdiler/  - Input articles
- content/{beirek_area}/{beirek_subarea}/raporlar/  - Generated reports
- data/processed_urls.json    - Processed URL tracking
- data/scan_log.json          - Scan history
- data/pending_approvals.json - Articles awaiting approval
"""

import json
import re
from pathlib import Path
from datetime import datetime, date
from typing import Optional, List, Dict, Any
import yaml
import hashlib
import shutil
from filelock import FileLock

from .logger import get_logger
from .config_manager import Constants, config

# Module logger
logger = get_logger(__name__)


class FolderStorage:
    """
    Folder-based storage system for BEIREK Content Scout.

    Replaces SQLite database with JSON files and folder structure.
    """

    def __init__(self):
        """Initialize folder storage with paths from config."""
        self.base_path = config.base_path
        self.content_path = self.base_path / config.get('storage.content_base', 'content')
        self.data_path = self.base_path / config.get('storage.data_path', 'data')

        # Folder names from config
        self.inputs_folder = config.get('folder_structure.inputs_folder', 'girdiler')
        self.reports_folder = config.get('folder_structure.reports_folder', 'raporlar')

        # JSON file paths
        self.processed_urls_file = self.data_path / 'processed_urls.json'
        self.scan_log_file = self.data_path / 'scan_log.json'
        self.pending_approvals_file = self.data_path / 'pending_approvals.json'
        self.sources_file = self.data_path / 'sources.json'
        self.stats_file = self.data_path / 'stats.json'

        # Lock files for thread safety
        self.urls_lock = FileLock(str(self.processed_urls_file) + '.lock')
        self.approvals_lock = FileLock(str(self.pending_approvals_file) + '.lock')

        # BEIREK areas mapping
        self.beirek_areas = config.beirek_areas

        # Ensure structure exists
        self.ensure_structure()

    def ensure_structure(self):
        """Create BEIREK folder structure if it doesn't exist."""
        # Create data folder
        self.data_path.mkdir(parents=True, exist_ok=True)

        # Create content folder structure for all BEIREK areas
        for area_num, area_info in self.beirek_areas.items():
            if isinstance(area_info, dict):
                area_name = area_info.get('name', '')
                subareas = area_info.get('subareas', {})

                area_folder = self.content_path / f"{area_num}-{area_name}"

                for subarea_num, subarea_name in subareas.items():
                    subarea_folder = area_folder / f"{subarea_num}-{subarea_name}"

                    # Create girdiler and raporlar folders
                    (subarea_folder / self.inputs_folder).mkdir(parents=True, exist_ok=True)
                    (subarea_folder / self.reports_folder).mkdir(parents=True, exist_ok=True)

        logger.info(f"Folder structure ensured at {self.content_path}")

    def _load_json(self, file_path: Path, default: Any = None) -> Any:
        """Load JSON file with default value if not exists."""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load {file_path}: {e}")
        return default if default is not None else {}

    def _save_json(self, file_path: Path, data: Any):
        """Save data to JSON file atomically."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            temp_path.replace(file_path)
        except Exception as e:
            logger.error(f"Could not save {file_path}: {e}")
            raise

    # ==========================================================================
    # URL TRACKING
    # ==========================================================================

    def is_url_processed(self, url: str) -> bool:
        """Check if URL has been processed."""
        with self.urls_lock:
            data = self._load_json(self.processed_urls_file, {'urls': {}})
            return url in data.get('urls', {})

    def mark_url_processed(self, url: str, article_data: Dict = None):
        """Mark URL as processed with optional article data."""
        with self.urls_lock:
            data = self._load_json(self.processed_urls_file, {'urls': {}})
            data['urls'][url] = {
                'processed_at': datetime.now().isoformat(),
                'title': article_data.get('title', '') if article_data else '',
                'source': article_data.get('source_name', '') if article_data else ''
            }
            self._save_json(self.processed_urls_file, data)

    def get_processed_urls_count(self) -> int:
        """Get count of processed URLs."""
        data = self._load_json(self.processed_urls_file, {'urls': {}})
        return len(data.get('urls', {}))

    # ==========================================================================
    # PENDING APPROVALS
    # ==========================================================================

    def add_pending_approval(self, article: Dict, filter_result: Dict) -> str:
        """
        Add article to pending approvals.

        Args:
            article: Article dict with title, url, summary, etc.
            filter_result: Filter result with score, beirek_area, reason, etc.

        Returns:
            Approval ID
        """
        with self.approvals_lock:
            data = self._load_json(self.pending_approvals_file, {'pending': [], 'approved': [], 'rejected': []})

            # Generate unique ID
            approval_id = hashlib.md5(f"{article['url']}:{datetime.now().isoformat()}".encode()).hexdigest()[:12]

            approval = {
                'id': approval_id,
                'article': {
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'summary': article.get('summary', ''),
                    'source_name': article.get('source_name', ''),
                    'published_at': str(article.get('published_at', ''))
                },
                'filter_result': {
                    'score': filter_result.get('score', 0),
                    'reason': filter_result.get('reason', ''),
                    'beirek_area': filter_result.get('beirek_area', ''),
                    'beirek_subarea': filter_result.get('beirek_subarea', ''),
                    'confidence_score': filter_result.get('confidence_score', 0)
                },
                'created_at': datetime.now().isoformat(),
                'status': 'pending'
            }

            data['pending'].append(approval)
            self._save_json(self.pending_approvals_file, data)

            return approval_id

    def get_pending_approvals(self) -> List[Dict]:
        """Get all pending approvals."""
        data = self._load_json(self.pending_approvals_file, {'pending': []})
        return data.get('pending', [])

    def get_approval_by_id(self, approval_id: str) -> Optional[Dict]:
        """Get approval by ID."""
        data = self._load_json(self.pending_approvals_file, {'pending': [], 'approved': [], 'rejected': []})

        for approval in data.get('pending', []) + data.get('approved', []) + data.get('rejected', []):
            if approval.get('id') == approval_id:
                return approval
        return None

    def approve_article(self, approval_id: str) -> bool:
        """
        Approve an article for content generation.

        Args:
            approval_id: Approval ID

        Returns:
            True if approved successfully
        """
        with self.approvals_lock:
            data = self._load_json(self.pending_approvals_file, {'pending': [], 'approved': [], 'rejected': []})

            for i, approval in enumerate(data.get('pending', [])):
                if approval.get('id') == approval_id:
                    approval['status'] = 'approved'
                    approval['approved_at'] = datetime.now().isoformat()
                    data['approved'].append(approval)
                    data['pending'].pop(i)
                    self._save_json(self.pending_approvals_file, data)
                    return True

            return False

    def reject_article(self, approval_id: str) -> bool:
        """
        Reject an article.

        Args:
            approval_id: Approval ID

        Returns:
            True if rejected successfully
        """
        with self.approvals_lock:
            data = self._load_json(self.pending_approvals_file, {'pending': [], 'approved': [], 'rejected': []})

            for i, approval in enumerate(data.get('pending', [])):
                if approval.get('id') == approval_id:
                    approval['status'] = 'rejected'
                    approval['rejected_at'] = datetime.now().isoformat()
                    data['rejected'].append(approval)
                    data['pending'].pop(i)
                    self._save_json(self.pending_approvals_file, data)
                    return True

            return False

    def get_approved_articles(self) -> List[Dict]:
        """Get all approved articles waiting for content generation."""
        data = self._load_json(self.pending_approvals_file, {'approved': []})
        return [a for a in data.get('approved', []) if not a.get('content_generated')]

    def mark_content_generated(self, approval_id: str, folder_path: str):
        """Mark approved article as content generated."""
        with self.approvals_lock:
            data = self._load_json(self.pending_approvals_file, {'approved': []})

            for approval in data.get('approved', []):
                if approval.get('id') == approval_id:
                    approval['content_generated'] = True
                    approval['content_folder'] = folder_path
                    approval['generated_at'] = datetime.now().isoformat()
                    break

            self._save_json(self.pending_approvals_file, data)

    # ==========================================================================
    # CONTENT SAVING
    # ==========================================================================

    def get_area_folder_name(self, area: str, subarea: str = None) -> tuple:
        """
        Get full folder names for BEIREK area and subarea.

        Args:
            area: Area number (e.g., "4")
            subarea: Subarea number (e.g., "3")

        Returns:
            Tuple of (area_folder_name, subarea_folder_name)
        """
        area_info = self.beirek_areas.get(str(area), {})

        if isinstance(area_info, dict):
            area_name = area_info.get('name', '')
            area_folder = f"{area}-{area_name}"

            subareas = area_info.get('subareas', {})
            subarea_name = subareas.get(str(subarea), '') if subarea else ''
            subarea_folder = f"{subarea}-{subarea_name}" if subarea_name else ''
        else:
            area_folder = f"{area}-{area_info}" if area_info else str(area)
            subarea_folder = str(subarea) if subarea else ''

        return area_folder, subarea_folder

    def save_article_input(self, article: Dict, area: str, subarea: str) -> str:
        """
        Save article as input markdown.

        Args:
            article: Article dict with title, url, summary, source_name
            area: BEIREK area number
            subarea: BEIREK subarea number

        Returns:
            Path to saved file
        """
        area_folder, subarea_folder = self.get_area_folder_name(area, subarea)
        today = date.today().isoformat()
        slug = generate_slug(article.get('title', 'untitled'))

        # Build path
        input_folder = self.content_path / area_folder / subarea_folder / self.inputs_folder
        input_folder.mkdir(parents=True, exist_ok=True)

        filename = f"{today}-{slug}.md"
        file_path = input_folder / filename

        # Build markdown content
        content = f"""---
title: "{article.get('title', '')}"
source: "{article.get('source_name', '')}"
url: "{article.get('url', '')}"
date: "{today}"
beirek_area: "{area}"
beirek_subarea: "{subarea}"
---

# {article.get('title', '')}

**Kaynak:** {article.get('source_name', '')}
**URL:** {article.get('url', '')}
**Tarih:** {article.get('published_at', today)}

## Ozet

{article.get('summary', '')}

## Tam Icerik

{article.get('full_content', article.get('summary', ''))}
"""

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Saved input article: {file_path}")
        return str(file_path)

    def save_report(self, content: Dict, article: Dict, area: str, subarea: str) -> str:
        """
        Save generated reports (makale.md, linkedin.md, twitter.md).

        Args:
            content: Dict with 'article', 'linkedin', 'twitter' keys
            article: Source article dict
            area: BEIREK area number
            subarea: BEIREK subarea number

        Returns:
            Path to report folder
        """
        area_folder, subarea_folder = self.get_area_folder_name(area, subarea)
        today = date.today().isoformat()
        slug = generate_slug(article.get('title', 'untitled'))

        # Build report folder path
        report_folder = self.content_path / area_folder / subarea_folder / self.reports_folder / f"{today}-{slug}"
        report_folder.mkdir(parents=True, exist_ok=True)

        # Common frontmatter
        frontmatter_base = {
            'title': article.get('title', ''),
            'date': today,
            'beirek_area': area,
            'beirek_subarea': subarea,
            'source_url': article.get('url', ''),
            'generated_by': 'BEIREK Content Scout'
        }

        # Save makale.md
        if content.get('article'):
            self._save_content_file(
                report_folder / 'makale.md',
                content['article'],
                {**frontmatter_base, 'format': 'article'}
            )

        # Save linkedin.md
        if content.get('linkedin'):
            self._save_content_file(
                report_folder / 'linkedin.md',
                content['linkedin'],
                {**frontmatter_base, 'format': 'linkedin'}
            )

        # Save twitter.md
        if content.get('twitter'):
            self._save_content_file(
                report_folder / 'twitter.md',
                content['twitter'],
                {**frontmatter_base, 'format': 'twitter'}
            )

        logger.info(f"Saved report folder: {report_folder}")
        return str(report_folder)

    def _save_content_file(self, file_path: Path, content: str, frontmatter: Dict):
        """Save content with YAML frontmatter."""
        fm_yaml = "---\n"
        for key, value in frontmatter.items():
            if isinstance(value, (list, dict)):
                fm_yaml += f"{key}: {json.dumps(value, ensure_ascii=False)}\n"
            else:
                fm_yaml += f'{key}: "{value}"\n'
        fm_yaml += "---\n\n"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fm_yaml + content)

    # ==========================================================================
    # SCAN LOG
    # ==========================================================================

    def start_scan(self) -> str:
        """Start a new scan and return scan ID."""
        data = self._load_json(self.scan_log_file, {'scans': []})

        scan_id = hashlib.md5(datetime.now().isoformat().encode()).hexdigest()[:12]
        scan = {
            'id': scan_id,
            'started_at': datetime.now().isoformat(),
            'status': 'running'
        }

        data['scans'].append(scan)
        self._save_json(self.scan_log_file, data)

        return scan_id

    def complete_scan(self, scan_id: str, sources_scanned: int,
                     articles_found: int, articles_relevant: int,
                     status: str = 'completed', error_message: str = None):
        """Complete a scan record."""
        data = self._load_json(self.scan_log_file, {'scans': []})

        for scan in data['scans']:
            if scan.get('id') == scan_id:
                scan['completed_at'] = datetime.now().isoformat()
                scan['sources_scanned'] = sources_scanned
                scan['articles_found'] = articles_found
                scan['articles_relevant'] = articles_relevant
                scan['status'] = status
                if error_message:
                    scan['error_message'] = error_message
                break

        self._save_json(self.scan_log_file, data)
        logger.info(f"Scan {scan_id} completed: {sources_scanned} sources, {articles_found} articles")

    def get_last_scan(self) -> Optional[Dict]:
        """Get the most recent scan."""
        data = self._load_json(self.scan_log_file, {'scans': []})
        scans = data.get('scans', [])
        return scans[-1] if scans else None

    # ==========================================================================
    # SOURCES MANAGEMENT
    # ==========================================================================

    def add_source(self, name: str, url: str, rss_url: str = None,
                  category: str = None, priority: int = 2) -> str:
        """Add a new source."""
        data = self._load_json(self.sources_file, {'sources': []})

        # Check if URL already exists
        for source in data['sources']:
            if source.get('url') == url:
                return source.get('id', '-1')

        source_id = hashlib.md5(url.encode()).hexdigest()[:12]
        source = {
            'id': source_id,
            'name': name,
            'url': url,
            'rss_url': rss_url,
            'category': category,
            'priority': priority,
            'is_active': True,
            'created_at': datetime.now().isoformat()
        }

        data['sources'].append(source)
        self._save_json(self.sources_file, data)

        return source_id

    def get_active_sources(self, priority: int = None) -> List[Dict]:
        """Get all active sources."""
        data = self._load_json(self.sources_file, {'sources': []})
        sources = [s for s in data['sources'] if s.get('is_active', True)]

        if priority is not None:
            sources = [s for s in sources if s.get('priority') == priority]

        return sorted(sources, key=lambda x: (x.get('priority', 2), x.get('name', '')))

    def get_source_count(self) -> int:
        """Get total active source count."""
        return len(self.get_active_sources())

    def update_source_last_checked(self, source_id: str):
        """Update source last checked timestamp."""
        data = self._load_json(self.sources_file, {'sources': []})

        for source in data['sources']:
            if source.get('id') == source_id:
                source['last_checked'] = datetime.now().isoformat()
                break

        self._save_json(self.sources_file, data)

    # ==========================================================================
    # STATISTICS
    # ==========================================================================

    def get_stats(self) -> Dict:
        """Get overall statistics."""
        stats = {
            'total_sources': self.get_source_count(),
            'total_urls_processed': self.get_processed_urls_count()
        }

        # Pending approvals stats
        approvals_data = self._load_json(self.pending_approvals_file, {})
        stats['pending_approvals'] = len(approvals_data.get('pending', []))
        stats['approved_articles'] = len(approvals_data.get('approved', []))
        stats['rejected_articles'] = len(approvals_data.get('rejected', []))

        # Scan stats
        scan_data = self._load_json(self.scan_log_file, {'scans': []})
        today = date.today().isoformat()
        stats['today_scans'] = len([s for s in scan_data.get('scans', [])
                                   if s.get('started_at', '').startswith(today)])

        # Last scan info
        last_scan = self.get_last_scan()
        if last_scan:
            stats['last_scan_sources'] = last_scan.get('sources_scanned', 0)
            stats['last_scan_articles'] = last_scan.get('articles_found', 0)
            stats['last_scan_relevant'] = last_scan.get('articles_relevant', 0)
            stats['last_scan_status'] = last_scan.get('status', '')

        return stats


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

# Global storage instance
_storage = None


def get_storage() -> FolderStorage:
    """Get or create folder storage instance."""
    global _storage
    if _storage is None:
        _storage = FolderStorage()
    return _storage


# =============================================================================
# COMPATIBILITY FUNCTIONS (for existing code)
# =============================================================================

def init_database() -> None:
    """Initialize storage (compatibility function)."""
    get_storage()  # This ensures folder structure is created
    logger.info("Folder-based storage initialized")


def article_exists(url: str) -> bool:
    """Check if article URL already exists."""
    return get_storage().is_url_processed(url)


def add_article(source_id: str, title: str, url: str,
                summary: str = None, published_at: datetime = None) -> int:
    """Add a new article (mark URL as processed)."""
    if not title or not title.strip():
        return Constants.DB_VALIDATION_ERROR

    if len(title.strip()) < Constants.MIN_TITLE_LENGTH:
        return Constants.DB_VALIDATION_ERROR

    storage = get_storage()
    if storage.is_url_processed(url):
        return Constants.DB_DUPLICATE

    storage.mark_url_processed(url, {
        'title': title,
        'source_id': source_id,
        'summary': summary,
        'published_at': published_at
    })

    return 1  # Success


def add_source(name: str, url: str, rss_url: str = None,
               category: str = None, priority: int = 2) -> int:
    """Add a new source."""
    source_id = get_storage().add_source(name, url, rss_url, category, priority)
    return 1 if source_id else Constants.DB_DUPLICATE


def get_active_sources(priority: int = None) -> List[Dict]:
    """Get all active sources."""
    return get_storage().get_active_sources(priority)


def update_source_last_checked(source_id: str) -> None:
    """Update source last checked timestamp."""
    get_storage().update_source_last_checked(source_id)


def get_source_count() -> int:
    """Get total source count."""
    return get_storage().get_source_count()


def start_scan() -> str:
    """Start a new scan record."""
    return get_storage().start_scan()


def complete_scan(scan_id: str, sources_scanned: int,
                 articles_found: int, articles_relevant: int,
                 status: str = 'completed', error_message: str = None) -> None:
    """Complete a scan record."""
    get_storage().complete_scan(
        scan_id, sources_scanned, articles_found,
        articles_relevant, status, error_message
    )


def get_last_scan() -> Optional[Dict]:
    """Get the most recent scan."""
    return get_storage().get_last_scan()


def get_stats() -> Dict:
    """Get overall statistics."""
    return get_storage().get_stats()


def is_duplicate_title(new_title: str, threshold: float = 0.85, days: int = 7) -> bool:
    """Check if a title is a duplicate (simplified for folder storage)."""
    # For now, just return False - full duplicate detection requires more work
    return False


def get_unfiltered_articles(limit: int = 100) -> List[Dict]:
    """Get unfiltered articles (returns pending approvals for now)."""
    return get_storage().get_pending_approvals()[:limit]


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def generate_slug(title: str) -> str:
    """
    Generate URL-friendly slug from title.

    Args:
        title: Original title

    Returns:
        Slugified string
    """
    if not title:
        return 'untitled'

    # Convert to lowercase
    slug = title.lower()

    # Replace Turkish characters
    tr_map = {
        'i': 'i', 'g': 'g', 'u': 'u', 's': 's', 'o': 'o', 'c': 'c',
        'I': 'i', 'G': 'g', 'U': 'u', 'S': 's', 'O': 'o', 'C': 'c'
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

    return slug or 'untitled'


def sanitize_path_component(component: str) -> str:
    """Sanitize a path component to prevent path traversal attacks."""
    if not component:
        return ''

    sanitized = component.replace('..', '').replace('/', '').replace('\\', '')
    sanitized = re.sub(r'[<>:"|?*]', '', sanitized)
    sanitized = sanitized.strip('. \t\n\r')

    return sanitized


def save_content_to_file(content: str, file_path: str) -> bool:
    """Save content to file."""
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
    """Add YAML frontmatter to content."""
    frontmatter = "---\n"
    for key, value in metadata.items():
        if isinstance(value, (list, dict)):
            frontmatter += f"{key}: {yaml.dump(value, default_flow_style=True).strip()}\n"
        else:
            frontmatter += f'{key}: "{value}"\n'
    frontmatter += "---\n\n"

    return frontmatter + content


def get_content_folder_path(beirek_area: str, beirek_subarea: str = None,
                           content_type: str = 'haber', slug: str = '') -> str:
    """Get full path for content folder."""
    storage = get_storage()
    area_folder, subarea_folder = storage.get_area_folder_name(beirek_area, beirek_subarea)

    today = date.today().isoformat()
    folder_name = f"{today}_{content_type}_{slug}"

    if subarea_folder:
        final_path = storage.content_path / area_folder / subarea_folder / folder_name
    else:
        final_path = storage.content_path / area_folder / folder_name

    return str(final_path)


# =============================================================================
# PROPOSAL FUNCTIONS (for compatibility with existing code)
# =============================================================================

def add_content_proposal(article_id: int, beirek_area: str, beirek_subarea: str,
                        suggested_title: str, content_angle: str,
                        brief_description: str = None, target_audience: str = None,
                        key_talking_points: str = None,
                        confidence_score: float = None) -> int:
    """Add a content proposal (stored as pending approval)."""
    storage = get_storage()

    article = {
        'id': article_id,
        'title': suggested_title,
        'url': '',
        'summary': brief_description or ''
    }

    filter_result = {
        'score': (confidence_score or 0.7) * 10,
        'reason': content_angle,
        'beirek_area': beirek_area,
        'beirek_subarea': beirek_subarea,
        'confidence_score': confidence_score,
        'target_audience': target_audience,
        'key_talking_points': key_talking_points
    }

    approval_id = storage.add_pending_approval(article, filter_result)
    return hash(approval_id) % 1000000  # Return numeric ID for compatibility


def get_proposals_by_status(status: str = 'suggested', limit: int = 50) -> List[Dict]:
    """Get proposals by status."""
    storage = get_storage()

    if status == 'suggested':
        return storage.get_pending_approvals()[:limit]
    elif status == 'accepted':
        return storage.get_approved_articles()[:limit]
    else:
        return []


def get_proposal_by_id(proposal_id: int) -> Optional[Dict]:
    """Get proposal by ID."""
    # For compatibility, this is simplified
    return None


def update_proposal_status(proposal_id: int, status: str, folder_path: str = None) -> None:
    """Update proposal status."""
    # For compatibility, this is simplified
    pass


def accept_proposal(proposal_id: int) -> None:
    """Accept a proposal."""
    pass


def reject_proposal(proposal_id: int) -> None:
    """Reject a proposal."""
    pass


def get_proposals_for_outline() -> List[Dict]:
    """Get accepted proposals ready for outline creation."""
    return get_storage().get_approved_articles()


def get_proposals_for_generation() -> List[Dict]:
    """Get proposals ready for content generation."""
    return get_storage().get_approved_articles()


def get_today_proposals() -> List[Dict]:
    """Get all proposals created today."""
    return get_storage().get_pending_approvals()


def get_proposal_stats() -> Dict[str, int]:
    """Get proposal statistics."""
    storage = get_storage()
    data = storage._load_json(storage.pending_approvals_file, {})

    return {
        'suggested': len(data.get('pending', [])),
        'accepted': len(data.get('approved', [])),
        'rejected': len(data.get('rejected', [])),
        'outline_created': 0,
        'content_generated': len([a for a in data.get('approved', []) if a.get('content_generated')]),
        'today_total': len(data.get('pending', []))
    }


# Dummy functions for unused features
def update_article_relevance(*args, **kwargs): pass
def update_article_beirek_area(*args, **kwargs): pass
def get_relevant_articles(*args, **kwargs): return []
def mark_article_selected(*args, **kwargs): pass
def mark_article_processed(*args, **kwargs): pass
def get_pending_articles(*args, **kwargs): return []
def get_article_by_id(*args, **kwargs): return None
def update_article_full_content(*args, **kwargs): pass
def get_recent_article_titles(*args, **kwargs): return []
def save_generated_content(*args, **kwargs): return 1
def get_content_by_article(*args, **kwargs): return []
def mark_content_published(*args, **kwargs): pass
def import_glossary_from_file(*args, **kwargs): return 0
def get_unused_terms(*args, **kwargs): return []
def mark_term_used(*args, **kwargs): pass
def get_term_by_id(*args, **kwargs): return None
def search_terms(*args, **kwargs): return []
def get_glossary_stats(*args, **kwargs): return {'total': 0, 'used': 0, 'remaining': 0}
def add_daily_concept(*args, **kwargs): return 1
def get_today_concept(*args, **kwargs): return None
def get_concept_history(*args, **kwargs): return []
def update_concept_content_path(*args, **kwargs): pass
def add_content_request(*args, **kwargs): return 1
def get_pending_requests(*args, **kwargs): return []
def get_request_by_folder(*args, **kwargs): return None
def update_request_status(*args, **kwargs): pass
def complete_request(*args, **kwargs): pass
def deactivate_source(*args, **kwargs): pass


if __name__ == "__main__":
    print("Initializing folder-based storage...")
    storage = get_storage()
    print(f"Content path: {storage.content_path}")
    print(f"Data path: {storage.data_path}")

    stats = storage.get_stats()
    print(f"\nCurrent stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
