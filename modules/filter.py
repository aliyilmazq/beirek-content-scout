"""
BEIREK Content Scout - Filter Module
====================================

Claude session integration for article filtering and relevance scoring.

Features:
- Batch article filtering
- Relevance scoring (0-10)
- BEIREK area assignment
- JSON response parsing
- Uses ClaudeSession for efficient API calls
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from .storage import (
    update_article_relevance, update_article_beirek_area,
    get_unfiltered_articles
)
from .logger import get_logger
from .config_manager import config, safe_json_parse
from .claude_session import get_session, ClaudeSessionError

# Module logger
logger = get_logger(__name__)


class FilterError(Exception):
    """Base exception for filtering errors."""
    pass


class ClaudeCLIError(FilterError):
    """Claude CLI execution error."""
    pass


class ArticleFilter:
    """
    Article filter using Claude session.

    Handles:
    - Preparing filter prompts
    - Calling Claude via session
    - Parsing responses
    - Updating article relevance
    """

    def __init__(self, config_path: str = None):
        """
        Initialize filter.

        Args:
            config_path: Path to config.yaml (optional, uses singleton config if not provided)
        """
        self.base_path = config.base_path

        # Use singleton config
        self.min_score = config.get('filtering.min_relevance_score', 7)
        self.batch_size = config.get('filtering.batch_size', 10)
        self.timeout = config.get('claude.timeout_seconds', 180)

        # Load filter prompt
        self.filter_prompt = self._load_prompt('filter_prompt.txt')

        # Get Claude session
        self.session = get_session()
        if not self.session.is_available():
            raise ClaudeCLIError("Claude CLI not found. Please install it first.")

        logger.info(f"Filter initialized: min_score={self.min_score}, batch_size={self.batch_size}")

    def _load_prompt(self, filename: str) -> str:
        """Load prompt from file."""
        prompt_path = self.base_path / "prompts" / filename

        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # Return default prompt if file doesn't exist
            return self._get_default_filter_prompt()

    def _get_default_filter_prompt(self) -> str:
        """Get default filter prompt."""
        return """Sen BEIREK için içerik filtreleme asistanısın.

GÖREV: Aşağıdaki haberleri BEIREK'in ilgi alanına göre değerlendir ve puanla.

BEIREK İLGİ ALANLARI:
1. Utility-scale güneş enerjisi projeleri (50MW+)
2. Rüzgar enerjisi projeleri (onshore/offshore)
3. Enerji depolama sistemleri (BESS)
4. Data center altyapı projeleri
5. Şebeke modernizasyonu ve transmission projeleri
6. Proje finansmanı ve IFI/DFI haberleri
7. EPC kontratları ve mega proje ihaleleri
8. ABD enerji politikaları ve teşvikler (IRA, vb.)
9. Hidrojen ve yeşil amonyak projeleri

COĞRAFİ ODAK:
- Birincil: ABD (özellikle Texas, California, Arizona, Virginia)
- İkincil: Latin Amerika, Orta Doğu

HARİÇ TUTULACAKLAR:
- Residential/konut ölçekli projeler
- Genel ekonomi haberleri (enerji bağlantısı olmayan)
- Şirket iç duyuruları (earnings)
- Ürün lansmanları

Her haber için 0-10 arası puan ver:
- 9-10: Çok ilgili, hemen işlenmeli
- 7-8: İlgili, içerik üretilebilir
- 4-6: Kısmen ilgili, düşük öncelik
- 0-3: İlgisiz, atlanmalı

YANIT FORMATI (JSON):
```json
[
  {"id": 1, "score": 9, "relevant": true, "reason": "500MW güneş projesi, Texas, proje finansmanı", "beirek_area": "4", "beirek_subarea": "3"},
  {"id": 2, "score": 3, "relevant": false, "reason": "Residential solar, ilgi alanı dışı"}
]
```

BEIREK ALANLARI:
1: Deal & Contract Advisory
2: CEO Office & Governance
3: Development Finance & Compliance
4: Project Development & Finance
5: Engineering & Delivery
6: Asset Management (O&M)
7: GTM & JV Management
8: Digital Platforms

