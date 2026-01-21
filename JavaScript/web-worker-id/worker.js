//@ts-check
'use strict';

/*
Adapted from: Promise based Web Worker Messaging --> https://muffinman.io/blog/web-workers-promises/
*/

self.addEventListener("message", function (evt) {
	// Do your computations here

	// Send the result back along with id
	self.postMessage({
		id: evt.data.id,
		data: `Hello ${evt.data.data}`,
	});
});
