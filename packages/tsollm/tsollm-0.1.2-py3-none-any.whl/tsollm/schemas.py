"""Structured output schemas for text extraction."""

from typing import List, Literal, Union

from pydantic import BaseModel, ConfigDict, Field


class NoteClassification(BaseModel):
    """Schema for classifying notes."""

    model_config = ConfigDict(
        extra="forbid",  # additionalProperties: false
        str_strip_whitespace=True,  # Clean input
        validate_default=True,  # Validate default values
    )

    title: str = Field(description="The main title or subject of the note")
    category: Literal[
        "personal", "work", "study", "idea", "todo", "meeting", "other"
    ] = Field(description="The category that best describes this note")
    priority: Literal["low", "medium", "high", "urgent"] = Field(
        description="The priority level of this note"
    )
    tags: List[str] = Field(
        description="Relevant tags for this note (max 5 tags)", max_length=5
    )
    summary: str = Field(
        description="A brief summary of the note content (max 200 characters)",
        max_length=200,
    )
    actionable: bool = Field(description="Whether this note contains actionable items")
    due_date: Union[str, None] = Field(
        default=None, description="Due date if applicable (ISO format: YYYY-MM-DD)"
    )


class BookmarkClassification(BaseModel):
    """Schema for classifying and cataloging URLs as bookmarks."""

    model_config = ConfigDict(
        extra="forbid",  # additionalProperties: false
        str_strip_whitespace=True,
        validate_default=True,
    )

    title: str = Field(description="The title of the webpage or a descriptive title")
    description: str = Field(
        description="A brief description of the content (max 300 characters)",
        max_length=300,
    )
    category: Literal[
        "news",
        "blog",
        "documentation",
        "tutorial",
        "tool",
        "resource",
        "social",
        "entertainment",
        "shopping",
        "reference",
        "other",
    ] = Field(description="The category that best describes this bookmark")
    tags: List[str] = Field(
        description="Relevant tags for this bookmark (max 8 tags)", max_length=8
    )
    domain: str = Field(description="The domain name of the URL")
    language: str = Field(
        description="The primary language of the content (ISO 639-1 code)",
        pattern="^[a-z]{2}$",
    )
    content_type: Literal[
        "article", "video", "podcast", "image", "document", "tool", "homepage", "other"
    ] = Field(description="The type of content")
    estimated_read_time: Union[int, None] = Field(
        default=None, description="Estimated reading time in minutes (if applicable)"
    )
    usefulness_score: int = Field(
        description="Usefulness score from 1-10 based on content quality and relevance",
        ge=1,
        le=10,
    )
    is_free: bool = Field(description="Whether the content is freely accessible")
