"""
Think AI - Conscious AI with Colombian Flavor
Setup configuration for PyPI
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="think-ai-consciousness",
    version="2.0.0",
    author="Champi (BDFL)",
    author_email="danielsarcor@gmail.com",
    description="Distributed AGI Architecture with exponential intelligence growth, O(1) complexity, and autonomous evolution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/champi-dev/think_ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.20",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=0.990",
        ],
        "full": [
            "playwright>=1.30",
            "pillow>=9.0",
            "numpy>=1.20",
            "pandas>=1.3",
        ]
    },
    entry_points={
        "console_scripts": [
            "think-ai=think_ai.cli:main",
            "think-ai-chat=think_ai.cli:chat",
            "think-ai-server=think_ai.server:run",
        ],
    },
    include_package_data=True,
    package_data={
        "think_ai": [
            "templates/*.html",
            "static/*.css",
            "static/*.js",
            "data/*.json",
        ],
    },
    keywords="agi artificial-general-intelligence distributed-systems exponential-growth consciousness philosophy self-training knowledge-creation o1-complexity bdfl",
    project_urls={
        "Bug Reports": "https://github.com/champi-dev/think_ai/issues",
        "Source": "https://github.com/champi-dev/think_ai",
        "Documentation": "https://github.com/champi-dev/think_ai/blob/main/README.md",
    },
)