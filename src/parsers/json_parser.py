"""JSON → Markdown parser."""

import json
from pathlib import Path

from .base_parser import BaseParser
from ..utils.markdown_formatter import MarkdownFormatter


class JSONParser(BaseParser):
    """Convert JSON / JSONL files to readable Markdown.

    - Objects and arrays are rendered as fenced JSON code blocks.
    - Flat arrays-of-objects are also rendered as a Markdown table when
      all items share the same keys.
    """

    MAX_TABLE_ROWS = 200

    def parse(self, file_path: Path) -> str:
        text = file_path.read_text(encoding="utf-8", errors="replace").strip()

        # Try JSONL (one JSON object per line)
        if "\n" in text and not text.startswith(("[", "{")):
            return self._parse_jsonl(text)

        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            return f"*Failed to parse JSON: {exc}*"

        return self._render(data)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _parse_jsonl(self, text: str) -> str:
        records: list[dict] = []
        for i, line in enumerate(text.splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                return MarkdownFormatter.wrap_code_block(text, "json")
        return self._render(records)

    def _render(self, data: object) -> str:
        # Try to render flat list-of-dicts as a table
        if isinstance(data, list) and data and all(isinstance(r, dict) for r in data):
            keys = list(data[0].keys())
            if all(set(r.keys()) == set(keys) for r in data):
                rows = [[str(r.get(k, "")) for k in keys] for r in data]
                table, note = MarkdownFormatter.truncate_table(
                    keys, rows, max_rows=self.MAX_TABLE_ROWS
                )
                parts = [table]
                if note:
                    parts.append(f"\n{note}")
                return "\n".join(parts)

        # Fall back to formatted JSON code block
        pretty = json.dumps(data, indent=2, ensure_ascii=False, default=str)
        return MarkdownFormatter.wrap_code_block(pretty, "json")

    def _file_type_label(self) -> str:
        return "JSON"
