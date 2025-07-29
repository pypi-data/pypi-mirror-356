"""TSO-LLM - Template Structured Output for Large Language Models."""

__version__ = "0.1.2"
__author__ = "Saverio Mazza"
__email__ = "saverio3107@gmail.com"

from .core import (
    TSO,
    extract_bookmark_info,
    extract_note_info,
)
from .exceptions import (
    ConfigurationError,
    ExtractionError,
    SchemaValidationError,
    TSOError,
)
from .schemas import (
    BookmarkClassification,
    NoteClassification,
)

__all__ = [
    "BookmarkClassification",
    "ConfigurationError",
    "ExtractionError",
    "NoteClassification",
    "SchemaValidationError",
    "TSO",
    "TSOError",
    "extract_bookmark_info",
    "extract_note_info",
]
