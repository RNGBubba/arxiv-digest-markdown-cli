"""Small, dependency-free arXiv Atom feed formatter."""

from .digest import Paper, format_digest, parse_feed

__all__ = ["Paper", "format_digest", "parse_feed"]
