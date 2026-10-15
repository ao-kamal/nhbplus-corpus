// PROBE - FULL HANDLE SWEEP. Captures the NODE HANDLE for every file.
// The handle is the row `id`. It mints the per-file URL:
//   https://mega.nz/folder/PH#KEY/file/<HANDLE>
// which is how ONE file is fetched instead of the whole tree.
//
// Why scroll-union: the MEGA grid is VIRTUALISED and un-mounts rows you scroll
// past. A single count measures a window - that defect hid 30 files and 8 calls
// across four earlier enumerations.
const HANDLE = "__H__";
const BASE = "https://mega.nz/folder/EzMk0Z4K#CrnHbM7tWaNtcByX0Ry_-Q";

const page = await browser.getPage("mega");
await page.setViewportSize({ width: 1600, height: 1200 });
await page.goto(BASE + "/folder/" + HANDLE, { waitUntil: "domcontentloaded", timeout: 20000 });
await page.reload({ waitUntil: "domcontentloaded", timeout: 20000 });

// Paint wait. An early evaluate returns 0 rows - indistinguishable from empty.
for (let i = 0; i < 16; i++) {
  if (await page.evaluate(() => document.querySelectorAll(
      "tr.megaListItem, a.mega-node.fm-item").length) > 0) break;
  await page.waitForTimeout(900);
}

const rows = await page.evaluate(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const seen = new Map();
  const grab = () => {
    for (const e of document.querySelectorAll("tr.megaListItem, a.mega-node.fm-item")) {
      const t = (e.innerText || "").replace(/\s+/g, " ").trim();
      if (!t || /examplefilename|Object \d/i.test(t)) continue;
      const id = e.id || "";
      const ti = e.getAttribute("title") || "";
      const isFolder = /\bfolder\b/i.test(String(e.className)) || /\bFolder\b/.test(t);
      // key on the HANDLE, not the text: text can repeat (Resources Links.txt)
      const k = id || ("T:" + t);
      if (!seen.has(k)) seen.set(k, [id, t, ti.slice(0, 200), isFolder ? 1 : 0]);
    }
  };
  grab();
  let best = null, bestMax = 0;
  for (const el of document.querySelectorAll("div,main,section,body")) {
    const m = el.scrollHeight - el.clientHeight;
    if (m > bestMax) { bestMax = m; best = el; }
  }
  let pos = 0;
  while (pos < bestMax && pos < 80000) {
    pos += 600;
    if (best) best.scrollTop = pos; else window.scrollTo(0, pos);
    await sleep(150); grab();
  }
  grab();
  return [...seen.entries()].map(([k, v]) => v);
});

console.log("N=" + rows.length);
console.log("JSON=" + JSON.stringify(rows));