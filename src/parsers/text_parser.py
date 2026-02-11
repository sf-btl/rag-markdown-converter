"""Plain text → Markdown parser."""

from pathlib import Path

from .base_parser import BaseParser


class TextParser(BaseParser):
    """Convert plain text files to Markdown (minimal transformation)."""

    def parse(self, file_path: Path) -> str:
    # Detect encoding
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))
    encoding = result['encoding'] if result['confidence'] > 0.5 else 'utf-8'
    
    # Read with detected encoding
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()

    def _file_type_label(self) -> str:
        return "Plain Text"
