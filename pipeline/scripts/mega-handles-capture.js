// PROBE ONLY. Capture the NODE HANDLE (row id) for every file in a folder.
// The handle is what goes into https://mega.nz/folder/PH#KEY/file/HANDLE
// which is the documented way to address ONE file inside a folder link.
const HANDLE = "kqUwSJJa";   // 2022/4. April
const BASE = "https://mega.nz/folder/EzMk0Z4K#CrnHbM7tWaNtcByX0Ry_-Q";

const page = await browser.getPage("mega");
await page.setViewportSize({ width: 1600, height: 1200 });
await page.goto(BASE + "/folder/" + HANDLE, { waitUntil: "domcontentloaded", timeout: 20000 });
await page.reload({ waitUntil: "domcontentloaded", timeout: 20000 });

// The grid is lazy AND the page needs a paint wait. An early evaluate returns 0
// rows, which is indistinguishable from an empty folder unless you wait for it.
for (let i = 0; i < 16; i++) {
  const n = await page.evaluate(() => document.querySelectorAll(
    "tr.megaListItem, a.mega-node.fm-item").length);
  if (n > 0) break;
  await page.waitForTimeout(900);
}
console.log("PAINTED=" + await page.evaluate(() =>
  document.querySelectorAll("tr.megaListItem, a.mega-node.fm-item").length));

// scroll-union, because the grid is virtualised and un-mounts rows
const rows = await page.evaluate(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const seen = new Map();
  const grab = () => {
    for (const e of document.querySelectorAll("tr.megaListItem, a.mega-node.fm-item")) {
      const t = (e.innerText || "").replace(/\s+/g, " ").trim();
      if (!t || /examplefilename|Object \d/i.test(t)) continue;
      // THE HANDLE IS THE ROW ID
      const h = e.id || "";
      if (h && h.length >= 6 && !seen.has(h)) seen.set(h, t);
    }
  };
  grab();
  let best = null, bestMax = 0;
  for (const el of document.querySelectorAll("div,main,section,body")) {
    const m = el.scrollHeight - el.clientHeight;
    if (m > bestMax) { bestMax = m; best = el; }
  }
  let pos = 0;
  while (pos < bestMax && pos < 60000) {
    pos += 600;
    if (best) best.scrollTop = pos; else window.scrollTo(0, pos);
    await sleep(160); grab();
  }
  grab();
  return [...seen.entries()];
});

console.log("ROWS=" + rows.length);
console.log("JSON=" + JSON.stringify(rows));