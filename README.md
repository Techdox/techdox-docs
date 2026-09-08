# Techdox Docs

Practical self-hosting and homelab guides at **https://docs.techdox.nz**. Built with MkDocs Material and a custom Techdox theme; Markdown remains the source of technical instructions.

## Local development

Use Python 3.11 and Node 22 for the validation toolchain. The site hooks also support the existing Cloudflare Python 3.8 build. System Cairo libraries are required by the existing social-card plugin.

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
npm ci
npx playwright install --with-deps chromium
mkdocs serve
```

For a production-style build:

```sh
python -m unittest discover -s tests -p 'test_*.py' -v
npm test
npm run test:interactions
mkdocs build --strict
python tests/check_links.py
python -m http.server 8766 --bind 127.0.0.1 --directory site
# In another terminal:
npm run test:browser
```

Set `BASE_URL` to test an immutable Cloudflare preview instead of localhost. Browser evidence is written to `artifacts/browser/` (gitignored). `npm run test:interactions` uses an isolated test fixture, not fabricated production guide data.

## Adding or updating a guide

1. Add or edit its Markdown under `docs/`. Keep existing paths and heading anchors stable: YouTube descriptions, bookmarks and external sites link to them.
2. Add one entry to **`data/guides.json`** with `path`, concise `title`, useful `description`, `topic`, `tags`, `aliases` and `type`. Optional prerequisites must accurately describe the guide. Rebuild-series entries also carry a unique `series.order`.
3. The catalogue hook validates full coverage. Every real guide must have exactly one entry; topic navigation, home counts, directory cards, tags, related guides and the quick-search index are generated from this source.
4. Run tests and a strict build before opening a feature-branch PR.

Topics: `networking`, `security`, `storage`, `monitoring`, `media`, `productivity`, `platform`. Guide types: `deployment`, `how-to`, `getting-started`, `reference`.

Aliases support old product names and abbreviations, for example `npm` and `hoarder`. They affect directory filtering and the compact matching-guide section of search; Material's full-text search remains available below it.

Do **not** infer technical verification from a Git edit date. This theme does not manufacture last-tested dates or claim that existing deployments have been revalidated. Guide instructions, particularly security-sensitive examples, need separate checks against official documentation and real deployments.

## Navigation and theme

- `hooks/catalogue.py`: validation, navigation, catalogue rendering and public `assets/guides.json` generation.
- `docs/guides/` and `docs/topics/`: marker-driven real listing pages; links still work with JavaScript disabled.
- `overrides/`: homepage, header, guide context, mobile navigation, theme controls and related/series links.
- `docs/stylesheets/extra.css`: shared semantic light/dark tokens and responsive components, aligned with techdox.nz.
- `docs/javascripts/docs.js`: progressive directory filters, URL state, keyboard search and exact-name/alias quick matches. Query values render as text, never HTML.
- `docs/fonts/`: locally hosted Hanken Grotesk and JetBrains Mono, with their OFL licences.

The catalogue remains browsable if JavaScript fails. Filter controls enable only after their enhancement loads. Search quick matches degrade to Material full-text search if the additional index cannot be retrieved.

## Checks and release

`.github/workflows/quality.yml` runs build, metadata/markup tests, search/filter interactions, browser accessibility/responsive checks and the legacy route/anchor baseline. It does **not** deploy. The existing **native Cloudflare Pages Git integration** owns deployments.

`tests/legacy-routes.json` records pre-overhaul public routes and non-generated anchors. Do not remove entries simply to make tests pass. Add tested redirects or preserve compatibility anchors for intentional changes.

Use a feature branch and review its immutable Cloudflare preview. Production commits are owner hardware-signed; do not merge or bypass that gate from automation. After release, verify the actual live domain and retain the previous successful Cloudflare deployment for rollback.

## Community

- [Techdox](https://techdox.nz)
- [YouTube](https://youtube.com/@techdox)
- [Discord](https://discord.com/invite/8mX2KRxDw8)
- [Report a documentation issue](https://github.com/Techdox/techdox-docs/issues)
- [Support the guides](https://docs.techdox.nz/support/)

See [LICENSE](LICENSE) for the repository licence; bundled fonts have their own licences.
