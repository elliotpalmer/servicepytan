# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **CLI Module**: Complete command-line interface with commands for:
  - `init`: Initialize configuration files
  - `test-connection`: Test API connectivity
  - `get`: Retrieve data from any endpoint
  - `jobs`: Get jobs data with date filtering
  - `list-endpoints`: Show available API endpoints
- **Authentication Token Caching**: Intelligent token caching with automatic expiration handling
- **Enhanced Rate Limiting**: Comprehensive retry logic with exponential backoff for transient errors
- **Comprehensive Test Suite**: Unit tests for authentication, requests, and core functionality
- **Code Quality Tools**: 
  - Black code formatting
  - MyPy type checking
  - Pre-commit hooks
  - Enhanced flake8 configuration
- **Modern CI/CD**: GitHub Actions workflow with security scanning
- **Configuration Management**: 
  - pyproject.toml for modern Python tooling
  - Pre-commit configuration
  - Enhanced tox configuration

### Changed
- **Python Support**: Updated from 3.6-3.8 to 3.8-3.12
- **Dependencies**: Updated all dependencies to latest secure versions:
  - Click 7.x → 8.x
  - requests → 2.31.0+ (security)
  - All dev dependencies to latest versions
- **Development Status**: Upgraded from Pre-Alpha to Alpha
- **Rate Limiting**: All API requests now use retry logic by default
- **Error Handling**: Improved error messages and credential validation
- **Security**: Removed credentials from log messages

### Fixed
- **Missing CLI Module**: Fixed broken entry point in setup.py
- **Authentication Inefficiency**: Eliminated unnecessary token requests
- **Security Vulnerabilities**: Updated dependencies and removed credential exposure
- **Inconsistent Rate Limiting**: Applied retry logic to all API endpoints

### Security
- **Credential Protection**: Credentials no longer logged in error messages
- **Input Validation**: Added comprehensive credential validation
- **Dependency Updates**: Updated to secure versions of all dependencies
- **Security Scanning**: Added automated security checks with Bandit and Safety

### Deprecated
- **Travis CI**: Migrated from Travis CI to GitHub Actions
- **Python 3.6-3.7**: Dropped support for end-of-life Python versions

## [0.3.2] - Previous Release
### Initial Features
- Basic ServiceTitan API v2 integration
- Endpoint class for API interactions
- Report class for reporting endpoints
- DataService for common data operations
- Basic authentication support