# Universal File-to-Markdown Converter for RAG

Convert any text-based file into well-structured Markdown optimized for Retrieval-Augmented Generation (RAG) preprocessing.

## Supported Formats

| Format | Extensions |
|--------|-----------|
| PDF | `.pdf` |
| Word | `.docx` |
| HTML | `.html`, `.htm` |
| CSV | `.csv` |
| JSON | `.json`, `.jsonl` |
| Plain text | `.txt`, `.rst` |
| Markdown | `.md`, `.markdown` |
| Code | `.py`, `.js`, `.ts`, `.java`, `.cpp`, `.go`, `.rs`, `.rb`, and 30+ more |

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Python API

```python
from src import UniversalMarkdownConverter

converter = UniversalMarkdownConverter()

# Single file
md = converter.convert("report.pdf")
print(md)

# Save to file
converter.convert("report.pdf", output_path="report.md")

# Batch convert a directory
results = converter.batch_convert("./docs", "./output", recursive=True)
```

### CLI

```bash
# Single file
python -m src convert document.pdf -o output.md

# Batch conversion
python -m src batch-convert ./documents -o ./markdown_output

# Non-recursive batch
python -m src batch-convert ./documents -o ./output --no-recursive

# List supported formats
python -m src list-formats

# Verbose mode
python -m src convert file.pdf -v
```

## Output Format

Every converted file includes a metadata header for RAG ingestion:

```markdown
# Document Title

*Source: original_file.pdf*
*Type: PDF*
*Converted: 2025-01-15 10:30 UTC*
*Pages: 12*

---

## Page 1

Content with preserved structure...
```

## Architecture

```
src/
├── converter.py           # Main UniversalMarkdownConverter class
├── cli.py                 # Command-line interface
├── parsers/
│   ├── base_parser.py     # Abstract base class
│   ├── pdf_parser.py      # PDF → Markdown
│   ├── docx_parser.py     # DOCX → Markdown
│   ├── html_parser.py     # HTML → Markdown
│   ├── csv_parser.py      # CSV → Markdown table
│   ├── json_parser.py     # JSON → Markdown
│   ├── code_parser.py     # Code → fenced block
│   ├── text_parser.py     # Plain text passthrough
│   └── markdown_passthrough.py
└── utils/
    ├── file_detector.py   # Extension-based type detection
    └── markdown_formatter.py
```

### Adding a New Parser

1. Create a class inheriting from `BaseParser` in `src/parsers/`
2. Implement `parse(file_path) -> str` and `_file_type_label() -> str`
3. Register the extension in `src/utils/file_detector.py`
4. Add the parser to `_register_parsers()` in `src/converter.py`

## Testing

```bash
pip install pytest
pytest tests/ -v
```

## Examples

See the `examples/` directory:

- **basic_usage.py** — convert a single file
- **batch_conversion.py** — convert an entire directory
- **rag_pipeline.py** — chunk Markdown for embedding in a RAG pipeline
