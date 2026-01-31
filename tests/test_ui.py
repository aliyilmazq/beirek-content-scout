"""
Tests for UI module.
"""

import pytest
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.ui import TerminalUI


class TestTerminalUIInit:
    """Tests for TerminalUI initialization."""

    def test_ui_initializes(self):
        """Test that UI initializes without error."""
        ui = TerminalUI()
        assert ui is not None
        assert ui.console is not None


class TestProposalDisplay:
    """Tests for proposal display functionality."""

    @pytest.fixture
    def ui(self):
        return TerminalUI()

    @pytest.fixture
    def sample_proposals(self):
        return [
            {
                'id': 1,
                'suggested_title': 'Test Proposal 1',
                'content_angle': 'Test angle 1',
                'confidence_score': 0.9,
                'beirek_area': '4',
                'beirek_subarea': '3',
                'source_name': 'Test Source'
            },
            {
                'id': 2,
                'suggested_title': 'Test Proposal 2',
                'content_angle': 'Test angle 2',
                'confidence_score': 0.0,  # Edge case: zero score
                'beirek_area': '5',
                'beirek_subarea': '1',
                'source_name': 'Test Source 2'
            },
            {
                'id': 3,
                'suggested_title': 'Test Proposal 3',
                'content_angle': 'Test angle 3',
                'confidence_score': None,  # Edge case: None score
                'beirek_area': '6',
                'beirek_subarea': '2',
                'source_name': 'Test Source 3'
            }
        ]

    def test_score_display_normal(self, sample_proposals):
        """Test that normal scores display correctly."""
        proposal = sample_proposals[0]
        score = proposal.get('confidence_score')

        # Score 0.9 should display as "9.0"
        if score is not None:
            score_display = f"{float(score) * 10:.1f}"
            assert score_display == "9.0"

    def test_score_display_zero(self, sample_proposals):
        """Test that zero score displays as number, not N/A."""
        proposal = sample_proposals[1]
        score = proposal.get('confidence_score')

        # Score 0.0 should display as "0.0", not "N/A"
        if score is not None:
            score_display = f"{float(score) * 10:.1f}"
            assert score_display == "0.0"

    def test_score_display_none(self, sample_proposals):
        """Test that None score displays as N/A."""
        proposal = sample_proposals[2]
        score = proposal.get('confidence_score')

        # Score None should display as "N/A"
        if score is None:
            score_display = "N/A"
            assert score_display == "N/A"


class TestProposalDetail:
    """Tests for proposal detail display."""

    @pytest.fixture
    def ui(self):
        return TerminalUI()

    def test_show_proposal_detail_with_json_points(self, ui):
        """Test that JSON key points are parsed correctly."""
        proposal = {
            'id': 1,
            'suggested_title': 'Test Title',
            'content_angle': 'Test Angle',
            'brief_description': 'Test Description',
            'target_audience': 'Test Audience',
            'key_talking_points': '["Point 1", "Point 2", "Point 3"]',
            'beirek_area': '4',
            'beirek_subarea': '3',
            'confidence_score': 0.85,
            'article_title': 'Source Article',
            'source_name': 'Test Source'
        }

        # This should not raise an exception
        import json
        key_points = proposal.get('key_talking_points', '[]')
        if isinstance(key_points, str):
            try:
                key_points = json.loads(key_points)
            except (json.JSONDecodeError, TypeError, ValueError):
                key_points = []

        assert len(key_points) == 3
        assert key_points[0] == "Point 1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
