//@ts-check
'use strict';

class State extends EventTarget {
	constructor(initialValue) {
		super();
		this._value = initialValue;
	}

	get value() {
		return this._value;
	}

	update(newValue) {
		this._value = newValue;
		this.dispatchEvent(new CustomEvent('change', {detail: this._value}));
	}

	subscribe(cb, opt) {
		function handler(evt) {
			cb(evt.detail);
		}

		this.addEventListener('change', handler, opt);

		return function () {
			this.removeEventListener('change', handler, opt);
		}
	}
}

const count = new State(0);

function handleChange(evt) {
	console.log(`Count is now ${evt.detail}`);
}

count.addEventListener('change', handleChange);

count.update(10);

count.removeEventListener('change', handleChange);

const count01 = new State(0);

// Only get 1 value
count01.subscribe(function (value) {
	console.log(value);
}, {once: true});

// Abortable event
const controller = new AbortController();

count01.subscribe(function (value) {
	console.log(value);
}, {signal: controller.signal});

// Unsubscribable
const unsubscribeFromCount = count01.subscribe(function (value) {
	console.log(value);
}, {signal: controller.signal});

count01.update(10);

unsubscribeFromCount();

controller.abort();
