"""
Tests for framer module.
"""

import pytest
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.framer import ContentFramer, FramerError, MAX_ARTICLE_CONTENT_LENGTH


class TestContentFramerInit:
    """Tests for ContentFramer initialization."""

    def test_framer_initializes(self):
        """Test that framer initializes without error."""
        framer = ContentFramer()
        assert framer is not None
        assert framer.framing_prompt is not None

    def test_framer_loads_config(self):
        """Test that framer loads BEIREK areas from config."""
        framer = ContentFramer()
        assert framer.beirek_areas is not None
        assert "4" in framer.beirek_areas


class TestGetAreaFullName:
    """Tests for area name resolution."""

    def test_area_4_subarea_3(self):
        """Test resolving area 4.3."""
        framer = ContentFramer()
        area, subarea = framer.get_area_full_name("4", "3")
        assert area == "4-project-development-finance"
        assert subarea == "3-project-finance-structuring"

    def test_area_1_subarea_1(self):
        """Test resolving area 1.1."""
        framer = ContentFramer()
        area, subarea = framer.get_area_full_name("1", "1")
        assert area == "1-deal-contract-advisory"
        assert subarea == "1-deal-architecture-term-sheet-design"

    def test_area_only(self):
        """Test resolving area without subarea."""
        framer = ContentFramer()
        area, subarea = framer.get_area_full_name("5", None)
        assert area == "5-engineering-delivery"
        assert subarea == ""

    def test_invalid_area(self):
        """Test that invalid area returns as-is."""
        framer = ContentFramer()
        area, subarea = framer.get_area_full_name("99", "1")
        assert "99" in area


class TestConstants:
    """Tests for module constants."""

    def test_max_content_length_defined(self):
        """Test that MAX_ARTICLE_CONTENT_LENGTH is defined."""
        assert MAX_ARTICLE_CONTENT_LENGTH == 3000


class TestFrameArticle:
    """Tests for article framing (requires Claude CLI)."""

    @pytest.fixture
    def framer(self):
        return ContentFramer()

    @pytest.fixture
    def sample_article(self):
        return {
            'id': 1,
            'title': 'Texas Solar Project Reaches Financial Close',
            'summary': 'A 500MW solar project in Texas reached financial close with $450M financing.',
            'source_name': 'Utility Dive'
        }

    def test_frame_article_returns_dict_or_none(self, framer, sample_article):
        """Test that frame_article returns dict or None."""
        # This test may fail if Claude CLI is not available
        try:
            result = framer.frame_article(sample_article)
            assert result is None or isinstance(result, dict)
            if result:
                assert 'beirek_area' in result
                assert 'suggested_title' in result
                assert 'content_angle' in result
        except FramerError:
            pytest.skip("Claude CLI not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
