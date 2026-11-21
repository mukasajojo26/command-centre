#!/usr/bin/env node
// Render an HTML composition to MP4, frame by frame, deterministically.
// Usage: node render.mjs <composition.html> <out.mp4> [--fps 30] [--width 1920] [--height 1080] [--duration 5]
// Contract (any of these, checked in order):
//   window.__seek(t)  -> your function sets the frame for time t (seconds). Use with GSAP: tl.pause(); window.__seek = t => tl.seek(t)
//   otherwise all CSS/Web Animations are paused and set to currentTime = t*1000.
//   window.__duration -> seconds (overrides --duration).
// Requires: Node 18+, playwright (npm i -D playwright && npx playwright install chromium), ffmpeg on PATH.
import { spawn } from 'node:child_process'
import { createRequire } from 'node:module'
import path from 'node:path'
import { pathToFileURL } from 'node:url'

const args = process.argv.slice(2)
const opt = (k, d) => { const i = args.indexOf(`--${k}`); return i >= 0 ? Number(args[i + 1]) : d }
const [input, output] = args.filter((a, i) => !a.startsWith('--') && !args[i - 1]?.startsWith('--'))
if (!input || !output) { console.error('Usage: node render.mjs <composition.html> <out.mp4> [--fps 30] [--width 1920] [--height 1080] [--duration 5]'); process.exit(2) }
const fps = opt('fps', 30), width = opt('width', 1920), height = opt('height', 1080)

const require = createRequire(path.join(process.cwd(), 'noop.js'))
let chromium
try { ({ chromium } = require('playwright')) } catch { ({ chromium } = await import('playwright')) }

const browser = await chromium.launch()
const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 })
const url = /^https?:/.test(input) ? input : pathToFileURL(path.resolve(input)).href
await page.goto(url, { waitUntil: 'networkidle' })
await page.evaluate(() => document.fonts && document.fonts.ready)
const duration = (await page.evaluate(() => window.__duration)) ?? opt('duration', 5)
const frames = Math.round(duration * fps)
console.log(`Rendering ${frames} frames @ ${fps}fps, ${width}x${height}, ${duration}s -> ${output}`)

const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', output], { stdio: ['pipe', 'inherit', 'inherit'] })
const done = new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error(`ffmpeg exit ${c}`))))

for (let f = 0; f < frames; f++) {
  const t = f / fps
  await page.evaluate(async (t) => {
    if (typeof window.__seek === 'function') { await window.__seek(t) } else {
      for (const a of document.getAnimations()) { a.pause(); a.currentTime = t * 1000 }
    }
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))
  }, t)
  const buf = await page.screenshot({ type: 'png' })
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r))
  if (f % fps === 0) process.stdout.write(`\r${Math.round((f / frames) * 100)}%`)
}
ff.stdin.end()
await done
await browser.close()
console.log(`\rDone: ${output}`)
