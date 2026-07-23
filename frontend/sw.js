const CACHE_NAME = "trainerapp-shell-v3";

const APP_SHELL = [
  "/",
  "/index.html",
  "/login.html",
  "/register.html",
  "/dashboard.html",
  "/planner.html",
  "/history.html",
  "/css/style.css",
  "/js/api.js",
  "/js/login.js",
  "/js/register.js",
  "/js/dashboard.js",
  "/js/planner.js",
  "/js/history.js",
  "/manifest.json",
  "/icons/icon-192.png",
  "/icons/icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))))
  );
  self.clients.claim();
});

function isApiRequest(pathname) {
  return (
    pathname === "/auth" ||
    pathname.startsWith("/auth/") ||
    pathname === "/workouts" ||
    pathname.startsWith("/workouts/") ||
    pathname === "/history" ||
    pathname.startsWith("/history/")
  );
}

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  if (event.request.method !== "GET" || url.origin !== self.location.origin) return;
  if (isApiRequest(url.pathname)) return;

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        const copy = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
