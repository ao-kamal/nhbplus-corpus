// PROBE ONLY - NOT PIPELINE CODE.
//
// THE MEGA GRID IS VIRTUALISED AND UN-MOUNTS ROWS YOU SCROLL PAST.
// Proof: 2025-Feb showed 36 rows, and scrolling to the BOTTOM dropped it to 31.
// A single before/after count therefore measures a WINDOW, not a list - which is
// exactly why the sweep under-counted 2022 (-1.93 GB), 2023 (-0.48 GB) and
// 2025 (-14.31 GB).
//
// CORRECT TECHNIQUE: scroll in viewport-sized STEPS and UNION the rows visible at
// every position. Never jump to the end. Never count once.
//
// CONCERN: "NO CORPUS BYTES FETCHED". Container listing only.

const HANDLE = "__H__";
const LABEL  = "__L__";

const page = await browser.getPage("mega");
await page.setViewportSize({ width: 1600, height: 900 });   // smaller => fewer steps
await page.goto("https://mega.nz/folder/EzMk0Z4K#CrnHbM7tWaNtcByX0Ry_-Q/folder/" + HANDLE,
                { waitUntil: "domcontentloaded", timeout: 20000 });
await page.reload({ waitUntil: "domcontentloaded", timeout: 20000 });

// Wait for the grid to actually paint before measuring anything. An early
// evaluate on an unpainted grid returns 0 rows, which looks exactly like an
// empty folder.
for (let i = 0; i < 16; i++) {
  const n = await page.evaluate(() => document.querySelectorAll(
    "tr.megaListItem, a.mega-node.fm-item").length);
  if (n) break;
  await page.waitForTimeout(900);
}
const painted = await page.evaluate(() => document.querySelectorAll(
  "tr.megaListItem, a.mega-node.fm-item").length);
console.log("PAINTED_AT_START=" + painted);

const union = await page.evaluate(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const seen = new Map();
  const grab = () => {
    for (const e of document.querySelectorAll("tr.megaListItem, a.mega-node.fm-item")) {
      const t = (e.innerText || "").replace(/\s+/g, " ").trim();
      if (!t || /examplefilename|Object \d/i.test(t)) continue;
      if (!seen.has(t)) seen.set(t, e.getAttribute("title") || "");
    }
  };
  const scroller = () => {
    let best = null, bestMax = 0;
    for (const el of document.querySelectorAll("div,main,section,body")) {
      const m = el.scrollHeight - el.clientHeight;
      if (m > bestMax) { bestMax = m; best = el; }
    }
    return { el: best, max: bestMax };
  };
  grab();
  const { el, max } = scroller();
  let pos = 0, steps = 0, prevCount = seen.size;
  while (pos < max && steps < 200) {
    pos += 600;                       // viewport-sized step, never jump to end
    if (el) el.scrollTop = pos; else window.scrollTo(0, pos);
    await sleep(170);
    grab();
    steps++;
    if (seen.size === prevCount && steps > 3 && pos > max * 0.6) { /* keep going */ }
    prevCount = seen.size;
  }
  grab();
  return { n: seen.size, steps, max, rows: [...seen.entries()] };
});

console.log("LABEL=" + LABEL);
console.log("UNIQUE_ROWS=" + union.n);
console.log("STEPS=" + union.steps + "  SCROLL_RANGE=" + union.max);
console.log("ROWS_JSON=" + JSON.stringify(union.rows));