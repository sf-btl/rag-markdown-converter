"""Markdown passthrough parser — adds metadata to existing .md files."""

from pathlib import Path

from .base_parser import BaseParser


class MarkdownPassthrough(BaseParser):
    """Pass-through for Markdown files.

    The original content is preserved as-is; only the RAG metadata header
    is prepended.
    """

    def parse(self, file_path: Path) -> str:
        text = file_path.read_text(encoding="utf-8", errors="replace").rstrip()
        return text if text else "*Empty file.*"

    def _file_type_label(self) -> str:
        return "Markdown"
