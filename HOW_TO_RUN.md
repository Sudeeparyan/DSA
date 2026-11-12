# How to run the site

This guide is for beginners. You do not need to know JavaScript.

## 1. Install Node.js (and Python, only to change lessons)

1. Download the **LTS** version from https://nodejs.org and install it with the default options.
2. Open a terminal (Windows: PowerShell, Mac: Terminal) and check:

```bash
node -v
npm -v
```

You only need Python (3.10 or newer, from https://www.python.org) if you want to change or
rebuild the lessons. The built lessons are already in `content/lessons/`.

## 2. Install and start

```bash
cd path/to/DSA
npm install        # one time
npm run dev
```

Open **http://localhost:3000**. Leave the terminal open while you study; `Ctrl+C` stops it.

## 3. Using a lesson

- **Next step →** / **← Back**, or the arrow keys, move one step. **Space** plays or pauses.
- Drag the 3D stage to look around it; click it, then scroll to zoom. On a phone, swipe sideways
  to rotate and pinch to zoom (an up/down swipe scrolls the page as usual). **Reset view** puts the
  camera back.
- **Full screen** (or the **F** key) gives the stage the whole screen; useful for the busier lessons.
- A link can open a lesson at a given step: `/problem/two-sum/?step=7`.
- Tick **I understand this one** at the bottom; the home page shows your progress and a
  **Continue** button.

## 4. Useful commands

| Command | What it does |
| --- | --- |
| `npm run dev` | Start the site locally |
| `npm run build` | Build the static site into `out/` |
| `npm test` | Check all 150 lesson files, plus the app's unit tests |
| `npm run lessons` | Rebuild the lesson files after changing `lessons/specs/` (needs Python) |
| `npm run lessons:verify` | Test every solution against a brute-force reference on random inputs |
| `npm run check` | Everything above, plus type check and lint. Run it before you commit |

The Python commands find Python by themselves (`python`, `python3` or `py`), so they work the same
on Windows, macOS and Linux.

How to change a lesson: **[docs/LESSONS.md](./docs/LESSONS.md)**.
How the code is organised: **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)**.

**If `npm run dev` shows an error page right after `npm run build`**, stop it, delete the `.next`
folder and start it again: the two commands share that folder.

## 5. Deploy for free

**Vercel**: push the repo to GitHub, import it at https://vercel.com, click **Deploy**.

**GitHub Pages**: run `npm run build` and publish the `out/` folder (Settings → Pages, or an
Actions workflow that uploads `out/`).

## 6. Offline use

After you open the deployed site once, it keeps working without internet: the home page and every
lesson you have opened before are saved on the device. Opening a lesson you have never visited
needs a connection the first time. Progress is saved in the browser (`localStorage`) on that device.
