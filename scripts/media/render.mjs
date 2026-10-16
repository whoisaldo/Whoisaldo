#!/usr/bin/env node
// Renders the two animated images at the top of the README.
//
//   node scripts/media/render.mjs hero   -> hero.webp
//   node scripts/media/render.mjs city   -> city.webp
//
// hero: a 360° turntable of the S4 from the portfolio (three.js, same lights),
// next to the name. 120 frames at 50 ms, rendered one by one so it loops clean.
// city: the S4's drift in the aliyounes.dev intro, recorded live, slowed to
// about half speed and faded through black at the seam. CITY_FROM/CITY_TO are
// where the drift sits in the intro today. Its timing moves by a few tenths of
// a second between runs, so look at the result and nudge the window if it
// caught the title card or missed the car.
//
// Needs: a Portfolio checkout (PORTFOLIO, default ../Portfolio next to this
// repo) for three.js and the model, `npm i --no-save playwright`, and
// img2webp (brew install webp). The city capture needs a real GPU (Metal).
import { chromium } from "playwright";
import { createServer } from "node:http";
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, writeFileSync, readdirSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { extname, join, resolve } from "node:path";

const ROOT = resolve(import.meta.dirname, "../..");
const PORTFOLIO = resolve(process.env.PORTFOLIO || join(ROOT, "../Portfolio"));
const CITY_FROM = 23.2, CITY_TO = 24.7, CITY_FPS = 40;
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript",
  ".woff2": "font/woff2", ".glb": "model/gltf-binary", ".jpg": "image/jpeg" };

function serve(frames) {
  const route = (url) => {
    if (url.startsWith("/three/")) return join(PORTFOLIO, "node_modules", url);
    if (url === "/model/ali-s4.glb") return join(PORTFOLIO, "public/models/ali-s4.glb");
    if (url.startsWith("/frames/")) return join(frames, url.slice(8));
    return join(ROOT, url);
  };
  const server = createServer((req, res) => {
    const file = route(decodeURIComponent(req.url.split("?")[0]));
    try {
      const body = readFileSync(file);
      res.writeHead(200, { "Content-Type": TYPES[extname(file)] || "application/octet-stream" }).end(body);
    } catch {
      res.writeHead(404).end();
    }
  });
  return new Promise((ok) => server.listen(0, "127.0.0.1", () => ok(server)));
}

function encode(dir, out, quality, delay) {
  const frames = readdirSync(dir).filter((f) => f.endsWith(".png")).sort().map((f) => join(dir, f));
  execFileSync("img2webp", ["-loop", "0", "-lossy", "-q", String(quality), "-m", "6", "-d", String(delay), ...frames, "-o", out]);
  console.log(`${out}: ${frames.length} frames, ${(statSync(out).size / 1e6).toFixed(2)} MB`);
}

async function hero(base, work) {
  const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
  const page = await browser.newPage({ viewport: { width: 880, height: 300 }, deviceScaleFactor: 2 });
  await page.goto(`${base}/scripts/media/hero.html`);
  await page.waitForFunction(() => window.ready === true, null, { timeout: 120000 });
  const card = await page.$("#card");
  for (let i = 0; i < 120; i++) {
    await page.evaluate((deg) => window.renderAt(deg), 35 - i * 3);
    await card.screenshot({ path: join(work, `f${String(i).padStart(4, "0")}.png`), omitBackground: true });
  }
  await browser.close();
  encode(work, join(ROOT, "hero.webp"), 86, 50);
}

async function city(base, work) {
  const browser = await chromium.launch({ channel: "chromium", args: ["--use-angle=metal", "--enable-gpu"] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 810 } });
  await page.goto("https://aliyounes.dev", { waitUntil: "load", timeout: 60000 });
  await page.waitForSelector("text=ENTER SILENT", { timeout: 90000 });
  await page.waitForTimeout(3000);

  // Record the intro with its real timestamps, then pick frames by time.
  const cdp = await page.context().newCDPSession(page);
  const shots = [];
  cdp.on("Page.screencastFrame", async (f) => {
    const name = `s${String(shots.length).padStart(5, "0")}.jpg`;
    writeFileSync(join(work, name), Buffer.from(f.data, "base64"));
    shots.push([f.metadata.timestamp, name]);
    await cdp.send("Page.screencastFrameAck", { sessionId: f.sessionId }).catch(() => {});
  });
  await page.evaluate(() => [...document.querySelectorAll("button")].find((b) => /enter silent/i.test(b.textContent)).click());
  await cdp.send("Page.startScreencast", { format: "jpeg", quality: 95 });
  await page.waitForTimeout((CITY_TO + 2) * 1000);
  await cdp.send("Page.stopScreencast");

  const t0 = shots[0][0];
  const picks = [];
  for (let t = CITY_FROM; t <= CITY_TO + 1e-9; t += 1 / CITY_FPS) {
    picks.push(shots.reduce((a, b) => (Math.abs(b[0] - t0 - t) < Math.abs(a[0] - t0 - t) ? b : a))[1]);
  }

  const comp = await browser.newPage({ viewport: { width: 880, height: 400 }, deviceScaleFactor: 1.5 });
  await comp.goto(`${base}/scripts/media/city.html`);
  await comp.waitForFunction(() => window.ready === true);
  const card = await comp.$("#card");
  const fadeIn = 4, fadeOut = 6, n = picks.length;
  for (let i = 0; i < n; i++) {
    let black = 0;
    if (i < fadeIn) black = 1 - (i + 1) / (fadeIn + 1);
    if (i >= n - fadeOut) black = (i - (n - fadeOut) + 1) / (fadeOut + 1);
    await comp.evaluate(([src, k]) => window.show(src, k), [`/frames/${picks[i]}`, black]);
    await card.screenshot({ path: join(work, `f${String(i).padStart(4, "0")}.png`), omitBackground: true });
  }
  await browser.close();
  encode(work, join(ROOT, "city.webp"), 58, 45);
}

const what = process.argv[2];
if (!["hero", "city"].includes(what)) {
  console.error("usage: node scripts/media/render.mjs hero|city");
  process.exit(2);
}
const work = mkdtempSync(join(tmpdir(), `readme-${what}-`));
const server = await serve(work);
const base = `http://127.0.0.1:${server.address().port}`;
try {
  await (what === "hero" ? hero : city)(base, work);
} finally {
  server.close();
}
