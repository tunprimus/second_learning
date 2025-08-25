#!/usr/bin/env python3
# Adapted from: How Trie Data Structures Work – Validate User Input with Automated Trie Visualisation -> https://www.freecodecamp.org/news/how-to-validate-user-input-with-automated-trie-visualization/
import httpx
import math
import matplotlib.pyplot as plt
import orjson
import pyvis
import random
from pyvis.network import Network

pyvis_major, pyvis_minor, pyvis_patch = pyvis.__version__.split(".")
pyvis_major, pyvis_minor, pyvis_patch = int(pyvis_major), int(pyvis_minor), int(pyvis_patch)

"""
The Trie data structure is a tree-like data structure that is used to store and retrieve information efficiently.

This is implemented with visualisation using pyvis

Example:

>>> tr_01 = Trie(("".join(chr(97 + int(j)) for j in str(i)) + str(k) for k in range(6) for i in range(6)))
>>> tr_01.to_graph()
>>>
>>> data = orjson.loads(httpx.get("https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json").content)
>>> data = list(data.keys())
>>>
>>> tr_02 = Trie(random.sample(data, 97))
>>> tr_02.to_graph()

"""

class TrieNode:
    def __init__(self, input_char):
        self.char = input_char
        self.is_end = False
        self.children = {}


class Trie():
    def __init__(self, starting_elements = None):
        self.root = TrieNode("")
        if starting_elements != None:
            for element in starting_elements:
                self.insert(element)

    def insert(self, word):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
        else:
            new_node = TrieNode(char)
            node.children[char] = new_node
            node = new_node
        node.is_end = True

    def search_and_split(self, x):
        node = self.root
        output = ["", ""]
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                return []
            output[1 if node.is_end else 0] += node.char
        return output if node.is_end else []

    def remove(self, root, word, index = 0):
        if not root:
            return None

        if index == len(word):
            if root.is_end:
                root.is_end = False
            if root.children == {}:
                del root
                root = None
            return root

        root.children[word[index]] = self.remove(root.children[word[index]], word, index + 1)

        if (root.children == {}) and not root.is_end:
            del root
            root = None

        return root

    def to_graph(self):
        """
        Visualise the Trie data structure as a directed graph after using a BFS.

        The graph is coloured in a way that the root node is red and the end of words are green.

        The graph is saved as "nx.html" in the current directory.

        Returns
        -------
        None
        """
        _graph = Network(directed=True)
        _graph.show_buttons()

        node_index = 1
        current_node = 0
        _queue = [self.root]
        _graph.add_node(current_node, label="", color="red")
        temp_labels = {0: ""}

        while _queue != []:
            _node = _queue.pop(0)
            for val in _node.children.values():
                if val:
                    temp_labels[node_index] = temp_labels[current_node] + val.char
                    _graph.add_node(node_index, label=temp_labels[current_node] + val.char, color="#48E073" if val.is_end else "blue")
                    _graph.add_edge(current_node, node_index)
                    node_index += 1
                    _queue.append(val)
            current_node += 1


        if pyvis_major >= 0 and pyvis_minor >= 3 and pyvis_patch >= 2:
            template = _graph.templateEnv.get_template(_graph.path)
            _graph.template = template
            try:
                _graph.show("nx.html", notebook = False)
            except TypeError:
                _graph.show("nx.html")
        else:
            _graph.show("nx.html")


