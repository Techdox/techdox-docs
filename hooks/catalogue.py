"""Validated catalogue and MkDocs hooks. Python 3.8+, no extra dependencies."""
from html import escape
import posixpath
import json
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'index.md', 'about.md', 'tags.md', 'support.md', 'racknerd.md',
            'docker-containers.md', 'networking-overview.md', 'logging-overview.md',
            'general-guides.md', 'homelab-rebuild/index.md', 'hoarder.md'}
TOPIC_SLUGS = {'networking', 'security', 'storage', 'monitoring', 'media', 'productivity', 'platform'}
TYPES = {'deployment': 'Deployment', 'how-to': 'How-to',
         'getting-started': 'Getting started', 'reference': 'Reference'}
RECORDS = []
TOPICS = []


def validate(data, docs_dir):
    """Reject incomplete inventory or unsafe metadata before rendering anything."""
    topics = data.get('topics', [])
    if len(topics) != len(TOPIC_SLUGS) or {t['slug'] for t in topics} != TOPIC_SLUGS:
        raise ValueError('Catalogue must define all seven unique topics')
    labels = {t['slug']: t['title'] for t in topics}
    for topic in topics:
        if any(not isinstance(topic.get(k), str) or not topic[k].strip()
               for k in ('slug', 'title', 'description')):
            raise ValueError('Topic fields must be non-empty strings')
    records, paths, orders = [], set(), set()
    for item in data['guides']:
        allowed = {'path', 'title', 'description', 'topic', 'tags', 'aliases', 'type', 'series', 'prerequisites'}
        if set(item) - allowed:
            raise ValueError('Unsupported metadata fields (verification requires real evidence)')
        for key in ('path', 'title', 'description', 'topic', 'type'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError('Missing or empty guide field: ' + key)
        path = item['path']
        if not re.fullmatch(r'[a-z0-9/-]+\.md', path) or PurePosixPath(path).is_absolute() or '..' in path:
            raise ValueError('Invalid guide path: ' + path)
        if path in paths or not (Path(docs_dir) / path).is_file():
            raise ValueError('Duplicate or missing guide: ' + path)
        if item['topic'] not in labels or item['type'] not in TYPES:
            raise ValueError('Unknown guide topic or type: ' + path)
        for key in ('tags', 'aliases', 'prerequisites'):
            values = item.get(key, [] if key == 'prerequisites' else None)
            if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
                raise ValueError('Expected a string list: ' + key)
        if 'series' in item:
            series = item['series']
            if (not isinstance(series, dict) or series.get('slug') != 'homelab-rebuild'
                    or type(series.get('order')) is not int or series['order'] < 1):
                raise ValueError('Invalid series metadata')
            order = (series['slug'], series['order'])
            if order in orders:
                raise ValueError('Duplicate series order')
            orders.add(order)
        paths.add(path)
        record = dict(item, url=path[:-3] + '/', topic_label=labels[item['topic']])
        record.setdefault('prerequisites', [])
        records.append(record)
    expected = {p.relative_to(docs_dir).as_posix() for p in Path(docs_dir).rglob('*.md')
                if p.relative_to(docs_dir).as_posix() not in EXCLUDED
                and p.relative_to(docs_dir).parts[0] not in ('guides', 'topics')}
    if paths != expected:
        raise ValueError('Catalogue coverage mismatch; missing: {}; non-guides: {}'.format(
            sorted(expected - paths), sorted(paths - expected)))
    return sorted(records, key=lambda g: (g['title'].casefold(), g['path']))


def on_config(config):
    """Populate shared template data and topic navigation from the one inventory."""
    global RECORDS, TOPICS
    data = json.loads((ROOT / 'data/guides.json').read_text(encoding='utf-8'))
    RECORDS = validate(data, Path(config['docs_dir']))
    TOPICS = [dict(t, url='topics/' + t['slug'] + '/',
                   count=sum(g['topic'] == t['slug'] for g in RECORDS)) for t in data['topics']]
    config['extra']['tx_topics'] = TOPICS
    config['extra']['tx_guide_count'] = len(RECORDS)
    for item in config.get('nav', []):
        if 'All Guides' in item:
            item['All Guides'] = [{'Browse all guides': 'guides/index.md'}] + [
                {t['title']: [{'Overview': 'topics/' + t['slug'] + '.md'}] + [
                    {g['title']: g['path']} for g in RECORDS if g['topic'] == t['slug']]}
                for t in TOPICS]
        if 'Homelab Rebuild' in item:
            members = sorted((g for g in RECORDS if g.get('series', {}).get('slug') == 'homelab-rebuild'),
                             key=lambda g: g['series']['order'])
            item['Homelab Rebuild'] = [{'Overview': 'homelab-rebuild/index.md'}] + [
                {g['title']: g['path']} for g in members]
    return config


def relative_url(target, page_url):
    """Link within the site, also when deployed below a path prefix."""
    base = page_url if page_url.endswith('/') else posixpath.dirname(page_url)
    result = posixpath.relpath(target.rstrip('/'), base or '.')
    return result + ('/' if target.endswith('/') else '')


def render_catalogue(page, topic=None, tag=None):
    records = [g for g in RECORDS if (not topic or g['topic'] == topic)
               and (not tag or tag in g['tags'])]
    def link(url):
        return escape(relative_url(url, page.url), quote=True)
    parts = ['<div class="tx-catalogue" data-catalogue>']
    # Enable controls only when the progressive enhancement has initialised.
    parts.append('<div class="tx-guide-filters">'
                 '<label for="guide-query">Find a guide, app or task</label>'
                 '<input id="guide-query" type="search" placeholder="Search guides" disabled>'
                 '<label for="guide-topic">Topic</label><select id="guide-topic" disabled>'
                 '<option value="">All topics</option>')
    for t in TOPICS:
        if not topic or t['slug'] == topic:
            parts.append('<option value="{}">{}</option>'.format(t['slug'], escape(t['title'])))
    parts.append('</select><label for="guide-type">Guide type</label>'
                 '<select id="guide-type" disabled><option value="">All types</option>')
    for value, label in TYPES.items():
        parts.append('<option value="{}">{}</option>'.format(value, label))
    parts.append('</select><button id="guide-reset" type="button" disabled>Reset filters</button></div>')
    parts.append('<noscript><p>All guides are listed below. Use the topic links to browse without JavaScript.</p></noscript>')
    parts.append('<nav class="tx-topic-links" aria-label="Browse guide topics">')
    for t in TOPICS:
        parts.append('<a href="{}">{}</a>'.format(link(t['url']), escape(t['title'])))
    parts.append('</nav><p id="guide-count" role="status" aria-live="polite" aria-atomic="true">{} guides</p>'.format(len(records)))
    parts.append('<p id="guide-empty" hidden>No guides match. Try another term or reset the filters.</p>')
    parts.append('<div class="tx-guide-grid">')
    for g in records:
        search = ' '.join([g['title'], g['description'], g['topic_label']] + g['tags'] + g['aliases'])
        parts.append('<a class="tx-guide-card" href="{}" data-topic="{}" data-type="{}" data-search="{}">'
                     '<span class="tx-guide-card__meta">{} · {}</span><h2>{}</h2><p>{}</p></a>'.format(
                         link(g['url']), g['topic'], g['type'], escape(search, quote=True),
                         escape(g['topic_label']), TYPES[g['type']], escape(g['title']), escape(g['description'])))
    parts.append('</div></div>')
    return '\n'.join(parts)


def on_page_markdown(markdown, page, config, files):
    """Render only explicit directory markers; never rewrite technical article bodies."""
    guide = next((g for g in RECORDS if g['path'] == page.file.src_uri), None)
    if guide:
        # Metadata improves search titles without touching headings or their anchors.
        page.meta['title'] = guide['title']
        page.meta['description'] = guide['description']
        page.meta['tags'] = guide['tags']
    if page.file.src_uri in EXCLUDED or page.file.src_uri.startswith(('guides/', 'topics/')):
        page.meta.setdefault('search', {})['exclude'] = True
    pattern = r'<!-- tx:catalogue(?: topic=([a-z-]+))?(?: tag=([a-z-]+))? -->'
    def replace(match):
        topic, tag = match.groups()
        if topic and topic not in TOPIC_SLUGS:
            raise ValueError('Unknown catalogue topic: ' + topic)
        return render_catalogue(page, topic, tag)
    return re.sub(pattern, replace, markdown)


# MkDocs event priority: metadata must be ready before the tags/search plugins
# consume it. Keep this module importable by dependency-free validation tests.
setattr(on_page_markdown, 'mkdocs_priority', 100)


def on_page_context(context, page, config, nav):
    guide = next((g for g in RECORDS if g['path'] == page.file.src_uri), None)
    if guide:
        page.meta['tx_guide'] = dict(guide)
        related = [g for g in RECORDS if g['topic'] == guide['topic'] and g['path'] != guide['path']]
        related.sort(key=lambda g: (-len(set(g['tags']) & set(guide['tags'])), g['title'].casefold()))
        page.meta['tx_related'] = [dict(g) for g in related[:3]]
        if 'series' in guide:
            members = sorted((g for g in RECORDS if g.get('series', {}).get('slug') == guide['series']['slug']),
                             key=lambda g: g['series']['order'])
            index = members.index(guide)
            page.meta['tx_series'] = {
                'title': 'Homelab Rebuild', 'url': 'homelab-rebuild/',
                'previous': dict(members[index - 1]) if index else None,
                'next': dict(members[index + 1]) if index + 1 < len(members) else None}
    return context


def on_post_build(config):
    fields = ('title', 'description', 'url', 'topic', 'topic_label', 'tags', 'aliases', 'type')
    output = [{k: g[k] for k in fields} for g in RECORDS]
    destination = Path(config['site_dir']) / 'assets/guides.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
