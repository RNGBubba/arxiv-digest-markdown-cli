"""Command-line interface for arXiv digest generation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

from .digest import format_digest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="arxiv-digest", description="Format an arXiv search as Markdown.")
    parser.add_argument("--query", help="arXiv search query, for example cat:cs.AI")
    parser.add_argument("--xml-file", type=Path, help="read a saved arXiv Atom response instead of making a request")
    parser.add_argument("--output", type=Path, default=Path("digest.md"), help="Markdown output path (default: digest.md)")
    parser.add_argument("--generated-at", help="deterministic timestamp for the digest")
    parser.add_argument("--max-results", type=int, default=10, help="number of results requested from arXiv")
    return parser


def _fetch(query: str, max_results: int) -> str:
    url = "https://export.arxiv.org/api/query?search_query=" + quote(query) + f"&max_results={max_results}"
    request = Request(url, headers={"User-Agent": "arxiv-digest/0.1 (mailto:opensource@example.invalid)"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.query:
        sys.stderr.write("--query is required\n")
        return 2
    try:
        xml = args.xml_file.read_text(encoding="utf-8") if args.xml_file else _fetch(args.query, args.max_results)
        args.output.write_text(format_digest(xml, args.query, args.generated_at), encoding="utf-8")
    except (OSError, ValueError, TimeoutError) as exc:
        sys.stderr.write(f"arxiv-digest: {exc}\n")
        return 1
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
