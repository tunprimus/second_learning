//@ts-check
'use strict';

/*
Adapted from: Promise based Web Worker Messaging --> https://muffinman.io/blog/web-workers-promises/
*/

// Worker initialisation
const worker = new Worker("worker.js");

// Map of promises
const promises = {};

worker.addEventListener("message", function (evt) {
	// Listen to worker messages and find the correct promise matching the id
  // Then resolve or reject it depending on the response
	if (evt.data.error) {
		promises[evt.data.id].reject(evt.data.error);
	} else {
		promises[evt.data.id].resolve(evt.data.result);
	}

	// Remove the resolver reference
	delete promises[evt.data.id];
});

// For identifiers it is safe to use a simple integer which will increment every time user sends a new message
let id = 0;

// The main method which returns a promise
function sendToWorker (data) {
	// Return a promise
	return new Promise((resolve, reject) => {
		// Add the resolver to the map
		promises[id] = {resolve, reject};

		// Send the message to the worker
		worker.postMessage({id, data});

		// Increment the id
		id++;
	});
}
