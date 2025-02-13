"""CSC111 Exercise 2 Part 2

Module Description
==================
This module contains the BinarySearchTree class we developed in this week's lectures, as well as
various methods and functions for you to implement for Exercise 2 Part 2.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 UofT DCS Teaching Team
"""
from __future__ import annotations
from typing import Any, Optional


class BinarySearchTree:
    """Binary Search Tree class.

    Representation Invariants:
      - (self._root is None) == (self._left is None)
      - (self._root is None) == (self._right is None)
      - (BST Property) if self._root is not None, then
          all items in self._left are <= self._root, and
          all items in self._right are >= self._root
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at the root of this tree, or None if this tree is empty.
    #   - _left:
    #       The left subtree, or None if this tree is empty.
    #   - _right:
    #       The right subtree, or None if this tree is empty.
    _root: Optional[Any]
    _left: Optional[BinarySearchTree]
    _right: Optional[BinarySearchTree]

    def __init__(self, root: Optional[Any]) -> None:
        """Initialize a new BST containing only the given root value.

        If <root> is None, initialize an empty tree.
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self) -> bool:
        """Return whether this BST is empty.

        >>> bst = BinarySearchTree(None)
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(10)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    def __str__(self) -> str:
        """Return a string representation of this BST.

        This string uses indentation to show depth.

        We've provided this method for debugging purposes, if you choose to print a BST.
        """
        return self._str_indented(0).rstrip()

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this BST.

        The indentation level is specified by the <depth> parameter.

        Preconditions:
            - depth >= 0
        """
        if self.is_empty():
            return ''
        else:
            return (
                depth * '  ' + f'{self._root}\n'
                + self._left._str_indented(depth + 1)
                + self._right._str_indented(depth + 1)
            )

    ############################################################################
    # Standard Multiset methods (search, insert, delete)
    ############################################################################
    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this BST.

        >>> bst = BinarySearchTree(3)
        >>> bst._left = BinarySearchTree(2)
        >>> bst._right = BinarySearchTree(5)
        >>> bst.__contains__(3)  # or, 3 in bst
        True
        >>> bst.__contains__(5)
        True
        >>> bst.__contains__(2)
        True
        >>> bst.__contains__(4)
        False
        """
        if self.is_empty():
            return False
        elif item == self._root:
            return True
        elif item < self._root:
            return self._left.__contains__(item)  # or, item in self._left
        else:
            return self._right.__contains__(item)  # or, item in self._right

    def insert(self, item: Any) -> None:
        """Insert the given item into this tree.

        Do not change positions of any other values.

        >>> bst = BinarySearchTree(10)
        >>> bst.insert(3)
        >>> bst.insert(20)
        >>> bst._root
        10
        >>> bst._left._root
        3
        >>> bst._right._root
        20
        """
        if self.is_empty():
            # Make new leaf.
            # Note that self._left and self._right cannot be None when the
            # tree is non-empty! (This is one of our invariants.)
            self._root = item
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)
        elif item <= self._root:
            self._left.insert(item)
        else:
            self._right.insert(item)

    def remove(self, item: Any) -> None:
        """Remove *one* occurrence of the given item from this BST.

        Do nothing if the item is not in this BST.
        """
        if self.is_empty():
            pass
        elif self._root == item:
            self._remove_root()
        elif item < self._root:
            self._left.remove(item)
        else:
            self._right.remove(item)

    def _remove_root(self) -> None:
        """Remove the root of this tree.

        Preconditions:
          - not self.is_empty()
        """
        if self._left.is_empty() and self._right.is_empty():
            self._root = None
            self._left = None
            self._right = None
        elif self._left.is_empty():
            # "Promote" the right subtree.
            # Note that self = self._right does NOT work!
            self._root, self._left, self._right = \
                self._right._root, self._right._left, self._right._right
        elif self._right.is_empty():
            # "Promote" the left subtree.
            self._root, self._left, self._right = \
                self._left._root, self._left._left, self._left._right
        else:
            # Both subtrees are non-empty. Can choose to replace the root
            # from either the max value of the left subtree, or the min value
            # of the right subtree. (Implementations are very similar.)
            self._root = self._left._extract_max()

    def _extract_max(self) -> Any:
        """Remove and return the maximum item stored in this tree.

        Preconditions:
          - not self.is_empty()
        """
        if self._right.is_empty():
            max_item = self._root
            # Like remove_root, "promote" the left subtree.
            # Alternate approach: call self.remove_root()!
            self._root, self._left, self._right = \
                self._left._root, self._left._left, self._left._right
            return max_item
        else:
            return self._right._extract_max()

    ############################################################################
    # Exercise 2 Part 2: BST Rotations
    ############################################################################
    def rotate_right(self) -> None:
        """Rotate this binary search tree clockwise.

        Preconditions:
            - not self.is_empty()
            - not self._left.is_empty()

        >>> bst = BinarySearchTree(7)
        >>> bst.insert(3)
        >>> bst.insert(11)
        >>> bst.insert(2)
        >>> bst.insert(5)
        >>> print(bst)
        7
          3
            2
            5
          11
        >>> bst.rotate_right()
        >>> print(bst)
        3
          2
          7
            5
            11
        >>> bst.rotate_right()
        >>> print(bst)
        2
          3
            7
              5
              11
        """
        new_right = BinarySearchTree(self._root)
        new_right._left = self._left._right
        new_right._right = self._right  # binary search tree object for right

        self._root = self._left._root
        self._left = self._left._left
        self._right = new_right

    def rotate_left(self) -> None:
        """Rotate this binary search tree counter-clockwise.

        Preconditions:
            - not self.is_empty()
            - not self._right.is_empty()

        >>> bst = BinarySearchTree(7)
        >>> bst.insert(3)
        >>> bst.insert(11)
        >>> bst.insert(2)
        >>> bst.insert(5)
        >>> bst.insert(9)
        >>> bst.insert(13)
        >>> print(bst)
        7
          3
            2
            5
          11
            9
            13
        >>> bst.rotate_left()
        >>> print(bst)
        11
          7
            3
              2
              5
            9
          13
        >>> bst.rotate_left()
        >>> print(bst)
        13
          11
            7
              3
                2
                5
              9
        """
        new_left = BinarySearchTree(self._root)
        new_left._left = self._left
        new_left._right = self._right._left

        self._root = self._right._root
        self._left = new_left
        self._right = self._right._right


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })
