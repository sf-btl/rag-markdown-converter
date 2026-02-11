"""Code file → Markdown parser."""

from pathlib import Path

from .base_parser import BaseParser
from ..utils.file_detector import FileDetector
from ..utils.markdown_formatter import MarkdownFormatter


class CodeParser(BaseParser):
    """Wrap source-code files in a Markdown fenced code block with syntax hints."""

    def parse(self, file_path: Path) -> str:
        code = file_path.read_text(encoding="utf-8", errors="replace")
        language = FileDetector.language_hint(file_path)
        return MarkdownFormatter.wrap_code_block(code.rstrip(), language)

    def _file_type_label(self) -> str:
        return "Code"

    def add_metadata(self, content: str, file_path: Path, **extra) -> str:
        lang = FileDetector.language_hint(file_path)
        if lang:
            extra.setdefault("Language", lang.capitalize())
        return super().add_metadata(content, file_path, **extra)
