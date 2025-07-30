"""
CryptoPix v4.0.0 - Core Functionality Module

This module contains the enhanced encryption and decryption algorithms,
advanced color transformation utilities, and performance-optimized functions.

Major Components:
- Enhanced Fast Mode with Color Transformation Preservation
- ColorTransformationCache for vectorized operations
- MemoryPoolManager for zero-allocation performance
- Binary color serialization and mapping utilities
- Comprehensive exception handling system

Performance Features:
- Pre-computed lookup tables
- Vectorized color transformations
- Memory pool management
- Thread-safe operations
- Automatic format detection
"""

from .encryption import CryptoPix
from .exceptions import *
from .mapping import ColorMapper
from .utils import *

__all__ = [
    'CryptoPix',
    'ColorMapper',
]