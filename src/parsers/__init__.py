"""File format parsers."""

from .base_parser import BaseParser
from .pdf_parser import PDFParser
from .docx_parser import DOCXParser
from .html_parser import HTMLParser
from .csv_parser import CSVParser
from .json_parser import JSONParser
from .code_parser import CodeParser
from .text_parser import TextParser
from .markdown_passthrough import MarkdownPassthrough

__all__ = [
    "BaseParser",
    "PDFParser",
    "DOCXParser",
    "HTMLParser",
    "CSVParser",
    "JSONParser",
    "CodeParser",
    "TextParser",
    "MarkdownPassthrough",
]
