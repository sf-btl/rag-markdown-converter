"""Unit tests for all parsers and the main converter."""

import csv
import json
import textwrap
from pathlib import Path

import pytest

from src.converter import UniversalMarkdownConverter
from src.parsers.csv_parser import CSVParser
from src.parsers.json_parser import JSONParser
from src.parsers.code_parser import CodeParser
from src.parsers.text_parser import TextParser
from src.parsers.html_parser import HTMLParser
from src.parsers.markdown_passthrough import MarkdownPassthrough
from src.utils.file_detector import FileDetector
from src.utils.markdown_formatter import MarkdownFormatter


# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture
def tmp_file(tmp_path):
    """Helper that writes content to a temp file and returns its Path."""
    def _write(name: str, content: str | bytes, mode: str = "w") -> Path:
        p = tmp_path / name
        if mode == "wb":
            p.write_bytes(content)
        else:
            p.write_text(content, encoding="utf-8")
        return p
    return _write


@pytest.fixture
def converter():
    return UniversalMarkdownConverter()


# ======================================================================
# FileDetector
# ======================================================================

class TestFileDetector:
    def test_detect_known_extension(self):
        assert FileDetector.detect(Path("report.pdf")) == "pdf"
        assert FileDetector.detect(Path("data.csv")) == "csv"
        assert FileDetector.detect(Path("app.py")) == "code"
        assert FileDetector.detect(Path("index.html")) == "html"
        assert FileDetector.detect(Path("notes.txt")) == "text"
        assert FileDetector.detect(Path("README.md")) == "markdown"
        assert FileDetector.detect(Path("doc.docx")) == "docx"

    def test_detect_unknown_extension(self):
        assert FileDetector.detect(Path("file.xyz")) is None

    def test_language_hint(self):
        assert FileDetector.language_hint(Path("main.py")) == "python"
        assert FileDetector.language_hint(Path("app.ts")) == "typescript"
        assert FileDetector.language_hint(Path("unknown.xyz")) == ""

    def test_supported_extensions_is_sorted(self):
        exts = FileDetector.supported_extensions()
        assert exts == sorted(exts)
        assert ".pdf" in exts
        assert ".py" in exts


# ======================================================================
# MarkdownFormatter
# ======================================================================

class TestMarkdownFormatter:
    def test_make_table(self):
        table = MarkdownFormatter.make_table(
            ["Name", "Age"],
            [["Alice", "30"], ["Bob", "25"]],
        )
        assert "| Name | Age |" in table
        assert "| --- | --- |" in table
        assert "| Alice | 30 |" in table

    def test_make_table_empty_headers(self):
        assert MarkdownFormatter.make_table([], []) == ""

    def test_wrap_code_block(self):
        block = MarkdownFormatter.wrap_code_block("print('hi')", "python")
        assert block.startswith("```python\n")
        assert block.endswith("\n```")

    def test_wrap_code_block_with_backticks_in_code(self):
        block = MarkdownFormatter.wrap_code_block("some ``` code", "")
        # Should use a longer fence
        assert block.startswith("````")

    def test_heading(self):
        assert MarkdownFormatter.heading("Title", 1) == "# Title"
        assert MarkdownFormatter.heading("Sub", 3) == "### Sub"

    def test_normalize_whitespace(self):
        text = "a\n\n\n\n\nb"
        assert MarkdownFormatter.normalize_whitespace(text) == "a\n\nb"

    def test_truncate_table(self):
        headers = ["X"]
        rows = [[str(i)] for i in range(10)]
        table, note = MarkdownFormatter.truncate_table(headers, rows, max_rows=5)
        assert note is not None
        assert "5 of 10" in note
        # Table should only contain 5 data rows
        lines = table.strip().splitlines()
        assert len(lines) == 7  # header + separator + 5 rows


# ======================================================================
# CSV Parser
# ======================================================================

class TestCSVParser:
    def test_parse_simple_csv(self, tmp_file):
        path = tmp_file("data.csv", "Name,Age\nAlice,30\nBob,25\n")
        md = CSVParser().parse(path)
        assert "| Name | Age |" in md
        assert "| Alice | 30 |" in md

    def test_parse_empty_csv(self, tmp_file):
        path = tmp_file("empty.csv", "")
        md = CSVParser().parse(path)
        assert "Empty" in md


# ======================================================================
# JSON Parser
# ======================================================================

