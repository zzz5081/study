class TreeNode:
    def __init__(self,val):
        self.val = val
        self.left = None
        self.right = right

    def invertTree(self,root):
        if root is None:
            return None
        left = self.invertTree(root.right)
        right = self.invertTree(root.left)
        root.left = left
        root.right = right
        return root

class solution:
    def isSymmetric(self,root):
        if root is None:
            return True
        return self.isMirror(root.left,root.right)
    def isMirror(self, left, right):
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        if left.val != right.val:
            return  False
        return self.isMirror(left.left,right.right) and self.isMirror(left.right,right.left)

def inorder(self,root):
    res = []
    stack = []
    cur = root
    while stack or cur:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        res.append(cur.val)
        cur = cur.right
    return res

def maxdeep(self,root):
    if root is None:
        return 0
    left = self.maxdeep(root.left)
    right = self.maxdeep(root.right)
    return 1 + max(left,right)
