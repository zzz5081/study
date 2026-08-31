# class TreeNode:
#     def __init__(self,val):
#         self.val = val
#         self.left = None
#         self.right = None
#
# def search(root,target):
#     if root is None:
#         return False
#     if root.val == target:
#         return True
#
#     return search(root.left,target) or search(root.right,target)
#
# root = TreeNode(5)
# root.left = TreeNode(3)
# root.right = TreeNode(8)
# root.left.left = TreeNode(1)
# root.left.right = TreeNode(4)
# root.right.right = TreeNode(9)
#
# print(search(root, 4))   # True
# print(search(root, 7))   # False
# print(search(None, 1))   # False

class TreeNode:
    def __init__(self,val):
        self.val = val
        self.left = None
        self.right = None

# def preorder(root):
#     if root is None:
#         return []
#     result = []
#     result.append(root.val)
#     result = result + preorder(root.left)
#     result = result + preorder(root.right)
#     return result
#
# def inorder(root):
#     if root is None:
#         return []
#     result = []
#     result = result + inorder(root.left)
#     result.append(root.val)
#     result = result + inorder(root.right)
#     return result
#
# def postorder(root):
#     if root is None:
#         return []
#     result = []
#     result = result + postorder(root.left)
#     result = result + postorder(root.right)
#     result.append(root.val)
#     return result
#
# root = TreeNode(5)
# root.left = TreeNode(3)
# root.right = TreeNode(8)
# root.left.left = TreeNode(1)
# root.left.right = TreeNode(4)
# root.right.right = TreeNode(9)
# print(preorder(root))
# print(inorder(root))
# print(postorder(root))
class Stack:
    def __init__(self):
        self.stack = []

    def push(data):
        return self.stack.append(data)

    def pop():
        return self.stack.pop()

    def peek():
        return self.stack[-1]

    def is_empty():
        return len(self.stack) == 0

def preorder(root):
    if root is None:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return result

def inorder(root):
    if root is None:
        return []
    stack = []
    result = []
    cur = root
    while cur is not None or stack:
        while cur is not None:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        result.append(cur.val)
        cur = cur.right
    return result