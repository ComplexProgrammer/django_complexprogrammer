/* Complex Programmer — service worker.
 * - Sahifalar va test ma'lumotlari: avval tarmoq, internet bo'lmasa — keshdan
 *   (bir marta ochilgan avtotest biletlari internetsiz ham ishlaydi).
 * - /static/ fayllari: avval kesh (tez yuklanadi).
 */
const VERSION = "cp-v2";
const PAGES = VERSION + "-pages";
const ASSETS = VERSION + "-assets";
const PRECACHE = ["/", "/avtotest/", "/offline/"];
const NEVER_CACHE = ["/admin", "/send_file", "/remove_file", "/add-comment", "/i18n/", "/search/"];
const MAX_PAGE_ENTRIES = 150;

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(PAGES).then((c) => c.addAll(PRECACHE)).catch(() => {}));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => !k.startsWith(VERSION)).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

async function trim(cacheName, max) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();
  for (let i = 0; i < keys.length - max; i++) await cache.delete(keys[i]);
}

async function networkFirst(request) {
  const cache = await caches.open(PAGES);
  try {
    const response = await fetch(request);
    if (response.status === 200 && response.type === "basic") {
      cache.put(request, response.clone());
      trim(PAGES, MAX_PAGE_ENTRIES);
    }
    return response;
  } catch (err) {
    const cached = await cache.match(request);
    if (cached) return cached;
    if (request.mode === "navigate") return (await cache.match("/offline/")) || Response.error();
    throw err;
  }
}

async function cacheFirst(request) {
  const cache = await caches.open(ASSETS);
  const cached = await cache.match(request);
  if (cached) return cached;
  const response = await fetch(request);
  if (response.status === 200 && !request.headers.has("range")) cache.put(request, response.clone()).catch(function () {});
  return response;
}

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  if (NEVER_CACHE.some((p) => url.pathname.startsWith(p))) return;

  if (url.pathname.startsWith("/static/") || url.pathname.startsWith("/media/")) {
    event.respondWith(cacheFirst(request));
  } else {
    event.respondWith(networkFirst(request));
  }
});
