/* Progressive enhancements: ordinary links and Material full-text search remain the fallback. */
(function () {
  'use strict';
  function normalise(value) {
    return String(value || '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  }
  function rankGuides(guides, query) {
    const term = normalise(query);
    if (!term) return [];
    const words = term.split(/\s+/);
    return guides.map(guide => {
      const title = normalise(guide.title);
      const aliases = (guide.aliases || []).map(normalise);
      const text = normalise([guide.title, guide.description, guide.topic_label, ...(guide.tags || []), ...(guide.aliases || [])].join(' '));
      const score = title === term ? 1000 : aliases.includes(term) ? 950 : title.startsWith(term) ? 800 : title.includes(term) ? 700 : words.every(word => text.includes(word)) ? 100 + words.filter(word => title.includes(word)).length * 50 : 0;
      return { guide, score };
    }).filter(result => result.score > 0).sort((a, b) => b.score - a.score || a.guide.title.localeCompare(b.guide.title)).map(result => result.guide);
  }
  function matchesGuide(guide, filters) {
    const terms = normalise(filters.q).split(/\s+/).filter(Boolean);
    const text = normalise(guide.search);
    return (!filters.topic || guide.topic === filters.topic) && (!filters.type || guide.type === filters.type) && terms.every(term => text.includes(term));
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { normalise, rankGuides, matchesGuide };
  if (typeof document === 'undefined') return;

  function setupCatalogue() {
    const catalogue = document.querySelector('[data-catalogue]');
    if (!catalogue) return;
    const query = catalogue.querySelector('#guide-query');
    const topic = catalogue.querySelector('#guide-topic');
    const type = catalogue.querySelector('#guide-type');
    const reset = catalogue.querySelector('#guide-reset');
    const count = catalogue.querySelector('#guide-count');
    const empty = catalogue.querySelector('#guide-empty');
    const cards = Array.from(catalogue.querySelectorAll('.tx-guide-card'));
    if (!query || !topic || !type || !reset || !count || !empty) return;
    function render() {
      let visible = 0;
      cards.forEach(card => {
        card.hidden = !matchesGuide(card.dataset, { q: query.value, topic: topic.value, type: type.value });
        if (!card.hidden) visible++;
      });
      count.textContent = `${visible} ${visible === 1 ? 'guide' : 'guides'}${visible === cards.length ? '' : ` of ${cards.length}`}`;
      empty.hidden = visible !== 0;
    }
    function loadState() {
      const params = new URLSearchParams(location.search);
      query.value = params.get('q') || '';
      topic.value = params.get('topic') || '';
      type.value = params.get('type') || '';
      if (topic.selectedIndex < 0) topic.value = '';
      if (type.selectedIndex < 0) type.value = '';
      render();
    }
    function update(push) {
      const url = new URL(location.href);
      for (const [key, value] of Object.entries({ q: query.value, topic: topic.value, type: type.value })) {
        if (value) url.searchParams.set(key, value); else url.searchParams.delete(key);
      }
      if (url.href !== location.href) history[push ? 'pushState' : 'replaceState'](null, '', url);
      render();
    }
    query.addEventListener('input', () => update(false));
    topic.addEventListener('change', () => update(true));
    type.addEventListener('change', () => update(true));
    reset.addEventListener('click', () => { query.value = ''; topic.value = ''; type.value = ''; update(true); query.focus(); });
    window.addEventListener('popstate', loadState);
    [query, topic, type, reset].forEach(control => { control.disabled = false; });
    loadState();
  }
  function setupSearch() {
    const toggle = document.getElementById('__search');
    const input = document.querySelector('.md-search input[name="query"]');
    const output = document.querySelector('.md-search__output');
    if (!toggle || !input || !output) return;
    let config;
    try { config = JSON.parse(document.getElementById('__config').textContent); } catch (_) { return; }
    const base = new URL(`${config.base || '.'}/`, location.href);
    let guides = null;
    let pending = null;
    let returnFocus = null;
    const quick = document.createElement('section');
    quick.className = 'tx-quick-matches';
    quick.setAttribute('aria-label', 'Matching guides');
    quick.hidden = true;
    output.prepend(quick);

    function renderQuick() {
      quick.replaceChildren();
      const matches = guides ? rankGuides(guides, input.value).slice(0, 3) : [];
      quick.hidden = !matches.length;
      if (!matches.length) return;
      const heading = document.createElement('p');
      heading.className = 'tx-quick-heading';
      heading.textContent = 'Matching guides';
      quick.append(heading);
      matches.forEach(guide => {
        const target = new URL(guide.url, base);
        if (target.origin !== base.origin || !['http:', 'https:'].includes(target.protocol)) return;
        const link = document.createElement('a');
        link.href = target.href;
        link.className = 'tx-quick-link';
        for (const [className, value] of [['tx-quick-title', guide.title], ['tx-quick-meta', guide.topic_label], ['tx-quick-description', guide.description]]) {
          const span = document.createElement('span');
          span.className = className;
          span.textContent = value || '';
          link.append(span);
        }
        quick.append(link);
      });
    }
    function loadGuides() {
      if (guides || pending) return;
      pending = fetch(new URL('assets/guides.json', base)).then(response => {
        if (!response.ok) throw new Error('Guide index unavailable');
        return response.json();
      }).then(data => {
        if (!Array.isArray(data)) throw new Error('Guide index malformed');
        guides = data.filter(guide => guide && typeof guide.title === 'string' && typeof guide.url === 'string');
        renderQuick();
      }).catch(() => {
        // Optional quick matches: Material full-text search stays available if this index fails.
        quick.hidden = true;
      }).finally(() => { pending = null; });
    }
    function openSearch(opener) {
      returnFocus = opener || document.activeElement;
      toggle.checked = true;
      toggle.dispatchEvent(new Event('change', { bubbles: true }));
      input.focus();
      loadGuides();
    }
    function closeSearch() {
      toggle.checked = false;
      toggle.dispatchEvent(new Event('change', { bubbles: true }));
      input.blur();
      if (returnFocus && returnFocus.isConnected) returnFocus.focus();
    }
    document.querySelectorAll('[data-open-search]').forEach(trigger => {
      trigger.addEventListener('click', () => openSearch(trigger));
    });
    input.addEventListener('focus', loadGuides);
    input.addEventListener('input', () => { loadGuides(); renderQuick(); });
    document.addEventListener('keydown', event => {
      const editing = document.activeElement.matches('input, textarea, select, [contenteditable]:not([contenteditable="false"])');
      if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey && !editing) {
        event.preventDefault(); event.stopImmediatePropagation(); openSearch(document.activeElement); return;
      }
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault(); event.stopImmediatePropagation(); openSearch(document.activeElement); return;
      }
      if (!toggle.checked) return;
      if (event.key === 'Escape') {
        event.preventDefault(); event.stopImmediatePropagation(); closeSearch(); return;
      }
      if (!['ArrowDown', 'ArrowUp'].includes(event.key) || !document.activeElement.closest('.md-search')) return;
      const links = Array.from(output.querySelectorAll('a.tx-quick-link, a.md-search-result__link')).filter(link => link.getClientRects().length);
      if (!links.length) return;
      event.preventDefault(); event.stopImmediatePropagation();
      const current = links.indexOf(document.activeElement);
      const next = event.key === 'ArrowDown' ? (current + 1) % links.length : current <= 0 ? links.length - 1 : current - 1;
      links[next].focus();
    }, true);
  }
  function init() { setupCatalogue(); setupSearch(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
