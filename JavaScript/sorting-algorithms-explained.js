//@ts-check

'use strict';

const ARRAY_TO_SORT = [8, 3, 5, 1, 4, 2, 1, 4, 1, 2, 7, 5, 2];

/**
 * @description
 * Say you have a list of integers from 0 to 5:

	input = [2, 5, 3, 1, 4, 2]

	First, you need to create a list of counts for each unique value in
	the `input` list. Since you know the range of the `input` is from 0 to
	5, you can create a list with five placeholders for the values 0 to 5,
	respectively:

	count = [0, 0, 0, 0, 0, 0]
		# val: 0  1  2  3  4  5

	Then, you go through the `input` list and iterate the index for each value by one.

	For example, the first value in the `input` list is 2, so you add one
	to the value at the second index of the `count` list, which represents
	the value 2:

	count = [0, 0, 1, 0, 0, 0]
		# val: 0  1  2  3  4  5

	The next value in the `input` list is 5, so you add one to the value at
	the last index of the `count` list, which represents the value 5:

	count = [0, 0, 1, 0, 0, 1]
		# val: 0  1  2  3  4  5

	Continue until you have the total count for each value in the `input`
	list:

	count = [0, 1, 2, 1, 1, 1]
		# val: 0  1  2  3  4  5

	Finally, since you know how many times each value in the `input` list
	appears, you can easily create a sorted `output` list. Loop through
	the `count` list, and for each count, add the corresponding value
	(0 - 5) to the `output` array that many times.

	For example, there were no 0's in the `input` list, but there was one
	occurrence of the value 1, so you add that value to the `output` array
	one time:

	output = [1]

	Then there were two occurrences of the value 2, so you add those to the
	`output` list:

	output = [1, 2, 2]

	And so on until you have the final sorted `output` list:

	output = [1, 2, 2, 3, 4, 5]

	@description
	Properties
		- Space complexity: O(k)
		- Best case performance: O(n+k)
		- Average case performance: O(n+k)
		- Worst case performance: O(n+k)
		- Stable: Yes (k is the range of the elements in the array)
 */
function countingSort() {
	let numbers = [1, 4, 1, 2, 7, 5, 2];
	let count = [];
	let output = [];
	let i;
	let max = Math.max(...numbers);

	// Initialise counter
	for (i = 0; i <= max; i++) {
		count[i] = 0;
	}

	// Initialise output array
	for (i = 0; i < numbers.length; i++) {
		output[i] = 0;
	}

	for (i = 0; i < numbers.length; i++) {
		count[numbers[i]]++;
	}

	for (i = 1; i < count.length; i++) {
		count[i] += count[i - 1];
	}

	for(i = numbers.length - 1; i >= 0; i--) {
		output[--count[numbers[i]]] = numbers[i];
	}

	// Output sorted array
	console.log(output);

	/** for(i = 0; i < output.length; i++) {
		console.log(output[i]);
	} */
}
countingSort()


/**
 * @description
 * Insertion sort is a simple sorting algorithm for a small number of elements.
 * In Insertion sort, you compare the key element with the previous elements. If the previous elements are greater than the key element, then you move the previous element to the next position.
 * Start from index 1 to size of the input array. [ 8 3 5 1 4 2 ]
 * 
 * Step 1 :
 * key = 3 //starting from 1st index.

      Here `key` will be compared with the previous elements.

      In this case, `key` is compared with 8. since 8 > 3, move the element 8
      to the next position and insert `key` to the previous position.

      Result: [ 3 8 5 1 4 2 ]
 * 
		Step 2 :
 *	key = 5 //2nd index

      8 > 5 //move 8 to 2nd index and insert 5 to the 1st index.

      Result: [ 3 5 8 1 4 2 ]
 *
 * Step 3 :
 *   key = 1 //3rd index

      8 > 1     => [ 3 5 1 8 4 2 ]  

      5 > 1     => [ 3 1 5 8 4 2 ]

      3 > 1     => [ 1 3 5 8 4 2 ]

      Result: [ 1 3 5 8 4 2 ]
 * 
 * Step 4 :
 *  key = 4 //4th index

      8 > 4   => [ 1 3 5 4 8 2 ]

      5 > 4   => [ 1 3 4 5 8 2 ]

      3 > 4   ≠>  stop

      Result: [ 1 3 4 5 8 2 ]
 * 
 * Step 5 :
 *  key = 2 //5th index

      8 > 2   => [ 1 3 4 5 2 8 ]

      5 > 2   => [ 1 3 4 2 5 8 ]

      4 > 2   => [ 1 3 2 4 5 8 ]

      3 > 2   => [ 1 2 3 4 5 8 ]

      1 > 2   ≠> stop

      Result: [1 2 3 4 5 8]
 * 
 * @param {number[]} arr Array of numbers
 * @returns {number[]} Array of numbers
 */
function insertionSort(arr) {
	let len = arr.length;
	let i = 1;

	while (i < len) {
		let buffer = arr[i];
		let j = i - 1;
		while (j >= 0 && arr[j] > buffer) {
			arr[j + 1] = arr[j];
			j--;
		}
		arr[j + 1] = buffer;
		i++;
	}
	return arr;
}
console.log(insertionSort(ARRAY_TO_SORT));
