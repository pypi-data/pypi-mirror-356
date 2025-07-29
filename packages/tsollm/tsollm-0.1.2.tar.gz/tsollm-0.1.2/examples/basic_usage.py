"""Basic usage examples for TSO-LLM."""

import os
from tsollm import TSO, extract_note_info, extract_bookmark_info

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, skip

# Make sure to set your OpenAI API key
# os.environ['OPENAI_API_KEY'] = 'your-api-key-here'


def main():
    # Initialize TSO
    tso = TSO()

    # Example 1: Extract note information
    note_text = """
    Meeting with the development team tomorrow at 2 PM.
    Need to discuss the new API endpoints and database migration.
    Don't forget to bring the architecture diagrams.
    This is high priority as the deadline is next week.
    """

    print("Extracting note information...")
    note_result = tso.extract(note_text, "note")
    print(f"Note classification: {note_result}")
    print()

    # Example 2: Extract bookmark information
    bookmark_text = """
    https://docs.python.org/3/tutorial/
    The official Python tutorial covering all the basics of Python programming.
    Great resource for beginners learning Python.
    """

    print("Extracting bookmark information...")
    bookmark_result = tso.extract(bookmark_text, "bookmark")
    print(f"Bookmark classification: {bookmark_result}")
    print()

    # Example 3: Using convenience functions
    simple_note = "Buy milk and eggs from the store today"
    simple_result = extract_note_info(simple_note)
    print(f"Simple note extraction: {simple_result}")
    print()

    # Example 4: Extract bookmark using convenience function
    simple_url = (
        "https://github.com/openai/openai-python - Official OpenAI Python library"
    )
    bookmark_simple = extract_bookmark_info(simple_url)
    print(f"Simple bookmark extraction: {bookmark_simple}")
    print()

    # Example 5: Extract note with additional context
    context_note = "Team standup at 9 AM"
    context_result = tso.extract(
        context_note,
        "note",
        additional_context="Daily recurring meeting with the engineering team",
    )
    print(f"Note with context: {context_result}")
    print()

    # Example 6: Display available schemas
    print("Available schemas:")
    schemas = tso.get_supported_schemas()
    for schema_name in schemas.keys():
        schema_info = tso.get_schema_info(schema_name)
        print(f"- {schema_name}: {schema_info['description']}")
    print()

    # Example 7: More complex note with multiple priorities and tags
    complex_note = """
    Project deadline is approaching fast - need to finish the user authentication system by Friday.
    Still need to implement OAuth integration, password reset functionality, and email verification.
    Meeting with the client on Thursday to review progress.
    This is critical for the product launch next month.
    Remember to update the documentation and run security tests.
    """

    print("Extracting complex note information...")
    complex_result = tso.extract(complex_note, "note")
    print(f"Complex note classification: {complex_result}")
    print()

    # Example 8: Technical documentation bookmark
    tech_bookmark = """
    https://fastapi.tiangolo.com/tutorial/
    FastAPI Tutorial - User Guide
    Comprehensive tutorial for building APIs with FastAPI, covering everything from basic concepts to advanced features like dependency injection, authentication, and testing.
    """

    print("Extracting technical bookmark...")
    tech_result = tso.extract(tech_bookmark, "bookmark")
    print(f"Technical bookmark classification: {tech_result}")


if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key before running this example:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print()
        print("For demonstration purposes, the code structure is shown above.")
        print("Uncomment the line below to run the actual examples:")
        print("# main()")
    else:
        main()
