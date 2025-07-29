# Changelog

All notable changes to the CryptoPix library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2025-06-17

### Changed
- Updated to commercial licensing model
- Removed free MIT license, replaced with proprietary commercial license
- Added comprehensive licensing tiers (Developer, Professional, Enterprise)
- Updated all documentation to reflect commercial nature
- Enhanced security with commercial-grade features

### Added
- Commercial license enforcement
- Professional pricing structure
- Enterprise support options
- Enhanced security documentation
- Commercial deployment guidelines

### Removed
- Free usage permissions
- Open source distribution rights
- MIT license compatibility

## [2.0.0] - 2025-01-15

### Added
- CryptoPix V2 algorithm with enhanced security
- Dynamic color generation eliminating static mapping files
- Improved password-derived key generation
- Enhanced smart key system with better metadata encryption
- Production-ready Flask API platform

### Changed
- Migrated from static color mapping to dynamic generation
- Improved encryption performance and security
- Enhanced API authentication and rate limiting

## [1.0.0] - 2024-12-17

### Added
- Complete library restructure from Flask web application
- Core CryptoPix encryption/decryption functionality
- Password-derived key generation using PBKDF2-HMAC-SHA256
- Dynamic color table shuffling for enhanced security
- Smart key metadata packaging with AES-256-GCM encryption
- Lossless WebP image generation
- Command-line interface with `cryptopix` command
- Comprehensive test suite with pytest
- Exception handling with custom exception classes
- Convenience functions for quick usage
- Performance optimizations with LRU caching
- Cross-platform compatibility (Python 3.8+)

### Security
- Post-quantum resistance through symmetric cryptography
- 256-bit derived keys with 128-bit random salts
- Constant-time operations where possible
- Secure random number generation
- Memory-safe implementations

### Documentation
- Complete README with usage examples
- Publishing guide for PyPI distribution
- API reference documentation
- Performance benchmarks and guidelines

### Dependencies
- Pillow >= 10.0.0 for image processing
- cryptography >= 41.0.0 for secure encryption
- numpy >= 1.24.0 for numerical operations
