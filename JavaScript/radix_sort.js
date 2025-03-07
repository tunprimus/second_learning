//@ts-check
'use strict';

/**
 * Function to get the digit at a specific place
 *
 * @param {number} num
 * @param {number} place
 * @returns {number}
 */
function getDigit(num, place) {
	// Calculate the absolute value of the number
	const absNum = Math.abs(num);

	// Divide the number by 10 raised to the power of the place
	const digit = Math.floor(absNum / Math.pow(10, place)) % 10;

	// Return the digit
	return digit;
}


/**
 * Function to count the number of digits in a number
 *
 * @param {number} num
 * @returns {number}
 */
function digitCount(num) {
	// If number is 0, return 1
	if (num === 0) {
		return 1;
	}

	// Otherwise, calculate the logarithm of the absolute value of the number and add 1 to get the number of digits
	return (Math.floor(Math.log10(Math.abs(num))) + 1);
}


/**
 * Description placeholder
 *
 * @param {number[]} nums
 * @returns {number}
 */
function mostDigits(nums) {
	// Initialise the maximum number of digits to 0
	let maxDigits = 0;

	// Iterate through the array of numbers
	for (const num of nums) {
		// Calculate the number of digits in the current number
		const numDigits = digitCount(num);
		// Update the maximum number of digits if the current number has more digits
		maxDigits = Math.max(maxDigits, numDigits);
	}

	// Return the maximum number of digits
	return maxDigits;
}

/**
 * Function to perform counting sort on an array of numbers based on a specific place
 *
 * @param {number[]} input
 * @param {number} place
 * @returns {number[]}
 */
function countingSort(input, place) {
	// Create an output array to store the sorted numbers
	const output = new Array(input.length);

	// Create a count array to store the count of each digit (0 - 9)
	const count = new Array(10).fill(0);

	// Iterate through the array of numbers
	for (const num of input) {
		// Get the digit at the specified place in the current number
		const digit = getDigit(num, place);
		// Increment the count of the digit
		count[digit]++;
	}

	// Update the count array to contain the cumulative count of each digit
	for (let i = 0; i < 10; i++) {
		count[i] += count[i - 1];
	}

	// Iterate through the array of numbers in reverse order
	for (let i = input.length - 1; i >= 0; i--) {
		// Get the digit at the specified place in the current number
		const digit = getDigit(input[i], place);

		// Calculate the index of the current number in the output array at the calculated index
		const index = count[digit] - 1;

		// Store the current number in the output array at the calculated index
		output[index] = input[i];

		// Decrement the count of the digit
		count[digit]--;
	}

	// Return the output array
	return output;
}


/**
 * Function to radix sort an array
 *
 * @param {number[]} input
 * @returns {number[]}
 */
function radixSort(input) {
	// Find the smallest element (to account for negative numbers)
	const min = Math.min(...input);

	// Shift all values in the input array by the min value
	input = input.map(function (val) {
		return val - min;
	});

	// Find the maximum element in the input array
	const max = Math.max(...input);

	// Find the maximum number of digits in the array of numbers
	const maxLength = mostDigits(input);

	// Iterate through the digits from 0 to the maximum number of digits
	for (let digit = 0; digit < maxLength; digit++) {
		// Perform counting sort on the array of numbers based on the current digit
		input = countingSort(input, digit);
	}

	// Having accounted for the minimum value, shift all values back
	input = input.map(function (val) {
		return val + min;
	});

	// Return the sorted array of numbers
	return input;
}
