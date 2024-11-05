//@ts-check
'use strict';

const recordButton = document.querySelectorAll('.record')[0];
const stopButton = document.querySelectorAll('.stop')[0];
const soundClips = document.querySelectorAll('.sound-clips')[0];
const canvas = document.querySelectorAll('.visualiser')[0];
const mainControls = document.querySelectorAll('.main-controls')[0];

// Disable stop button while not recording
stopButton.disabled = true;

// Visualiser setup - create web audio api context and canvas
let audioCtx;
const canvasCtx = canvas.getContext('2d');

// Main block for doing the audio recording
if (navigator.mediaDevices.getUserMedia) {
	console.log('getUserMedia supported.');

	const constraints = { audio: true };
	let chunks = [];

	let onSuccess = function(stream) {
		const mediaRecorder = new MediaRecorder(stream);

		visualise(stream);

		recordButton.onclick = function() {
			mediaRecorder.start();
			console.log(mediaRecorder.state);
			console.log('recorder started');
			recordButton.style.background = 'red';

			stopButton.disabled = false;
			recordButton.disabled = true;
		};

		stopButton.onclick = function() {
			mediaRecorder.stop();
			console.log(mediaRecorder.state);
			console.log('recorder stopped');
			recordButton.style.background = '';
			recordButton.style.color = '';
			// mediaRecorder.requestData();

			stopButton.disabled = true;
			recordButton.disabled = false;
		};

		mediaRecorder.onstop = function(evt) {
			console.log('Data available after MediaRecorder.stop() called.');

			const clipName = prompt('Enter a name for your sound clip?', 'My unnamed clip');

			const clipContainer = document.createElement('article');
			const clipLabel = document.createElement('p');
			const audio = document.createElement('audio');
			const deleteButton = document.createElement('button');

			clipContainer.classList.add('clip');
			clipLabel.classList.add('clip__text');
			audio.setAttribute('controls', '');
			audio.classList.add('audio');
			deleteButton.textContent = 'Delete';
			deleteButton.className = 'delete';
			deleteButton.classList.add('button__delete');

			if (clipName === null) {
				clipLabel.textContent = 'My unnamed clip';
			} else {
				clipLabel.textContent = clipName;
			}

			clipContainer.appendChild(audio);
			clipContainer.appendChild(clipLabel);
			clipContainer.appendChild(deleteButton);
			soundClips.appendChild(clipContainer);

			audio.controls = true;
			const blob = new Blob(chunks, { 'type': 'audio/ogg; codecs=opus' });
			chunks = [];
			const audioURL = window.URL.createObjectURL(blob);
			audio.src = audioURL;
			console.log('recorder stopped');

			deleteButton.onclick = function(evt) {
				let evtTgt = evt.target;
				evtTgt.parentNode.parentNode.removeChild(evtTgt.parentNode);
			};

			clipLabel.onclick = function() {
				const existingName = clipLabel.textContent;
				const newClipName = prompt('Enter a new name for your sound clip?');
				if (newClipName === null) {
					clipLabel.textContent = existingName;
				} else {
					clipLabel.textContent = newClipName;
				}
			}
		};

		mediaRecorder.ondataavailable = function(evt) {
			chunks.push(evt.data);
		};
	}

	let onError = function(err) {
		console.error('The following error occurred: ' + err);
	};

	navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);
} else {
	console.log('getUserMedia not supported on your browser!');
}

function visualise(stream) {
	if (!audioCtx) {
		audioCtx = new AudioContext();
	}

	const source = audioCtx.createMediaSource(stream);

	const analyser = audioCtx.createAnalyser();
	analyser.fftSize = 2048;
	const bufferLength = analyser.frequencyBinCount;
	const dataArray = new Uint8Array(bufferLength);

	source.connect(analyser);
	// analyser.connect(audioCtx.destination);

	draw();

	function draw() {
		const WIDTH = canvas.width;
		const HEIGHT = canvas.height;

		requestAnimationFrame(draw);

		analyser.getByteTimeDomainData(dataArray);

		canvasCtx.fillStyle = 'rgb(200, 200, 200)';
		canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

		canvasCtx.lineWidth = 2;
		canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

		canvasCtx.beginPath();

		let sliceWidth = WIDTH * 1.0 / bufferLength;
		let x = 0;

		for (let i = 0; i < bufferLength; i++) {
			let v = dataArray[i] / 128.0;
			let y = v * HEIGHT / 2;

			if (i === 0) {
				canvasCtx.moveTo(x, y);
			} else {
				canvasCtx.lineTo(x, y);
			}

			x += sliceWidth;
		}

		canvasCtx.lineTo(canvas.width, canvas.height / 2);
		canvasCtx.stroke();
	}
}

window.onresize = function() {
	canvas.width = mainControls.offsetWidth;
};

window.onresize();
