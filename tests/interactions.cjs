const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
(async () => {
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    // Isolated test fixture, never deployed or presented as real guide data.
    await page.route('https://fixture.test/**', route => route.fulfill({contentType:'text/html',body:`<!doctype html><html><body>
    <div data-catalogue><input id="guide-query" disabled><select id="guide-topic"><option value="">All topics</option><option value="networking">Networking</option><option value="storage">Storage</option></select><select id="guide-type"><option value="">All types</option><option value="tutorial">Tutorial</option></select><button id="guide-reset">Reset</button><p id="guide-count" role="status"></p><p id="guide-empty" hidden>No guides match</p><a class="tx-guide-card" href="/npm/" data-topic="networking" data-type="tutorial" data-search="Nginx Proxy Manager NPM">Nginx Proxy Manager</a><a class="tx-guide-card" href="/duplicati/" data-topic="storage" data-type="tutorial" data-search="Duplicati backup">Duplicati</a></div></body></html>`}));
    await page.goto('https://fixture.test/guides/');
    await page.addScriptTag({content:fs.readFileSync('docs/javascripts/docs.js','utf8')});
    assert.equal(await page.locator('#guide-query').isEnabled(), true, 'progressive enhancement enables filters');
    await page.locator('#guide-query').fill('npm');
    assert.equal(await page.locator('.tx-guide-card:visible').count(), 1, 'typing filters to one guide');
    assert.equal(new URL(page.url()).searchParams.get('q'), 'npm');
    await page.locator('#guide-reset').click();
    assert.equal(await page.locator('.tx-guide-card:visible').count(), 2);
    await page.locator('#guide-topic').selectOption('storage');
    assert.equal(await page.locator('.tx-guide-card:visible').innerText(), 'Duplicati');
    await page.goBack();
    assert.equal(await page.locator('.tx-guide-card:visible').count(), 2, 'Back restores previous filters');
    await page.locator('#guide-query').fill('nonexistent');
    assert.equal(await page.locator('#guide-empty').isVisible(), true);
    console.log('PASS: directory typing, combined filters, reset, URL state, Back and empty state');
    await page.route('https://fixture.test/assets/guides.json', route => route.fulfill({contentType:'application/json',body:JSON.stringify([{title:'Nginx Proxy Manager',description:'Add HTTPS',url:'npm/',topic_label:'Networking',aliases:['npm'],tags:[]}])}));
    await page.setContent('<script id="__config" type="application/json">{"base":".."}</script><button data-open-search>Find a guide</button><input id="__search" type="checkbox"><div class="md-search"><input name="query"><div class="md-search__output"><div class="md-search-result"><ol class="md-search-result__list"></ol></div></div></div>');
    await page.addScriptTag({content:fs.readFileSync('docs/javascripts/docs.js','utf8')});
    await page.locator('[data-open-search]').click();
    assert.equal(await page.locator('#__search').isChecked(), true, 'home trigger opens native search');
    await page.locator('input[name=query]').fill('npm');
    await page.waitForSelector('.tx-quick-link', {timeout:3000});
    assert.equal(await page.locator('.tx-quick-link').first().getAttribute('href'), 'https://fixture.test/npm/');
    await page.keyboard.press('ArrowDown');
    assert.equal(await page.evaluate(() => document.activeElement.classList.contains('tx-quick-link')), true, 'keyboard selects exact alias result');
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('#__search').isChecked(), false);
    assert.equal(await page.locator('[data-open-search]').evaluate(e => e === document.activeElement), true, 'Escape restores focus');
    await page.keyboard.press('/');
    assert.equal(await page.locator('#__search').isChecked(), true, 'slash opens search from outside a text field');
    await page.keyboard.press('Escape');
    await page.keyboard.press('Control+k');
    assert.equal(await page.locator('#__search').isChecked(), true);
    console.log('PASS: search trigger, fetched exact alias result, keyboard selection, Escape focus and Ctrl+K');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
