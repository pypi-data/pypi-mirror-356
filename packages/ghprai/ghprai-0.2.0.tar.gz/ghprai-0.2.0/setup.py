#!/usr/bin/env python3
"""Setup script for GitHub PR AI Agent."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = []
with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="ghprai",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered GitHub PR reviewer using Ollama for intelligent code analysis and test generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-agent-pr-reviewer",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.23.5",
            "black",
            "flake8",
            "mypy",
            "pre-commit",
        ],
        "server": [
            "gunicorn>=20.1.0",
            "docker",
        ],
    },
    entry_points={
        "console_scripts": [
            "ghprai-server=ghprai.server.app:main",
            "ghprai=ghprai.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ghprai": ["templates/*.txt", "config/*.yaml"],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai-agent-pr-reviewer/issues",
        "Source": "https://github.com/yourusername/ai-agent-pr-reviewer",
        "Documentation": "https://github.com/yourusername/ai-agent-pr-reviewer/blob/main/README.md",
    },
)
