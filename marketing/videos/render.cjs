// Génère les vidéos MP4 (1080x1920, 30 i/s, H.264, sans son) à partir de videos.json.
// Usage : node marketing/videos/render.cjs [id...]
// Le son est à ajouter dans TikTok/Instagram (sons tendance, droits inclus).
const { chromium } = require("playwright");
const { spawn } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const FPS = 30;
const dir = __dirname;
const outDir = path.join(dir, "out");
fs.mkdirSync(outDir, { recursive: true });

const videos = JSON.parse(fs.readFileSync(path.join(dir, "videos.json"), "utf8"));
const only = process.argv.slice(2);

function encoder(file) {
  const ff = spawn("ffmpeg", [
    "-y", "-loglevel", "error",
    "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-",
    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
    "-movflags", "+faststart", file,
  ], { stdio: ["pipe", "inherit", "inherit"] });
  const done = new Promise((res, rej) => ff.on("close", (code) => (code === 0 ? res() : rej(new Error("ffmpeg " + code)))));
  return { ff, done };
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto("file://" + path.join(dir, "render.html"));
  await page.evaluate(() => document.fonts.ready);

  for (const v of videos) {
    if (only.length && !only.includes(v.id)) continue;
    const duration = await page.evaluate((video) => window.setup(video), v);
    const frames = Math.ceil(duration * FPS);
    const file = path.join(outDir, `${v.id}.mp4`);
    const { ff, done } = encoder(file);
    const t0 = Date.now();
    for (let i = 0; i < frames; i++) {
      await page.evaluate((t) => window.renderAt(t), i / FPS);
      const buf = await page.screenshot({ type: "jpeg", quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    }
    ff.stdin.end();
    await done;
    // Miniature (image de couverture) : l'accroche + la conversation à mi-parcours.
    await page.evaluate((t) => window.renderAt(t), duration * 0.55);
    await page.screenshot({ path: path.join(outDir, `${v.id}.jpg`), type: "jpeg", quality: 85 });
    fs.writeFileSync(path.join(outDir, `${v.id}.txt`), v.caption + "\n");
    console.log(`${v.id}: ${duration.toFixed(1)} s, ${frames} images, ${((Date.now() - t0) / 1000).toFixed(0)} s de rendu`);
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
