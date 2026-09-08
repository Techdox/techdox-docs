const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = (process.env.BASE_URL || 'http://127.0.0.1:8766').replace(/\/$/, '');
const artifacts = process.env.ARTIFACT_DIR || 'artifacts/browser';
fs.mkdirSync(artifacts, { recursive: true });
(async () => {
  const browser = await chromium.launch();
  const results = [];
  try {
    for (const scheme of ['slate', 'default']) {
      const context = await browser.newContext({ colorScheme: scheme === 'slate' ? 'dark' : 'light' });
      const page = await context.newPage();
      // Local acceptance must not emit analytics or depend on embedded third-party media.
      await page.route('**/*', route => new URL(route.request().url()).origin === new URL(base).origin ? route.continue() : route.abort());
      for (const width of [320, 390, 768, 1440]) {
        await page.setViewportSize({ width, height: 900 });
        for (const slug of ['', 'npm/']) {
          await page.goto(base + '/' + slug, { waitUntil: 'networkidle' });
          await page.evaluate(() => document.fonts.ready);
          const metrics = await page.evaluate(() => ({
            scheme: document.body.dataset.mdColorScheme,
            overflow: document.documentElement.scrollWidth > innerWidth,
            headerHeight: document.querySelector('header').getBoundingClientRect().height,
            background: getComputedStyle(document.body).backgroundColor,
            border: getComputedStyle(document.querySelector('header')).borderBottomColor,
            fontsLoaded: document.fonts.check('16px "Hanken Grotesk"') && document.fonts.check('16px "JetBrains Mono"'),
            logos: [...document.querySelectorAll('.tx-wordmark')].map(link => {
              const images = [...link.querySelectorAll('img')].filter(img => getComputedStyle(img).display !== 'none');
              const box = link.getBoundingClientRect();
              return { href: link.href, name: link.getAttribute('aria-label'), visible: images.length,
                images: images.map(img => {
                  const source = img.getBoundingClientRect();
                  const r = img.closest('.tx-wordmark-art')?.getBoundingClientRect() || source;
                  return { artworkWidth: source.width * 576 / 960, sourceWidth: source.width, sourceHeight: source.height, src: img.getAttribute('src'), width: r.width, height: r.height, loaded: img.complete && img.naturalWidth > 0,
                    clearspace: [r.left-box.left, box.right-r.right, r.top-box.top, box.bottom-r.bottom],
                    animation: getComputedStyle(img).animationName };
                }) };
            })
          }));
          results.push({ scheme, width, slug, ...metrics });
          assert.equal(metrics.scheme, scheme);
          assert.equal(metrics.background, scheme === 'slate' ? 'rgb(9, 12, 18)' : 'rgb(248, 250, 252)');
          assert.equal(metrics.border, scheme === 'slate' ? 'rgb(41, 52, 69)' : 'rgb(211, 220, 232)');
          assert.ok(metrics.fontsLoaded, 'existing local fonts load');
          assert.equal(metrics.overflow, false, `overflow at ${width}`);
          assert.ok(metrics.headerHeight <= 80, 'keep compact header');
          assert.equal(metrics.logos.length, 2, 'header and footer wordmarks');
          for (const logo of metrics.logos) {
            assert.equal(logo.href, 'https://techdox.nz/');
            assert.equal(logo.name, 'Techdox main site');
            assert.equal(logo.visible, 1, 'only the matching themed wordmark is visible');
            const image = logo.images[0];
            assert.ok(image.loaded);
            assert.ok(image.src.endsWith(`wordmark-web-${scheme === 'slate' ? 'dark' : 'light'}.svg`));
            assert.ok(image.artworkWidth >= 140, 'visible full wordmark minimum 140 CSS px, excluding transparent canvas');
            assert.ok(Math.abs(image.sourceWidth / image.sourceHeight - 960 / 180) < 0.01, 'undistorted master');
            assert.ok(image.clearspace.every(space => space >= image.height / 2 - 0.1), 'half-height clearspace on all sides');
            assert.equal(image.animation, 'none', 'image/letters stay static; pixel suite checks internal cursor');
          }
          assert.equal(new URL(await page.locator('.tx-docs-link').getAttribute('href'), page.url()).pathname, '/');
          if (width === 320) {
            await page.locator('[data-open-search]').first().click();
            assert.equal(await page.locator('#__search').isChecked(), true);
            await page.keyboard.press('Escape');
            await page.locator('.tx-mobile-menu summary').click();
            assert.notEqual(await page.locator('.tx-mobile-menu').getAttribute('open'), null);
            await page.locator('.tx-mobile-menu summary').click();
          }
          if ([320, 390, 1440].includes(width)) await page.screenshot({ path: path.join(artifacts, `brand-${slug ? 'guide' : 'home'}-${scheme}-${width}.png`), fullPage: width === 1440 });
        }
      }
      await context.close();
    }
  } finally {
    fs.writeFileSync(path.join(artifacts, 'brand-report.json'), JSON.stringify(results, null, 2));
    await browser.close();
  }
  console.log(`Brand layout: ${results.length} page/theme/viewport combinations passed`);
})().catch(error => { console.error(error); process.exitCode = 1; });
