import sys
from rich import print
 
class Node():
    def __init__(self, item):
        self.item = item
        self.parent = None  #parent node
        self.left = None   # left node
        self.right = None  # right node
        self.color = 1     #1=red , 0 = black
        self.count = 1
 
 
class RedBlackTree():
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.TNULL.count = 0
        self.root = self.TNULL
 
    # Preorder
    def pre_order_helper(self, node):
        if node != self.TNULL:
            sys.stdout.write(node.item + " ")
            self.pre_order_helper(node.left)
            self.pre_order_helper(node.right)
 
    # Balancing the tree after deletion
    def delete_fix(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right
 
                if s.left.color == 0 and s.right.color == 0:  # crash here -- AttributeError: 'NoneType' object has no attribute 'color'
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right
 
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left
 
                if s.right.color == 0 and s.right.color == 0:  # crash -- AttributeError: 'NoneType' object has no attribute 'color'
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left
 
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0
 
    def __rb_transplant(self, u, v):
        print (f'transplant (u={u.item}, v={v.item})')
        if u.parent is None:        # root node
            self.root = v
        elif u == u.parent.left:    # left child
            u.parent.left = v
        else:                       # right child
            u.parent.right = v
        v.parent = u.parent
        if u.parent is not None:
            u.parent.count = u.parent.left.count + 1 + u.parent.right.count

 
    # Fine nearest
    def find_with_successor_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.item == key:
                z = node
                return node.item

            if node.item <= key:
                next_node = node.right
            else:
                next_node = node.left
            if next_node == self.TNULL:
                return self.successor(node, True).item

    # Node deletion
    def delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.item == key:
                z = node
 
            if node.item <= key:
                node = node.right
            else:
                node = node.left
 
        if z == self.TNULL:
            print("Cannot find key in the tree")
            return
 
        print (f'delete node. found {z.item}')

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.TNULL):
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
 
            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        p = x.parent
        while p:
            p.count = p.left.count + 1 + p.right.count
            p = p.parent

        if z.item == 14:
            self.traverse()
            
        if y_original_color == 0:
            if z.item == 14:
                print (f'delete_fix {x.item=}')
            self.delete_fix(x)
        
        self.traverse()
 
    # Balance the tree after insertion
    def fix_insert(self, k):
        while k.parent.color == 1:
            print (f'fix_insert(red parent: k={k.item}, k.parent={k.parent.item})')
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    print (f'fix insert left rotate {k.item}->{k.parent.item}->{k.parent.parent.item}')
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
 
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    print (f'fix insert right rotate {k.item}->{k.parent.item}->{k.parent.parent.item}')
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0
        print (f'fix insert complete')
        self.traverse()
 
    # Print
    def __print_helper(self, node, indent, last):
        if node != self.TNULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
 
            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.item) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)
 
    def preorder(self):
        self.pre_order_helper(self.root)
 
    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node
 
    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node
 
    def successor(self, x, wrap = False):
        if x.right != self.TNULL:
            return self.minimum(x.right)
 
        y = x.parent
        while y != self.TNULL and x == y.right:
            x,y = y,y.parent
            if y is None:
                if wrap:
                    return self.minimum(x)
                break
        return y
 
    def predecessor(self,  x, wrap = False):
        if (x.left != self.TNULL):
            return self.maximum(x.left)
 
        y = x.parent
        while y != self.TNULL and x == y.left:
            x,y = y,y.parent
            if y is None:
                if wrap:
                    return self.maximum(x)
                break
 
        return y
 
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
 
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        x.count = x.left.count + 1 + x.right.count
        y.count = y.left.count + 1 + y.right.count
        #print (f'left_rotate recalc x: {x.left.item},{x.left.count} + {y.right.item},{y.right.count}')
        print (f'left_rotate recalc {x.item}->{x.count}, parent:  {y.item}->{y.count}')

 
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
 
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        x.count = x.left.count + 1 + x.right.count
        y.count = y.left.count + 1 + y.right.count
        #print (f'right_rotate recalc x: {x.left.item},{x.left.count} + {y.right.item},{y.right.count}')
        print (f'right_rotate recalc {x.item}->{x.count}, parent:  {y.item}->{y.count}')
 
    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.item = key
        node.left = self.TNULL  # Black leaf node
        node.right = self.TNULL # Black leaf node
        node.color = 1 # red
        node.count = 1
 
        y = None
        x = self.root
 
        while x != self.TNULL:
            y = x
            y.count += 1
            if node.item < x.item:
                x = x.left
            else:
                x = x.right
 
        node.parent = y
        if y == None:
            self.root = node
        elif node.item < y.item:
            y.left = node
        else:
            y.right = node
 
        print (f'insert({node.item})')
        self.traverse()

        if node.parent == None:
            node.color = 0
            return
 
        if node.parent.parent == None:
            return
 
        self.fix_insert(node)
 
    def get_root(self):
        return self.root
 
    def delete_node(self, item):
        self.delete_node_helper(self.root, item)
 
    def print_tree(self):
        self.__print_helper(self.root, "", True)

    def traverse_node(self, node:Node, path:str='', prefix:str = ''):
        if node:
            suffix = ''
            if node.right or node.left:
                if node.right and node.left:
                    suffix += '\u252B'
                elif node.right:
                    suffix += '\u251B'
                else:
                    suffix += '\u2513'
            #label = f'{node.item},{node.size},{node.height}'
            label_raw = f' {(f"{node.item},{node.count}","\u2205,"+f"{node.count}")[node == self.TNULL]}'
            label = f'[bold {('black','bright_red')[node.color]}]{label_raw}[/]'
            label_len = len(label_raw)
            self.traverse_node(node.right, path+"R", prefix.replace('\u250F', ' ').replace('\u2517', '\u2503') + ' '*label_len + ' \u250F')
            print(f'{prefix}{label} {suffix}')
            self.traverse_node(node.left, path+"L", prefix.replace('\u2517', ' ').replace('\u250F', '\u2503') + ' '*label_len + ' \u2517')

    def traverse(self, prefix:str = ' '):
        self.traverse_node(self.root, '', prefix)

    def is_red_black_tree(self, root):
        """
        Checks if a given tree is a valid red-black tree.
        """
        def is_red(node):
            return node and node.color == 1

        def black_height(node):
            if node == self.TNULL:
                return 0
            left_height = black_height(node.left)
            right_height = black_height(node.right)
            if left_height != right_height:
                return -1
            return left_height + (1 if node.color == 0 else 0)

        def check_rules(node):
            if not node:
                return True

            # Rule 1: Every node is either red or black.
            if node.color not in (1, 0):
                return False

            # Rule 2: The root is black.
            if not node.parent and node.color == 1:
                return False

            # Rule 3: All leaves (NIL) are black.
            if not node.left and not node.right and node.color == 1:
                return False

            # Rule 4: If a node is red, then both its children are black.
            if is_red(node) and (is_red(node.left) or is_red(node.right)):
                return False

            # Rule 5: Every path from a given node to any of its descendant leaves 
            # contains the same number of black nodes.
            if black_height(node) == -1:
                return False

            return check_rules(node.left) and check_rules(node.right)

        return check_rules(root)

 
if __name__ == "__main__":

    import random
    bst = RedBlackTree()
    nums = list(range(15))
    seed = random.randint(0, sys.maxsize)
    seed = 7105939855445245191
    random.seed(seed)
    print (f'random seed: {seed}')
    random.shuffle(nums)
    for i in nums:
        bst.insert(i)
        assert bst.is_red_black_tree(bst.root)
    #input()
    random.shuffle(nums)
    for i in nums:
        bst.delete_node(i)
        assert bst.is_red_black_tree(bst.root)
    if False:
        node = bst.root
        for _ in range(len(nums) + 5):
            next_node = bst.successor(node, True)
            print (f'successor({node.item}) => {next_node.item}')
            node = next_node
        for _ in range(len(nums) + 5):
            next_node = bst.predecessor(node, True)
            print (f'predecessor({node.item}) => {next_node.item}')
            node = next_node
