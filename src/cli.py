"""Command-line interface for the Universal Markdown Converter."""

import argparse
import logging
import sys
from pathlib import Path

from .converter import UniversalMarkdownConverter


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rag-md-converter",
        description="Universal File-to-Markdown Converter for RAG Preprocessing",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # -- convert ----------------------------------------------------------
    p_convert = sub.add_parser("convert", help="Convert a single file to Markdown")
    p_convert.add_argument("input", help="Path to the source file")
    p_convert.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file path (default: print to stdout)",
    )

    # -- batch-convert ----------------------------------------------------
    p_batch = sub.add_parser(
        "batch-convert", help="Convert all supported files in a directory"
    )
    p_batch.add_argument("input_dir", help="Source directory")
    p_batch.add_argument(
        "-o", "--output-dir", required=True, help="Destination directory"
    )
    p_batch.add_argument(
        "--no-recursive",
        action="store_true",
        help="Do not recurse into sub-directories",
    )

    # -- list-formats -----------------------------------------------------
    sub.add_parser("list-formats", help="Show all supported file extensions")

    # Global flags
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    converter = UniversalMarkdownConverter()

    if args.command == "convert":
        try:
            md = converter.convert(args.input, args.output)
        except (FileNotFoundError, ValueError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        if args.output is None:
            print(md)
        else:
            print(f"Converted → {args.output}")
        return 0

    if args.command == "batch-convert":
        results = converter.batch_convert(
            args.input_dir,
            args.output_dir,
            recursive=not args.no_recursive,
        )
        ok = sum(1 for v in results.values() if isinstance(v, str))
        fail = sum(1 for v in results.values() if isinstance(v, Exception))
        print(f"Done: {ok} converted, {fail} failed")
        if fail:
            for path, exc in results.items():
                if isinstance(exc, Exception):
                    print(f"  FAIL {path}: {exc}", file=sys.stderr)
        return 1 if fail else 0

    if args.command == "list-formats":
        exts = converter.supported_formats()
        print("Supported file extensions:")
        for ext in exts:
            print(f"  {ext}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
