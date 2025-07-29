"""
CryptoPix - Core Encryption Module (Simplified Clean Version)

A clean, minimal implementation of the CryptoPix encryption system
focusing on core functionality without unnecessary complexity.
"""

import os
import json
import base64
import secrets
import hashlib
import struct
import time
from io import BytesIO
from PIL import Image
import numpy as np
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import logging
from threading import Lock

from .exceptions import (
    EncryptionError,
    DecryptionError,
    InvalidPasswordError,
    InvalidKeyError,
    UnsupportedFormatError
)

logger = logging.getLogger(__name__)

# CryptoPix Configuration
PBKDF2_ITERATIONS = 1000
KEY_LENGTH = 32  # 256 bits
SALT_LENGTH = 16  # 128 bits
VERSION = "4.0.0"


class ColorTransformationCache:
    """Pre-computed lookup tables for ultra-fast color transformations"""
    
    def __init__(self):
        self._lock = Lock()
        self._initialized = False
        self.transform_table = None
        self.reverse_table = None
    
    def _initialize(self):
        """Initialize lookup tables (called once)"""
        with self._lock:
            if self._initialized:
                return
                
            # Pre-compute all possible (value + key_byte) % 256 combinations
            self.transform_table = np.zeros((256, 256), dtype=np.uint8)
            self.reverse_table = np.zeros((256, 256), dtype=np.uint8)
            
            for i in range(256):
                for k in range(256):
                    self.transform_table[i, k] = (i + k) % 256
                    self.reverse_table[i, k] = (i - k) % 256
            
            self._initialized = True
    
    def fast_transform(self, pixels, key_bytes):
        """Vectorized transformation using lookup tables"""
        if not self._initialized:
            self._initialize()
            
        if self.transform_table is None:
            raise RuntimeError("Transform table not initialized")
            
        result = np.zeros_like(pixels, dtype=np.uint8)
        for channel in range(3):
            key_idx = channel % len(key_bytes)
            result[:, channel] = self.transform_table[pixels[:, channel], key_bytes[key_idx]]
        return result
    
    def fast_reverse(self, pixels, key_bytes):
        """Vectorized reverse transformation using lookup tables"""
        if not self._initialized:
            self._initialize()
            
        if self.reverse_table is None:
            raise RuntimeError("Reverse table not initialized")
            
        result = np.zeros_like(pixels, dtype=np.uint8)
        for channel in range(3):
            key_idx = channel % len(key_bytes)
            result[:, channel] = self.reverse_table[pixels[:, channel], key_bytes[key_idx]]
        return result


class MemoryPoolManager:
    """Pre-allocated memory pools for zero-allocation operations"""
    
    def __init__(self):
        self.buffer_sizes = [1024, 4096, 16384, 65536]  # Common sizes
        self.pools = {size: [] for size in self.buffer_sizes}
        self.max_pool_size = 10
        self._lock = Lock()
    
    def _find_pool_size(self, size):
        """Find appropriate pool size for given buffer size"""
        for pool_size in self.buffer_sizes:
            if size <= pool_size:
                return pool_size
        return max(self.buffer_sizes)
    
    def get_buffer(self, size):
        """Get pre-allocated buffer or create new one"""
        pool_size = self._find_pool_size(size)
        
        with self._lock:
            if pool_size in self.pools and self.pools[pool_size]:
                return self.pools[pool_size].pop()
        
        return np.zeros(pool_size, dtype=np.uint8)
    
    def return_buffer(self, buffer):
        """Return buffer to pool for reuse"""
        if buffer is None:
            return
            
        size = len(buffer)
        pool_size = self._find_pool_size(size)
        
        with self._lock:
            if len(self.pools[pool_size]) < self.max_pool_size:
                buffer.fill(0)  # Clear sensitive data
                self.pools[pool_size].append(buffer)


# Global instances for performance
_global_cache = ColorTransformationCache()
_global_pool = MemoryPoolManager()


def serialize_colors_to_binary(color_pixels):
    """Convert color pixel array to binary format (fastest)"""
    return struct.pack(f'{len(color_pixels)*3}B', 
                      *[channel for pixel in color_pixels for channel in pixel])


def deserialize_binary_to_colors(binary_data):
    """Convert binary data back to color pixels"""
    channels = struct.unpack(f'{len(binary_data)}B', binary_data)
    return [(channels[i], channels[i+1], channels[i+2]) 
            for i in range(0, len(channels), 3)]


