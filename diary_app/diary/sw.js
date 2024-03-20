// Cache name
const CACHE_NAME = 'pwa-diary-v1';
// Cache targets
const urlsToCache = [
  '/diary_app/diary/templates/diary_app/home.html',
  '/diary_app/diary/templates/diary_app/graph.html',
  '/diary_app/diary/static/css/contents.css',
  '/diary_app/diary/static/css/control.css',
  '/diary_app/diary/static/js/diary.js',
  // '/bbs/static/images/chat.png'
];

self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache.map(url => new Request(url, {credentials: 'same-origin'})));
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
