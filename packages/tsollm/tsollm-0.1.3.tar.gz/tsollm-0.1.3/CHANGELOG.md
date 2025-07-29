# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure and development setup

## [0.1.1] - 2024-01-XX

### Fixed
- Fixed MyPy configuration to target Python 3.9+ instead of 3.8
- Fixed Black configuration to target Python 3.9+ for consistency
- Resolved Pydantic compatibility issues in CI/CD pipeline

### Changed
- Updated development tool configurations for Python 3.9+ support

## [0.1.0] - 2024-01-XX

### Added
- Initial release of TSO-LLM package
- Note classification schema with categories, priorities, and tags
- Bookmark classification schema with usefulness scoring
- Core TSO class for text extraction using OpenAI Structured Outputs
- Convenience functions for direct note and bookmark extraction
- Comprehensive test suite with mocked OpenAI responses
- GitHub Actions workflows for CI/CD
- Pre-commit hooks for code quality
- Documentation and usage examples
- MIT license and contributing guidelines

### Features
- Support for Python 3.9+
- OpenAI GPT-4o integration with structured outputs
- Pydantic validation for type safety
- Error handling for API failures and invalid responses
- Schema introspection capabilities
- Additional context support for better extraction accuracy

[Unreleased]: https://github.com/yourusername/tsollm/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/yourusername/tsollm/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/yourusername/tsollm/releases/tag/v0.1.0 