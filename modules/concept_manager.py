"""
BEIREK Content Scout - Concept Manager Module
=============================================

Daily concept selection and content generation from glossary.

Features:
- Glossary import from markdown
- AI-powered concept selection
- Content generation for selected concepts
- History tracking
"""

import subprocess
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, date

from .storage import (
    import_glossary_from_file, get_unused_terms, mark_term_used,
    add_daily_concept, get_today_concept, update_concept_content_path,
    get_glossary_stats, generate_slug, save_content_to_file, add_frontmatter,
    save_generated_content
)
from .logger import get_logger
from .config_manager import config

# Module logger
logger = get_logger(__name__)


class ConceptError(Exception):
    """Base exception for concept operations."""
    pass


class ConceptManager:
    """
    Manager for daily concept selection and content generation.

    Handles:
    - Loading glossary from markdown files
    - AI-powered concept selection
    - Content generation in 3 formats
    - File management
    """

    def __init__(self, config_path: str = None):
        """
        Initialize concept manager.

        Args:
            config_path: Path to config.yaml (optional, uses singleton config if not provided)
        """
        self.base_path = config.base_path

        # Use singleton config
        self.timeout = config.get('claude.timeout_seconds', 180)

        # Content output path
        self.output_base = Path(self.base_path) / config.get('content.output_base_path', '../content')

        # Default glossary path (in data folder)
        self.default_glossary_path = Path(self.base_path) / "data" / "kavram-sozlugu.md"

        # Daily concepts output folder
        self.concepts_output_path = self.output_base / "daily-concepts"

        # Load prompts
        self.selection_prompt = self._load_prompt('concept_selection_prompt.txt')
        self.content_prompt = self._load_prompt('concept_content_prompt.txt')

        logger.info("ConceptManager initialized")

    def _load_prompt(self, filename: str) -> str:
        """Load prompt from file or return default."""
        prompt_path = self.base_path / "prompts" / filename

        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            if 'selection' in filename:
                return self._get_default_selection_prompt()
            else:
                return self._get_default_content_prompt()

    def _get_default_selection_prompt(self) -> str:
        """Default concept selection prompt."""
        return """Sen BEIREK için günlük kavram seçim asistanısın.

GÖREV: Aşağıdaki terimlerden bugün için en uygun kavramı seç.

SEÇİM KRİTERLERİ:
1. BEIREK UYUMU: 8 çalışma alanından birine doğrudan bağlı olmalı
2. ÇARPICILIK: Sektörde tartışmalı veya dikkat çekici
3. C-LEVEL İLGİSİ: Üst yönetimin ilgisini çekebilir
4. GÜNCELLIK: Güncel gelişmelerle bağlantı kurulabilir

BEIREK ALANLARI:
1: Deal & Contract Advisory
2: CEO Office & Governance
3: Development Finance & Compliance
4: Project Development & Finance
5: Engineering & Delivery
6: Asset Management (O&M)
7: GTM & JV Management
8: Digital Platforms

YANIT FORMATI (sadece JSON):
{
  "selected_id": 42,
  "term_en": "Force Majeure",
  "term_tr": "Mücbir Sebep",
  "beirek_area": "1",
  "beirek_subarea": "3",
  "selection_reason": "Küresel tedarik zinciri sorunları nedeniyle çok güncel bir konu"
}

TERİMLER:
{terms}

DAHA ÖNCE KULLANILAN (KAÇIN):
{used_terms}
"""

    def _get_default_content_prompt(self) -> str:
        """Default concept content prompt."""
        return """Sen BEIREK'in thought leadership yazarısın. Seçilen kavram için 3 formatta içerik üret.

KAVRAM: {concept_en} ({concept_tr})
BEIREK ALANI: {beirek_area}
SEÇIM NEDENİ: {selection_reason}

⚠️ ÖNEMLİ:
- Gerçek örnekler ve veriler kullan (uydurma yasak)
- BEIREK perspektifi ve çözüm yaklaşımı ekle
- Her format birbirinden bağımsız yazılmalı

---

FORMAT 1: MAKALE (1500-2500 kelime)
- Kavramın tanımı ve önemi
- Sektördeki uygulamalar
- Yaygın hatalar ve riskler
- BEIREK yaklaşımı
- Sonuç ve öneriler

---

FORMAT 2: LINKEDIN (150-300 kelime)
Yapı:
1. HOOK: Dikkat çekici açılış
2. PROBLEM: Sektörün yaşadığı zorluk
3. BEIREK YAKLAŞIMI: "Biz bu konuya farklı bakıyoruz..."
4. CTA: "Biz böyle çözüyoruz. Sizin projelerinizde bu nasıl yönetiliyor?"

---

FORMAT 3: TWITTER (5-10 tweet)
- Her tweet 280 karakter altında
- 1/X formatında numaralandır
- Her tweet bağımsız değer sunmalı

---

YANIT FORMATI:
Lütfen her formatı aşağıdaki şekilde ayır:

===MAKALE===
[makale içeriği]

===LINKEDIN===
[linkedin içeriği]

===TWITTER===
[twitter içeriği]
"""

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
                raise ConceptError(f"Claude CLI error: {stderr}")

            return stdout.strip()

        except subprocess.TimeoutExpired:
            process.kill()
            raise ConceptError("Claude CLI timed out")
        except Exception as e:
            raise ConceptError(f"Failed to call Claude CLI: {e}")

    def import_glossary(self, file_path: str = None) -> int:
        """
        Import glossary from markdown file to database.

        Args:
            file_path: Path to glossary file (optional)

        Returns:
            Number of terms imported
        """
        path = file_path or str(self.default_glossary_path)

        if not Path(path).exists():
            raise ConceptError(f"Glossary file not found: {path}")

        return import_glossary_from_file(path)

    def get_glossary_status(self) -> Dict:
        """Get glossary statistics."""
        return get_glossary_stats()

    def select_daily_concept(self, recent_news: List[Dict] = None) -> Dict:
        """
        Select today's concept.

        Args:
            recent_news: Recent news for context (optional)

        Returns:
            Selected concept dict
        """
        # Check if already selected today
        existing = get_today_concept()
        if existing:
            return existing

        # Get unused terms
        unused = get_unused_terms(limit=50)
        if not unused:
            raise ConceptError("No unused terms available in glossary")

        # Get recently used terms (to avoid similar topics)
        from .storage import get_concept_history
        recent_concepts = get_concept_history(days=30)
        used_terms = [c['concept_en'] for c in recent_concepts]

        # Prepare terms for prompt
        terms_text = "\n".join([
            f"[{t['id']}] {t['term_en']} ({t.get('term_tr', '')}) - {t.get('category', 'genel')}"
            for t in unused[:30]  # Limit to 30 for prompt
        ])

        used_text = ", ".join(used_terms[:20]) if used_terms else "Yok"

        # Prepare selection prompt
        prompt = self.selection_prompt.replace('{terms}', terms_text)
        prompt = prompt.replace('{used_terms}', used_text)

        # Add recent news context if available
        if recent_news:
            news_text = "\n".join([f"- {n.get('title', '')}" for n in recent_news[:5]])
            prompt += f"\n\nGÜNCEL HABERLER:\n{news_text}"

        # Call Claude for selection
        response = self.call_claude_cli(prompt)

        # Parse response
        concept = self._parse_selection_response(response, unused)

        if not concept:
            # Fallback: select random unused term
            import random
            term = random.choice(unused)
            concept = {
                'glossary_id': term['id'],
                'concept_en': term['term_en'],
                'concept_tr': term.get('term_tr', ''),
                'beirek_area': '4',  # Default to Project Development & Finance
                'beirek_subarea': '1',
                'selection_reason': 'Rastgele seçim'
            }

        # Save to database
        concept_id = add_daily_concept(
            glossary_id=concept['glossary_id'],
            concept_en=concept['concept_en'],
            concept_tr=concept['concept_tr'],
            beirek_area=concept['beirek_area'],
            beirek_subarea=concept.get('beirek_subarea', ''),
            selection_reason=concept.get('selection_reason', '')
        )

        # Mark term as used
        mark_term_used(concept['glossary_id'])

        concept['id'] = concept_id
        return concept

    def _parse_selection_response(self, response: str, terms: List[Dict]) -> Optional[Dict]:
        """Parse Claude's selection response."""
        # Try to extract JSON
        json_match = re.search(r'\{[\s\S]*\}', response)

        if json_match:
            try:
                parsed = json.loads(json_match.group())

                # Find the term
                selected_id = parsed.get('selected_id')
                term = next((t for t in terms if t['id'] == selected_id), None)

                if term:
                    return {
                        'glossary_id': term['id'],
                        'concept_en': parsed.get('term_en', term['term_en']),
                        'concept_tr': parsed.get('term_tr', term.get('term_tr', '')),
                        'beirek_area': str(parsed.get('beirek_area', '4')),
                        'beirek_subarea': str(parsed.get('beirek_subarea', '1')),
                        'selection_reason': parsed.get('selection_reason', '')
                    }
            except json.JSONDecodeError:
                pass

        return None

    def generate_concept_content(self, concept: Dict) -> Dict:
        """
        Generate content for selected concept.

        Args:
            concept: Selected concept dict

        Returns:
            Dict with generated content
        """
        # Map BEIREK area number to name
        beirek_areas = self.config['beirek_areas']
        area_num = concept.get('beirek_area', '4')
        area_info = beirek_areas.get(area_num, beirek_areas.get('4'))
        area_name = area_info['name'] if isinstance(area_info, dict) else area_info

        # Prepare prompt
        prompt = self.content_prompt.replace('{concept_en}', concept['concept_en'])
        prompt = prompt.replace('{concept_tr}', concept.get('concept_tr', ''))
        prompt = prompt.replace('{beirek_area}', area_name)
        prompt = prompt.replace('{selection_reason}', concept.get('selection_reason', ''))

        # Generate content
        response = self.call_claude_cli(prompt)

        # Parse response into formats
        content = self._parse_content_response(response)
        content['metadata'] = {
            'concept_en': concept['concept_en'],
            'concept_tr': concept.get('concept_tr', ''),
            'beirek_area': concept['beirek_area'],
            'beirek_subarea': concept.get('beirek_subarea', ''),
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

        # Try to split by markers
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
            # Fallback: try to identify sections by headers
            sections = re.split(r'\n#{1,3}\s+', response)
            for section in sections:
                lower = section.lower()
                if 'makale' in lower[:50] or 'article' in lower[:50]:
                    content['article'] = section.strip()
                elif 'linkedin' in lower[:50]:
                    content['linkedin'] = section.strip()
                elif 'twitter' in lower[:50] or 'tweet' in lower[:50]:
                    content['twitter'] = section.strip()

            # If still empty, use whole response as article
            if not content['article'] and not content['linkedin']:
                content['article'] = response

        return content

    def save_concept_content(self, concept: Dict, content: Dict) -> str:
        """
        Save concept content to files.

        Args:
            concept: Concept dict
            content: Generated content dict

        Returns:
            Content folder path
        """
        # Create folder name
        today = date.today().isoformat()
        slug = generate_slug(concept['concept_en'])
        folder_name = f"{today}_kavram_{slug}"

        # Folder path
        folder_path = self.concepts_output_path / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        # Frontmatter data
        frontmatter_data = {
            'title': f"{concept['concept_en']} ({concept.get('concept_tr', '')})",
            'date': today,
            'type': 'daily-concept',
            'beirek_area': concept.get('beirek_area', ''),
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

                # Save to database
                save_generated_content(
                    content_type=format_key,
                    title=concept['concept_en'],
                    content=content[format_key],
                    file_path=str(file_path),
                    concept_id=concept.get('id')
                )

        # Update concept with content path
        if concept.get('id'):
            update_concept_content_path(concept['id'], str(folder_path))

        return str(folder_path)

    def run_daily_concept_flow(self, recent_news: List[Dict] = None) -> Dict:
        """
        Run complete daily concept flow.

        Args:
            recent_news: Recent news for context (optional)

        Returns:
            Result dict with concept and content info
        """
        result = {
            'concept': None,
            'content_generated': False,
            'content_path': None,
            'word_counts': {}
        }

        # Select concept
        print("Selecting daily concept...")
        concept = self.select_daily_concept(recent_news)
        result['concept'] = concept
        print(f"Selected: {concept['concept_en']} ({concept.get('concept_tr', '')})")

        # Generate content
        print("Generating content...")
        content = self.generate_concept_content(concept)

        # Calculate word counts
        result['word_counts'] = {
            'article': len(content.get('article', '').split()),
            'linkedin': len(content.get('linkedin', '').split()),
            'twitter': len(content.get('twitter', '').split())
        }

        # Save content
        print("Saving content...")
        content_path = self.save_concept_content(concept, content)
        result['content_path'] = content_path
        result['content_generated'] = True

        print(f"Content saved to: {content_path}")

        return result


if __name__ == "__main__":
    print("Testing ConceptManager...")

    manager = ConceptManager()

    # Check glossary status
    stats = manager.get_glossary_status()
    print(f"\nGlossary stats: {stats}")

    # If no terms, try to import
    if stats['total'] == 0:
        print("\nNo terms in glossary. Attempting import...")
        try:
            count = manager.import_glossary()
            print(f"Imported {count} terms")
        except Exception as e:
            print(f"Import failed: {e}")

    print("\nConceptManager ready!")
