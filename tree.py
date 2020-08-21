from graphviz import Digraph
from collections import deque


# Tree node
class Node:
    def __init__(self, value, level):
        self.value = value
        self.children = list()
        self.level = level

    def __repr__(self):
        return f"{self.value}"

    def add_child(self, child):
        self.children.append(child)


# N-ary tree
class Tree:
    def __init__(self, order=2, root=None):
        if order < 2:
            raise ValueError("Order of a tree must have a value of at least 2")
        self.order = order
        self.root = root
        self.height = 0

    # Creates a visual and textual representation of a tree using graphviz module
    def __repr__(self):

        # Empty tree is represented by an empty string
        if self.root is None:
            return ""

        # Create directed graph object
        dot = Digraph(comment=f"{self.order}-ary tree", format='png')

        # Queue for traversing through the tree one level at a time
        queue = deque()
        queue.append(self.root)

        # Build a graph node by node until all nodes are recreated
        dot.node(f"{self.root.value}", f"{self.root.value}")
        while queue:
            current = queue.popleft()
            queue.extend(current.children)

            # Create child nodes and then connect them to their parent through edges
            for child in current.children:
                dot.node(f"{child.value}", f"{child.value}")
                dot.edges([f"{current.value}{child.value}"])

        # Visualized graph
        dot.render(f"{self.order}-ary tree", view=True)

        # Graph in a text format
        return dot.source

    # Returns the number of edges between a tree's root and its furthest leaf
    def __len__(self):
        return self.height

    # Recursive method that prints current node, then it's children
    def pre_order_traversal(self, current):
        if self.root:
            print(current)
            for child in current.children:
                self.pre_order_traversal(child)

    # Recursive method that prints node's children first, then the node itself
    def post_order_traversal(self, current):
        if self.root:
            for child in current.children:
                self.post_order_traversal(child)
            print(current)

    # Recursive DFS method
    def depth_first_search(self, value, current):
        if self.root:
            if current.value == value:
                return current
            for child in current.children:
                found = self.depth_first_search(value, child)
                if found:
                    return found
        return None

    # Searches breadth-first using a queue
    def breadth_first_search(self, value):
        if self.root:
            queue = deque()
            queue.append(self.root)
            while queue:
                current = queue.popleft()
                if current.value == value:
                    return current
                else:
                    queue.extend(current.children)
        return None

    # This method inserts a new node in the tree
    # User has an option of specifying a parent for the new node
    def insert(self, value, parent_value=None):

        # If the tree is empty, set self.root to the newly created node
        if self.root is None:
            self.root = Node(value, 0)

        # If the value already exists in the tree, it won't be inserted
        elif self.breadth_first_search(value):
            raise ValueError(f"Cannot insert {value}: node already exists in the tree")

        # If user didn't pass parent_value as a parameter,
        # find first open spot in the tree and insert there
        elif parent_value is None:
            new_parent = self._find_first_available_parent()
            new_parent.children.append(Node(value, level=self._update_height(new_parent.level+1)))

        # Insert after parent from the parameter list
        else:
            self._insert_after_parent(value, parent_value)

    # Deletes node from a tree
    def delete(self, value):
        if self.root is None:
            raise ValueError("Cannot delete node: tree is empty")
        elif value == self.root.value:
            self._delete_root()
        else:
            self._delete_node(value)

    # This method checks whether a tree is complete
    def is_complete(self):

        # Empty tree is considered complete
        if self.root is None:
            return True

        # Queue for traversing through the tree level by level
        queue = deque()
        queue.append(self.root)

        # all_full flag shows whether all visited nodes had max amount of children
        all_full = True

        # Go through the tree until we reach the last level
        # At that point we will already know if the tree is complete
        while queue[0].level < self.height:
            current = queue.popleft()

            # Check if all previous nodes were full
            if all_full:

                # Check node's level if it has less than max amount of children
                if len(current.children) < self.order:

                    # If node is on second to last level, set the flag to False and continue
                    if current.level == self.height - 1:
                        all_full = False

                    # If the non-full parent node is located higher, the tree is not complete
                    else:
                        return False

                # Add child nodes to the queue for further check
                queue.extend(current.children)

            # If there are nodes following a gap, the tree is not complete
            elif current.children:
                return False

        # If we haven't exited by this point, the tree is complete
        return True

    # Checks whether a tree is perfect
    def is_perfect(self):

        # Empty tree is considered perfect
        if self.root is None:
            return True

        # Queue for checking one level of tree at a time
        queue = deque()
        queue.append(self.root)

        while queue[0].level < self.height:
            current = queue.popleft()

            # Check if current node has a max amount of children
            if len(current.children) == self.order:
                queue.extend(current.children)

            # If it doesn't, we immediately know the tree is not perfect
            else:
                return False

        # If there hasn't been a node with less than max children, the tree is perfect
        return True

    # Checks whether a tree is full
    def is_full(self, current):

        # Empty tree is considered full
        if self.root is None:
            return True

        # Check if current node has 0 or max children
        if len(current.children) in (0, self.order):

            # Recursively check every subtree
            for child in current.children:

                # As soon as one subtree isn't full, we know the tree isn't full
                if not self.is_full(child):
                    return False

            # Return true if all subtrees were full
            # or the loop didn't run at all (0 children)
            return True

        # Return False if current node has neither 0 nor max children
        return False

    # Checks if a tree is balanced:
    # all subtrees must be balanced and their heights must differ by at most 1
    def is_balanced(self, current):

        # Empty tree is considered balanced
        if self.root is None:
            return 0, True

        # Max and min amount of levels in subtrees
        max_levels = 0
        min_levels = self.height

        # Find each subtree's amount of levels and whether it's balanced
        for child_index in range(0, self.order):

            # If child is non-existent, it's an empty tree
            if child_index > len(current.children) - 1:
                subtree = (0, True)

            # If child exists, check if it's a root of a balanced subtree
            else:
                subtree = self.is_balanced(current.children[child_index])

            # Find longest and shortest subtrees' amount of levels
            max_levels = max(subtree[0], max_levels)
            min_levels = min(subtree[0], min_levels)

            # As soon as there's a big difference between the number of levels of subtrees
            # or one of subtrees is imbalanced, we know to return False
            if max_levels - min_levels > 1 or subtree[1] is False:
                return max_levels + 1, False

        # Executes only if balanced tree properties are satisfied
        return max_levels + 1, True

    # Searches for the highest leftmost open spot in the tree for insertion
    def _find_first_available_parent(self):
        queue = deque()
        queue.append(self.root)
        while queue:
            current = queue.popleft()
            if len(current.children) < self.order:
                return current
            else:
                queue.extend(current.children)

    # Updates tree's height if newly inserted node added a level to the tree
    def _update_height(self, current_level):
        if current_level > self.height:
            self.height = current_level
        return current_level

    # Inserts a new node after specific parent
    def _insert_after_parent(self, value, parent_value):

        # Search for parent in the tree
        parent_node = self.depth_first_search(parent_value, self.root)

        # If parent node exists in the tree, try to insert the new child
        if parent_node:

            # If there is room for more children, add the new node
            if len(parent_node.children) < self.order:
                parent_node.add_child(Node(value, level=self._update_height(parent_node.level+1)))

            # If there's no more room for child nodes, raise an error
            else:
                raise IndexError(f"Cannot insert new node {value}: "
                                 f"Reached maximum amount of children for parent {parent_value}")

        # If parent wasn't found, raise an error
        else:
            raise ValueError(f"Cannot insert new node: "
                             f"parent node with the value of {parent_value} does not exist in the tree")

    # Deletes root from a tree
    def _delete_root(self):
        if not self.root.children:
            self.root = None
        elif len(self.root.children) == 1:
            self.root = self.root.children[0]
        else:
            self._delete_node_with_mult_children(self.root)

    # Deletes node with multiple children by pulling the leftmost one up
    # and doing the same for all it's descendants until it reaches the end
    def _delete_node_with_mult_children(self, node_to_delete):
        while node_to_delete.children:
            parent = node_to_delete
            node_to_delete = node_to_delete.children[0]
            parent.value = node_to_delete.value
        parent.children.pop(0)

    # Deletes any non-root node from a tree
    def _delete_node(self, value):

        # Find parent of the node that is being deleted
        parent, index = self._find_parent(value, self.root)

        # If parent wasn't found, the node that is being deleted doesn't exist
        if (parent, index) == (None, None):
            raise ValueError(f"Cannot delete node: {value} does not exists in the tree")

        node_to_delete = parent.children[index]

        # If it's a leaf node, remove it from it's parent's children list
        if not node_to_delete.children:
            parent.children.pop(index)

        # If the node has one child, connect it straight to the parent
        elif len(node_to_delete.children) == 1:
            parent.children[index] = node_to_delete.children[0]

        # If the node has multiple children, call another method to rearrange nodes
        else:
            self._delete_node_with_mult_children(node_to_delete)

    # Searches for node's parent for further use in _delete_node method
    def _find_parent(self, value, current):
        if self.root:
            for index, child in enumerate(current.children):
                if child.value == value:
                    return current, index
                found = self._find_parent(value, child)
                if found != (None, None):
                    return found
        return None, None
