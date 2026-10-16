import typing
from typing import Optional, Dict
from collections.abc import Iterator

from py_boggle.boggle_dictionary import BoggleDictionary


class TrieNode:
    """
    Our TrieNode class. Feel free to add new properties/functions, but 
    DO NOT edit the names of the given properties (children and is_word).
    """
    def __init__(self):
        self.children : Dict[str, TrieNode] = {} # maps a child letter to its TrieNode class
        self.is_word = False # whether or not this Node is a valid word ending


class TrieDictionary(BoggleDictionary):
    """
    Your implementation of BoggleDictionary.
    Several functions have been filled in for you from our solution, but you are free to change their implementations.
    Do NOT change the name of self.root, as our autograder will manually traverse using self.root
    """

    def __init__(self):
        self.root : TrieNode = TrieNode()

    def load_dictionary(self, filename: str) -> None:
        # Remember to add every word to the trie, not just the words over some length.
        with open(filename) as wordsfile:
            for line in wordsfile:
                word = line.strip().lower()
                if not word:
                    continue
                node = self.root
                for char in word:
                    if char not in node.children:
                        node.children[char] = TrieNode()
                    node = node.children[char]
                node.is_word = True

    def traverse(self, prefix: str) -> Optional[TrieNode]:
        """
        Traverse will traverse the Trie down a given path of letters `prefix`.
        If there is ever a missing child node, then returns None.
        Otherwise, returns the TrieNode referenced by `prefix`.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def is_prefix(self, prefix: str) -> bool:
        return self.traverse(prefix.lower()) is not None

    def contains(self, word: str) -> bool:
        node = self.traverse(word.lower())
        return node is not None and node.is_word

    def __iter__(self) -> typing.Iterator[str]:
        stack = [(self.root, "")]  # (node, the word spelled so far)
        while stack:
            node, prefix = stack.pop()
            if node.is_word:
                yield prefix
            for ch in sorted(node.children, reverse=True):
                stack.append((node.children[ch], prefix + ch))

