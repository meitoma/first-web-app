// Cache name
const CACHE_NAME = 'pwa-sample-caches-v2';
// Cache targets
const urlsToCache = [
  './templates/bbs_app/layout_bbs.html',
  // './templates/layout_login.html',
  // './templates/layout.html',
  // './templates/bbs.html',
  // './templates/home.html',
  // './templates/confirm.html',
  // './templates/comp_load.html ',
  // './templates/login.html',
  // '/bbs/static/css/login.css',
  // '/bbs/static/css/sp_bbs.css',
  // '/bbs/static/css/pc_bbs.css',
  // '/bbs/static/js/bbs.js',
  // '/bbs/static/js/login.js',
  // '/bbs/static/images/chat.png'
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

self.addEventListener('push', function (event) {
  // メッセージを表示する
  var data = {};
  if (event.data) {
    data = event.data.json();
  }
  var title = data.notification.title || "無題";
  var message = data.notification.body || "メッセージが届いています。";
  event.waitUntil(
    self.registration.showNotification(title, {
      'body': message
    })
  );
});
self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  clients.openWindow("/");
}, false);