def text_to_color_pixels(text_bytes, key):
    """Convert text bytes to color pixels using CryptoPix transformation"""
    global _global_cache
    
    # Pad text to multiple of 3
    padded_length = ((len(text_bytes) + 2) // 3) * 3
    padded_text = text_bytes + b'\x00' * (padded_length - len(text_bytes))
    
    # Reshape to RGB pixels
    pixels = np.frombuffer(padded_text, dtype=np.uint8).reshape(-1, 3)
    
    # Apply CryptoPix color transformation using optimized cache
    key_array = np.array(list(key), dtype=np.uint8)
    transformed_pixels = _global_cache.fast_transform(pixels, key_array[:3])
    
    return [(int(transformed_pixels[i, 0]), int(transformed_pixels[i, 1]), int(transformed_pixels[i, 2])) 
            for i in range(len(transformed_pixels))]


def color_pixels_to_text(color_pixels, key, original_length):
    """Convert color pixels back to text using reverse transformation"""
    global _global_cache
    
    # Convert to numpy array
    pixels = np.array(color_pixels, dtype=np.uint8)
    
    # Apply reverse transformation
    key_array = np.array(list(key), dtype=np.uint8)
    reversed_pixels = _global_cache.fast_reverse(pixels, key_array[:3])
    
    # Convert back to bytes and trim to original length
    text_bytes = reversed_pixels.flatten().tobytes()[:original_length]
    return text_bytes


class CryptoPix:
    """Clean CryptoPix implementation with core encryption/decryption functionality"""
    
    def __init__(self):
        """Initialize CryptoPix"""
        pass
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive a 256-bit key from password using PBKDF2-HMAC-SHA256"""
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=KEY_LENGTH,
                salt=salt,
                iterations=PBKDF2_ITERATIONS,
                backend=default_backend()
            )
            return kdf.derive(password.encode('utf-8'))
        except Exception as e:
            raise EncryptionError(f"Failed to derive key: {str(e)}")
    
    def encrypt(self, text: str, password: str, width=None) -> tuple:
        """
        Encrypt text to an image using CryptoPix algorithm
        
        Args:
            text: Text to encrypt
            password: Password for encryption
            width: Optional image width
            
        Returns:
            Tuple of (BytesIO image, smart_key)
        """
        if not text:
            raise ValueError("Text cannot be empty")
        if not password:
            raise ValueError("Password cannot be empty")
        
        try:
            # Generate salt and derive key
            salt = secrets.token_bytes(SALT_LENGTH)
            key = self._derive_key(password, salt)
            
            # Convert text to binary
            text_bytes = text.encode('utf-8')
            
            # Create color pixels from binary data
            colors = []
            for i in range(0, len(text_bytes), 3):
                chunk = text_bytes[i:i+3]
                # Pad chunk if necessary
                while len(chunk) < 3:
                    chunk += b'\x00'
                
                # Generate RGB color using key-based transformation
                r = (chunk[0] + key[i % KEY_LENGTH]) % 256
                g = (chunk[1] + key[(i+1) % KEY_LENGTH]) % 256
                b = (chunk[2] + key[(i+2) % KEY_LENGTH]) % 256
                colors.append((r, g, b))
            
            # Calculate image dimensions
            total_pixels = len(colors)
            if width is None:
                width = int(np.ceil(np.sqrt(total_pixels)))
            height = int(np.ceil(total_pixels / width))
            
            # Create image
            img = Image.new('RGB', (width, height), (0, 0, 0))
            pixels = img.load()
            
            for i, color in enumerate(colors):
                x = i % width
                y = i // width
                if y < height:
                    pixels[x, y] = color
            
            # Save as WebP
            img_buffer = BytesIO()
            img.save(img_buffer, format='WebP', lossless=True, quality=100)
            img_buffer.seek(0)
            
            # Create smart key
            metadata = {
                'salt': base64.b64encode(salt).decode(),
                'text_length': len(text_bytes),
                'width': width,
                'height': height
            }
            
            smart_key = f"cryptopix_v4:{base64.b64encode(json.dumps(metadata).encode()).decode()}"
            
            return img_buffer, smart_key
            
        except Exception as e:
            raise EncryptionError(f"Encryption failed: {str(e)}")
    
    def decrypt(self, img: Image.Image, smart_key: str, password: str) -> dict:
        """
        Decrypt an encrypted image back to text
        
        Args:
            img: PIL Image object
            smart_key: Smart key containing encrypted metadata
            password: Password for decryption
            
        Returns:
            Dictionary with decrypted content and type
        """
        if not smart_key:
            raise InvalidKeyError("Smart key cannot be empty")
        if not password:
            raise ValueError("Password cannot be empty")
        
        try:
            if smart_key.startswith("cryptopix_v4:"):
                # Parse metadata
                metadata_b64 = smart_key.split(":", 1)[1]
                metadata = json.loads(base64.b64decode(metadata_b64).decode())
                
                salt = base64.b64decode(metadata['salt'])
                text_length = metadata['text_length']
                
                # Derive key
                key = self._derive_key(password, salt)
                
                # Extract colors from image
                pixels = list(img.getdata())
                
                # Reverse color transformation to get binary data
                text_bytes = bytearray()
                for i, (r, g, b) in enumerate(pixels):
                    if len(text_bytes) >= text_length:
                        break
                    
                    # Reverse transformation
                    orig_r = (r - key[i*3 % KEY_LENGTH]) % 256
                    orig_g = (g - key[(i*3+1) % KEY_LENGTH]) % 256
                    orig_b = (b - key[(i*3+2) % KEY_LENGTH]) % 256
                    
                    text_bytes.extend([orig_r, orig_g, orig_b])
                
                # Trim to actual text length
                text_bytes = text_bytes[:text_length]
                
                # Decode to text
                decrypted_text = bytes(text_bytes).decode('utf-8')
                return {
                    'content': decrypted_text,
                    'type': 'text',
                    'success': True
                }
            else:
                raise InvalidKeyError("Unsupported smart key format")
                
        except Exception as e:
            raise DecryptionError(f"Decryption failed: {str(e)}")
    
    def encrypt_fast(self, text: str, password: str) -> tuple:
        """
        Ultra-fast encryption with CryptoPix color transformation preservation
        
        Args:
            text: Text to encrypt
            password: Password for encryption
            
        Returns:
            Tuple of (encrypted_bytes, key_data)
        """
        if not text:
            raise ValueError("Text cannot be empty")
        if not password:
            raise ValueError("Password cannot be empty")
        
        try:
            # Generate salt and derive key
            salt = secrets.token_bytes(SALT_LENGTH)
            key = self._derive_key(password, salt)
            
            # Step 1: Convert text to bytes
            text_bytes = text.encode('utf-8')
            original_length = len(text_bytes)
            
            # Step 2: Apply CryptoPix color transformation (PRESERVED)
            color_pixels = text_to_color_pixels(text_bytes, key)
            
            # Step 3: Serialize colors to binary string (NEW)
            color_binary = serialize_colors_to_binary(color_pixels)
            
            # Step 4: Encrypt color binary with AES-GCM
            iv = secrets.token_bytes(12)  # 96-bit IV for GCM
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(color_binary) + encryptor.finalize()
            
            # Create enhanced key data with original length
            metadata = {
                'salt': base64.b64encode(salt).decode(),
                'iv': base64.b64encode(iv).decode(),
                'tag': base64.b64encode(encryptor.tag).decode(),
                'original_length': original_length,
                'version': 'enhanced_fast'
            }
            key_data = f"cryptopix_fast_v2:{base64.b64encode(json.dumps(metadata).encode()).decode()}"
            
            return ciphertext, key_data
            
        except Exception as e:
            raise EncryptionError(f"Fast encryption failed: {str(e)}")
    
    def decrypt_fast(self, encrypted_data: bytes, key_data: str, password: str) -> str:
        """
        Ultra-fast decryption with CryptoPix color transformation preservation
        
        Args:
            encrypted_data: Encrypted byte data
            key_data: Key data from encryption
            password: Password for decryption
            
        Returns:
            Decrypted text
        """
        if not encrypted_data:
            raise ValueError("Encrypted data cannot be empty")
        if not key_data:
            raise InvalidKeyError("Key data cannot be empty")
        if not password:
            raise ValueError("Password cannot be empty")
        
        try:
            if not key_data.startswith("cryptopix_fast_v2:"):
                raise InvalidKeyError("Invalid fast mode key format")
            
            # Parse enhanced key data format
            metadata_b64 = key_data.split(":", 1)[1]
            metadata = json.loads(base64.b64decode(metadata_b64).decode())
            
            # Check if this is enhanced fast mode
            if metadata.get('version') == 'enhanced_fast':
                # Enhanced fast mode with color transformation
                salt = base64.b64decode(metadata['salt'])
                iv = base64.b64decode(metadata['iv'])
                tag = base64.b64decode(metadata['tag'])
                original_length = metadata['original_length']
                
                # Derive key and decrypt color binary
                key = self._derive_key(password, salt)
                cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
                decryptor = cipher.decryptor()
                color_binary = decryptor.update(encrypted_data) + decryptor.finalize()
                
                # Step 1: Deserialize binary to color pixels
                color_pixels = deserialize_binary_to_colors(color_binary)
                
                # Step 2: Reverse color transformation to get original text
                text_bytes = color_pixels_to_text(color_pixels, key, original_length)
                
                return text_bytes.decode('utf-8')
            else:
                # Legacy format support
                parts = key_data.split(":")
                if len(parts) != 4:
                    raise InvalidKeyError("Invalid key data format")
                
                salt = base64.b64decode(parts[1])
                iv = base64.b64decode(parts[2])
                tag = base64.b64decode(parts[3])
                
                # Derive key and decrypt
                key = self._derive_key(password, salt)
                cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
                decryptor = cipher.decryptor()
                decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
                
                return decrypted_data.decode('utf-8')
            
        except Exception as e:
            raise DecryptionError(f"Fast decryption failed: {str(e)}")


# Convenience functions for backward compatibility
def encrypt_text_to_image_v2(text: str, password: str, width=None) -> tuple:
    """Convenience function for text to image encryption"""
    cp = CryptoPix()
    return cp.encrypt(text, password, width)


def decrypt_image_to_text_v2(img: Image.Image, smart_key: str, password: str) -> dict:
    """Convenience function for image to text decryption"""
    cp = CryptoPix()
    return cp.decrypt(img, smart_key, password)