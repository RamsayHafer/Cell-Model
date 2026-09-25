// Real Chromium captures at the target mobile viewport; no browser dependency
// is needed in the shipped app (the workflow installs Playwright temporarily).
import { chromium } from 'playwright';
const browser = await chromium.launch({ headless:true });
const page = await browser.newPage({ viewport:{width:390,height:844}, deviceScaleFactor:2, isMobile:true, hasTouch:true });
await page.goto('http://127.0.0.1:4173/', {waitUntil:'networkidle'});
await page.screenshot({path:'preview/browser-visit-mobile.png'});
await page.getByRole('button', {name:'Marker study'}).click();
await page.screenshot({path:'preview/browser-a-mobile.png'});
await page.locator('.cell-composition').screenshot({path:'preview/browser-a-markers-closeup.png'});
const cellBounds = await page.locator('.cell-composition').boundingBox();
if (!cellBounds) throw new Error('Cell composition was not rendered');
await page.screenshot({path:'preview/browser-a-receptors-closeup.png',clip:{
  x:cellBounds.x,y:cellBounds.y+cellBounds.height*.045,
  width:cellBounds.width,height:cellBounds.height*.65,
}});
await page.getByRole('button', {name:'B Illustration + Overlay'}).click();
await page.screenshot({path:'preview/browser-b-mobile.png'});
await page.locator('.cell-composition').screenshot({path:'preview/browser-b-markers-closeup.png'});
await page.getByRole('button', {name:'CD30: Illustrated receptor'}).click();
await page.getByRole('region', {name:'CD30 details'}).waitFor();
await page.screenshot({path:'preview/browser-b-selected.png'});
await page.goto('http://127.0.0.1:4173/?reference=1', {waitUntil:'networkidle'});
await page.screenshot({path:'preview/browser-reference-mobile.png'});
await page.locator('.cell-composition').screenshot({path:'preview/browser-reference-cell.png'});
await browser.close();
