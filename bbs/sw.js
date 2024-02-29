// Cache name
const CACHE_NAME = 'pwa-sample-caches-v1';
// Cache targets
const urlsToCache = [
  './templates/layout_bbs.html',
  './templates/layout_login.html',
  './templates/layout.html',
  './templates/bbs.html',
  './templates/home.html',
  './templates/confirm.html',
  './templates/comp_load.html ',
  './templates/login.html',
  '/bbs/static/css/login.css',
  '/bbs/static/css/sp_bbs.css',
  '/bbs/static/css/pc_bbs.css',
  '/bbs/static/js/bbs.js',
  '/bbs/static/js/login.js',
  '/bbs/static/images/chat.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches
      .match(event.request)
      .then((response) => {
        return response ? response : fetch(event.request);
      })
  );
});
