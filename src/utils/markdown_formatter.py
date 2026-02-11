"""Markdown formatting utilities for clean, RAG-friendly output."""

import re
from typing import Optional


class MarkdownFormatter:
    """Static helpers that normalise and clean Markdown text."""

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Collapse runs of 3+ blank lines down to 2 (one visual blank line)."""
        return re.sub(r"\n{3,}", "\n\n", text)

    @staticmethod
    def make_table(headers: list[str], rows: list[list[str]]) -> str:
        """Build a GitHub-Flavoured Markdown table.

        Args:
            headers: Column header strings.
            rows: List of rows, each row a list of cell strings.

        Returns:
            A Markdown table as a string.
        """
        if not headers:
            return ""

        # Escape pipe characters in cell values
        def escape(cell: str) -> str:
            return str(cell).replace("|", "\\|").strip()

        header_line = "| " + " | ".join(escape(h) for h in headers) + " |"
        sep_line = "| " + " | ".join("---" for _ in headers) + " |"

        body_lines: list[str] = []
        for row in rows:
            # Pad or trim row to match header count
            padded = list(row) + [""] * (len(headers) - len(row))
            padded = padded[: len(headers)]
            body_lines.append("| " + " | ".join(escape(c) for c in padded) + " |")

        return "\n".join([header_line, sep_line, *body_lines])

    @staticmethod
    def wrap_code_block(code: str, language: str = "") -> str:
        """Wrap *code* in a fenced code block."""
        fence = "```"
        # Use longer fence if the code itself contains triple backticks
        while fence in code:
            fence += "`"
        return f"{fence}{language}\n{code}\n{fence}"

    @staticmethod
    def heading(text: str, level: int = 1) -> str:
        """Create a Markdown heading (level 1–6)."""
        level = max(1, min(6, level))
        return f"{'#' * level} {text}"

    @staticmethod
    def strip_excessive_newlines(text: str) -> str:
        """Final cleanup pass: trim trailing whitespace per line, collapse blanks."""
        lines = [line.rstrip() for line in text.splitlines()]
        result = "\n".join(lines)
        return MarkdownFormatter.normalize_whitespace(result).strip() + "\n"

    @staticmethod
    def truncate_table(
        headers: list[str],
        rows: list[list[str]],
        max_rows: int = 100,
    ) -> tuple[str, Optional[str]]:
        """Build a table, truncating if it exceeds *max_rows*.

        Returns:
            (table_markdown, note_or_None)
        """
        note = None
        if len(rows) > max_rows:
            note = f"*Table truncated: showing {max_rows} of {len(rows)} rows.*"
            rows = rows[:max_rows]
        return MarkdownFormatter.make_table(headers, rows), note
