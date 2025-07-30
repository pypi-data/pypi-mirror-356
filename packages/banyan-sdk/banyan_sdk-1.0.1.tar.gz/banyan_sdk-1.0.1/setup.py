#!/usr/bin/env python
"""
Setup script for Banyan SDK 
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
def read_file(filename):
    """Read file contents"""
    try:
        with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

# Read version from __init__.py
def get_version():
    """Extract version from __init__.py"""
    version_file = os.path.join('banyan', '__init__.py')
    with open(version_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                # Handle both single and double quotes
                if '"' in line:
                    return line.split('"')[1]
                elif "'" in line:
                    return line.split("'")[1]
    return "1.0.0"

setup(
    name="banyan-sdk",
    version=get_version(),
    author="Banyan Team",
    author_email="talrejayuvvan@gmail.com",
    description="Python SDK for Banyan - manage, version, and A/B test your LLM prompts",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/yuvvantalreja/banyan-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio",
            "black",
            "flake8",
            "mypy",
            "twine",
            "build"
        ],
    },
    keywords="llm prompt logging ai machine-learning openai anthropic experiments a-b-testing versioning banyan",
    project_urls={
        "Bug Reports": "https://github.com/banyan-team/banyan-sdk/issues",
        "Source": "https://github.com/banyan-team/banyan-sdk",
        "Documentation": "https://docs.banyan.dev",
    },
    entry_points={
        "console_scripts": [
            # Add CLI tools if needed in the future
        ],
    },
) 