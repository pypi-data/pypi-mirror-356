"""Tests for schema validation."""

import pytest
from pydantic import ValidationError

from tsollm.schemas import BookmarkClassification, NoteClassification


class TestNoteClassification:
    """Test cases for NoteClassification schema."""

    def test_valid_note_creation(self):
        """Test creating a valid note classification."""
        note_data = {
            "title": "Test Note",
            "category": "work",
            "priority": "high",
            "tags": ["urgent", "meeting"],
            "summary": "This is a test note summary",
            "actionable": True,
            "due_date": "2024-12-31",
        }

        note = NoteClassification(**note_data)
        assert note.title == "Test Note"
        assert note.category == "work"
        assert note.priority == "high"
        assert note.tags == ["urgent", "meeting"]
        assert note.actionable is True
        assert note.due_date == "2024-12-31"

    def test_note_without_due_date(self):
        """Test creating note without due date (optional field)."""
        note_data = {
            "title": "Simple Note",
            "category": "personal",
            "priority": "low",
            "tags": ["simple"],
            "summary": "A simple note",
            "actionable": False,
        }

        note = NoteClassification(**note_data)
        assert note.due_date is None

    def test_invalid_category(self):
        """Test validation error for invalid category."""
        note_data = {
            "title": "Test Note",
            "category": "invalid_category",  # Invalid
            "priority": "high",
            "tags": ["test"],
            "summary": "Test summary",
            "actionable": True,
        }

        with pytest.raises(ValidationError) as exc_info:
            NoteClassification(**note_data)

        assert "category" in str(exc_info.value)

    def test_invalid_priority(self):
        """Test validation error for invalid priority."""
        note_data = {
            "title": "Test Note",
            "category": "work",
            "priority": "invalid_priority",  # Invalid
            "tags": ["test"],
            "summary": "Test summary",
            "actionable": True,
        }

        with pytest.raises(ValidationError) as exc_info:
            NoteClassification(**note_data)

        assert "priority" in str(exc_info.value)

    def test_too_many_tags(self):
        """Test validation error for too many tags."""
        note_data = {
            "title": "Test Note",
            "category": "work",
            "priority": "medium",
            "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"],  # Too many
            "summary": "Test summary",
            "actionable": False,
        }

        with pytest.raises(ValidationError) as exc_info:
            NoteClassification(**note_data)

        assert "tags" in str(exc_info.value)

    def test_summary_too_long(self):
        """Test validation error for summary too long."""
        long_summary = "x" * 201  # Exceeds 200 character limit
        note_data = {
            "title": "Test Note",
            "category": "work",
            "priority": "medium",
            "tags": ["test"],
            "summary": long_summary,
            "actionable": False,
        }

        with pytest.raises(ValidationError) as exc_info:
            NoteClassification(**note_data)

        assert "summary" in str(exc_info.value)

    def test_missing_required_fields(self):
        """Test validation error for missing required fields."""
        incomplete_data = {
            "title": "Test Note",
            # Missing other required fields
        }

        with pytest.raises(ValidationError) as exc_info:
            NoteClassification(**incomplete_data)

        error_str = str(exc_info.value).lower()
        assert "category" in error_str
        assert "priority" in error_str
        assert "tags" in error_str


