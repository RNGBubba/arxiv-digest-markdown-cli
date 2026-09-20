"""Parse arXiv's Atom response and render a linked Markdown digest."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape
from defusedxml import ElementTree


ATOM = "http://www.w3.org/2005/Atom"
ARXIV = "http://arxiv.org/schemas/atom"


@dataclass(frozen=True)
class Paper:
    title: str
    authors: tuple[str, ...]
    abstract: str
    published: str
    categories: tuple[str, ...]
    abs_url: str
    pdf_url: str | None


def _text(element: ElementTree.Element | None) -> str:
    if element is None or element.text is None:
        return ""
    return " ".join(element.text.split())


def parse_feed(xml: str) -> list[Paper]:
    """Return normalized papers from an arXiv Atom response."""
    root = ElementTree.fromstring(xml)
    papers: list[Paper] = []
    for entry in root.findall(f"{{{ATOM}}}entry"):
        links = entry.findall(f"{{{ATOM}}}link")
        abs_url = _text(entry.find(f"{{{ATOM}}}id"))
        pdf_url = next(
            (link.attrib.get("href") for link in links if link.attrib.get("title") == "pdf"),
            None,
        )
        papers.append(
            Paper(
                title=_text(entry.find(f"{{{ATOM}}}title")),
                authors=tuple(
                    _text(author.find(f"{{{ATOM}}}name"))
                    for author in entry.findall(f"{{{ATOM}}}author")
                ),
                abstract=_text(entry.find(f"{{{ATOM}}}summary")),
                published=_text(entry.find(f"{{{ATOM}}}published")),
                categories=tuple(
                    category.attrib["term"]
                    for category in entry.findall(f"{{{ATOM}}}category")
                    if "term" in category.attrib
                ),
                abs_url=abs_url,
                pdf_url=pdf_url,
            )
        )
    return papers


def format_digest(xml: str, query: str, generated_at: str | None = None) -> str:
    """Render a feed as deterministic Markdown suitable for a daily digest."""
    if not query.strip():
        raise ValueError("query must not be empty")
    if generated_at is None:
        generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    papers = parse_feed(xml)
    lines = [
        f"# arXiv Digest: {escape(query.strip())}",
        "",
        f"Generated: {generated_at}",
        f"Papers: {len(papers)}",
        "",
    ]
    if not papers:
        lines.append("No papers found.")
    for index, paper in enumerate(papers, 1):
        lines.extend(
            [
                f"## {index}. {escape(paper.title)}",
                "",
                f"**Authors:** {escape('; '.join(paper.authors) or 'Unknown')}",
                f"**Published:** {escape(paper.published or 'Unknown')}",
                f"**Categories:** {escape(', '.join(paper.categories) or 'None')}",
                "",
                escape(paper.abstract),
                "",
                f"[Abstract]({paper.abs_url})",
            ]
        )
        if paper.pdf_url:
            lines.append(f"[PDF]({paper.pdf_url})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
