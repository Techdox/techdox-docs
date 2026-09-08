const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = (process.env.BASE_URL || 'http://127.0.0.1:8766').replace(/\/$/, '');
const artifacts = process.env.ARTIFACT_DIR || 'artifacts/browser';
fs.mkdirSync(artifacts, {recursive:true});
(async () => {
  const browser = await chromium.launch();
  const report = {base, checks:[], pages:[], failures:[], requestFailures:[], errors:[]};
  const check = (name, condition, detail) => { report.checks.push({name,passed:!!condition,detail}); if (!condition) report.failures.push(name); };
  try {
    const context = await browser.newContext({viewport:{width:1440,height:1000},permissions:['clipboard-read','clipboard-write']});
    const page = await context.newPage();
    page.on('pageerror', error => report.errors.push(String(error)));
    page.on('requestfailed', request => report.requestFailures.push({url:request.url(),failure:request.failure()}));
    const response = await page.request.get(base + '/assets/guides.json');
    check('guide index returns 200',response.status()===200);
    const guides = await response.json();
    for (const slug of ['', 'guides/', 'npm/', 'start-here/', 'homelab-rebuild/dns-stack/']) {
      for (const width of [320,375,390,768,1440]) {
        await page.setViewportSize({width,height:1000});
        await page.goto(base+'/'+slug,{waitUntil:'networkidle'});
        await page.evaluate(() => document.fonts.ready);
        await page.waitForTimeout(300);
        const metrics = await page.evaluate(() => ({width:innerWidth,scroll:document.documentElement.scrollWidth,title:document.title,h1:document.querySelector('h1')?.innerText,fonts:[...document.fonts].map(f=>({family:f.family,status:f.status}))}));
        report.pages.push({slug,...metrics});
        check(`${slug||'home'} no page overflow at ${width}`,metrics.scroll<=width+1,metrics);
        if (width === 1440 && slug === 'npm/') check('desktop uses only sidebar TOC',!(await page.locator('.tx-mobile-toc').isVisible()));
        if ([320,390,1440].includes(width)) await page.screenshot({path:path.join(artifacts,(slug.replaceAll('/','-')||'home')+width+'.png'),fullPage:width===1440});
      }
    }
    await page.goto(base+'/guides/',{waitUntil:'networkidle'});
    check('all indexed guides are browsable',await page.locator('[data-catalogue] .tx-guide-card').count()===guides.length);
    await page.locator('#guide-query').fill('npm');
    check('NPM directory alias matches NPM',await page.locator('[data-catalogue] .tx-guide-card:visible').evaluateAll(links=>links.some(a=>new URL(a.href).pathname==='/npm/')));
    await page.locator('#guide-reset').click();
    await page.locator('#guide-topic').selectOption('storage');
    check('topic filter only shows storage',await page.locator('[data-catalogue] .tx-guide-card:visible').evaluateAll(links=>links.length>0&&links.every(a=>a.dataset.topic==='storage')));
    await page.reload({waitUntil:'networkidle'});
    check('filter survives reload',await page.locator('#guide-topic').inputValue()==='storage');
    await page.locator('#guide-query').fill('no-such-guide-zzzzz');
    check('clear empty state',await page.locator('#guide-empty').isVisible());
    await page.locator('#guide-reset').click();
    check('reset restores all guides',await page.locator('[data-catalogue] .tx-guide-card:visible').count()===guides.length);
    await page.goto(base+'/',{waitUntil:'networkidle'});
    await page.keyboard.press('Control+k');
    check('Ctrl K opens search',await page.locator('#__search').isChecked());
    for (const [query,expected] of [['npm','/npm/'],['nginx proxy manager','/npm/'],['duplicati','/duplicati/'],['hoarder','/karakeep/'],['matrix','/matrix/']]) {
      await page.locator('input[name=query]').fill('');
      await page.locator('input[name=query]').pressSequentially(query,{delay:25});
      await page.waitForTimeout(500);
      check(`search ${query} prioritises expected guide`,await page.locator('.tx-quick-link').first().evaluate(a=>new URL(a.href).pathname)===expected);
    }
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('Enter');
    await page.waitForURL('**/matrix/');
    check('search keyboard opens matched guide',new URL(page.url()).pathname==='/matrix/');
    await page.goto(base+'/npm/',{waitUntil:'networkidle'});
    await page.locator('button.md-clipboard').first().click();
    check('copy preserves code', (await page.evaluate(()=>navigator.clipboard.readText())).trim()===(await page.locator('pre code').first().textContent()).trim());
    for (const slug of ['', 'guides/', 'npm/']) {
      await page.goto(base+'/'+slug,{waitUntil:'networkidle'});
      for (const theme of ['default','slate']) {
        await page.locator(`input[data-md-color-scheme="${theme}"]`).evaluate(e=>{e.checked=true;e.dispatchEvent(new Event('change',{bubbles:true}));});
        await page.waitForTimeout(300);
        await page.addScriptTag({path:require.resolve('axe-core')});
        const axe=await page.evaluate(()=>axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}}));
        const violations=axe.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}));
        report.pages.push({slug,theme,violations});
        check(`${slug||'home'} ${theme} accessibility`,violations.length===0,violations);
      }
    }
    await page.setViewportSize({width:390,height:844});
    await page.goto(base+'/npm/',{waitUntil:'networkidle'});
    const menu=page.locator('.tx-mobile-menu summary');
    await menu.click();
    check('mobile menu opens',await page.locator('.tx-mobile-menu').getAttribute('open')!==null);
    await page.screenshot({path:path.join(artifacts,'mobile-menu.png')});
    await menu.click();
    check('mobile page TOC present',await page.locator('.tx-mobile-toc').isVisible());
    await page.locator('.tx-mobile-toc summary').click();
    check('mobile TOC expands',await page.locator('.tx-mobile-toc').getAttribute('open')!==null);
    await page.locator('[data-open-search]').first().click();
    await page.locator('input[name=query]').pressSequentially('reverse proxy', {delay:25});
    await page.waitForTimeout(1200);
    check('native full-text previews stay compact',await page.locator('.md-search-result__article').first().evaluate(e=>e.getBoundingClientRect().height<=200));
    check('search has one reachable scrolling surface',await page.locator('.md-search__output').evaluate(e=>['auto','scroll'].includes(getComputedStyle(e).overflowY)));
    await page.screenshot({path:path.join(artifacts,'mobile-search.png')});
    await page.keyboard.press('Escape');
    const beforeScheme=await page.locator('body').getAttribute('data-md-color-scheme');
    const targetScheme=beforeScheme==='slate'?'default':'slate';
    await page.locator(`input[data-md-color-scheme=${targetScheme}]`).focus();
    await page.keyboard.press('Space');
    await page.waitForTimeout(100);
    check('theme is keyboard operable',await page.locator('body').getAttribute('data-md-color-scheme')===targetScheme);
    const noJs=await browser.newContext({javaScriptEnabled:false});
    const plain=await noJs.newPage();
    await plain.goto(base+'/guides/');
    check('no-JS directory retains every guide link',await plain.locator('[data-catalogue] .tx-guide-card').count()===guides.length);
    check('no-JS filter controls are disabled',await plain.locator('#guide-query').isDisabled());
    await noJs.close();
    check('no runtime exceptions',report.errors.length===0,report.errors);
  } finally {
    fs.writeFileSync(path.join(artifacts,'report.json'),JSON.stringify(report,null,2));
    await browser.close();
  }
  console.log(JSON.stringify({checks:report.checks.length,failures:report.failures,errors:report.errors},null,2));
  assert.equal(report.failures.length,0,'Browser acceptance checks failed; see artifact report');
})().catch(error=>{console.error(error);process.exitCode=1;});
