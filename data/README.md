# Guide catalogue

`guides.json` is the single maintained discovery inventory. Technical Markdown remains in its original path; do not duplicate or move it to change its topic.

## Adding a guide

1. Add the article under `docs/` and one record under `guides` in `guides.json`.
2. Supply `path`, a short `title`, a one-sentence `description`, one primary `topic`, `tags`, `aliases`, and `type` (`deployment`, `how-to`, `getting-started`, or `reference`). Tags and aliases are string arrays; use aliases for abbreviations and former app names.
3. Add `prerequisites` only when supported by the article. Missing prerequisites become an empty array, not an invented claim. Do not add verification dates from Git history; the current schema deliberately contains no verification claim.
4. Rebuild series records use `series: {"slug": "homelab-rebuild", "order": 1}` with unique positive orders.
5. Run `python -m unittest discover -s tests -p test_catalogue.py -v`, then the normal MkDocs build. Coverage validation fails if an article is missing from the catalogue, a path does not exist, metadata is invalid, or records duplicate a path.

Home, about, support, deals, tags, legacy category listings, the rebuild index and the Hoarder redirect are not guides. New non-guide pages require an explicit exclusion in `hooks/catalogue.py` and the coverage test; do not silently omit articles.

## Generated contracts

- `hooks/catalogue.py` populates `config.extra.tx_topics` (`slug`, `title`, `description`, `url`, `count`) and `config.extra.tx_guide_count` in `on_config`. It replaces All Guides navigation with the topic overview and every article in each topic, and generates the ordered Homelab Rebuild sidebar from series metadata.
- Checked-in `docs/guides/index.md` and `docs/topics/*.md` use `<!-- tx:catalogue -->` or `<!-- tx:catalogue topic=networking -->`. The legacy Docker listing uses `tag=docker`. HTML is generated at build time, with all article and topic links usable without JS.
- Filtering contract: `.tx-catalogue[data-catalogue]`, `#guide-query`, `#guide-topic`, `#guide-type`, `#guide-reset`, live `#guide-count`, hidden `#guide-empty`, and semantic `a.tx-guide-card` carrying `data-topic`, `data-type`, `data-search`. Presentation wrappers are `.tx-guide-filters`, `.tx-topic-links`, `.tx-guide-grid`, `.tx-guide-card__meta`. The site JS owns filtering and URL state.
- `page.meta.tx_guide` and `page.meta.tx_related` expose full normalized records with `url`, `topic_label` and `prerequisites`; related results are capped at three, exclude the current guide and rank shared tags within the same topic. `page.meta.tx_series` supplies `title`, `url`, `previous` and `next`; endpoint neighbors are `None`.
- `assets/guides.json` is written to the built site as a JSON array containing exactly `title`, `description`, `url`, `topic`, `topic_label`, `tags`, `aliases`, `type`. URLs are site-root-relative without a leading slash (`npm/`); templates should use Material's `url` filter and JS should resolve from the site base, not the current article directory.
- Short search metadata is set at build time; technical headings, anchors, code and article bodies are unchanged. Index/listing pages are excluded from the full-text search index so they do not swamp article results.

The hook uses the standard library and syntax compatible with Python 3.8. No additional MkDocs plugins or dependency upgrades are needed.
