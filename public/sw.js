// Offline support for the lesson site.
//
// Pages and lesson data are fetched fresh whenever there is a network and fall
// back to the last saved copy when offline.  Only fingerprinted build assets
// (their file names change whenever their content does) are served cache-first.
const CACHE = "nc150-lessons-v2";
const PRECACHE = ["/", "/manifest.webmanifest"];
const IMMUTABLE = /^\/(_next\/static|fonts)\//;

// shown when a page that was never opened before is requested without a network
const OFFLINE_PAGE = `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Offline · NeetCode 150</title>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0b1018;color:#e8edf5;
font:17px/1.6 "Segoe UI",system-ui,sans-serif;padding:1.25rem;box-sizing:border-box}
main{max-width:30rem}h1{font-size:1.6rem;margin:0 0 .6rem}p{color:#a9b5c8;margin:0 0 1.2rem}
a{display:inline-block;padding:.65rem 1rem;border-radius:.7rem;background:#f7b731;color:#1c1400;
font-weight:600;text-decoration:none}</style></head><body><main><h1>You are offline</h1>
<p>This lesson has not been opened on this device yet, so there is no saved copy of it. Lessons you have
opened before still work offline.</p><a href="/">Back to all problems</a></main></body></html>`;

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE)
      .then((cache) => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener("activate", (event) => {
  // drop the caches of earlier versions so nobody keeps seeing old pages
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  if (IMMUTABLE.test(url.pathname)) {
    event.respondWith(
      caches.open(CACHE).then(async (cache) => {
        const cached = await cache.match(req);
        if (cached) return cached;
        const res = await fetch(req);
        if (res.ok) cache.put(req, res.clone());
        return res;
      }),
    );
    return;
  }

  event.respondWith(
    caches.open(CACHE).then(async (cache) => {
      try {
        const res = await fetch(req);
        if (res.ok) cache.put(req, res.clone());
        return res;
      } catch (err) {
        // a lesson opened at a step (?step=7) is the same page as the one without it
        const cached = await cache.match(req, { ignoreSearch: req.mode === "navigate" });
        if (cached) return cached;
        if (req.mode === "navigate") {
          return new Response(OFFLINE_PAGE, {
            status: 503,
            headers: { "content-type": "text/html; charset=utf-8" },
          });
        }
        throw err;
      }
    }),
  );
});
