"""
PDF Parser with complete text cleaning (ligatures + UTF-8 fix)
Replace src/parsers/pdf_parser.py with this
"""
from pathlib import Path
from .base_parser import BaseParser
import fitz  # PyMuPDF


def fix_pdf_ligatures(text: str) -> str:
    """Fix common ligature encoding issues from PDFs"""
    ligatures = {
        'Ɵ': 'ti',
        'Ʃ': 'tt',
        'ƒ': 'fi',
        'Ɛ': 'ff',
        'ﬁ': 'fi',
        'ﬂ': 'fl',
        'ﬀ': 'ff',
        'ﬃ': 'ffi',
        'ﬄ': 'ffl',
        'ﬅ': 'ft',
        'ﬆ': 'st',
    }
    
    for bad, good in ligatures.items():
        text = text.replace(bad, good)
    
    return text


def fix_utf8_encoding(text: str) -> str:
    """Fix common UTF-8 mojibake patterns"""
    replacements = {
        'Ã©': 'é',
        'Ã¨': 'è',
        'Ã ': 'à',
        'Ã´': 'ô',
        'Ã®': 'î',
        'Ã¹': 'ù',
        'Ã§': 'ç',
        'Ã‰': 'É',
        'Ã€': 'À',
        'Ãª': 'ê',
        'Ã«': 'ë',
        'Ã¯': 'ï',
        'Ã»': 'û',
        'â€™': "'",
        'â€"': '—',
        'â€œ': '"',
        'â€': '"',
        'Â«': '«',
        'Â»': '»',
        'Â ': ' ',
    }
    
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    
    return text


class PDFParser(BaseParser):
    """Parser for PDF files using PyMuPDF with complete text cleaning"""
    
    def _file_type_label(self) -> str:
        return "PDF"
    
    def parse(self, file_path: Path) -> str:
        """Parse PDF file with PyMuPDF and clean all encoding issues"""
        
        content_parts = []
        
        # Open PDF with PyMuPDF
        doc = fitz.open(file_path)
        
        for page_num, page in enumerate(doc, 1):
            # Extract text
            text = page.get_text()
            
            # Clean ligature issues first
            text = fix_pdf_ligatures(text)
            
            # Then fix UTF-8 encoding issues
            text = fix_utf8_encoding(text)
            
            if text.strip():
                content_parts.append(f"## Page {page_num}\n\n{text}\n")
        
        doc.close()
        
        return "\n".join(content_parts)