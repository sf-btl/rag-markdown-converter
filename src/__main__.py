"""Allow running the package as ``python -m src``."""

from .cli import main

raise SystemExit(main())
