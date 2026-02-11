"""Text Parser with automatic encoding detection"""
from pathlib import Path
from .base_parser import BaseParser
import chardet


class TextParser(BaseParser):
    """Parser for plain text files with automatic encoding detection"""
    
    def _file_type_label(self) -> str:
        """Return the file type label for metadata"""
        return "Plain Text"
    
    def parse(self, file_path: Path) -> str:
        """Parse plain text file with encoding detection"""
        
        # Detect encoding
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read(10000))
        
        encoding = result.get('encoding', 'utf-8')
        confidence = result.get('confidence', 0)
        
        if confidence < 0.5:
            encoding = 'utf-8'
        
        # Read with detected encoding
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()