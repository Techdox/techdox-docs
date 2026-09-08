# Techdox template contracts

- `home.html` uses `config.extra.tx_topics` (`slug`, `title`, `description`, `url`, `count`) and `tx_guide_count`. No hardcoded catalogue counts.
- `page.meta.template: home.html`, with `hide: [navigation, toc]`, selects the discovery homepage.
- Header and home use `button[data-open-search]`. Shared `docs.js` opens native Material search. Indexing, native modal, results and Escape handling remain Material's responsibility.
- Mobile navigation is a native `<details class="tx-mobile-menu">`; its links work without JavaScript. Shared JS may close it on navigation/Escape/outside click for polish.
- Theme retains Material's `data-md-component="palette"`, `__palette_*` radios and next-scheme labels. Radios are visually hidden, **not** display:none: Tab and arrow keys can change the theme without new JS.
- Guide metadata: `page.meta.tx_guide` has `title`, `description`, `topic`, `topic_label`, `type`, optional `prerequisites` (text/list). Topic URLs are resolved against the generated topics, falling back to the guide directory. Existing article headings/content are untouched.
- Related guides: `page.meta.tx_related`, list of `title`, `url`, optional `description`, rendered with a maximum of three links.
- Directory: `.tx-catalogue`, `.tx-catalogue-controls` / `.tx-filters` / `.tx-filter-bar`, `.tx-guide-grid` / `.tx-catalogue-grid` / `.tx-guides`, `.tx-guide-card`, `.tx-guide-meta` / `.tx-card-meta` / `.tx-meta`, the agreed `guide-*` IDs. `[hidden]` cards override flex/grid display.
- Metadata search matches: `.tx-quick-matches`, `.tx-quick-heading`, `.tx-quick-link`, `.tx-quick-title`, `.tx-quick-meta`, `.tx-quick-description`.

## Targeted template test

Run from repository root. This test failed on the previous template (missing generated topic URL/count), then passed with the home implementation. It does not need MkDocs installed. Fixture data is synthetic test input, not published catalogue data.

```sh
python -c "from pathlib import Path; from jinja2 import Environment,DictLoader; env=Environment(loader=DictLoader({'main.html':'{% block content %}{% endblock %}'}),autoescape=True); env.filters['url']=lambda v:v; template=env.from_string(Path('overrides/home.html').read_text()); html=template.render(config={'extra':{'tx_topics':[{'slug':'networking','title':'Networking & Remote Access','description':'DNS and VPNs','url':'topics/networking/','count':7}], 'tx_guide_count':7}}); assert 'topics/networking/' in html and '7 guides' in html; assert 'Networking &amp; Remote Access' in html; assert 'data-open-search' in html; singular=template.render(config={'extra':{'tx_topics':[{'title':'One','description':'Only one','url':'topics/one/','count':1}]}}); assert '1 guide<' in singular and '1 guides' not in singular; print('PASS: topic URL/count/singular/escaping/search trigger')"
```

Full MkDocs build, keyboard checks and responsive browser/contrast QA are integration gates, not replaced by this targeted test. Local fonts come from the main site's `/fonts/hanken-latin.woff2` and `/fonts/jetbrains-latin.woff2` endpoints.
