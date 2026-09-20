from pathlib import Path

from arxiv_digest_cli import format_digest, parse_feed
from arxiv_digest_cli.cli import main


FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <title>arXiv Query: cat:cs.AI</title>
  <entry>
    <id>http://arxiv.org/abs/2401.00001</id>
    <title>  A Useful \n    Paper  </title>
    <summary>  We study useful things.\n</summary>
    <published>2024-01-02T03:04:05Z</published>
    <author><name>Ada Lovelace</name></author>
    <author><name>Grace Hopper</name></author>
    <category term="cs.AI" />
    <category term="cs.LG" />
    <link title="pdf" href="http://arxiv.org/pdf/2401.00001" />
  </entry>
</feed>"""


def test_parse_feed_normalizes_entry_fields():
    entries = parse_feed(FEED)

    assert len(entries) == 1
    assert entries[0].title == "A Useful Paper"
    assert entries[0].authors == ("Ada Lovelace", "Grace Hopper")
    assert entries[0].abstract == "We study useful things."
    assert entries[0].categories == ("cs.AI", "cs.LG")
    assert entries[0].abs_url == "http://arxiv.org/abs/2401.00001"
    assert entries[0].pdf_url == "http://arxiv.org/pdf/2401.00001"


def test_format_digest_is_readable_markdown():
    digest = format_digest(FEED, query="cat:cs.AI", generated_at="2024-01-03T00:00:00Z")

    assert digest.startswith("# arXiv Digest: cat:cs.AI\n")
    assert "Generated: 2024-01-03T00:00:00Z" in digest
    assert "## 1. A Useful Paper" in digest
    assert "**Authors:** Ada Lovelace; Grace Hopper" in digest
    assert "[Abstract]" in digest
    assert "[PDF]" in digest


def test_cli_formats_local_feed_without_network(tmp_path: Path):
    source = tmp_path / "feed.xml"
    destination = tmp_path / "digest.md"
    source.write_text(FEED, encoding="utf-8")

    assert main(["--xml-file", str(source), "--query", "cat:cs.AI", "--generated-at", "2024-01-03T00:00:00Z", "--output", str(destination)]) == 0
    assert destination.read_text(encoding="utf-8").count("## 1. A Useful Paper") == 1


def test_cli_requires_query_or_xml_file(capsys):
    assert main([]) == 2
    assert "--query is required" in capsys.readouterr().err
