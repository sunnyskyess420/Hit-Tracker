// Service Worker for Sunnys Hit Tracker — offline-first PWA
const CACHE_NAME = 'sunnys-hit-tracker-v1';
const ASSETS = [
  './',
  './index.html',
  './hit-tracker.html',
  './manifest.json',
  './icon-192.png',
  './icon-256.png',
  './icon-512.png',
  './weed-bg.png',
  './lighting-weed.mp3'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE_NAME).then((c) => c.addAll(ASSETS)));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  // Network-first for CDN (Chart.js) so updates come through, with cache fallback
  if (url.hostname === 'cdn.jsdelivr.net' || url.hostname === 'cdnjs.cloudflare.com') {
    e.respondWith(
      fetch(e.request).catch(() => caches.match(e.request))
    );
    return;
  }
  // Cache-first for app shell and local assets
  e.respondWith(
    caches.match(e.request).then((cached) => cached || fetch(e.request))
  );
});