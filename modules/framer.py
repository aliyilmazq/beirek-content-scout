"""
BEIREK Content Scout - Framer Module
=====================================

Content framing for BEIREK perspective.

Takes filtered articles and creates content proposals
with BEIREK area assignment, content angles, and key talking points.
"""

import subprocess
import json
import re
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple

from .storage import (
    add_content_proposal, get_proposal_by_id, update_proposal_status,
    get_article_by_id, save_content_to_file, generate_slug
)
from .logger import get_logger
from .config_manager import config, Constants, safe_json_parse

# Module logger
logger = get_logger(__name__)


class FramerError(Exception):
    """Base exception for framer errors."""
    pass


class ContentFramer:
    """
    Content framer using Claude CLI.

    Analyzes articles and creates content proposals from BEIREK perspective.
    """

    def __init__(self, config_path: str = None):
        """
        Initialize framer.

        Args:
            config_path: Path to config.yaml (optional, uses singleton config if not provided)
        """
        self.base_path = config.base_path

        # Use singleton config
        self.config = {
            'content': config.content,
            'beirek_areas': config.beirek_areas
        }
        self.timeout = config.get('claude.timeout_seconds', 180)
        self.beirek_areas = config.beirek_areas

        # Load framing prompt
        self.framing_prompt = self._load_prompt('framing_prompt.txt')

        logger.info("Framer initialized")

    def _load_prompt(self, filename: str) -> str:
        """Load prompt from file."""
        prompt_path = self.base_path / "prompts" / filename

        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise FramerError(f"Prompt file not found: {prompt_path}")

    def call_claude_cli(self, prompt: str) -> str:
        """
        Call Claude CLI with prompt.

        Args:
            prompt: Prompt string

        Returns:
            Claude's response
        """
        process = None
        try:
            process = subprocess.Popen(
                ['claude', '--print'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False  # Explicit for security
            )

            stdout, stderr = process.communicate(
                input=prompt,
                timeout=self.timeout
            )

            if process.returncode != 0:
                raise FramerError(f"Claude CLI error: {stderr}")

            return stdout.strip()

        except subprocess.TimeoutExpired:
            if process:
                process.kill()
                process.wait()  # Ensure process is reaped
            logger.error(f"Claude CLI timeout after {self.timeout}s during framing")
            raise FramerError(
                f"Claude CLI timeout ({self.timeout}s asildi). "
                "Cerceveleme islemi cok uzun suruyor."
            )
        except FileNotFoundError:
            raise FramerError(
                "Claude CLI bulunamadi! Lutfen kurun: https://claude.ai/cli"
            )
        except FramerError:
            raise
        except Exception as e:
            if process and process.poll() is None:
                process.kill()
                process.wait()
            logger.error(f"Claude CLI error in framer: {e}")
            raise FramerError(f"Claude CLI hatasi: {e}")

    def frame_article(self, article: Dict) -> Optional[Dict]:
        """
        Create content proposal for a single article.

        Args:
            article: Article dict with title, summary, source_name

        Returns:
            Proposal dict or None if framing failed
        """
        # Prepare prompt
        content = article.get('full_content') or article.get('summary') or ''
        prompt = self.framing_prompt.replace('{article_content}', content[:Constants.MAX_ARTICLE_CONTENT_LENGTH])
        prompt = prompt.replace('{article_title}', article.get('title', ''))
        prompt = prompt.replace('{source_name}', article.get('source_name', 'Unknown'))

        try:
            response = self.call_claude_cli(prompt)

            # Parse JSON response using safe_json_parse
            parsed = safe_json_parse(response, default={})

            # Validate required fields
            if not all(k in parsed for k in ['beirek_area', 'suggested_title', 'content_angle']):
                logger.warning(f"Missing required fields in framing response for article {article.get('id')}")
                return None

            # Validate confidence_score
            confidence = parsed.get('confidence_score', 0.7)
            try:
                confidence = float(confidence)
                confidence = max(0.0, min(1.0, confidence))  # Clamp to 0-1
            except (TypeError, ValueError):
                confidence = 0.7

            return {
                'article_id': article.get('id'),
                'beirek_area': str(parsed.get('beirek_area', '4')),
                'beirek_subarea': str(parsed.get('beirek_subarea', '')),
                'suggested_title': parsed.get('suggested_title', ''),
                'content_angle': parsed.get('content_angle', ''),
                'brief_description': parsed.get('brief_description', ''),
                'target_audience': parsed.get('target_audience', ''),
                'key_talking_points': json.dumps(
                    parsed.get('key_talking_points', []),
                    ensure_ascii=False
                ),
                'confidence_score': confidence
            }

        except FramerError as e:
            logger.warning(f"Framing error for article {article.get('id')}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error framing article {article.get('id')}: {e}")

        return None

    def frame_articles(self, articles: List[Dict],
                      progress_callback=None) -> List[Dict]:
        """
        Create content proposals for multiple articles.

        Args:
            articles: List of article dicts
            progress_callback: Optional callback(current, total)

        Returns:
            List of created proposal dicts
        """
        proposals = []
        total = len(articles)

        for i, article in enumerate(articles):
            if progress_callback:
                progress_callback(i + 1, total)

            proposal_data = self.frame_article(article)

            if proposal_data:
                # Save to database
                proposal_id = add_content_proposal(
                    article_id=proposal_data['article_id'],
                    beirek_area=proposal_data['beirek_area'],
                    beirek_subarea=proposal_data['beirek_subarea'],
                    suggested_title=proposal_data['suggested_title'],
                    content_angle=proposal_data['content_angle'],
                    brief_description=proposal_data['brief_description'],
                    target_audience=proposal_data['target_audience'],
                    key_talking_points=proposal_data['key_talking_points'],
                    confidence_score=proposal_data['confidence_score']
                )

                proposal_data['id'] = proposal_id
                proposal_data['article_title'] = article.get('title', '')
                proposal_data['source_name'] = article.get('source_name', '')
                proposals.append(proposal_data)

        return proposals

    def get_area_full_name(self, area: str, subarea: str = None) -> tuple:
        """
        Get full area and subarea names from numbers.

        Args:
            area: Area number (e.g., "4")
            subarea: Sub-area number (e.g., "3")

        Returns:
            Tuple of (full_area_name, full_subarea_name)
        """
        area_info = self.beirek_areas.get(str(area), {})

        if isinstance(area_info, dict):
            area_name = f"{area}-{area_info.get('name', '')}"
            subareas = area_info.get('subareas', {})
            subarea_name = subareas.get(str(subarea), '') if subarea else ''
            if subarea_name:
                subarea_name = f"{subarea}-{subarea_name}"
        else:
            area_name = f"{area}-{area_info}" if area_info else str(area)
            subarea_name = str(subarea) if subarea else ''

        return area_name, subarea_name

    def create_outline_folder(self, proposal_id: int) -> str:
        """
        Create folder structure and outline for accepted proposal.

        Args:
            proposal_id: Proposal ID

        Returns:
            Created folder path
        """
        proposal = get_proposal_by_id(proposal_id)
        if not proposal:
            raise FramerError(f"Proposal not found: {proposal_id}")

        # Get full area names
        area_name, subarea_name = self.get_area_full_name(
            proposal['beirek_area'],
            proposal.get('beirek_subarea')
        )

        # Create folder path
        today = date.today().isoformat()
        slug = generate_slug(proposal['suggested_title'])
        folder_name = f"{today}_haber_{slug}"

        # Build path
        output_base = Path(self.base_path) / self.config['content']['output_base_path']

        if subarea_name:
            folder_path = output_base / area_name / subarea_name / folder_name
        else:
            folder_path = output_base / area_name / folder_name

        # Create folder
        folder_path.mkdir(parents=True, exist_ok=True)

        # Create _proposal.json
        proposal_data = {
            'id': proposal['id'],
            'article_id': proposal['article_id'],
            'beirek_area': proposal['beirek_area'],
            'beirek_subarea': proposal.get('beirek_subarea', ''),
            'suggested_title': proposal['suggested_title'],
            'content_angle': proposal['content_angle'],
            'brief_description': proposal.get('brief_description', ''),
            'target_audience': proposal.get('target_audience', ''),
            'key_talking_points': json.loads(proposal.get('key_talking_points', '[]')),
            'confidence_score': proposal.get('confidence_score'),
            'created_at': proposal.get('created_at'),
            'accepted_at': proposal.get('accepted_at')
        }

        proposal_file = folder_path / '_proposal.json'
        with open(proposal_file, 'w', encoding='utf-8') as f:
            json.dump(proposal_data, f, ensure_ascii=False, indent=2)

        # Create _source.json
        source_data = {
            'article_id': proposal.get('article_id'),
            'title': proposal.get('article_title', ''),
            'url': proposal.get('article_url', ''),
            'summary': proposal.get('article_summary', ''),
            'source_name': proposal.get('source_name', ''),
            'scraped_at': datetime.now().isoformat()
        }

        source_file = folder_path / '_source.json'
        with open(source_file, 'w', encoding='utf-8') as f:
            json.dump(source_data, f, ensure_ascii=False, indent=2)

        # Create _outline.md
        key_points = json.loads(proposal.get('key_talking_points', '[]'))
        outline_content = self._generate_outline(proposal, key_points)

        outline_file = folder_path / '_outline.md'
        with open(outline_file, 'w', encoding='utf-8') as f:
            f.write(outline_content)

        # Update proposal status
        update_proposal_status(proposal_id, 'outline_created', str(folder_path))

        return str(folder_path)

    def _generate_outline(self, proposal: Dict, key_points: List[str]) -> str:
        """
        Generate outline content.

        Args:
            proposal: Proposal dict
            key_points: List of key talking points

        Returns:
            Outline markdown content
        """
        area_name, subarea_name = self.get_area_full_name(
            proposal['beirek_area'],
            proposal.get('beirek_subarea')
        )

        outline = f"""# {proposal['suggested_title']}

## Meta Bilgileri

- **BEIREK Alan:** {area_name}
- **BEIREK Alt Alan:** {subarea_name}
- **Bakış Açısı:** {proposal['content_angle']}
- **Hedef Kitle:** {proposal.get('target_audience', 'Belirlenmedi')}
- **Güven Skoru:** {proposal.get('confidence_score', 0):.2f}

## Kaynak

- **Başlık:** {proposal.get('article_title', '')}
- **Kaynak:** {proposal.get('source_name', '')}
- **URL:** {proposal.get('article_url', '')}

## Kısa Açıklama

{proposal.get('brief_description', 'Açıklama eklenmedi.')}

## Ana Konuşma Noktaları

"""
        for i, point in enumerate(key_points, 1):
            outline += f"{i}. {point}\n"

        outline += """
## İçerik Yapısı (Taslak)

### 1. Giriş
- Hook: [Dikkat çekici açılış]
- Context: [Konunun önemi ve güncelliği]

### 2. Ana Bölüm: [Konu 1]
- Alt başlık 1.1
- Alt başlık 1.2

### 3. Ana Bölüm: [Konu 2]
- Alt başlık 2.1
- Alt başlık 2.2

### 4. BEIREK Perspektifi
- Bu konu neden önemli?
- BEIREK bu sorunu nasıl çözüyor?

### 5. Sonuç ve Çıkarımlar
- Temel öğrenimler
- Eylem önerileri

## Notlar

[Ek notlar ve araştırma gereksinimleri buraya eklenebilir]

---
*Bu outline otomatik olarak BEIREK Content Scout tarafından oluşturulmuştur.*
"""
        return outline

    def create_outlines_for_accepted(self, progress_callback=None) -> List[str]:
        """
        Create outlines for all accepted proposals.

        Args:
            progress_callback: Optional callback(current, total)

        Returns:
            List of created folder paths
        """
        from .storage import get_proposals_for_outline

        proposals = get_proposals_for_outline()
        created_paths = []
        total = len(proposals)

        for i, proposal in enumerate(proposals):
            if progress_callback:
                progress_callback(i + 1, total)

            try:
                path = self.create_outline_folder(proposal['id'])
                created_paths.append(path)
            except Exception as e:
                logger.error(f"Error creating outline for proposal {proposal['id']}: {e}")

        return created_paths


if __name__ == "__main__":
    print("Testing ContentFramer...")

    try:
        framer = ContentFramer()
        print("Framer initialized successfully!")

        # Test area name resolution
        area, subarea = framer.get_area_full_name("4", "3")
        print(f"Area 4.3: {area} / {subarea}")

    except Exception as e:
        print(f"Error: {e}")
