//@ts-check

/**
 * @example
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

	@example
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
	for(i = 0; i < output.length; i++) {
		console.log(output[i]);
	}
}
countingSort()
