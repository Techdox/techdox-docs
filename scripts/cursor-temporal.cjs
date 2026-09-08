const {chromium} = require('playwright');
const fs = require('fs');
const assert = require('assert/strict');
(async () => {
 const browser = await chromium.launch({args: ['--no-sandbox']});
 const base = process.env.BASE_URL;
 const site = process.env.SITE || 'docs';
 const out = process.env.ARTIFACT_DIR;
 fs.mkdirSync(out, {recursive:true});
 const results=[];
 try {
 for (const theme of ['dark','light']) for (const motion of ['no-preference','reduce']) {
 const page=await browser.newPage({viewport:{width:1440,height:900},colorScheme:theme,reducedMotion:motion});
 for (const route of (site==='landing'?['/','/404.html']:['/'])) {
 await page.goto(base+route,{waitUntil:'networkidle'});
 await page.evaluate(async ({site,theme})=>{await document.fonts.ready;if(site==='docs')document.body.dataset.mdColorScheme=theme==='dark'?'slate':'default';if(site==='blog')document.documentElement.dataset.theme=theme;},{site,theme});
 await page.waitForTimeout(500); // Let the site's existing theme transition settle before pixel sampling.
 const logos=page.locator(site==='landing'?'.brand img':site==='docs'?'.tx-wordmark img:visible':'.brand-mark img:visible');
 assert.equal(await logos.count(),route==='/404.html'?1:2);
 for(let j=0;j<await logos.count();j++) {
 const logo=logos.nth(j);await logo.scrollIntoViewIfNeeded();
 const prefix=`${site}-${theme}-${motion}-${route==='/404.html'?'404':'home'}-${j}`;
 const box=await logo.boundingBox();
 assert.ok(await logo.evaluate(i=>i.complete&&i.naturalWidth>0));
 // Capture the painted/cropped artwork wrapper (full original canvas may overflow).
 const target=site==='landing'?logo:logo.locator(site==='docs'?'xpath=ancestor::span[contains(@class,"tx-wordmark-art")]':'xpath=ancestor::span[contains(@class,"brand-mark")]');
 for(let k=0;k<8;k++){await target.screenshot({path:`${out}/${prefix}-${k}.png`,animations:'allow'});await page.waitForTimeout(170);}
 const selected=await logo.evaluate(i=>i.currentSrc);
 const expected=motion==='reduce'?(site==='landing'?'wordmark-':'primary-'):'wordmark-web-';
 assert.equal(new URL(selected).pathname.split('/').pop(),`${expected}${site==='landing'?'dark':theme}.svg`);
 const targetBox=await target.boundingBox();
 const scale=box.width/(site==='landing'?575.4:960);
 const cursor={x:box.x-targetBox.x+(615.28-(site==='landing'?54.44:0))*scale,y:box.y-targetBox.y+(52.2-(site==='landing'?32.04:0))*scale,width:14.56*scale,height:72.8*scale};
 results.push({prefix,site,theme,motion,route,logo:j,box,cursor,src:await logo.evaluate(i=>i.currentSrc)});
 }
 }
 await page.close();
 }
 }finally{await browser.close();fs.writeFileSync(`${out}/captures.json`,JSON.stringify(results,null,2));}
})();
