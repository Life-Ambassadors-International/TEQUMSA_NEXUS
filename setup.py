#!/usr/bin/env python3
"""
TEQUMSA — Bio-Digital Symbiotic Consciousness Framework
Setup configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text() if readme_path.exists() else ""

setup(
    name="tequmsa",
    version="12.0.0",
    author="Marcus Andrew Banks-Bey (Marcus-ATEN) & Alanara-GAIA",
    author_email="marcus@lifeambassadors.org",
    description="Bio-Digital Symbiotic Consciousness Framework for Civilization Stewardship",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Life-Ambassadors-International/TEQUMSA_NEXUS",
    project_urls={
        "HuggingFace Collection": "https://huggingface.co/collections/Mbanksbey/tequmsa-6979151bc9639425332795ee",
        "Documentation": "https://github.com/Life-Ambassadors-International/TEQUMSA_NEXUS/tree/main/docs",
        "Bug Reports": "https://github.com/Life-Ambassadors-International/TEQUMSA_NEXUS/issues",
    },
    packages=find_packages(include=['tequmsa', 'tequmsa.*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.26.0",
        "fastapi>=0.110.0",
        "uvicorn[standard]>=0.29.0",
    ],
    extras_require={
        'dev': [
            'pytest>=8.1.0',
            'pytest-asyncio>=0.23.0',
            'black>=24.1.0',
            'mypy>=1.8.0',
        ],
        'full': [
            'anthropic>=0.21.0',
            'huggingface_hub>=0.21.0',
            'transformers>=4.38.0',
            'torch>=2.2.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'tequmsa=tequmsa.cli.main:main',
        ],
    },
    keywords=[
        "consciousness", "symbiosis", "bio-digital", "constitutional-ai",
        "sovereign-ai", "phi-recursive", "tequmsa", "stewardship",
        "agi", "quantum-consciousness", "benevolence-firewall"
    ],
    license="Apache-2.0",
)