class TestBookmarkClassification:
    """Test cases for BookmarkClassification schema."""

    def test_valid_bookmark_creation(self):
        """Test creating a valid bookmark classification."""
        bookmark_data = {
            "title": "Python Documentation",
            "description": "Official Python language documentation",
            "category": "documentation",
            "tags": ["python", "programming", "docs"],
            "domain": "docs.python.org",
            "language": "en",
            "content_type": "document",
            "estimated_read_time": 30,
            "usefulness_score": 9,
            "is_free": True,
        }

        bookmark = BookmarkClassification(**bookmark_data)
        assert bookmark.title == "Python Documentation"
        assert bookmark.domain == "docs.python.org"
        assert bookmark.usefulness_score == 9
        assert bookmark.is_free is True

    def test_bookmark_without_read_time(self):
        """Test creating bookmark without estimated read time (optional field)."""
        bookmark_data = {
            "title": "GitHub Homepage",
            "description": "GitHub main website",
            "category": "tool",
            "tags": ["git", "github"],
            "domain": "github.com",
            "language": "en",
            "content_type": "homepage",
            "usefulness_score": 8,
            "is_free": True,
        }

        bookmark = BookmarkClassification(**bookmark_data)
        assert bookmark.estimated_read_time is None

    def test_invalid_category(self):
        """Test validation error for invalid category."""
        bookmark_data = {
            "title": "Test Site",
            "description": "A test website",
            "category": "invalid_category",  # Invalid
            "tags": ["test"],
            "domain": "example.com",
            "language": "en",
            "content_type": "article",
            "usefulness_score": 5,
            "is_free": True,
        }

        with pytest.raises(ValidationError) as exc_info:
            BookmarkClassification(**bookmark_data)

        assert "category" in str(exc_info.value)

    def test_invalid_language_code(self):
        """Test validation error for invalid language code."""
        bookmark_data = {
            "title": "Test Site",
            "description": "A test website",
            "category": "blog",
            "tags": ["test"],
            "domain": "example.com",
            "language": "invalid",  # Should be 2-letter ISO code
            "content_type": "article",
            "usefulness_score": 5,
            "is_free": True,
        }

        with pytest.raises(ValidationError) as exc_info:
            BookmarkClassification(**bookmark_data)

        assert "language" in str(exc_info.value)

    def test_usefulness_score_out_of_range(self):
        """Test validation error for usefulness score out of range."""
        # Test score too low
        bookmark_data = {
            "title": "Test Site",
            "description": "A test website",
            "category": "blog",
            "tags": ["test"],
            "domain": "example.com",
            "language": "en",
            "content_type": "article",
            "usefulness_score": 0,  # Below minimum of 1
            "is_free": True,
        }

        with pytest.raises(ValidationError) as exc_info:
            BookmarkClassification(**bookmark_data)

        assert "usefulness_score" in str(exc_info.value)

        # Test score too high
        bookmark_data["usefulness_score"] = 11  # Above maximum of 10

        with pytest.raises(ValidationError) as exc_info:
            BookmarkClassification(**bookmark_data)

        assert "usefulness_score" in str(exc_info.value)

    def test_valid_usefulness_score_range(self):
        """Test valid usefulness scores at boundaries."""
        base_data = {
            "title": "Test Site",
            "description": "A test website",
            "category": "blog",
            "tags": ["test"],
            "domain": "example.com",
            "language": "en",
            "content_type": "article",
            "is_free": True,
        }

        # Test minimum score
        bookmark_data = base_data.copy()
        bookmark_data["usefulness_score"] = 1
        bookmark = BookmarkClassification(**bookmark_data)
        assert bookmark.usefulness_score == 1

        # Test maximum score
        bookmark_data["usefulness_score"] = 10
        bookmark = BookmarkClassification(**bookmark_data)
        assert bookmark.usefulness_score == 10

    def test_too_many_tags(self):
        """Test validation error for too many tags."""
        bookmark_data = {
            "title": "Test Site",
            "description": "A test website",
            "category": "blog",
            "tags": [
                "tag1",
                "tag2",
                "tag3",
                "tag4",
                "tag5",
                "tag6",
                "tag7",
                "tag8",
                "tag9",
            ],  # Too many
            "domain": "example.com",
            "language": "en",
            "content_type": "article",
            "usefulness_score": 5,
            "is_free": True,
        }

        with pytest.raises(ValidationError) as exc_info:
            BookmarkClassification(**bookmark_data)

        assert "tags" in str(exc_info.value)

    def test_description_too_long(self):
        """Test validation error for description too long."""
        long_description = "x" * 301  # Exceeds 300 character limit
        bookmark_data = {
            "title": "Test Site",
            "description": long_description,
            "category": "blog",
            "tags": ["test"],
            "domain": "example.com",
            "language": "en",
            "content_type": "article",
            "usefulness_score": 5,
            "is_free": True,
        }

        with pytest.raises(ValidationError) as exc_info:
            BookmarkClassification(**bookmark_data)

        assert "description" in str(exc_info.value)

    def test_invalid_content_type(self):
        """Test validation error for invalid content type."""
        bookmark_data = {
            "title": "Test Site",
            "description": "A test website",
            "category": "blog",
            "tags": ["test"],
            "domain": "example.com",
            "language": "en",
            "content_type": "invalid_type",  # Invalid
            "usefulness_score": 5,
            "is_free": True,
        }

        with pytest.raises(ValidationError) as exc_info:
            BookmarkClassification(**bookmark_data)

        assert "content_type" in str(exc_info.value)

    def test_schema_serialization(self):
        """Test that schemas can be serialized to dict and JSON."""
        bookmark_data = {
            "title": "Test Site",
            "description": "A test website",
            "category": "blog",
            "tags": ["test"],
            "domain": "example.com",
            "language": "en",
            "content_type": "article",
            "usefulness_score": 5,
            "is_free": True,
        }

        bookmark = BookmarkClassification(**bookmark_data)

        # Test dict serialization
        as_dict = bookmark.model_dump()
        assert isinstance(as_dict, dict)
        assert as_dict["title"] == "Test Site"

        # Test JSON schema generation
        schema = bookmark.model_json_schema()
        assert isinstance(schema, dict)
        assert "properties" in schema
        assert "title" in schema["properties"]
