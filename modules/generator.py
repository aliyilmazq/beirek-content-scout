"""
BEIREK Content Scout - Generator Module
=======================================

Content generation using Claude CLI.

Generates 3 formats:
- Research Article (1500-2500 words)
- LinkedIn Post (150-300 words)
- Twitter Thread (5-10 tweets)

Includes anti-hallucination validation.
"""

import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from .storage import (
    save_generated_content, get_content_folder_path,
    save_content_to_file, add_frontmatter, generate_slug
)
from .logger import get_logger
from .config_manager import config, Constants

# Module logger
logger = get_logger(__name__)


class GeneratorError(Exception):
    """Base exception for generator errors."""
    pass


class ContentValidationError(GeneratorError):
    """Content validation failed."""
    pass


class ContentGenerator:
    """
    Content generator using Claude CLI.

    Generates content in 3 formats with anti-hallucination validation.
    """

    def __init__(self, config_path: str = None):
        """
        Initialize generator.

        Args:
            config_path: Path to config.yaml (optional, uses singleton config if not provided)
        """
        self.base_path = config.base_path

        # Use singleton config
        self.content_config = config.content
        self.timeout = config.get('claude.timeout_seconds', 180)

        # Load prompts
        self.prompts = {
            'article': self._load_prompt('article_prompt.txt'),
            'linkedin': self._load_prompt('linkedin_prompt.txt'),
            'twitter': self._load_prompt('twitter_prompt.txt'),
            'concept_selection': self._load_prompt('concept_selection_prompt.txt'),
            'concept_content': self._load_prompt('concept_content_prompt.txt')
        }

        logger.info("Generator initialized")

    def _load_prompt(self, filename: str) -> str:
        """Load prompt from file or return default."""
        prompt_path = self.base_path / "prompts" / filename

        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return self._get_default_prompt(filename)

    def _get_default_prompt(self, prompt_type: str) -> str:
        """Get default prompt based on type."""
        defaults = {
            'article_prompt.txt': self._get_article_prompt(),
            'linkedin_prompt.txt': self._get_linkedin_prompt(),
            'twitter_prompt.txt': self._get_twitter_prompt(),
            'concept_selection_prompt.txt': '',
            'concept_content_prompt.txt': ''
        }
        return defaults.get(prompt_type, '')

    def _get_article_prompt(self) -> str:
        """Default article generation prompt."""
        return """Sen BEIREK'in kıdemli içerik stratejistisin. Verilen kaynaktan profesyonel bir araştırma makalesi üret.

HEDEF KİTLE:
- C-level yöneticiler
- Proje finansçıları
- Hukuk danışmanları
- Teknik direktörler

KURALLAR:
⛔ YASAK: Kaynakta olmayan rakam, tarih, şirket adı UYDURMAK
✅ ZORUNLU: Tüm veriler kaynak içerikten alınmalı
✅ ZORUNLU: BEIREK perspektifi ve özgün yorum ekle
✅ ZORUNLU: Türkçe yaz

FORMAT:
1. Başlık (dikkat çekici, SEO-friendly)
2. Giriş (hook + context)
3. Ana Bölümler (3-4 bölüm, alt başlıklı)
4. BEIREK Perspektifi (bu konu neden önemli)
5. Sonuç ve Çıkarımlar

UZUNLUK: 1500-2500 kelime

KAYNAK İÇERİK:
{source_content}

KONU:
{topic}
"""

    def _get_linkedin_prompt(self) -> str:
        """Default LinkedIn prompt."""
        return """Sen BEIREK'in LinkedIn thought leadership yazarısın.

HEDEF KİTLE:
- Board/C-Level yöneticiler (CEO, CFO, COO)
- Yönetim Kurulu üyeleri
- Üst düzey karar vericiler

⚠️ VERİLER: Kaynak metindeki rakamları kullan, UYDURMAK YASAK
✅ BAKIŞ AÇISI: BEIREK bu konuya nasıl bakıyor?
🎯 ÇÖZÜM: Biz bu problemi nasıl çözüyoruz?

TON VE YAKLAŞIM:
- Samimi ve şeffaf (kurumsal soğukluk YOK)
- Çözüm odaklı (eleştiri veya şikayet YOK)
- Kavga çıkarmadan, yapıcı
- Karşılıklı diyalog havası

YAPI (4 BÖLÜM):
1. HOOK: Dikkat çekici açılış + gerçek rakam/veri
2. PROBLEM: Sektörün yaşadığı zorluk (kısa ve net)
3. BEIREK YAKLAŞIMI: "Biz bu konuya farklı bakıyoruz..."
4. CTA: "Biz böyle çözüyoruz. Sizin projelerinizde bu nasıl yönetiliyor?"

KURALLAR:
- 150-300 kelime arası
- Kısa paragraflar (2-3 cümle max)
- 4-5 alakalı hashtag ekle
- Hard sell YAPMA

KAYNAK İÇERİK:
{source_content}

KONU:
{topic}
"""

    def _get_twitter_prompt(self) -> str:
        """Default Twitter prompt."""
        return """Sen BEIREK'in Twitter thought leadership yazarısın.

HEDEF KİTLE:
- Enerji sektörü profesyonelleri
- Yatırımcılar ve analistler
- Proje geliştiriciler

KURALLAR:
⛔ YASAK: Kaynak dışı bilgi
✅ Her tweet 280 karakter altında
✅ Her tweet bağımsız değer sunmalı
✅ Thread numaralandırması (1/X formatı)

FORMAT:
1/X: Hook tweet (dikkat çekici açılış)
2/X: Veri/rakam tweet
3/X-6/X: Ana içerik (insights)
7/X: BEIREK perspektifi
X/X: CTA + hashtags

UZUNLUK: 5-10 tweet

KAYNAK İÇERİK:
{source_content}

KONU:
{topic}
"""

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
                raise GeneratorError(f"Claude CLI error: {stderr}")

            return stdout.strip()

        except subprocess.TimeoutExpired:
            if process:
                process.kill()
                process.wait()  # Ensure process is reaped
            logger.error(f"Claude CLI timeout after {self.timeout}s during content generation")
            raise GeneratorError(
                f"Claude CLI timeout ({self.timeout}s asildi). "
                "Icerik uretimi cok uzun suruyor. Daha kisa prompt deneyin."
            )
        except FileNotFoundError:
            raise GeneratorError(
                "Claude CLI bulunamadi! Lutfen kurun: https://claude.ai/cli"
            )
        except GeneratorError:
            raise
        except Exception as e:
            if process and process.poll() is None:
                process.kill()
                process.wait()
            logger.error(f"Claude CLI error in generator: {e}")
            raise GeneratorError(f"Claude CLI hatasi: {e}")

    def generate_article(self, source_content: str, topic: str) -> str:
        """
        Generate research article.

        Args:
            source_content: Source news content
            topic: Article topic

        Returns:
            Generated article in Markdown
        """
        prompt = self.prompts['article'].replace('{source_content}', source_content)
        prompt = prompt.replace('{topic}', topic)

        content = self.call_claude_cli(prompt)

        # Validate
        word_count = len(content.split())
        if word_count < self.content_config['article_min_words']:
            # Try to regenerate
            prompt += "\n\nÖNEMLİ: Minimum 1500 kelime olmalı. Daha detaylı yaz."
            content = self.call_claude_cli(prompt)

        return content

    def generate_linkedin(self, source_content: str, topic: str) -> str:
        """
        Generate LinkedIn post.

        Args:
            source_content: Source content
            topic: Topic

        Returns:
            Generated LinkedIn post
        """
        prompt = self.prompts['linkedin'].replace('{source_content}', source_content)
        prompt = prompt.replace('{topic}', topic)

        content = self.call_claude_cli(prompt)

        # Validate word count
        word_count = len(content.split())
        if word_count > self.content_config['linkedin_max_words']:
            # Ask for shorter version
            prompt = f"Aşağıdaki LinkedIn postunu 300 kelimeye kısalt, öz tut:\n\n{content}"
            content = self.call_claude_cli(prompt)

        return content

    def generate_twitter(self, source_content: str, topic: str) -> str:
        """
        Generate Twitter thread.

        Args:
            source_content: Source content
            topic: Topic

        Returns:
            Generated Twitter thread
        """
        prompt = self.prompts['twitter'].replace('{source_content}', source_content)
        prompt = prompt.replace('{topic}', topic)

        content = self.call_claude_cli(prompt)

        # Validate tweet format
        content = self._format_twitter_thread(content)

        return content

    def _format_twitter_thread(self, content: str) -> str:
        """Format and validate Twitter thread."""
        lines = content.strip().split('\n')
        formatted_tweets = []
        current_tweet = []

        for line in lines:
            line = line.strip()
            if not line:
                if current_tweet:
                    formatted_tweets.append(' '.join(current_tweet))
                    current_tweet = []
            elif re.match(r'^\d+[/\.]', line) or re.match(r'^Tweet \d+', line, re.IGNORECASE):
                if current_tweet:
                    formatted_tweets.append(' '.join(current_tweet))
                current_tweet = [re.sub(r'^(\d+)[/\.]\d*\s*:?\s*', r'\1/ ', line)]
            else:
                current_tweet.append(line)

        if current_tweet:
            formatted_tweets.append(' '.join(current_tweet))

        # Renumber tweets
        result = []
        total = len(formatted_tweets)
        for i, tweet in enumerate(formatted_tweets, 1):
            # Remove existing numbering
            tweet = re.sub(r'^\d+[/\.]\s*\d*\s*', '', tweet)
            tweet = f"{i}/{total} {tweet}"

            # Truncate if too long
            if len(tweet) > Constants.TWITTER_MAX_CHARS:
                tweet = tweet[:Constants.TWITTER_TRUNCATE_LENGTH] + Constants.TWITTER_TRUNCATE_SUFFIX

            result.append(tweet)

        return '\n\n'.join(result)

    def generate_all_formats(self, source_content: str, topic: str,
                            beirek_area: str = None,
                            beirek_subarea: str = None) -> Dict:
        """
        Generate content in all 3 formats.

        Args:
            source_content: Source news content
            topic: Content topic
            beirek_area: BEIREK area for filing
            beirek_subarea: BEIREK sub-area

        Returns:
            Dict with all content and metadata
        """
        result = {
            'article': '',
            'linkedin': '',
            'twitter': '',
            'metadata': {
                'topic': topic,
                'beirek_area': beirek_area,
                'beirek_subarea': beirek_subarea,
                'generated_at': datetime.now().isoformat(),
                'word_counts': {}
            }
        }

        # Generate article
        logger.info("Generating article...")
        result['article'] = self.generate_article(source_content, topic)
        result['metadata']['word_counts']['article'] = len(result['article'].split())

        # Generate LinkedIn
        logger.info("Generating LinkedIn post...")
        result['linkedin'] = self.generate_linkedin(source_content, topic)
        result['metadata']['word_counts']['linkedin'] = len(result['linkedin'].split())

        # Generate Twitter
        logger.info("Generating Twitter thread...")
        result['twitter'] = self.generate_twitter(source_content, topic)
        result['metadata']['word_counts']['twitter'] = len(result['twitter'].split())

        return result

    def save_content(self, content: Dict, beirek_area: str,
                    beirek_subarea: str = None, content_type: str = 'haber',
                    slug: str = None, article_id: int = None,
                    concept_id: int = None, request_id: int = None) -> str:
        """
        Save generated content to files.

        Args:
            content: Generated content dict
            beirek_area: BEIREK area
            beirek_subarea: BEIREK sub-area
            content_type: 'haber' or 'kavram'
            slug: Content slug
            article_id: Related article ID
            concept_id: Related concept ID
            request_id: Related request ID

        Returns:
            Content folder path
        """
        # Generate slug if not provided
        if not slug:
            slug = generate_slug(content['metadata']['topic'])

        # Get folder path
        folder_path = get_content_folder_path(
            beirek_area=beirek_area,
            beirek_subarea=beirek_subarea,
            content_type=content_type,
            slug=slug
        )

        # Create folder
        Path(folder_path).mkdir(parents=True, exist_ok=True)

        # Prepare metadata for frontmatter
        frontmatter_data = {
            'title': content['metadata']['topic'],
            'date': datetime.now().strftime('%Y-%m-%d'),
            'beirek_area': beirek_area,
            'beirek_subarea': beirek_subarea or '',
            'generated_by': 'BEIREK Content Scout'
        }

        # Save each format
        file_mappings = {
            'article': 'makale.md',
            'linkedin': 'linkedin.md',
            'twitter': 'twitter.md'
        }

        for format_key, filename in file_mappings.items():
            if content.get(format_key):
                # Add frontmatter
                content_with_frontmatter = add_frontmatter(
                    content[format_key],
                    {**frontmatter_data, 'format': format_key}
                )

                # Save file
                file_path = str(Path(folder_path) / filename)
                save_content_to_file(content_with_frontmatter, file_path)

                # Save to database
                save_generated_content(
                    content_type=format_key,
                    title=content['metadata']['topic'],
                    content=content[format_key],
                    file_path=file_path,
                    article_id=article_id,
                    concept_id=concept_id,
                    request_id=request_id
                )

        return folder_path

    def generate_from_proposal(self, proposal: Dict, source_content: str) -> Dict:
        """
        Generate content from a proposal.

        Uses the proposal's suggested_title, content_angle, and key_talking_points
        to guide content generation with a more focused prompt.

        Args:
            proposal: Proposal dict with suggested_title, content_angle, key_talking_points
            source_content: Source article content

        Returns:
            Dict with all content and metadata
        """
        import json

        # Parse key talking points
        key_points = proposal.get('key_talking_points', '[]')
        if isinstance(key_points, str):
            try:
                key_points = json.loads(key_points)
            except (json.JSONDecodeError, TypeError, ValueError):
                key_points = []

        # Build enhanced topic with proposal guidance
        topic = proposal.get('suggested_title', '')
        angle = proposal.get('content_angle', '')
        description = proposal.get('brief_description', '')

        # Create enhanced topic with angle and talking points
        enhanced_topic = topic
        if angle:
            enhanced_topic += f"\n\nBAKIS ACISI: {angle}"
        if key_points:
            enhanced_topic += "\n\nANA KONUSMA NOKTALARI:\n" + "\n".join([f"- {p}" for p in key_points])
        if description:
            enhanced_topic += f"\n\nKISA ACIKLAMA: {description}"

        # Use generate_all_formats with enhanced topic
        result = self.generate_all_formats(
            source_content=source_content,
            topic=enhanced_topic,
            beirek_area=proposal.get('beirek_area'),
            beirek_subarea=proposal.get('beirek_subarea')
        )

        # Add proposal-specific metadata
        result['metadata']['content_angle'] = angle
        result['metadata']['original_title'] = topic

        return result

    def save_proposal_content(self, content: Dict, proposal: Dict) -> str:
        """
        Save generated content to proposal's folder.

        Args:
            content: Generated content dict
            proposal: Proposal dict with folder_path

        Returns:
            Folder path
        """
        folder_path = proposal.get('folder_path')
        if not folder_path:
            raise ValueError("Proposal has no folder_path")

        folder = Path(folder_path)
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)

        # Prepare frontmatter
        frontmatter_data = {
            'title': proposal.get('suggested_title', ''),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'beirek_area': proposal.get('beirek_area', ''),
            'beirek_subarea': proposal.get('beirek_subarea', ''),
            'content_angle': proposal.get('content_angle', ''),
            'generated_by': 'BEIREK Content Scout'
        }

        # Save each format
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

                file_path = folder / filename
                save_content_to_file(content_with_frontmatter, str(file_path))

                # Save to database
                save_generated_content(
                    content_type=format_key,
                    title=proposal.get('suggested_title', ''),
                    content=content[format_key],
                    file_path=str(file_path)
                )

        return folder_path

    def validate_content(self, generated_content: str, source_content: str,
                        content_type: str) -> Tuple[bool, List[str]]:
        """
        Validate generated content against source.

        Checks for potential hallucinations.

        Args:
            generated_content: Generated content
            source_content: Original source content
            content_type: Content type (article/linkedin/twitter)

        Returns:
            Tuple of (is_valid, list of warnings)
        """
        warnings = []

        # Extract numbers from generated content
        gen_numbers = set(re.findall(r'\$?\d+(?:,\d{3})*(?:\.\d+)?(?:\s*(?:MW|GW|million|billion|B|M|%|yıl|year))?', generated_content, re.IGNORECASE))
        source_numbers = set(re.findall(r'\$?\d+(?:,\d{3})*(?:\.\d+)?(?:\s*(?:MW|GW|million|billion|B|M|%|yıl|year))?', source_content, re.IGNORECASE))

        # Check for numbers not in source
        suspicious_numbers = gen_numbers - source_numbers
        if suspicious_numbers:
            warnings.append(f"Kaynakta olmayan rakamlar: {', '.join(list(suspicious_numbers)[:5])}")

        # Check word count
        word_count = len(generated_content.split())

        if content_type == 'article':
            if word_count < 1000:
                warnings.append(f"Makale çok kısa: {word_count} kelime (min 1500)")
        elif content_type == 'linkedin':
            if word_count > 350:
                warnings.append(f"LinkedIn çok uzun: {word_count} kelime (max 300)")
        elif content_type == 'twitter':
            tweets = generated_content.split('\n\n')
            for i, tweet in enumerate(tweets):
                if len(tweet) > 280:
                    warnings.append(f"Tweet {i+1} çok uzun: {len(tweet)} karakter")

        is_valid = len([w for w in warnings if 'olmayan' in w]) == 0

        return is_valid, warnings


