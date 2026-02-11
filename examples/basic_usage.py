"""Basic usage example: convert a single file to Markdown."""

from src import UniversalMarkdownConverter

converter = UniversalMarkdownConverter()

# Convert and print to stdout
md = converter.convert("path/to/document.pdf")
print(md)

# Convert and save to disk
converter.convert("path/to/document.pdf", output_path="output/document.md")
