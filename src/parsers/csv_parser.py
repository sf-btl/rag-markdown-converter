"""CSV → Markdown parser."""

import csv
from pathlib import Path

from .base_parser import BaseParser
from ..utils.markdown_formatter import MarkdownFormatter


class CSVParser(BaseParser):
    """Convert CSV files to a Markdown table."""

    MAX_ROWS = 500  # safety limit for very large CSVs

    def parse(self, file_path: Path) -> str:
        with file_path.open(newline="", encoding="utf-8", errors="replace") as fh:
            sniffer = csv.Sniffer()
            sample = fh.read(8192)
            fh.seek(0)

            try:
                dialect = sniffer.sniff(sample)
            except csv.Error:
                dialect = csv.excel

            reader = csv.reader(fh, dialect)
            rows = list(reader)

        if not rows:
            return "*Empty CSV file.*"

        headers = rows[0]
        body = rows[1:]

        table, note = MarkdownFormatter.truncate_table(
            headers, body, max_rows=self.MAX_ROWS
        )

        parts = [table]
        if note:
            parts.append(f"\n{note}")
        return "\n".join(parts)

    def _file_type_label(self) -> str:
        return "CSV"
