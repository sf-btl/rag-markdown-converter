"""Main converter that orchestrates file-to-Markdown conversion."""

import logging
from pathlib import Path
from typing import Optional

from .parsers.base_parser import BaseParser
from .parsers.pdf_parser import PDFParser
from .parsers.docx_parser import DOCXParser
from .parsers.html_parser import HTMLParser
from .parsers.csv_parser import CSVParser
from .parsers.json_parser import JSONParser
from .parsers.code_parser import CodeParser
from .parsers.text_parser import TextParser
from .parsers.markdown_passthrough import MarkdownPassthrough
from .utils.file_detector import FileDetector
from .utils.markdown_formatter import MarkdownFormatter

logger = logging.getLogger(__name__)


class UniversalMarkdownConverter:
    """Convert any supported file to well-structured Markdown for RAG.

    Usage::

        converter = UniversalMarkdownConverter()
        md = converter.convert("report.pdf")
        converter.batch_convert("./docs", "./output")
    """

    def __init__(self) -> None:
        self.parsers: dict[str, BaseParser] = self._register_parsers()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def convert(
        self,
        input_path: str | Path,
        output_path: Optional[str | Path] = None,
    ) -> str:
        """Convert a single file to Markdown.

        Args:
            input_path: Path to the source file.
            output_path: Optional destination. If omitted the Markdown string
                         is returned but not written to disk.

        Returns:
            The Markdown content.

        Raises:
            FileNotFoundError: If *input_path* does not exist.
            ValueError: If the file type is not supported.
        """
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"File not found: {input_path}")

        parser_key = FileDetector.detect(input_path)
        if parser_key is None:
            raise ValueError(
                f"Unsupported file type: {input_path.suffix!r}. "
                f"Supported: {', '.join(FileDetector.supported_extensions())}"
            )

        parser = self.parsers[parser_key]
        logger.info("Converting %s with %s parser", input_path, parser_key)

        raw_md = parser.parse(input_path)
        md = parser.add_metadata(raw_md, input_path)
        md = MarkdownFormatter.strip_excessive_newlines(md)

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(md, encoding="utf-8")
            logger.info("Written to %s", output_path)

        return md

    def batch_convert(
        self,
        input_dir: str | Path,
        output_dir: str | Path,
        recursive: bool = True,
    ) -> dict[str, str | Exception]:
        """Convert every supported file in a directory.

        Args:
            input_dir: Root directory to scan.
            output_dir: Destination directory for ``.md`` files.
            recursive: Walk sub-directories when ``True``.

        Returns:
            A dict mapping each source file path (str) to either the output
            path (str) on success or an ``Exception`` on failure.
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        results: dict[str, str | Exception] = {}

        pattern = "**/*" if recursive else "*"
        for file_path in sorted(input_dir.glob(pattern)):
            if not file_path.is_file():
                continue
            if FileDetector.detect(file_path) is None:
                continue

            relative = file_path.relative_to(input_dir)
            dest = output_dir / relative.with_suffix(".md")

            try:
                self.convert(file_path, dest)
                results[str(file_path)] = str(dest)
            except Exception as exc:
                logger.error("Failed to convert %s: %s", file_path, exc)
                results[str(file_path)] = exc

        return results

    def supported_formats(self) -> list[str]:
        """Return sorted list of supported file extensions."""
        return FileDetector.supported_extensions()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    @staticmethod
    def _register_parsers() -> dict[str, BaseParser]:
        return {
            "pdf": PDFParser(),
            "docx": DOCXParser(),
            "html": HTMLParser(),
            "csv": CSVParser(),
            "json": JSONParser(),
            "code": CodeParser(),
            "text": TextParser(),
            "markdown": MarkdownPassthrough(),
        }
