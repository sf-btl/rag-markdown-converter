"""
PDF Parser with table extraction and text cleaning
"""
from pathlib import Path
from .base_parser import BaseParser
import fitz  # PyMuPDF
import pdfplumber


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


def table_to_markdown(table_data: list) -> str:
    """Convert table data to Markdown table format"""
    if not table_data or len(table_data) < 2:
        return ""
    
    markdown = "\n"
    
    # Header row
    headers = [str(cell or '').strip() for cell in table_data[0]]
    markdown += "| " + " | ".join(headers) + " |\n"
    
    # Separator row
    markdown += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    
    # Data rows
    for row in table_data[1:]:
        cells = [str(cell or '').strip() for cell in row]
        # Pad row if needed
        while len(cells) < len(headers):
            cells.append('')
        markdown += "| " + " | ".join(cells[:len(headers)]) + " |\n"
    
    markdown += "\n"
    return markdown


class PDFParser(BaseParser):
    """Parser for PDF files with table extraction and text cleaning"""
    
    def _file_type_label(self) -> str:
        return "PDF"
    
    def parse(self, file_path: Path) -> str:
        """Parse PDF with table extraction and encoding fixes"""
        
        content_parts = []
        
        # Use pdfplumber for table detection
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_content = f"## Page {page_num}\n\n"
                
                # Try to extract tables
                tables = page.extract_tables()
                
                if tables:
                    # Page has tables - extract text first
                    text = page.extract_text()
                    
                    if text:
                        # Apply encoding fixes to text
                        text = fix_pdf_ligatures(text)
                        text = fix_utf8_encoding(text)
                        page_content += text + "\n\n"
                    
                    # Add tables in Markdown format
                    for i, table in enumerate(tables, 1):
                        if len(tables) > 1:
                            page_content += f"### Tableau {i}\n"
                        page_content += table_to_markdown(table)
                
                else:
                    # No tables - use PyMuPDF for better text extraction
                    doc = fitz.open(file_path)
                    fitz_page = doc[page_num - 1]
                    text = fitz_page.get_text()
                    doc.close()
                    
                    # Apply encoding fixes
                    text = fix_pdf_ligatures(text)
                    text = fix_utf8_encoding(text)
                    page_content += text + "\n"
                
                if page_content.strip() != f"## Page {page_num}":
                    content_parts.append(page_content)
        
        return "\n".join(content_parts)