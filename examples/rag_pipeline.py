"""Example: integrate the converter into a simple RAG preprocessing pipeline."""

import re
from pathlib import Path

from src import UniversalMarkdownConverter


def chunk_markdown(text: str, max_chars: int = 1000) -> list[str]:
    """Split Markdown into chunks on section boundaries.

    Splits on ``## `` headings first, then falls back to paragraph breaks.
    Each chunk is at most *max_chars* characters.
    """
    sections = re.split(r"(?=^## )", text, flags=re.MULTILINE)
    chunks: list[str] = []

    for section in sections:
        section = section.strip()
        if not section:
            continue
        if len(section) <= max_chars:
            chunks.append(section)
        else:
            # Split long sections by paragraph
            paragraphs = section.split("\n\n")
            current = ""
            for para in paragraphs:
                if current and len(current) + len(para) + 2 > max_chars:
                    chunks.append(current.strip())
                    current = para
                else:
                    current = f"{current}\n\n{para}" if current else para
            if current.strip():
                chunks.append(current.strip())

    return chunks


def main() -> None:
    converter = UniversalMarkdownConverter()

    # 1. Convert source documents to Markdown
    source_dir = Path("./documents")
    if not source_dir.exists():
        print("Create a ./documents directory with files to convert.")
        return

    results = converter.batch_convert(source_dir, "./md_output", recursive=True)
    print(f"Converted {sum(1 for v in results.values() if isinstance(v, str))} files")

    # 2. Chunk each Markdown file for embedding
    all_chunks: list[dict] = []
    for md_path in Path("./md_output").rglob("*.md"):
        text = md_path.read_text(encoding="utf-8")
        chunks = chunk_markdown(text, max_chars=800)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": md_path.name,
                "chunk_index": i,
                "text": chunk,
            })

    print(f"Generated {len(all_chunks)} chunks ready for embedding")

    # 3. At this point you'd send all_chunks to your embedding model
    #    and store in a vector database.
    for chunk in all_chunks[:3]:
        print(f"\n--- {chunk['source']} chunk {chunk['chunk_index']} ---")
        print(chunk["text"][:200] + "...")


if __name__ == "__main__":
    main()