MAKALELER:
"""


    def prepare_batch_prompt(self, articles: List[Dict]) -> str:
        """
        Prepare filtering prompt for a batch of articles.

        Args:
            articles: List of article dicts

        Returns:
            Complete prompt string
        """
        prompt = self.filter_prompt + "\n"

        for i, article in enumerate(articles, 1):
            # Skip articles with empty or missing titles
            title = article.get('title', '').strip()
            if not title:
                title = "[Başlık Bulunamadı]"

            prompt += f"\n[{i}] Başlık: {title}\n"
            prompt += f"Kaynak: {article.get('source_name', 'Unknown')}\n"
            if article.get('summary'):
                # Truncate summary if too long
                summary = article['summary'][:500]
                prompt += f"Özet: {summary}\n"
            prompt += "\n"

        return prompt

    def call_claude_cli(self, prompt: str) -> str:
        """
        Call Claude via session.

        Args:
            prompt: Prompt string

        Returns:
            Claude's response
        """
        try:
            # Use session for efficient Claude calls
            return self.session.query(prompt, include_system_prompt=False)

        except ClaudeSessionError as e:
            logger.error(f"Claude session error: {e}")
            raise ClaudeCLIError(f"Claude CLI hatasi: {e}")

    def parse_filter_response(self, response: str, articles: List[Dict]) -> List[Dict]:
        """
        Parse Claude's filtering response.

        Args:
            response: Claude's response string
            articles: Original articles list (for ID mapping)

        Returns:
            List of parsed results
        """
        results = []

        # Try to extract JSON using safe_json_parse
        parsed = safe_json_parse(response, default=[])

        if isinstance(parsed, list) and parsed:
            for item in parsed:
                idx = item.get('id', 0) - 1  # Convert to 0-indexed

                if 0 <= idx < len(articles):
                    results.append({
                        'article_id': articles[idx].get('id'),
                        'article': articles[idx],
                        'score': float(item.get('score', 0)),
                        'relevant': item.get('relevant', False),
                        'reason': item.get('reason', ''),
                        'beirek_area': str(item.get('beirek_area', '')),
                        'beirek_subarea': str(item.get('beirek_subarea', ''))
                    })

            if results:
                return results

        # Fallback: Try to parse line by line
        for line in response.split('\n'):
            # Look for patterns like "[1] Score: 8" or "1. score=8"
            match = re.search(r'\[?(\d+)\]?\s*[:\-]?\s*(?:score|puan)[:\s=]*(\d+)', line, re.IGNORECASE)
            if match:
                idx = int(match.group(1)) - 1
                score = int(match.group(2))

                if 0 <= idx < len(articles):
                    results.append({
                        'article_id': articles[idx].get('id'),
                        'article': articles[idx],
                        'score': float(score),
                        'relevant': score >= self.min_score,
                        'reason': '',
                        'beirek_area': '',
                        'beirek_subarea': ''
                    })

        return results

    def filter_articles(self, articles: List[Dict] = None,
                       progress_callback=None) -> List[Dict]:
        """
        Filter articles using Claude.

        Args:
            articles: Articles to filter (or fetch from DB if None)
            progress_callback: Progress callback function

        Returns:
            List of relevant articles
        """
        # Get articles from DB if not provided
        if articles is None:
            articles = get_unfiltered_articles()

        if not articles:
            return []

        all_results = []
        total_batches = (len(articles) + self.batch_size - 1) // self.batch_size

        # Process in batches
        for batch_num in range(total_batches):
            start_idx = batch_num * self.batch_size
            end_idx = min(start_idx + self.batch_size, len(articles))
            batch = articles[start_idx:end_idx]

            if progress_callback:
                progress_callback(batch_num + 1, total_batches)

            try:
                # Prepare and send prompt
                prompt = self.prepare_batch_prompt(batch)
                response = self.call_claude_cli(prompt)

                # Parse response
                results = self.parse_filter_response(response, batch)

                # Update database
                for result in results:
                    if result['article_id']:
                        update_article_relevance(
                            result['article_id'],
                            result['score'],
                            result['relevant'],
                            result['reason']
                        )

                        if result['relevant'] and result['beirek_area']:
                            update_article_beirek_area(
                                result['article_id'],
                                result['beirek_area'],
                                result['beirek_subarea']
                            )

                all_results.extend(results)

            except Exception as e:
                logger.error(f"Error filtering batch {batch_num + 1}: {e}")
                # Mark batch as unfiltered (score = -1)
                for article in batch:
                    if article.get('id'):
                        update_article_relevance(article['id'], -1, False, f"Error: {e}")

        # Return only relevant articles
        return [r for r in all_results if r['relevant']]

    def get_beirek_area_for_article(self, article: Dict) -> Tuple[str, str]:
        """
        Get BEIREK area assignment for a single article.

        Args:
            article: Article dict with title and content

        Returns:
            Tuple of (beirek_area, beirek_subarea)
        """
        prompt = f"""Aşağıdaki makale için en uygun BEIREK çalışma alanını belirle.

MAKALE:
Başlık: {article.get('title', '')}
İçerik: {article.get('summary', article.get('full_content', ''))[:1000]}

BEIREK ALANLARI:
1: Deal & Contract Advisory (1-4 alt alan)
2: CEO Office & Governance (1-4 alt alan)
3: Development Finance & Compliance (1-4 alt alan)
4: Project Development & Finance (1-4 alt alan)
5: Engineering & Delivery (1-4 alt alan)
6: Asset Management (O&M) (1-4 alt alan)
7: GTM & JV Management (1-4 alt alan)
8: Digital Platforms (1-3 alt alan)

YANIT FORMATI (sadece JSON):
{{"area": "4", "subarea": "3", "reason": "Proje finansmanı ile ilgili"}}
"""

        try:
            response = self.call_claude_cli(prompt)

            # Parse JSON response using safe_json_parse
            parsed = safe_json_parse(response, default={'area': '4', 'subarea': '3'})
            return (
                str(parsed.get('area', '4')),
                str(parsed.get('subarea', '3'))
            )

        except Exception as e:
            logger.warning(f"Error getting BEIREK area: {e}")

        # Default fallback
        return ('4', '3')  # Project Development & Finance / Project Finance Structuring


if __name__ == "__main__":
    # Test filter
    print("Testing ArticleFilter...")

    try:
        filter = ArticleFilter()
        print("Claude CLI is available!")

        # Test with sample articles
        test_articles = [
            {
                'id': 1,
                'title': 'Texas Solar Project Reaches $500M Financial Close',
                'summary': 'A 500MW solar project in Texas has reached financial close with $500 million in project financing from major IFIs.',
                'source_name': 'Utility Dive'
            },
            {
                'id': 2,
                'title': 'New iPhone Released',
                'summary': 'Apple announces the latest iPhone with improved features.',
                'source_name': 'Tech News'
            }
        ]

        print("\nPreparing filter prompt...")
        prompt = filter.prepare_batch_prompt(test_articles)
        print(f"Prompt length: {len(prompt)} chars")

        print("\nFilter module ready!")

    except ClaudeCLIError as e:
        print(f"Claude CLI Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
