//@ts-check
'use strict';

class Graph {
	constructor(numOfVertices) {
		this.numOfVertices = numOfVertices;
		this.adjList = new Map();
	}

	addVertex(vertex) {
		this.adjList.set(vertex, []);
	}

	addEdge(src, dest) {
		this.adjList.get(src).push(dest);
		this.adjList.get(dest).push(src);
	}

	printGraph() {
		var getKeys = this.adjList.keys();
		for (var i of getKeys) {
			var getValues = this.adjList.get(i);
			var conjoined = '';
			for (var j of getValues) {
				conjoined += j + ' ';
				// console.log(i + ' -> ' + conjoined);
			}
			console.log(i + ' -> ' + conjoined);
		}
	}

	bfs(startingNode) {
		var visited = {};
		var currentQueue = new Queue();
		visited[startingNode] = true;
		currentQueue.enqueue(startingNode);
		while (!currentQueue.isEmpty()) {
			var getQueueElement = currentQueue.dequeue();
			console.log(getQueueElement);
			var getList = this.adjList.get(getQueueElement);
			for (var i in getList) {
				var neighbour = getList[i];
				if (!visited[neighbour]) {
					visited[neighbour] = true;
					currentQueue.enqueue(neighbour);
				}
			}
		}
	}

	dfs(startingNode) {
		var visited = {};
		this.DFSUtil(startingNode, visited);
	}

	DFSUtil(vertex, visited) {
		visited[vertex] = true;
		console.log(vertex);
		var getNeighbours = this.adjList.get(vertex);
		for (var i in getNeighbours) {
			var getElement = getNeighbours[i];
			if (!visited[getElement]) {
				this.DFSUtil(getElement, visited);
			}
		}
	}
}

var test01 = new Graph(6);
var vertices = ['A', 'B', 'C', 'D', 'E', 'F'];
for (var i = 0; i < vertices.length; i++) {
	test01.addVertex(vertices[i]);
}

test01.addEdge('A', 'B');
test01.addEdge('A', 'D');
test01.addEdge('A', 'E');
test01.addEdge('B', 'C');
test01.addEdge('D', 'E');
test01.addEdge('E', 'F');
test01.addEdge('E', 'C');
test01.addEdge('C', 'F');

test01.printGraph();
