"""
Tests for generator module.
"""

import pytest
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.generator import (
    ContentGenerator, GeneratorError,
    TWITTER_MAX_CHARS, TWITTER_TRUNCATE_SUFFIX, TWITTER_TRUNCATE_LENGTH
)


class TestConstants:
    """Tests for module constants."""

    def test_twitter_max_chars(self):
        """Test Twitter max chars constant."""
        assert TWITTER_MAX_CHARS == 280

    def test_twitter_truncate_suffix(self):
        """Test Twitter truncate suffix."""
        assert TWITTER_TRUNCATE_SUFFIX == "..."

    def test_twitter_truncate_length(self):
        """Test Twitter truncate length is calculated correctly."""
        assert TWITTER_TRUNCATE_LENGTH == 277


class TestContentGeneratorInit:
    """Tests for ContentGenerator initialization."""

    def test_generator_initializes(self):
        """Test that generator initializes without error."""
        generator = ContentGenerator()
        assert generator is not None

    def test_generator_loads_prompts(self):
        """Test that generator loads prompts."""
        generator = ContentGenerator()
        assert 'article' in generator.prompts
        assert 'linkedin' in generator.prompts
        assert 'twitter' in generator.prompts


class TestFormatTwitterThread:
    """Tests for Twitter thread formatting."""

    @pytest.fixture
    def generator(self):
        return ContentGenerator()

    def test_formats_numbered_tweets(self, generator):
        """Test that tweets are properly numbered."""
        raw_content = """1/ First tweet here
2/ Second tweet here
3/ Third tweet here"""

        formatted = generator._format_twitter_thread(raw_content)
        lines = [l for l in formatted.split('\n\n') if l.strip()]

        assert len(lines) == 3
        assert lines[0].startswith("1/3")
        assert lines[1].startswith("2/3")
        assert lines[2].startswith("3/3")

    def test_truncates_long_tweets(self, generator):
        """Test that long tweets are truncated."""
        long_tweet = "1/ " + "A" * 300  # Definitely over 280

        formatted = generator._format_twitter_thread(long_tweet)

        # Should be truncated to 280 or less
        first_tweet = formatted.split('\n\n')[0]
        assert len(first_tweet) <= TWITTER_MAX_CHARS


class TestGenerateFromProposal:
    """Tests for proposal-based generation."""

    @pytest.fixture
    def generator(self):
        return ContentGenerator()

    @pytest.fixture
    def sample_proposal(self):
        return {
            'suggested_title': 'Test Solar Project Analysis',
            'content_angle': 'Project finance perspective',
            'brief_description': 'Analysis of financing structure',
            'key_talking_points': '["Point 1", "Point 2"]',
            'beirek_area': '4',
            'beirek_subarea': '3',
            'target_audience': 'C-level executives'
        }

    def test_generate_from_proposal_structure(self, generator, sample_proposal):
        """Test that generate_from_proposal calls generate_all_formats."""
        # This is a structural test - actual generation requires Claude CLI
        # We're verifying the method exists and has correct signature
        assert hasattr(generator, 'generate_from_proposal')
        assert callable(generator.generate_from_proposal)


class TestValidateContent:
    """Tests for content validation."""

    @pytest.fixture
    def generator(self):
        return ContentGenerator()

    def test_validate_finds_suspicious_numbers(self, generator):
        """Test that validation flags numbers not in source."""
        source = "The project cost $100 million."
        generated = "The project cost $500 million."  # Different number

        is_valid, warnings = generator.validate_content(generated, source, 'article')

        assert len(warnings) > 0

    def test_validate_accepts_matching_content(self, generator):
        """Test that validation accepts content with matching numbers."""
        source = "The 500MW project cost $450 million."
        generated = "This 500MW solar installation required $450 million in financing."

        is_valid, warnings = generator.validate_content(generated, source, 'article')

        # Should have no warnings about mismatched numbers
        number_warnings = [w for w in warnings if 'olmayan' in w]
        assert len(number_warnings) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
