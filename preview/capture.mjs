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
// QA-only comparison. The shipped app continues to use the new vector art;
// swap the old SVG into this browser session to capture the same markers,
// placement and viewport against the approved traced cell.
const vectorMarkup = await page.locator('.inline-art').innerHTML();
await page.locator('.inline-art').evaluate(async el => {
  const response = await fetch('/src/assets/cell-reference.svg');
  if (!response.ok) throw new Error('Could not load approved traced reference');
  el.innerHTML = await response.text();
});
await page.screenshot({path:'preview/browser-trace-reference-mobile.png'});
await page.locator('.cell-composition').screenshot({path:'preview/browser-trace-reference-cell.png'});
// Move the composition alone onto an opaque inspection board. Scaling the
// original stage would crop the right half and reveal UI behind the drawing.
await page.setViewportSize({width:1200,height:1200});
await page.locator('.cell-composition').evaluate(el => {
  const board = document.createElement('div');
  board.className = 'reference-scene';
  Object.assign(board.style, {position:'fixed',inset:'0',zIndex:'10000',background:'#fffcfa'});
  document.body.appendChild(board);
  board.appendChild(el);
  Object.assign(el.style, {position:'absolute',top:'0',left:'0',width:'378px',height:'378px'});
  el.style.transform = 'scale(2)';
  el.style.transformOrigin = 'top left';
});
await page.locator('.cell-composition').screenshot({path:'preview/browser-trace-reference-2x.png'});
await page.locator('.inline-art').evaluate((el,markup) => {el.innerHTML=markup;},vectorMarkup);
await page.locator('.cell-composition').screenshot({path:'preview/browser-vector-reference-2x.png'});
await browser.close();
