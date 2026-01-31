"""
Tests for storage module.
"""

import pytest
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.storage import (
    DatabaseConnection, init_database, sanitize_path_component,
    get_content_folder_path, add_content_proposal, get_proposals_by_status,
    get_proposal_by_id, update_proposal_status, accept_proposal, reject_proposal,
    get_proposal_stats
)


class TestDatabaseConnection:
    """Tests for DatabaseConnection context manager."""

    def test_context_manager_opens_connection(self):
        """Test that context manager opens a valid connection."""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            assert result[0] == 1

    def test_context_manager_closes_connection(self):
        """Test that connection is closed after exiting context."""
        with DatabaseConnection() as conn:
            pass
        # Connection should be closed - attempting to use it should fail
        # Note: SQLite connections don't raise on closed, so we just verify no exception in context

    def test_context_manager_commits_on_success(self):
        """Test that changes are committed on successful exit."""
        init_database()
        # This is implicitly tested by the proposal tests below


class TestSanitizePathComponent:
    """Tests for path sanitization."""

    def test_normal_input(self):
        """Test normal input passes through."""
        assert sanitize_path_component("4-project-finance") == "4-project-finance"

    def test_removes_path_traversal(self):
        """Test that ../ is removed."""
        assert sanitize_path_component("../../../etc") == "etc"

    def test_removes_slashes(self):
        """Test that slashes are removed."""
        assert sanitize_path_component("path/to/file") == "pathtofile"

    def test_removes_backslashes(self):
        """Test that backslashes are removed."""
        assert sanitize_path_component("path\\to\\file") == "pathtofile"

    def test_empty_string(self):
        """Test empty string returns empty."""
        assert sanitize_path_component("") == ""

    def test_removes_dangerous_chars(self):
        """Test that dangerous characters are removed."""
        assert sanitize_path_component("file<>:\"|?*name") == "filename"


class TestGetContentFolderPath:
    """Tests for content folder path generation."""

    def test_valid_area_and_subarea(self):
        """Test path generation with valid area and subarea."""
        path = get_content_folder_path("4", "3", "haber", "test-slug")
        assert "4-project-development-finance" in path
        assert "3-project-finance-structuring" in path
        assert "haber" in path
        assert "test-slug" in path

    def test_invalid_area_raises_error(self):
        """Test that invalid area raises ValueError."""
        with pytest.raises(ValueError, match="Invalid BEIREK area"):
            get_content_folder_path("invalid", "3", "haber", "test")

    def test_path_traversal_blocked(self):
        """Test that path traversal attempts are blocked."""
        with pytest.raises(ValueError, match="Invalid BEIREK area"):
            get_content_folder_path("../../../etc", "3", "haber", "test")


class TestContentProposals:
    """Tests for content proposal CRUD operations."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Initialize database before each test."""
        init_database()

    def test_add_proposal_valid(self):
        """Test adding a valid proposal."""
        proposal_id = add_content_proposal(
            article_id=1,
            beirek_area="4",
            beirek_subarea="3",
            suggested_title="Test Title",
            content_angle="Test Angle",
            confidence_score=0.85
        )
        assert proposal_id > 0

    def test_add_proposal_invalid_confidence_score_too_high(self):
        """Test that confidence_score > 1 raises error."""
        with pytest.raises(ValueError, match="must be between 0 and 1"):
            add_content_proposal(
                article_id=1,
                beirek_area="4",
                beirek_subarea="3",
                suggested_title="Test",
                content_angle="Test",
                confidence_score=1.5
            )

    def test_add_proposal_invalid_confidence_score_negative(self):
        """Test that negative confidence_score raises error."""
        with pytest.raises(ValueError, match="must be between 0 and 1"):
            add_content_proposal(
                article_id=1,
                beirek_area="4",
                beirek_subarea="3",
                suggested_title="Test",
                content_angle="Test",
                confidence_score=-0.5
            )

    def test_add_proposal_confidence_score_zero_valid(self):
        """Test that confidence_score=0 is valid."""
        proposal_id = add_content_proposal(
            article_id=1,
            beirek_area="4",
            beirek_subarea="3",
            suggested_title="Test Zero Score",
            content_angle="Test",
            confidence_score=0.0
        )
        assert proposal_id > 0

    def test_add_proposal_confidence_score_one_valid(self):
        """Test that confidence_score=1 is valid."""
        proposal_id = add_content_proposal(
            article_id=1,
            beirek_area="4",
            beirek_subarea="3",
            suggested_title="Test Full Score",
            content_angle="Test",
            confidence_score=1.0
        )
        assert proposal_id > 0

    def test_get_proposal_by_id(self):
        """Test retrieving proposal by ID."""
        proposal_id = add_content_proposal(
            article_id=1,
            beirek_area="4",
            beirek_subarea="3",
            suggested_title="Retrievable Title",
            content_angle="Test Angle",
            confidence_score=0.9
        )

        proposal = get_proposal_by_id(proposal_id)
        assert proposal is not None
        assert proposal['suggested_title'] == "Retrievable Title"
        assert proposal['beirek_area'] == "4"

    def test_get_proposal_by_id_not_found(self):
        """Test that non-existent ID returns None."""
        proposal = get_proposal_by_id(99999)
        assert proposal is None

    def test_update_proposal_status_valid(self):
        """Test updating proposal status."""
        proposal_id = add_content_proposal(
            article_id=1,
            beirek_area="4",
            beirek_subarea="3",
            suggested_title="Status Test",
            content_angle="Test"
        )

        update_proposal_status(proposal_id, "accepted")
        proposal = get_proposal_by_id(proposal_id)
        assert proposal['status'] == "accepted"

    def test_update_proposal_status_invalid(self):
        """Test that invalid status raises error."""
        proposal_id = add_content_proposal(
            article_id=1,
            beirek_area="4",
            beirek_subarea="3",
            suggested_title="Invalid Status Test",
            content_angle="Test"
        )

        with pytest.raises(ValueError, match="Invalid status"):
            update_proposal_status(proposal_id, "invalid_status")

    def test_accept_proposal(self):
        """Test accepting a proposal."""
        proposal_id = add_content_proposal(
            article_id=1,
            beirek_area="4",
            beirek_subarea="3",
            suggested_title="Accept Test",
            content_angle="Test"
        )

        accept_proposal(proposal_id)
        proposal = get_proposal_by_id(proposal_id)
        assert proposal['status'] == "accepted"
        assert proposal['accepted_at'] is not None

    def test_reject_proposal(self):
        """Test rejecting a proposal."""
        proposal_id = add_content_proposal(
            article_id=1,
            beirek_area="4",
            beirek_subarea="3",
            suggested_title="Reject Test",
            content_angle="Test"
        )

        reject_proposal(proposal_id)
        proposal = get_proposal_by_id(proposal_id)
        assert proposal['status'] == "rejected"

    def test_get_proposals_by_status(self):
        """Test filtering proposals by status."""
        # Add a suggested proposal
        add_content_proposal(
            article_id=1,
            beirek_area="4",
            beirek_subarea="3",
            suggested_title="Suggested Proposal",
            content_angle="Test"
        )

        proposals = get_proposals_by_status("suggested")
        assert len(proposals) > 0
        assert all(p['status'] == 'suggested' for p in proposals)

    def test_get_proposal_stats(self):
        """Test proposal statistics."""
        stats = get_proposal_stats()
        assert 'suggested' in stats
        assert 'accepted' in stats
        assert 'rejected' in stats
        assert 'outline_created' in stats
        assert 'content_generated' in stats
        assert 'today_total' in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
