# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2024-01-XX

### Changed
- Added Banyan CLI

### Fixed
- Production deployment configuration

## [1.0.0] - 2024-01-XX

### Added
- Initial release of Banyan SDK (Prompt Stack Manager Python SDK)
- Support for prompt fetching from Banyan platform
- Real-world prompt usage logging with background processing
- A/B testing and experiment management with sticky routing
- Asynchronous/background-safe logging with retry logic
- Local queue for offline resilience
- API key authentication and project-level binding
- Prompt caching for performance optimization
- Comprehensive error handling and logging
- Production-ready configuration options
- Statistics and monitoring capabilities
- Graceful shutdown with log flushing

### Features
- **Prompt Management**: Fetch prompts by name, version, and branch
- **Experiment Routing**: Automatic A/B test routing with sticky context
- **Background Logging**: Non-blocking prompt usage logging
- **Retry Logic**: Exponential backoff for failed requests
- **Caching**: Local prompt caching for improved performance
- **Project Support**: Multi-project organization support
- **Statistics**: Real-time logging and performance metrics
- **Production Ready**: Configurable timeouts, retries, and queue sizes

### Technical Details
- Python 3.7+ support
- Modern packaging with pyproject.toml
- Comprehensive documentation and examples
- Type hints throughout the codebase
- Extensive error handling and logging
- Thread-safe background processing

## [Unreleased]

### Planned Features
- CLI tools for prompt management
- Webhook support for real-time updates
- Advanced caching strategies
- Bulk operations support
- Enhanced analytics and reporting 