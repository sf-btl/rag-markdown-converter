"""Abstract base class for all file parsers."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path


class BaseParser(ABC):
    """Base class that every format-specific parser must inherit from."""

    @abstractmethod
    def parse(self, file_path: Path) -> str:
        """Convert a file to Markdown content (without metadata header).

        Args:
            file_path: Path to the source file.

        Returns:
            Markdown-formatted string of the file's content.
        """

    def add_metadata(self, content: str, file_path: Path, **extra) -> str:
        """Wrap parsed content with a metadata header for RAG ingestion.

        Args:
            content: The Markdown body produced by ``parse``.
            file_path: Original source file path.
            **extra: Additional metadata key/value pairs (e.g. pages, language).

        Returns:
            Complete Markdown document with metadata block.
        """
        title = self._derive_title(file_path, content)
        file_type = self._file_type_label()
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        header_lines = [
            f"# {title}",
            "",
            f"*Source: {file_path.name}*  ",
            f"*Type: {file_type}*  ",
            f"*Converted: {now}*  ",
        ]
        for key, value in extra.items():
            header_lines.append(f"*{key}: {value}*  ")

        header_lines.append("")
        header_lines.append("---")
        header_lines.append("")

        return "\n".join(header_lines) + content

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _derive_title(self, file_path: Path, content: str) -> str:
        """Try to extract a title from the content; fall back to file stem."""
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("# ") and len(stripped) > 2:
                return stripped[2:].strip()
        return file_path.stem.replace("_", " ").replace("-", " ").title()

    @abstractmethod
    def _file_type_label(self) -> str:
        """Return a human-readable label for the file type (e.g. 'PDF')."""
