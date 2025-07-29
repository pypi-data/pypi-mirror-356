"""Core functionality for TSO-LLM - Template Structured Output LLM."""

import json
from typing import Any, Dict, Optional, Type

from openai import OpenAI
from pydantic import BaseModel

from .exceptions import ConfigurationError, ExtractionError
from .schemas import BookmarkClassification, NoteClassification


class TSO:
    """Main class for Template Structured Output using OpenAI LLMs."""

    SUPPORTED_SCHEMAS: Dict[str, Type[BaseModel]] = {
        "note": NoteClassification,
        "bookmark": BookmarkClassification,
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-2024-08-06",
        temperature: float = 0.1,
    ):
        """
        Initialize TSO (Template Structured Output).

        Args:
            api_key: OpenAI API key. If None, will use OPENAI_API_KEY env var
            model: The OpenAI model to use
            temperature: Temperature for generation (lower = more deterministic)
        """
        try:
            self.client = OpenAI(api_key=api_key)
            self.model = model
            self.temperature = temperature
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize OpenAI client: {e}")

    def _prepare_schema_for_openai(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare schema for OpenAI Structured Outputs v2 compatibility."""

        def process_schema(obj: Any) -> None:
            if isinstance(obj, dict):
                # Ensure all objects have additionalProperties: false
                if obj.get("type") == "object":
                    obj["additionalProperties"] = False

                    # Ensure all properties are in required array for OpenAI
                    if "properties" in obj:
                        obj["required"] = list(obj["properties"].keys())

                # Process nested objects recursively
                for key, value in obj.items():
                    if isinstance(value, (dict, list)):
                        process_schema(value)
            elif isinstance(obj, list):
                for item in obj:
                    process_schema(item)

        # Deep copy and process
        prepared_schema: Dict[str, Any] = json.loads(json.dumps(schema))
        process_schema(prepared_schema)
        return prepared_schema

    def extract(
        self, text: str, schema_type: str, additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract structured information from text using OpenAI Structured Outputs v2.

        Args:
            text: The input text to process
            schema_type: Type of schema to use ('note' or 'bookmark')
            additional_context: Additional context to help with extraction

        Returns:
            Dictionary containing the extracted structured data

        Raises:
            ExtractionError: If extraction fails
            ValueError: If schema_type is not supported
        """
        if schema_type not in self.SUPPORTED_SCHEMAS:
            raise ValueError(
                f"Unsupported schema type: {schema_type}. "
                f"Supported types: {list(self.SUPPORTED_SCHEMAS.keys())}"
            )

        schema_class = self.SUPPORTED_SCHEMAS[schema_type]
        system_prompt = self._get_system_prompt(schema_type, additional_context)

        # Get and prepare schema for OpenAI
        raw_schema = schema_class.model_json_schema()
        prepared_schema = self._prepare_schema_for_openai(raw_schema)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": f"{schema_type}_extraction",
                        "strict": True,  # Enable strict mode for v2
                        "schema": prepared_schema,
                    },
                },
                temperature=self.temperature,
            )

            # Parse and validate response
            content = response.choices[0].message.content
            if not content:
                raise ExtractionError("Empty response from OpenAI")

            # Parse JSON and validate with Pydantic
            parsed_data: Dict[str, Any] = json.loads(content)
            validated_data = schema_class(**parsed_data)

            return validated_data.model_dump()

        except json.JSONDecodeError as e:
            raise ExtractionError(f"Failed to parse JSON response: {e}")
        except Exception as e:
            raise ExtractionError(f"Extraction failed: {e}")

    def _get_system_prompt(
        self, schema_type: str, additional_context: Optional[str]
    ) -> str:
        """Generate system prompt based on schema type."""
        base_prompts = {
            "note": (
                "You are an expert at analyzing and classifying notes. "
                "Extract structured information from the given note text, "
                "identifying the category, priority, actionable items, "
                "and other relevant details. "
                "Be accurate and concise in your analysis."
            ),
            "bookmark": (
                "You are an expert at analyzing web content and URLs. "
                "Extract structured information to create a "
                "well-organized bookmark entry. "
                "Analyze the content for its type, usefulness, "
                "category, and other relevant metadata. "
                "If the input contains a URL, consider both the URL "
                "and any provided content description."
            ),
        }

        prompt = base_prompts.get(
            schema_type, "Extract structured information from the text."
        )

        if additional_context:
            prompt += f"\n\nAdditional context: {additional_context}"

        return prompt

    def get_supported_schemas(self) -> Dict[str, Type[BaseModel]]:
        """Get all supported schema types and their classes."""
        return self.SUPPORTED_SCHEMAS.copy()

    def get_schema_info(self, schema_type: str) -> Dict[str, Any]:
        """Get detailed information about a specific schema."""
        if schema_type not in self.SUPPORTED_SCHEMAS:
            raise ValueError(f"Unsupported schema type: {schema_type}")

        schema_class = self.SUPPORTED_SCHEMAS[schema_type]
        return {
            "name": schema_type,
            "class": schema_class.__name__,
            "description": schema_class.__doc__,
            "schema": schema_class.model_json_schema(),
            "fields": {
                name: {
                    "type": str(field.annotation),
                    "description": field.description,
                    "required": field.is_required(),
                }
                for name, field in schema_class.model_fields.items()
            },
        }


# Convenience functions for direct usage
def extract_note_info(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Extract structured information from a note."""
    tso = TSO(api_key=api_key)
    return tso.extract(text, "note")


def extract_bookmark_info(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Extract structured information for bookmarking a URL."""
    tso = TSO(api_key=api_key)
    return tso.extract(text, "bookmark")
