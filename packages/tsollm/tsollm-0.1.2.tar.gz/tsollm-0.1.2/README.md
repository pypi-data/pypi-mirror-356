# TSO-LLM

**Template Structured Output for Large Language Models**

[![PyPI version](https://badge.fury.io/py/tsollm.svg)](https://badge.fury.io/py/tsollm)
[![Tests](https://github.com/yourusername/tsollm/workflows/Tests/badge.svg)](https://github.com/yourusername/tsollm/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Get structured data from text using predefined schemas and OpenAI's Structured Outputs. No schema design needed!

## ✨ Features

- 🎯 **Ready-to-use templates** for notes and bookmarks
- ⚡ **OpenAI Structured Outputs** integration
- 🛡️ **Type safety** with Pydantic validation
- 📚 **Simple API** with convenience functions

## 🚀 Quick Start

```bash
pip install tsollm
```

```python
import os
from tsollm import TSO

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = 'your-api-key-here'

# Initialize and extract
tso = TSO()

# Extract note information
note = "Remember to buy groceries tomorrow - milk, bread, eggs. This is urgent!"
result = tso.extract(note, "note")
print(result)
# {
#   "title": "Grocery Shopping",
#   "category": "personal", 
#   "priority": "urgent",
#   "tags": ["shopping", "groceries"],
#   "summary": "Buy milk, bread, and eggs tomorrow",
#   "actionable": True
# }

# Extract bookmark information  
bookmark = "https://github.com/openai/openai-python - Official OpenAI Python library"
result = tso.extract(bookmark, "bookmark")
print(result)
# {
#   "title": "OpenAI Python Library",
#   "category": "tool",
#   "tags": ["python", "openai", "api"],
#   "usefulness_score": 9,
#   "is_free": True
# }