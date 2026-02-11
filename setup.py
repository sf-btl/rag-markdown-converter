"""Package setup for rag-markdown-converter."""

from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="rag-markdown-converter",
    version="1.0.0",
    description="Universal File-to-Markdown Converter for RAG Preprocessing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "pypdf>=4.0",
        "python-docx>=1.1",
        "beautifulsoup4>=4.12",
        "html2text>=2024.2",
    ],
    entry_points={
        "console_scripts": [
            "rag-md-converter=src.cli:main",
        ],
    },
)
