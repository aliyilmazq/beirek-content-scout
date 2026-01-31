"""
BEIREK Content Scout - Request Manager Module
=============================================

Manual content request handling.

Features:
- Scan request pool folder for new requests
- Parse brief files
- Generate content for requests
- Copy to BEIREK areas
"""

import subprocess
import json
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from .storage import (
    add_content_request, get_pending_requests, update_request_status,
    complete_request, get_request_by_folder, generate_slug,
    save_content_to_file, add_frontmatter, save_generated_content
)
from .logger import get_logger
from .config_manager import config, safe_json_parse

# Module logger
logger = get_logger(__name__)


class RequestError(Exception):
    """Base exception for request operations."""
    pass


class RequestManager:
    """
    Manager for content request pool.

    Handles:
    - Scanning request pool folder
    - Parsing brief.md files
    - Content generation
    - Copying to BEIREK areas
    """

    def __init__(self, config_path: str = None):
        """
        Initialize request manager.

        Args:
            config_path: Path to config.yaml (optional, uses singleton config if not provided)
        """
        self.base_path = config.base_path

        # Use singleton config
        self.timeout = config.get('claude.timeout_seconds', 180)

        # Paths
        self.output_base = Path(self.base_path) / config.get('content.output_base_path', '../content')
        self.request_pool_path = self.output_base / "istek-havuzu"

        # BEIREK areas mapping
        self.beirek_areas = config.beirek_areas

        logger.info("RequestManager initialized")

    def scan_request_pool(self) -> List[Dict]:
        """
        Scan request pool folder for new requests.

        Returns:
            List of request dicts
        """
        requests = []

        if not self.request_pool_path.exists():
            return requests

        # Iterate through folders
        for item in self.request_pool_path.iterdir():
            if item.is_dir() and item.name != 'NASIL-KULLANILIR.md':
                # Check if already processed
                has_content = (item / 'makale.md').exists()

                request = {
                    'folder_name': item.name,
                    'folder_path': str(item),
                    'has_brief': (item / 'brief.md').exists(),
                    'brief_content': None,
                    'status': 'completed' if has_content else 'pending',
                    'created_at': datetime.fromtimestamp(item.stat().st_ctime)
                }

                # Parse brief if exists
                if request['has_brief']:
                    request['brief_content'] = self.parse_brief(item / 'brief.md')

                requests.append(request)

        # Sort by creation time
        requests.sort(key=lambda x: x['created_at'])

        return requests

    def parse_brief(self, brief_path: Path) -> Dict:
        """
        Parse brief.md file.

        Expected format:
        # Konu
        Topic title

        # Odak
        - Focus point 1
        - Focus point 2

        # Hedef Kitle
        - Target 1

        # BEIREK Alanı
        4-project-development-finance/3-project-finance-structuring
        """
        brief = {
            'topic': '',
            'focus_points': [],
            'target_audience': [],
            'beirek_area': '',
            'beirek_subarea': '',
            'raw_content': ''
        }

        if not brief_path.exists():
            return brief

        with open(brief_path, 'r', encoding='utf-8') as f:
            content = f.read()

        brief['raw_content'] = content

        # Parse sections
        current_section = None
        for line in content.split('\n'):
            line = line.strip()

            if line.startswith('# '):
                section_name = line[2:].lower()
                if 'konu' in section_name or 'topic' in section_name:
                    current_section = 'topic'
                elif 'odak' in section_name or 'focus' in section_name:
                    current_section = 'focus'
                elif 'hedef' in section_name or 'kitle' in section_name or 'target' in section_name:
                    current_section = 'target'
                elif 'beirek' in section_name or 'alan' in section_name:
                    current_section = 'beirek'
                else:
                    current_section = None
            elif line and current_section:
                if current_section == 'topic':
                    brief['topic'] = line
                elif current_section == 'focus':
                    if line.startswith('-'):
                        brief['focus_points'].append(line[1:].strip())
                    else:
                        brief['focus_points'].append(line)
                elif current_section == 'target':
                    if line.startswith('-'):
                        brief['target_audience'].append(line[1:].strip())
                    else:
                        brief['target_audience'].append(line)
                elif current_section == 'beirek':
                    # Parse BEIREK area path
                    if '/' in line:
                        parts = line.split('/')
                        brief['beirek_area'] = parts[0].strip()
                        brief['beirek_subarea'] = parts[1].strip() if len(parts) > 1 else ''
                    else:
                        brief['beirek_area'] = line.strip()

        # If no topic, use folder name
        if not brief['topic']:
            brief['topic'] = brief_path.parent.name.replace('-', ' ').title()

        return brief

    def determine_beirek_area(self, topic: str, focus_points: List[str] = None) -> tuple:
        """
        Determine BEIREK area for a topic using Claude.

        Args:
            topic: Content topic
            focus_points: Focus points from brief

        Returns:
            Tuple of (beirek_area, beirek_subarea)
        """
        focus_text = "\n".join([f"- {p}" for p in (focus_points or [])])

        prompt = f"""Aşağıdaki konu için en uygun BEIREK çalışma alanını belirle.

KONU: {topic}
ODAK NOKTALARI:
{focus_text}

BEIREK ALANLARI:
1-deal-contract-advisory (alt alanlar: 1-4)
2-ceo-office-governance (alt alanlar: 1-4)
3-development-finance-compliance (alt alanlar: 1-4)
4-project-development-finance (alt alanlar: 1-4)
5-engineering-delivery (alt alanlar: 1-4)
6-asset-management-om (alt alanlar: 1-4)
7-gtm-jv-management (alt alanlar: 1-4)
8-digital-platforms (alt alanlar: 1-3)

YANIT (sadece JSON):
{{"area": "4-project-development-finance", "subarea": "3-project-finance-structuring"}}
"""

        try:
            response = self.call_claude_cli(prompt)

            # Use safe_json_parse
            parsed = safe_json_parse(response, default={
                'area': '4-project-development-finance',
                'subarea': '3-project-finance-structuring'
            })

            return (
                parsed.get('area', '4-project-development-finance'),
                parsed.get('subarea', '3-project-finance-structuring')
            )
        except Exception as e:
            logger.warning(f"Error determining BEIREK area: {e}")

        # Default fallback
        return ('4-project-development-finance', '3-project-finance-structuring')

    def call_claude_cli(self, prompt: str) -> str:
        """Call Claude CLI with prompt."""
        try:
            process = subprocess.Popen(
                ['claude', '--print'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = process.communicate(
                input=prompt,
                timeout=self.timeout
            )

            if process.returncode != 0:
                raise RequestError(f"Claude CLI error: {stderr}")

            return stdout.strip()

        except subprocess.TimeoutExpired:
            process.kill()
            logger.error(f"Claude CLI timeout after {self.timeout}s in request manager")
            raise RequestError(
                f"Claude CLI timeout ({self.timeout}s asildi). "
                "Istek isleme cok uzun suruyor."
            )
        except FileNotFoundError:
            raise RequestError(
                "Claude CLI bulunamadi! Lutfen kurun: https://claude.ai/cli"
            )
        except Exception as e:
            logger.error(f"Claude CLI error in request manager: {e}")
            raise RequestError(f"Claude CLI hatasi: {e}")

    def generate_request_content(self, request: Dict) -> Dict:
        """
        Generate content for a request.

        Args:
            request: Request dict with topic and brief

        Returns:
            Generated content dict
        """
        brief = request.get('brief_content', {})
        topic = brief.get('topic', request['folder_name'].replace('-', ' ').title())
        focus_points = brief.get('focus_points', [])
        target_audience = brief.get('target_audience', [])

        # Build context
        focus_text = "\n".join([f"- {p}" for p in focus_points]) if focus_points else "Belirtilmemiş"
        target_text = "\n".join([f"- {t}" for t in target_audience]) if target_audience else "Genel profesyonel kitle"

        prompt = f"""Sen BEIREK'in kıdemli içerik stratejistisin. Aşağıdaki konu için 3 formatta içerik üret.

KONU: {topic}

ODAK NOKTALARI:
{focus_text}

HEDEF KİTLE:
{target_text}

---

FORMAT 1: MAKALE (1500-2500 kelime)
- Kapsamlı araştırma makalesi
- BEIREK perspektifi ekle
- Profesyonel, thought leadership tonu

FORMAT 2: LINKEDIN (150-300 kelime)
Yapı:
1. HOOK: Dikkat çekici açılış
2. PROBLEM: Sektörün yaşadığı zorluk
3. BEIREK YAKLAŞIMI: "Biz bu konuya farklı bakıyoruz..."
4. CTA: "Biz böyle çözüyoruz. Sizin projelerinizde bu nasıl yönetiliyor?"

FORMAT 3: TWITTER (5-10 tweet)
- Her tweet 280 karakter altında
- 1/X formatında numaralandır

---

YANIT FORMATI:

===MAKALE===
[makale içeriği]

===LINKEDIN===
[linkedin içeriği]

===TWITTER===
[twitter içeriği]
"""

        response = self.call_claude_cli(prompt)

        # Parse response
        content = self._parse_content_response(response)
        content['metadata'] = {
            'topic': topic,
            'generated_at': datetime.now().isoformat()
        }

        return content

    def _parse_content_response(self, response: str) -> Dict:
        """Parse Claude's content response into formats."""
        content = {
            'article': '',
            'linkedin': '',
            'twitter': ''
        }

        if '===MAKALE===' in response:
            parts = response.split('===')
            for i, part in enumerate(parts):
                if 'MAKALE' in part and i + 1 < len(parts):
                    content['article'] = parts[i + 1].strip()
                elif 'LINKEDIN' in part and i + 1 < len(parts):
                    content['linkedin'] = parts[i + 1].strip()
                elif 'TWITTER' in part and i + 1 < len(parts):
                    content['twitter'] = parts[i + 1].strip()
        else:
            # Fallback: use whole response as article
            content['article'] = response

        return content

    def save_request_content(self, request: Dict, content: Dict,
                            beirek_area: str, beirek_subarea: str,
                            request_id: int = None) -> str:
        """
        Save request content to files and database.

        Args:
            request: Request dict
            content: Generated content
            beirek_area: BEIREK area
            beirek_subarea: BEIREK sub-area
            request_id: Request ID for DB linking (optional)

        Returns:
            Content folder path
        """
        folder_path = Path(request['folder_path'])
        topic = request.get('brief_content', {}).get('topic', request['folder_name'])

        # Frontmatter
        frontmatter_data = {
            'title': topic,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'request',
            'beirek_area': beirek_area,
            'beirek_subarea': beirek_subarea,
            'generated_by': 'BEIREK Content Scout'
        }

        # Save files
        file_mappings = {
            'article': 'makale.md',
            'linkedin': 'linkedin.md',
            'twitter': 'twitter.md'
        }

        for format_key, filename in file_mappings.items():
            if content.get(format_key):
                content_with_frontmatter = add_frontmatter(
                    content[format_key],
                    {**frontmatter_data, 'format': format_key}
                )

                file_path = folder_path / filename
                save_content_to_file(content_with_frontmatter, str(file_path))

                # Save to database for tracking
                save_generated_content(
                    content_type=format_key,
                    title=topic,
                    content=content[format_key],
                    file_path=str(file_path),
                    request_id=request_id
                )

        return str(folder_path)

    def copy_to_beirek_area(self, source_folder: str, beirek_area: str,
                           beirek_subarea: str) -> str:
        """
        Copy content to BEIREK area folder.

        Args:
            source_folder: Source folder path
            beirek_area: Target BEIREK area
            beirek_subarea: Target sub-area

        Returns:
            Destination folder path
        """
        source = Path(source_folder)

        # Build destination path
        dest_base = self.output_base / beirek_area
        if beirek_subarea:
            dest_base = dest_base / beirek_subarea

        # Create folder with date prefix
        today = datetime.now().strftime('%Y-%m-%d')
        folder_name = f"{today}_istek_{source.name}"
        dest_folder = dest_base / folder_name

        # Copy folder
        if dest_folder.exists():
            shutil.rmtree(dest_folder)

        shutil.copytree(source, dest_folder)

        return str(dest_folder)

    def process_request(self, request: Dict) -> Dict:
        """
        Process a single request.

        Args:
            request: Request dict

        Returns:
            Processing result
        """
        result = {
            'request_id': None,
            'content_generated': False,
            'files_created': [],
            'copied_to': None,
            'error': None
        }

        try:
            # Get or create database record
            db_request = get_request_by_folder(request['folder_name'])
            if not db_request:
                brief = request.get('brief_content', {})
                request_id = add_content_request(
                    folder_name=request['folder_name'],
                    topic=brief.get('topic', ''),
                    brief=brief.get('raw_content', '')
                )
                result['request_id'] = request_id
            else:
                result['request_id'] = db_request['id']

            # Update status
            update_request_status(result['request_id'], 'processing')

            # Determine BEIREK area
            brief = request.get('brief_content', {})
            if brief.get('beirek_area'):
                beirek_area = brief['beirek_area']
                beirek_subarea = brief.get('beirek_subarea', '')
            else:
                beirek_area, beirek_subarea = self.determine_beirek_area(
                    brief.get('topic', request['folder_name']),
                    brief.get('focus_points', [])
                )

            # Generate content
            logger.info(f"Generating content for: {request['folder_name']}")
            content = self.generate_request_content(request)

            # Save to request folder with DB tracking
            self.save_request_content(
                request, content, beirek_area, beirek_subarea,
                request_id=result['request_id']
            )
            result['files_created'] = ['makale.md', 'linkedin.md', 'twitter.md']
            result['content_generated'] = True

            # Copy to BEIREK area
            copied_path = self.copy_to_beirek_area(
                request['folder_path'],
                beirek_area,
                beirek_subarea
            )
            result['copied_to'] = copied_path

            # Complete request
            complete_request(
                result['request_id'],
                beirek_area,
                beirek_subarea,
                request['folder_path']
            )

        except Exception as e:
            result['error'] = str(e)
            if result['request_id']:
                update_request_status(result['request_id'], 'failed')

        return result

    def process_all_pending(self) -> Dict:
        """
        Process all pending requests.

        Returns:
            Summary of processing
        """
        requests = self.scan_request_pool()
        pending = [r for r in requests if r['status'] == 'pending']

        summary = {
            'processed': 0,
            'success': 0,
            'failed': 0,
            'details': []
        }

        for request in pending:
            print(f"\nProcessing: {request['folder_name']}")
            result = self.process_request(request)

            summary['processed'] += 1
            summary['details'].append({
                'folder': request['folder_name'],
                'success': result['content_generated'],
                'copied_to': result['copied_to'],
                'error': result['error']
            })

            if result['content_generated']:
                summary['success'] += 1
            else:
                summary['failed'] += 1

        return summary


if __name__ == "__main__":
    print("Testing RequestManager...")

    manager = RequestManager()

    # Scan request pool
    requests = manager.scan_request_pool()
    print(f"\nFound {len(requests)} requests in pool")

    for req in requests:
        print(f"  - {req['folder_name']} ({req['status']})")
        if req['has_brief']:
            print(f"    Topic: {req['brief_content'].get('topic', 'N/A')}")

    print("\nRequestManager ready!")