class TestJSONParser:
    def test_parse_object(self, tmp_file):
        data = {"key": "value", "num": 42}
        path = tmp_file("data.json", json.dumps(data))
        md = JSONParser().parse(path)
        assert "```json" in md
        assert '"key": "value"' in md

    def test_parse_array_of_objects_as_table(self, tmp_file):
        data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
        path = tmp_file("list.json", json.dumps(data))
        md = JSONParser().parse(path)
        assert "| name | age |" in md

    def test_parse_invalid_json(self, tmp_file):
        path = tmp_file("bad.json", "{not json!!")
        md = JSONParser().parse(path)
        assert "Failed to parse" in md


# ======================================================================
# Code Parser
# ======================================================================

class TestCodeParser:
    def test_parse_python(self, tmp_file):
        code = 'def hello():\n    print("world")\n'
        path = tmp_file("hello.py", code)
        md = CodeParser().parse(path)
        assert "```python" in md
        assert "def hello():" in md

    def test_metadata_includes_language(self, tmp_file):
        path = tmp_file("app.ts", "const x = 1;")
        parser = CodeParser()
        content = parser.parse(path)
        md = parser.add_metadata(content, path)
        assert "Language: Typescript" in md


# ======================================================================
# Text Parser
# ======================================================================

class TestTextParser:
    def test_parse_text(self, tmp_file):
        path = tmp_file("notes.txt", "Hello World\nLine 2")
        md = TextParser().parse(path)
        assert "Hello World" in md

    def test_empty_text(self, tmp_file):
        path = tmp_file("empty.txt", "")
        md = TextParser().parse(path)
        assert "Empty" in md


# ======================================================================
# Markdown Passthrough
# ======================================================================

class TestMarkdownPassthrough:
    def test_passthrough(self, tmp_file):
        original = "# Title\n\nSome content\n"
        path = tmp_file("doc.md", original)
        md = MarkdownPassthrough().parse(path)
        assert "# Title" in md
        assert "Some content" in md


# ======================================================================
# HTML Parser
# ======================================================================

class TestHTMLParser:
    def test_parse_simple_html(self, tmp_file):
        html = "<html><body><h1>Hello</h1><p>World</p></body></html>"
        path = tmp_file("page.html", html)
        md = HTMLParser().parse(path)
        assert "Hello" in md
        assert "World" in md

    def test_parse_empty_html(self, tmp_file):
        path = tmp_file("empty.html", "<html><body></body></html>")
        md = HTMLParser().parse(path)
        # Should return something (possibly empty-content note)
        assert isinstance(md, str)


# ======================================================================
# Converter integration
# ======================================================================

class TestUniversalMarkdownConverter:
    def test_convert_txt(self, converter, tmp_file):
        path = tmp_file("hello.txt", "Hello from text file")
        md = converter.convert(path)
        assert "Hello from text file" in md
        assert "*Source: hello.txt*" in md

    def test_convert_csv(self, converter, tmp_file):
        path = tmp_file("data.csv", "a,b\n1,2\n")
        md = converter.convert(path)
        assert "| a | b |" in md

    def test_convert_unsupported(self, converter, tmp_file):
        path = tmp_file("data.xyz", "stuff")
        with pytest.raises(ValueError, match="Unsupported"):
            converter.convert(path)

    def test_convert_missing_file(self, converter):
        with pytest.raises(FileNotFoundError):
            converter.convert("/nonexistent/file.txt")

    def test_convert_with_output(self, converter, tmp_file, tmp_path):
        path = tmp_file("notes.txt", "Some notes")
        out = tmp_path / "output" / "notes.md"
        md = converter.convert(path, out)
        assert out.exists()
        assert out.read_text(encoding="utf-8") == md

    def test_batch_convert(self, converter, tmp_path):
        src = tmp_path / "input"
        src.mkdir()
        (src / "a.txt").write_text("File A", encoding="utf-8")
        (src / "b.csv").write_text("x,y\n1,2\n", encoding="utf-8")
        (src / "skip.xyz").write_text("ignored", encoding="utf-8")

        out = tmp_path / "output"
        results = converter.batch_convert(src, out)

        assert len(results) == 2  # .xyz skipped
        assert all(isinstance(v, str) for v in results.values())
        assert (out / "a.md").exists()
        assert (out / "b.md").exists()

    def test_supported_formats(self, converter):
        fmts = converter.supported_formats()
        assert ".pdf" in fmts
        assert ".py" in fmts
