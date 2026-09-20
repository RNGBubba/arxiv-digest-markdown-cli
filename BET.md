BET: arXiv Digest CLI

Offer
-----
A local, original command-line formatter for legal arXiv API searches. It turns Atom results into readable Markdown with titles, authors, abstracts, categories, dates, and links to the source and PDF.

Price and 30-day path
----------------------
Suggested setup price: $25 for a research team that wants a tailored query/template. The first 30 days are a direct, human-led offer: publish the public repository, demonstrate the offline fixture workflow, and offer one custom digest template. No paid API, ads, or hosted service is required.

Human click
-----------
A buyer must choose to contact and pay; this artifact does not claim an automated payment rail.

Legal and safety
----------------
Uses the public arXiv API endpoint, preserves source links, sends a descriptive User-Agent, and documents rate-limit compliance. It does not scrape pages, impersonate arXiv, include secrets, or redistribute full papers.

Artifact
--------
The working artifact is this repository's arxiv_digest package, CLI, README, pyproject.toml, and pytest suite. `defusedxml` is used for safe Atom parsing.

Verification receipt
--------------------
DoneMeans receipt
-----------------
Ticket: `t_57c56b596be0`
Receipt: `receipts/t_57c56b596be0.json`
Code SHA: `a3cbfa65bcbd2f9ab778788aa7b4928ca03ae187`
Command: `uv run pytest -q`
Exit: `0`
Artifact: `artifacts/pytest.txt`
Receipt verification: passed with `uv run donemeans --root /home/vboxuser/projects/overnight-revenue/bets/arxiv-digest-cli receipt verify /home/vboxuser/projects/overnight-revenue/bets/arxiv-digest-cli/receipts/t_57c56b596be0.json`

GitHub
------
New public repository: https://github.com/RNGBubba/arxiv-digest-markdown-cli
