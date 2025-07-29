#!/usr/bin/env python3
"""
CryptoPix v4.0.0 - Setup Configuration
"""

from setuptools import setup, find_packages
import os

# Read version from __init__.py
def get_version():
    import re
    init_file = os.path.join(os.path.dirname(__file__), 'cryptopix', '__init__.py')
    if os.path.exists(init_file):
        with open(init_file, 'r') as f:
            content = f.read()
            match = re.search(r"__version__\s*=\s*['\"]([^'\"]*)['\"]", content)
            if match:
                return match.group(1)
    return '4.0.0'


# Read README for long description
def get_long_description():
    readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "CryptoPix v4.0.0 - Advanced Secure Text Encryption Library"


setup(
    name="cryptopix",
    version=get_version(),
    author="CryptoPix Development Team",
    author_email="founder@cryptopix.in",
    description=
    "Advanced secure text encryption library with dual-mode operation",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/cryptopix-official/cryptopix",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "cryptography>=41.0.0",
        "Pillow>=9.0.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-benchmark>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "performance": [
            "numba>=0.57.0",  # Optional JIT compilation
            "psutil>=5.9.0",  # Memory monitoring
        ],
    },
    include_package_data=True,
    package_data={
        "cryptopix": ["VERSION", "*.md"],
    },
    keywords=[
        "cryptography", "encryption", "steganography", "security",
        "image-encryption", "text-encryption", "password-protection", "aes",
        "cryptopix", "fast-encryption", "color-transformation"
    ],
    project_urls={
        "Bug Reports":
        "https://github.com/cryptopix-official/cryptopix/issues",
        "Source":
        "https://github.com/cryptopix-official/cryptopix",
        "Documentation":
        "https://github.com/cryptopix-official/cryptopix",
        "Changelog":
        "https://github.com/cryptopix-official/cryptopix/blob/main/CHANGELOG.md",
    },
)
