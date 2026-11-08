# How to run NeetCode 150 Learn

This guide is for beginners. You do not need to know JavaScript.

## 1. Install Node.js

1. Open https://nodejs.org
2. Download the **LTS** version for your computer.
3. Install it with the default options.
4. Open a terminal (Mac: Terminal, Windows: PowerShell) and check:

```bash
node -v
npm -v
```

You should see version numbers. If not, restart the terminal and try again.

## 2. Open the project folder

```bash
cd path/to/DSA
```

## 3. Install dependencies (one time)

```bash
npm install
```

Wait until it finishes. This downloads the libraries the website needs.

## 4. Start the learning site

```bash
npm run dev
```

Then open your browser to:

**http://localhost:3000**

Leave the terminal open while you study. Press `Ctrl+C` to stop the server.

## 5. Useful commands

| Command | What it does |
| --- | --- |
| `npm run dev` | Start local website |
| `npm run build` | Build a static site into the `out/` folder |
| `npm test` | Run automated checks |
| `npm run content:validate` | Check all 150 problem files |

## 6. Deploy for free

### Option A — Vercel

1. Push this repo to GitHub.
2. Go to https://vercel.com and sign in with GitHub.
3. Click **Add New Project** → import this repo.
4. Click **Deploy**. Vercel detects Next.js automatically.

### Option B — GitHub Pages

1. Run `npm run build` (creates `out/`).
2. Publish the `out/` folder to GitHub Pages (Settings → Pages → deploy from a branch/folder, or use an Actions workflow that uploads `out/`).

## 7. Offline use

After you open the site once on a device (production / deployed build), the service worker caches pages so you can keep studying without internet while travelling.

Progress, notes, and revision cards are saved in your browser (`localStorage`) on that device.
