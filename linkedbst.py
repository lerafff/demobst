"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
# from linkedqueue import LinkedQueue
from math import log
import random
import time
import sys
sys.setrecursionlimit(100000)


class bcolors:
    '''
    Module with colors
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            str_r = ""
            if node != None:
                str_r += recurse(node.right, level + 1)
                str_r += "| " * level
                str_r += str(node.data) + "\n"
                str_r += recurse(node.left, level + 1)
            return str_r

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        # print('inorder ' + str(lyst))
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        preroot = BSTNode(None)
        preroot.left = self._root
        parent = preroot
        direction = 'L'
        currentnode = self._root
        while not currentnode == None:
            if currentnode.data == item:
                item_removed = currentnode.data
                break
            parent = currentnode
            if currentnode.data > item:
                direction = 'L'
                currentnode = currentnode.left
            else:
                direction = 'R'
                currentnode = currentnode.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentnode.left == None \
                and not currentnode.right == None:
            lift_max_in_left_subtree_to_top(currentnode)
        else:

            # Case 2: The node has no left child
            if currentnode.left == None:
                new_child = currentnode.right

                # Case 3: The node has no right child
            else:
                new_child = currentnode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preroot.left
        return item_removed

    def replace(self, item, newitem):
        """
        If item is in self, replaces it with newitem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = newitem
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return 0
            left_branch = height1(top.left)
            right_branch = height1(top.right)
            return max(left_branch, right_branch) + 1

        return height1(self._root) - 1


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return True if self.height() < (2 * log(self._size + 1) - 1) else False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        list_ordered = list(self.inorder())
        if low > high or low > max(list_ordered) or\
            high < min(list_ordered):
            return None
        index_start = self.successor(low) if low not in list_ordered else low
        index_finish = self.predecessor(high) if high not in list_ordered else high
        return list_ordered[list_ordered.index(index_start) : list_ordered.index(index_finish) + 1]


    def rebalance1(self, apexes):
        '''
        Recursive function that inserts in the middle
        if len is pair number - left branch will be bigger
        :param apexes: list
        :return: None
        '''
        middle = len(apexes) // 2
        if not apexes:
            return None
        else:
            self.add(apexes[middle]), apexes.pop(middle)
            # middle = len(apexes) // 2
            self.rebalance1(apexes[middle :])
            self.rebalance1(apexes[: middle])


    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''

        list_inordered = list(self.inorder())
        self.clear()
        self.rebalance1(list_inordered)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        list_ordered = list(self.inorder())
        if item > max(list_ordered):
            return None
        for elem in list_ordered:
            if elem > item:
                return elem
        return None


    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        list_ordered = list(self.inorder())
        if item < min(list_ordered):
            return None
        for elem in list_ordered[::-1]:
            if elem < item:
                return elem
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        list_words = list()
        with open(path) as file:
            for line in file:
                list_words.append(line.strip())
        # Task 1 - search 10 000 random words
        selected_random = random.sample(list_words, 10000)
        start = time.time()
        for elem in selected_random:
            list_words.index(elem)
        finish = time.time()
        time_process = finish - start
        # print(time_process)

        # Task 2 - search in binary tree
        # word list is cut because of limit of recursion
        randomed = random.sample(list_words[:25000], 10000)
        tree = LinkedBST()
        for elem2 in list_words[:25000]:
            tree.add(elem2)

        start2 = time.time()
        for word in randomed:
            tree.find(word)
        finish2 = time.time()

        time_process2 = finish2 - start2
        # print(time_process2)

        # Task 3 - finding words in mixed list
        tree2 = LinkedBST()
        mixed_list = random.sample(list_words, len(list_words))
        for elem3 in mixed_list:
            tree2.add(elem3)

        start3 = time.time()
        for word2 in selected_random:
            tree2.find(word2)
        finish3 = time.time()

        time_process3 = finish3 - start3
        # print(time_process3)

        # Task 4 - search in rebalanced binary tree
        start4 = time.time()
        tree2.rebalance()
        for word3 in selected_random:
            tree2.find(word3)
        finish4 = time.time()

        time_process4 = finish4 - start4
        # print(time_process4)

        line = ' - '
        print(line * 18 + bcolors.HEADER + '\nRESULTS\t\t\t\t\t\t\t\t\t\tTIME\n' + bcolors.ENDC +
              line * 18 + bcolors.OKCYAN + '\n Task 1     search 10 000 random words      ' +
              bcolors.HEADER + bcolors.BOLD + str(time_process) + bcolors.ENDC + bcolors.OKCYAN +
              '\n Task 2     search in binary tree           ' + bcolors.HEADER +
              bcolors.BOLD + str(time_process2) + bcolors.ENDC + bcolors.OKCYAN +
              '\n Task 3     finding words in mixed list     ' + bcolors.HEADER + bcolors.BOLD +
              str(time_process3) + bcolors.ENDC + bcolors.OKCYAN + '\n Task 4     ' +
              'search in rebalanced binary tree   ' + bcolors.HEADER + bcolors.BOLD +
              str(time_process4) + bcolors.ENDC + '\n' + line * 18)


tree = LinkedBST()
tree.demo_bst('words.txt')
