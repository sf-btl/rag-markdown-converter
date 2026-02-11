"""Detect file types and map them to the appropriate parser key."""

from pathlib import Path
from typing import Optional

# Mapping from file extension (lower-case, with dot) → parser registry key.
EXTENSION_MAP: dict[str, str] = {
    # Documents
    ".pdf": "pdf",
    ".docx": "docx",
    # Web
    ".html": "html",
    ".htm": "html",
    # Data
    ".csv": "csv",
    ".json": "json",
    ".jsonl": "json",
    # Text / Markdown
    ".txt": "text",
    ".md": "markdown",
    ".markdown": "markdown",
    ".rst": "text",
    # Code — grouped under the "code" parser
    ".py": "code",
    ".java": "code",
    ".js": "code",
    ".ts": "code",
    ".tsx": "code",
    ".jsx": "code",
    ".cpp": "code",
    ".c": "code",
    ".h": "code",
    ".hpp": "code",
    ".cs": "code",
    ".go": "code",
    ".rs": "code",
    ".rb": "code",
    ".php": "code",
    ".swift": "code",
    ".kt": "code",
    ".scala": "code",
    ".r": "code",
    ".sql": "code",
    ".sh": "code",
    ".bash": "code",
    ".zsh": "code",
    ".ps1": "code",
    ".yaml": "code",
    ".yml": "code",
    ".toml": "code",
    ".ini": "code",
    ".cfg": "code",
    ".xml": "code",
    ".css": "code",
    ".scss": "code",
    ".less": "code",
    ".lua": "code",
    ".pl": "code",
    ".ex": "code",
    ".exs": "code",
    ".erl": "code",
    ".hs": "code",
    ".dart": "code",
    ".vue": "code",
    ".svelte": "code",
}

# Language labels for syntax-highlighted code fences.
LANGUAGE_MAP: dict[str, str] = {
    ".py": "python",
    ".java": "java",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".jsx": "jsx",
    ".cpp": "cpp",
    ".c": "c",
    ".h": "c",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin",
    ".scala": "scala",
    ".r": "r",
    ".sql": "sql",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "zsh",
    ".ps1": "powershell",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".ini": "ini",
    ".cfg": "ini",
    ".xml": "xml",
    ".css": "css",
    ".scss": "scss",
    ".less": "less",
    ".lua": "lua",
    ".pl": "perl",
    ".ex": "elixir",
    ".exs": "elixir",
    ".erl": "erlang",
    ".hs": "haskell",
    ".dart": "dart",
    ".vue": "vue",
    ".svelte": "svelte",
}


class FileDetector:
    """Detect file types by extension and return parser keys / language hints."""

    @staticmethod
    def detect(file_path: Path) -> Optional[str]:
        """Return the parser registry key for *file_path*, or ``None``."""
        return EXTENSION_MAP.get(file_path.suffix.lower())

    @staticmethod
    def language_hint(file_path: Path) -> str:
        """Return the Markdown code-fence language identifier."""
        return LANGUAGE_MAP.get(file_path.suffix.lower(), "")

    @staticmethod
    def supported_extensions() -> list[str]:
        """Return a sorted list of all supported file extensions."""
        return sorted(EXTENSION_MAP.keys())
