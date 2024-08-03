//@ts-check

'use strict';

const ARRAY_TO_SORT_1 = [8, 3, 5, 1, 4, 2, 1, 4, 1, 2, 7, 5, 2];
const ARRAY_TO_SORT_2 = [16, 6, 10, 2, 8, 4, 2, 8, 2, 4, 14, 10, 4];
const ARRAY_TO_SORT_3 = [6, 1, 3, -1, 2, 0, -1, 2, -1, 0, 5, 3, 0];
const ARRAY_TO_SORT_4 = [1, 4, 7, 45, 7, 43, 44, 25, 6, 4, 6, 9];
const ARRAY_TO_SORT_5 = [6, 2, 5, 3, 8, 7, 1, 4];


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
	@param {number[]} [arr=[]] An optional array of numbers
 */
function countingSort(arr = []) {
	let numbers;
	if (arr.length === 0) {
		numbers = [1, 4, 1, 2, 7, 5, 2];
	} else {
		numbers = arr;
	}
	
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
	return output;
}
console.log(countingSort());
console.log(countingSort(ARRAY_TO_SORT_1));


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
console.log(insertionSort(ARRAY_TO_SORT_2));

/**
 * 
 * @param {number[]} arr Array of numbers
 * @param {number} x Index
 * @param {number} y Index
 */
function swap(arr, x, y) {
	let temp = arr[x];
	arr[x] = arr[y];
	arr[y] = temp;
}

/**
 * @description
 * Here's how it works:

Find the smallest element in the array and swap it with the first element.
Find the second smallest element and swap with with the second element in the array.
Find the third smallest element and swap wit with the third element in the array.
Repeat the process of finding the next smallest element and swapping it into the correct position until the entire array is sorted.
 * But, how would you write the code for finding the index of the second smallest value in an array?

An easy way is to notice that the smallest value has already been swapped into index 0, so the problem reduces to finding the smallest element in the array starting at index 1.

Selection sort always takes the same number of key comparisons — N(N − 1)/2.
 * Properties
		- Space Complexity:  O(n)
		- Time Complexity:  O(n2)
		- Sorting in Place:  Yes
		- Stable:  No
 * @param {number[]} arr Array of number
 * @returns {number[]} Array of number
 */
function selectionSort(arr) {
	let len = arr.length;
	for (let i = 0; i < len - 1; i++) {
		let jMin = i;
		for (let j = i + 1; j < len; j++) {
			if (arr[j] < arr[jMin]) {
				jMin = j;
			}
		}
		if (jMin !== i) {
			swap(arr, i, jMin);
		}
	}

	return arr;
}
console.log(selectionSort(ARRAY_TO_SORT_3));


/**
 * @description
 * With a worst-case complexity of O(n^2), bubble sort is very slow compared to other sorting algorithms like quicksort. The upside is that it is one of the easiest sorting algorithms to understand and code from scratch.
 * 
 * Properties
		- Space complexity: O(1)
		- Best case performance: O(n)
		- Average case performance: O(n*n)
		- Worst case performance: O(n*n)
		- Stable: Yes
 * 
 * @param {number[]} arr Array of numbers
 * @returns {number[]} Array of numbers
 */
function bubbleSort(arr) {
	let sorted = false;

	while (!sorted) {
		sorted = true;
		for (let i = 0; i < arr.length; i++) {
			if (arr[i] < arr[i - 1]) {
				let temp = arr[i];
				arr[i] = arr[i - 1];
				arr[i - 1] = temp;
				sorted = false;
			}
		}
	}

	return arr;
}
console.log(bubbleSort(ARRAY_TO_SORT_4));


function partitionArray(arr, start, end) {
	let pivot = end;
	// Set i to start - 1 so that it can access the first index in the event that the value at arr[0] is greater than arr[pivot]
  // Succeeding comments will expound upon the above comment
	let i = start - 1;
	let j = start;

	 // Increment j up to the index preceding the pivot
	while (j < pivot) {
		// If the value is greater than the pivot increment j
		if (arr[j] > arr[pivot]) {
			j++;
		} else { // When the value at arr[j] is less than the pivot:
			// increment i (arr[i] will be a value greater than arr[pivot]) and swap the value at arr[i] and arr[j]
			i++;
			swap(arr, j, i);
			j++;
		}
	}

	// The value at arr[i + 1] will be greater than the value of arr[pivot]
	swap(arr, i + 1, pivot);

	// You return i + 1, as the values to the left of it are less than arr[i+1], and values to the right are greater than arr[i + 1]
  // As such, when the recursive quicksorts are called, the new sub arrays will not include this the previously used pivot value
	return i + 1;
}

/**
 * 
 * @description
 * Quick sort is an efficient divide and conquer sorting algorithm. Average case time complexity of Quick Sort is O(nlog(n)) with worst case time complexity being O(n^2) depending on the selection of the pivot element, which divides the current array into two sub arrays.

For instance, the time complexity of Quick Sort is approximately O(nlog(n)) when the selection of pivot divides original array into two nearly equal sized sub arrays.

On the other hand, if the algorithm, which selects of pivot element of the input arrays, consistently outputs 2 sub arrays with a large difference in terms of array sizes, quick sort algorithm can achieve the worst case time complexity of O(n^2).

The steps involved in Quick Sort are:

Choose an element to serve as a pivot, in this case, the last element of the array is the pivot.
Partitioning: Sort the array in such a manner that all elements less than the pivot are to the left, and all elements greater than the pivot are to the right.
Call Quicksort recursively, taking into account the previous pivot to properly subdivide the left and right arrays. (A more detailed explanation can be found in the comments below)
 * 
 * Properties
 * Best, average, worst, memory: n log(n)n log(n)n 2log(n). It's not a stable algorithm, and quicksort is usually done in-place with O(log(n)) stack space.

The space complexity of quick sort is O(n). This is an improvement over other divide and conquer sorting algorithms, which take O(n log(n)) space.
 * 
 * @param {number[]} arr Array of numbers
 * @param {number} start Index
 * @param {number} end Index
 * @returns {number[]} Array of numbers
 */
function quickSort(arr, start = 0, end = arr.length - 1) {
	if (start < end) {
		let pivot = partitionArray(arr, start, end);

		quickSort(arr, start, pivot - 1);
		quickSort(arr, pivot + 1, end);
	}

	return arr;
}
console.log('\n======= Quick Sort Start =======\n');
console.log(quickSort(ARRAY_TO_SORT_1));
console.log(quickSort(ARRAY_TO_SORT_2));
console.log(quickSort(ARRAY_TO_SORT_3));
console.log(quickSort(ARRAY_TO_SORT_4));
console.log(quickSort(ARRAY_TO_SORT_5));
console.log('\n======= End Quick Sort =======\n');
