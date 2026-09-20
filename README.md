# arXiv Digest CLI

`arxiv-digest` turns a search from the public arXiv API into readable Markdown. It is a small, original formatter: it does not copy paper text beyond the abstract returned by the API, and it leaves source and PDF links intact.

## Usage

Fetch a live result set:

```bash
arxiv-digest --query 'cat:cs.AI AND ti:agents' --output digest.md
```

For reproducible offline runs, provide a saved Atom response:

```bash
arxiv-digest --query 'cat:cs.AI' --xml-file response.xml --generated-at 2024-01-03T00:00:00Z
```

The CLI uses `https://export.arxiv.org/api/query`, sends a descriptive User-Agent, and applies a 30-second timeout. Respect arXiv's API terms and rate limits when fetching data.

## Development

```bash
uv sync --group dev
uv run pytest -q
```

## Offer

A useful paid extension is a tailored daily digest template for a research team: $25 for setup, with no hosted service or recurring spend required. The buyer supplies their query and schedule; this repository remains a local command-line tool.
