"""
CryptoPix v4.0.0 - Advanced Secure Text Encryption Library

A powerful Python library for encrypting text using advanced cryptographic techniques
with dual-mode operation: steganographic image encryption and ultra-fast binary encryption.

🚀 NEW in v4.0.0: Enhanced Fast Mode with Color Transformation Preservation
- Ultra-fast encryption (0.5-1ms) while maintaining CryptoPix's core color essence
- 500x+ performance improvement over image mode
- Backward compatibility with all previous versions

Core Features:
- Dual encryption modes: Image steganography and enhanced fast binary
- Password-derived key generation using PBKDF2-HMAC-SHA256
- Advanced color transformation algorithms with vectorized optimizations
- Pre-computed lookup tables and memory pool management
- Lossless WebP image generation for steganographic mode
- Post-quantum resistance through symmetric cryptography
- Smart key metadata with automatic format detection

Basic Usage - Enhanced Fast Mode (NEW):
    >>> from cryptopix import CryptoPix
    >>> cp = CryptoPix()
    >>> 
    >>> # Ultra-fast encryption (recommended)
    >>> encrypted_data, key_data = cp.encrypt_fast("Hello, World!", "my_password")
    >>> decrypted_text = cp.decrypt_fast(encrypted_data, key_data, "my_password")
    >>> print(decrypted_text)  # "Hello, World!"

Basic Usage - Image Steganography Mode:
    >>> # Encrypt text to image
    >>> image_data, smart_key = cp.encrypt("Hello, World!", "my_password")
    >>> 
    >>> # Decrypt image back to text
    >>> from PIL import Image
    >>> import io
    >>> image = Image.open(io.BytesIO(image_data.getvalue()))
    >>> result = cp.decrypt(image, smart_key, "my_password")
    >>> print(result['content'])  # "Hello, World!"

Performance Comparison:
- Enhanced Fast Mode: 0.5-1ms encryption/decryption
- Image Mode: 200-400ms encryption, 1-2ms decryption
- Speed improvement: 300-800x faster while preserving color transformation

For more advanced usage and examples, see the documentation.
"""

from .core.encryption import CryptoPix
from .core.exceptions import (CryptoPixError, EncryptionError, DecryptionError,
                              InvalidPasswordError, InvalidKeyError,
                              UnsupportedFormatError)

# Version information
__version__ = "4.0.0"
__author__ = "CryptoPix Team"
__email__ = "founder@cryptopix.in"
__license__ = "Commercial"

# Main API exports
__all__ = [
    # Main classes
    'CryptoPix',

    # Exceptions
    'CryptoPixError',
    'EncryptionError',
    'DecryptionError',
    'InvalidPasswordError',
    'InvalidKeyError',
    'UnsupportedFormatError',

    # Convenience functions
    'encrypt_text',
    'decrypt_image',
    'encrypt_fast',
    'decrypt_fast',

    # Version info
    '__version__',
]


# Convenience functions for simple usage
def encrypt_text(text, password, width=None):
    """
    Convenience function to encrypt text to image using steganography mode.
    
    Args:
        text (str): Text to encrypt
        password (str): Password for encryption
        width (int, optional): Image width in pixels
        
    Returns:
        tuple: (image_data, smart_key) where image_data is BytesIO object
        
    Note:
        For faster encryption, use encrypt_fast() which provides 300-800x performance
        improvement while preserving CryptoPix's color transformation essence.
        
    Example:
        >>> image_data, smart_key = encrypt_text("Secret message", "password123")
        >>> with open("encrypted.webp", "wb") as f:
        ...     f.write(image_data.getvalue())
    """
    cp = CryptoPix()
    return cp.encrypt(text, password, width)


def decrypt_image(image, smart_key, password):
    """
    Convenience function to decrypt image to text.
    
    Args:
        image (PIL.Image.Image): Image to decrypt
        smart_key (str): Smart key from encryption
        password (str): Password used for encryption
        
    Returns:
        dict: Decryption result with 'content' and 'type' keys
        
    Example:
        >>> from PIL import Image
        >>> image = Image.open("encrypted.webp")
        >>> result = decrypt_image(image, smart_key, "password123")
        >>> print(result['content'])
    """
    cp = CryptoPix()
    return cp.decrypt(image, smart_key, password)


def encrypt_fast(text, password):
    """
    Convenience function for ultra-fast encryption with color transformation preservation.
    
    NEW in v4.0.0: Enhanced fast mode now preserves CryptoPix's core color transformation
    while achieving 300-800x performance improvement over image mode.
    
    Args:
        text (str): Text to encrypt
        password (str): Password for encryption
        
    Returns:
        tuple: (encrypted_bytes, key_data) where encrypted_bytes contains color-transformed data
        
    Performance:
        - Encryption: 0.5-1ms for typical data
        - 500x+ faster than image mode
        - Maintains algorithmic consistency with steganographic mode
        
    Example:
        >>> encrypted_data, key_data = encrypt_fast("Hello, World!", "password123")
        >>> decrypted = decrypt_fast(encrypted_data, key_data, "password123")
        >>> print(decrypted)  # "Hello, World!"
    """
    cp = CryptoPix()
    return cp.encrypt_fast(text, password)


def decrypt_fast(encrypted_data, key_data, password):
    """
    Convenience function for ultra-fast decryption with color transformation reversal.
    
    NEW in v4.0.0: Enhanced fast mode automatically detects format and applies proper
    color transformation reversal for maximum performance and accuracy.
    
    Args:
        encrypted_data (bytes): Encrypted byte data containing color-transformed content
        key_data (str): Key data from encryption (supports both enhanced and legacy formats)
        password (str): Password used for encryption
        
    Returns:
        str: Decrypted text
        
    Performance:
        - Decryption: 0.25-0.6ms for typical data
        - Automatic format detection (enhanced vs legacy)
        - Backward compatibility with all previous versions
        
    Example:
        >>> encrypted_data, key_data = encrypt_fast("Hello, World!", "password123")
        >>> decrypted_text = decrypt_fast(encrypted_data, key_data, "password123")
        >>> print(decrypted_text)  # "Hello, World!"
    """
    cp = CryptoPix()
    return cp.decrypt_fast(encrypted_data, key_data, password)
