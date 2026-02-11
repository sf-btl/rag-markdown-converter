"""Batch conversion example: convert all files in a directory."""

from src import UniversalMarkdownConverter

converter = UniversalMarkdownConverter()

results = converter.batch_convert(
    input_dir="./documents",
    output_dir="./markdown_output",
    recursive=True,
)

# Report results
for source, outcome in results.items():
    if isinstance(outcome, Exception):
        print(f"FAIL  {source}: {outcome}")
    else:
        print(f"OK    {source} -> {outcome}")
