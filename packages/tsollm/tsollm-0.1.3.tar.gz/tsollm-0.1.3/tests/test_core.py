"""Tests for core functionality."""

import json
from unittest.mock import Mock, patch

import pytest

from tsollm.core import TSO, extract_note_info
from tsollm.exceptions import ConfigurationError, ExtractionError


class TestTSO:
    """Test cases for TSO class."""

    def setup_method(self):
        """Set up test fixtures."""
        with patch("tsollm.core.OpenAI"):
            self.tso = TSO(api_key="test-key")

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        with patch("tsollm.core.OpenAI") as mock_openai:
            tso = TSO(api_key="test-key")
            mock_openai.assert_called_once_with(api_key="test-key")
            assert tso.model == "gpt-4o-2024-08-06"
            assert tso.temperature == 0.1

    def test_init_configuration_error(self):
        """Test initialization failure."""
        with patch("tsollm.core.OpenAI", side_effect=Exception("API Error")):
            with pytest.raises(ConfigurationError):
                TSO(api_key="invalid-key")

    def test_unsupported_schema_type(self):
        """Test extraction with unsupported schema type."""
        with pytest.raises(ValueError):
            self.tso.extract("test text", "unsupported_type")

    @patch("tsollm.core.OpenAI")
    def test_successful_note_extraction(self, mock_openai_class):
        """Test successful note extraction."""
        # Mock response - FIX: configuriamo correttamente la struttura
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = json.dumps(
            {
                "title": "Test Note",
                "category": "personal",
                "priority": "medium",
                "tags": ["test"],
                "summary": "A test note",
                "actionable": False,
                "due_date": None,
            }
        )
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]  # Fix: lista invece di Mock

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        tso = TSO(api_key="test-key")
        result = tso.extract("This is a test note", "note")

        assert result["title"] == "Test Note"
        assert result["category"] == "personal"
        assert result["priority"] == "medium"

    @patch("tsollm.core.OpenAI")
    def test_successful_bookmark_extraction(self, mock_openai_class):
        """Test successful bookmark extraction."""
        # Mock response - FIXED structure
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = json.dumps(
            {
                "title": "Test Site",
                "description": "A test website",
                "category": "documentation",
                "tags": ["test", "docs"],
                "domain": "example.com",
                "language": "en",
                "content_type": "article",
                "estimated_read_time": 5,
                "usefulness_score": 8,
                "is_free": True,
            }
        )
        mock_choice.message = mock_message

        mock_response = Mock()
        mock_response.choices = [mock_choice]  # FIX: List instead of Mock

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        tso = TSO(api_key="test-key")
        result = tso.extract("https://example.com", "bookmark")

        assert result["title"] == "Test Site"
        assert result["domain"] == "example.com"
        assert result["usefulness_score"] == 8

    @patch("tsollm.core.OpenAI")
    def test_extraction_with_additional_context(self, mock_openai_class):
        """Test extraction with additional context."""
        # FIXED: Proper mock structure
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = json.dumps(
            {
                "title": "Context Note",
                "category": "work",
                "priority": "high",
                "tags": ["context"],
                "summary": "A note with context",
                "actionable": True,
                "due_date": None,
            }
        )
        mock_choice.message = mock_message

        mock_response = Mock()
        mock_response.choices = [mock_choice]  # FIX: List not Mock

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        tso = TSO(api_key="test-key")
        result = tso.extract("Meeting tomorrow", "note", "Project planning meeting")

        # Verify context is in prompt
        call_args = mock_client.chat.completions.create.call_args
        system_message = call_args[1]["messages"][0]["content"]
        assert "Project planning meeting" in system_message
        assert result["title"] == "Context Note"

    @patch("tsollm.core.OpenAI")
    def test_empty_response_error(self, mock_openai_class):
        """Test handling of empty OpenAI response."""
        # FIXED: Proper mock structure
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = None  # Empty response
        mock_choice.message = mock_message

        mock_response = Mock()
        mock_response.choices = [mock_choice]  # FIX: List not Mock

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        tso = TSO(api_key="test-key")

        with pytest.raises(ExtractionError, match="Empty response from OpenAI"):
            tso.extract("test", "note")

    @patch("tsollm.core.OpenAI")
    def test_json_decode_error(self, mock_openai_class):
        """Test handling of invalid JSON response."""
        # FIXED: Proper mock structure
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "invalid json"  # Invalid JSON
        mock_choice.message = mock_message

        mock_response = Mock()
        mock_response.choices = [mock_choice]  # FIX: List not Mock

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        tso = TSO(api_key="test-key")

        with pytest.raises(ExtractionError, match="Failed to parse JSON response"):
            tso.extract("test", "note")

    @patch("tsollm.core.OpenAI")
    def test_openai_api_error(self, mock_openai_class):
        """Test handling of OpenAI API errors."""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai_class.return_value = mock_client

        tso = TSO(api_key="test-key")

        with pytest.raises(ExtractionError, match="Extraction failed"):
            tso.extract("test", "note")

    def test_get_supported_schemas(self):
        """Test getting supported schemas."""
        schemas = self.tso.get_supported_schemas()
        assert "note" in schemas
        assert "bookmark" in schemas
        assert len(schemas) == 2

    def test_get_schema_info_note(self):
        """Test getting schema information for note."""
        info = self.tso.get_schema_info("note")
        assert info["name"] == "note"
        assert info["class"] == "NoteClassification"
        assert "schema" in info
        assert "fields" in info
        assert "title" in info["fields"]
        assert "category" in info["fields"]

    def test_get_schema_info_bookmark(self):
        """Test getting schema information for bookmark."""
        info = self.tso.get_schema_info("bookmark")
        assert info["name"] == "bookmark"
        assert info["class"] == "BookmarkClassification"
        assert "schema" in info
        assert "fields" in info
        assert "domain" in info["fields"]
        assert "usefulness_score" in info["fields"]

    def test_get_schema_info_invalid(self):
        """Test getting schema info for invalid schema type."""
        with pytest.raises(ValueError, match="Unsupported schema type"):
            self.tso.get_schema_info("invalid")

    def test_system_prompt_generation_note(self):
        """Test system prompt generation for notes."""
        prompt = self.tso._get_system_prompt("note", None)
        assert "analyzing and classifying notes" in prompt
        assert "category, priority, actionable items" in prompt

    def test_system_prompt_generation_bookmark(self):
        """Test system prompt generation for bookmarks."""
        prompt = self.tso._get_system_prompt("bookmark", None)
        assert "analyzing web content and URLs" in prompt
        assert "bookmark entry" in prompt

    def test_system_prompt_with_context(self):
        """Test system prompt generation with additional context."""
        context = "This is important context"
        prompt = self.tso._get_system_prompt("note", context)
        assert context in prompt
        assert "Additional context:" in prompt


def test_extract_note_info_convenience_function():
    """Test the convenience function for note extraction."""
    with patch("tsollm.core.TSO") as mock_tso_class:
        mock_tso = Mock()
        mock_tso.extract.return_value = {"title": "Test"}
        mock_tso_class.return_value = mock_tso

        result = extract_note_info("test note", api_key="test-key")

        mock_tso_class.assert_called_once_with(api_key="test-key")
        mock_tso.extract.assert_called_once_with("test note", "note")
        assert result == {"title": "Test"}


def test_extract_bookmark_info_convenience_function():
    """Test the convenience function for bookmark extraction."""
    with patch("tsollm.core.TSO") as mock_tso_class:
        mock_tso = Mock()
        mock_tso.extract.return_value = {"title": "Test Bookmark"}
        mock_tso_class.return_value = mock_tso

        from tsollm.core import extract_bookmark_info

        result = extract_bookmark_info("https://example.com", api_key="test-key")

        mock_tso_class.assert_called_once_with(api_key="test-key")
        mock_tso.extract.assert_called_once_with("https://example.com", "bookmark")
        assert result == {"title": "Test Bookmark"}
