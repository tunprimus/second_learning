//@ts-check
'use strict';

const VERSION = '0.0.1';
const CACHE_KEYS = {
	MAIN: `main-${VERSION}`,
};

// URLs that should be cached when the worker is installed
const PRE_CACHE_URLS = ['/', '/css/global.css', '/js/app.js'];

/**
 * Takes an array of strings and puts them in a named cache store
 *
 * @param {string} cacheName
 * @param {array} items=[]
 */
function addItemsToCache(cacheName, items = []) {
	return caches.open(cacheName).then(function (cache) {
		return cache.addAll(items);
	});
}

self.addEventListener('install', function (evt) {
	self.skipWaiting();

	addItemsToCache(CACHE_KEYS.MAIN, PRE_CACHE_URLS);
});

self.addEventListener('activate', function (evt) {
	// Look for any old caches that don't match our set and clear them out
  evt.waitUntil(
		caches
			.keys()
			.then(function(cacheNames) {
				return cacheNames.filter(function(item) {
					return !Object.values(CACHE_KEYS).includes(item);
				})
			})
			.then(function(itemsToDelete) {
				return Promise.all(itemsToDelete.map(function(item) {
					return caches.delete(item);
				}));
			})
			.then(function() {
				return self.clients.claim()
			})
	);
});

self.addEventListener('fetch', function(evt) {
	return evt.respondWith(caches.match(evt.request).then(function(cachedResponse) {
		// Item found in cache so return
		if (cachedResponse) {
			return cachedResponse;
		}

		// Nothing found so load up the request from the network
		return caches.open(CACHE_KEYS.MAIN).then(function(cache) {
			return fetch(evt.request)
				.then(function(response) {
					// Put the new response in cache and return it
					return cache.put(evt.request, response.clone()).then(function() {
						return response;
					})
				})
				.catch(function(excp) {
					return;
				});
		})
	}));
});
