// Service Worker for Sunnys Hit Tracker - offline-first PWA
const CACHE_NAME = 'sunnys-hit-tracker-v5';
const ASSETS = [
  './',
  './index.html',
  './hit-tracker.html',
  './chart.umd.min.js',
  './manifest.json',
  './icon-192.png',
  './icon-256.png',
  './icon-512.png',
  './icon-512-maskable.png',
  './weed-bg.png',
  './hit-sound.wav'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      // Add individually so one missing file cannot block the whole install
      .then((c) => Promise.all(ASSETS.map((url) => c.add(url).catch(() => null))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);

  // Never intercept non-GET or cross-origin requests
  if (e.request.method !== 'GET' || url.origin !== self.location.origin) return;

  // Network-first for page loads: deploys show up immediately, offline still works from cache
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((c) => c.put(e.request, copy)).catch(() => {});
          return res;
        })
        .catch(() => caches.match(e.request).then((r) => r || caches.match('./index.html')))
    );
    return;
  }

  // Cache-first with background refresh for local assets (icons, sound, chart bundle)
  e.respondWith(
    caches.match(e.request).then((cached) => {
      const network = fetch(e.request).then((res) => {
        if (res && res.ok) {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((c) => c.put(e.request, copy)).catch(() => {});
        }
        return res;
      }).catch(() => cached);
      return cached || network;
    })
  );
});
