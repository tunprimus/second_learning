//@ts-check
'use strict';

function getContrast50(hexColour) {
	// If a leading # is provided, remove it
	if (hexColour.slice(0, 1) === '#') {
		hexColour = hexColour.slice(1);
	}

	// If a three-character hex-code, make six-character
	if (hexColour.length === 3) {
		hexColour = hexColour.split('').map(function (hex) {
			return hex + hex;
		}).join('');
	}

	return (parseInt(hexColour, 16) > 0xFFFFFF/2) ? 'black': 'white';
}

/*!
 * Get the contrasting colour for any hex colour
 * (c) 2024 tunprimus
 * Derived from work by Chris Ferdinandi, https://gomakethings.com
 * Derived from work by Brian Suda, https://24ways.org/2010/calculating-color-contrast/
 * @param  {string} hexColour - A hex-colour value
 * @param  {number} contrastLevel - A contrast level value
 * @return {string} The contrasting colour (black or white)
 */
function getContrastYIQ(hexColour, contrastLevel=128) {
	// If a leading # is provided, remove it
	if (hexColour.slice(0, 1) === '#') {
		hexColour = hexColour.slice(1);
	}

	// If a three-character hex-code, make six-character
	if (hexColour.length === 3) {
		hexColour = hexColour.split('').map(function (hex) {
			return hex + hex;
		}).join('');
	}

	// Convert to RGB value
	let redHue = parseInt(hexColour.substr(0, 2), 16);
	let greenHue = parseInt(hexColour.substr(2, 2), 16);
	let blueHue = parseInt(hexColour.substr(4, 2), 16);

	// Get YIQ ratio
	let yiqRatio = (((redHue * 229) + (greenHue * 587) + (blueHue * 114)) / 1000);

	// Check contrast
	return (yiqRatio >= contrastLevel) ? 'black' : 'white';
}