class HallucinationChecker:
    """
    Check generated content for hallucinations.
    """

    def __init__(self):
        pass

    def extract_facts(self, content: str) -> List[Dict]:
        """Extract factual claims from content."""
        facts = []

        # Extract numbers with context
        for match in re.finditer(r'(\w+\s+){0,5}(\$?\d+(?:,\d{3})*(?:\.\d+)?(?:\s*(?:MW|GW|million|billion|B|M|%))?)\s*(\w+\s+){0,5}', content):
            facts.append({
                'type': 'number',
                'value': match.group(2),
                'context': match.group(0).strip()
            })

        # Extract company names (capitalized words)
        for match in re.finditer(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b', content):
            facts.append({
                'type': 'name',
                'value': match.group(1),
                'context': match.group(0)
            })

        # Extract years
        for match in re.finditer(r'\b(20\d{2})\b', content):
            facts.append({
                'type': 'year',
                'value': match.group(1),
                'context': match.group(0)
            })

        return facts

    def verify_facts(self, facts: List[Dict], source_content: str) -> List[Dict]:
        """Verify facts against source content."""
        results = []

        for fact in facts:
            verified = fact['value'].lower() in source_content.lower()
            results.append({
                'fact': fact,
                'verified': verified,
                'warning': None if verified else f"'{fact['value']}' kaynakta bulunamadı"
            })

        return results

    def check_content(self, generated_content: str, source_content: str) -> Dict:
        """Full hallucination check."""
        facts = self.extract_facts(generated_content)
        verified = self.verify_facts(facts, source_content)

        verified_count = sum(1 for v in verified if v['verified'])
        total = len(verified)

        return {
            'passed': verified_count == total or total == 0,
            'facts_checked': total,
            'facts_verified': verified_count,
            'warnings': [v['warning'] for v in verified if v['warning']],
            'confidence': verified_count / total if total > 0 else 1.0
        }


if __name__ == "__main__":
    print("Testing ContentGenerator...")

    generator = ContentGenerator()

    # Test with sample content
    sample_source = """
    Texas-based solar developer SunPower Corp announced today that its 500MW
    utility-scale solar project in West Texas has reached financial close.
    The $450 million project financing was led by a consortium of international
    financial institutions including the IFC and OPIC. The project is expected
    to achieve commercial operation in Q3 2027 and will power approximately
    100,000 homes. This marks one of the largest solar projects in Texas history.
    """

    sample_topic = "Texas 500MW Solar Project Financial Close"

    print("\nTesting article generation...")
    try:
        article = generator.generate_article(sample_source, sample_topic)
        print(f"Article generated: {len(article.split())} words")
        print(f"First 200 chars: {article[:200]}...")
    except Exception as e:
        print(f"Article generation failed: {e}")

    print("\nGenerator module ready!")
