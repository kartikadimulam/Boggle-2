import copy
import random
from typing import List, Optional, Set, Tuple

from py_boggle.boggle_dictionary import BoggleDictionary
from py_boggle.boggle_game import BoggleGame

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

SHORT = 3
CUBE_SIDES = 6

class MyGameManager(BoggleGame):
    """Your implementation of `BoggleGame`
    """

    def __init__(self):
        """Constructs an empty Boggle Game.

        A newly-constructed game is unplayable.
        The `new_game` method will be called to initialize a playable game.
        Do not call `new_game` here.

        This method is provided for you, but feel free to change it.
        """

        self.board: List[List[str]] # current game board
        self.size: int # board size
        self.words: List[str] # player's current words
        self.dictionary: BoggleDictionary # the dictionary to use
        self.last_added_word: Optional[List[Tuple[int, int]]] # the position of the last added word, or None

    def new_game(self, size: int, cubefile: str, dictionary: BoggleDictionary) -> None:
        """This method is provided for you, but feel free to change it.
        """
        with open(cubefile, 'r') as infile:
            faces = [line.strip() for line in infile]
        cubes = [f.lower() for f in faces if len(f) == CUBE_SIDES]
        if size < 2 or len(cubes) < size*size:
            raise ValueError('ERROR: Invalid Dimensions (size, cubes)')
        random.shuffle(cubes)
        # Set all of the game parameters
        self.board =[[random.choice(cubes[r*size + c]) 
                    for r in range(size)] for c in range(size)]
        self.size = size
        self.words = []
        self.dictionary = dictionary
        self.last_added_word = None


    def get_board(self) -> List[List[str]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.board

    def find_word_in_board(self, word: str) -> Optional[List[Tuple[int, int]]]:
        """Helper method called by add_word()
        Expected behavior:
        Returns an ordered list of coordinates of a word on the board in the same format as get_last_added_word()
        (see documentation in boggle_game.py).
        If `word` is not present on the board, return None.
        """
        word = word.lower()
        if not word:
            return None

        # start with a one-cell path for every cell matching the first letter
        stack = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == word[0]:
                    stack.append([(r, c)])

        while stack:
            path = stack.pop()
            if len(path) == len(word):  # every letter matched
                return path

            r, c = path[-1]  # last cell in the path
            nxt = word[len(path)]  # the letter we need next
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if ((dr != 0 or dc != 0)
                            and 0 <= nr < self.size and 0 <= nc < self.size
                            and (nr, nc) not in path
                            and self.board[nr][nc] == nxt):
                        stack.append(path + [(nr, nc)])

        return None




    def add_word(self, word: str) -> int:
        """This method is provided for you, but feel free to change it.
        """
        word = word.lower()
        if (len(word) > SHORT and word not in self.words and self.dictionary.contains(word)):
            location = self.find_word_in_board(word)
            if location is not None:
                self.last_added_word = location
                self.words.append(word)
                return len(word) - SHORT
        return 0

    def get_last_added_word(self) -> Optional[List[Tuple[int, int]]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.last_added_word

    def set_game(self, board: List[List[str]]) -> None:
        """This method is provided for you, but feel free to change it.
        """
        self.board = [[c.lower() for c in row] for row in board]

    def get_score(self) -> int:
        """This method is provided for you, but feel free to change it.
        """
        return sum([len(word) - SHORT for word in self.words])

    def dictionary_driven_search(self) -> Set[str]:
        """Find all words using a dictionary-driven search.

        The dictionary-driven search attempts to find every word in the
        dictionary on the board.

        Returns:
            A set containing all words found on the board.
        """
        wordset = set()
        for word in self.dictionary:
            if len(word) > SHORT:
                word = word.lower()
                # start with a one-cell path for every cell matching the first letter
                stack = []
                for r in range(self.size):
                    for c in range(self.size):
                        if self.board[r][c] == word[0]:
                            stack.append([(r, c)])

                while stack:
                    path = stack.pop()
                    if len(path) == len(word):  # every letter matched
                        wordset.add(word)
                        break
                    r, c = path[-1]  # last cell in the path
                    nxt = word[len(path)]  # the letter we need next
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            nr, nc = r + dr, c + dc
                            if ((dr != 0 or dc != 0)
                                    and 0 <= nr < self.size and 0 <= nc < self.size
                                    and (nr, nc) not in path
                                    and self.board[nr][nc] == nxt):
                                stack.append(path + [(nr, nc)])
        return wordset


    def board_driven_search(self) -> Set[str]:
        """Find all words using a board-driven search.

        The board-driven search constructs a string using every path on
        the board and checks whether each string is a valid word in the
        dictionary.

        Returns:
            A set containing all words found on the board.
        """
        wordset = set()
        stack = []
        for r in range(self.size):
            for c in range(self.size):
                stack.append([(r, c)])

        while stack:
            path = stack.pop()
            word = "".join(self.board[pr][pc] for pr, pc in path)  # word for THIS path

            if not self.dictionary.is_prefix(word):  # dead end: no word starts this way
                continue
            if len(word) > SHORT and self.dictionary.contains(word):
                wordset.add(word)  # record it, but keep searching

            r, c = path[-1]
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if ((dr != 0 or dc != 0)
                            and 0 <= nr < self.size and 0 <= nc < self.size
                            and (nr, nc) not in path):
                        stack.append(path + [(nr, nc)])
        return wordset
