class TreeNode:
    def __init__(self,val):
        self.val = val
        self.left = None
        self.right = None

    def preorder(self,root):
        if root is None:
            return []
        result = []
        result.append(root.val)
        result = result + self.preorder(root.left)
        result = result + self.preorder(root.right)
        return result

    def inorder(self,root):
        if root is None:
            return []
        result = []
        result = result + self.inorder(root.left)
        result.append(root.val)
        result = result + self.inorder(root.right)
        return  result

    def postorder(self,root):
        if root is None:
            return []
        result = []
        result = result + self.postorder(root.left)
        result = result + self.postorder(root.right)
        result.append(root.val)
        return result

    def search(self,root,target):
        if root is None:
            return False
        if root.val == target:
            return True
        return self.search(root.left,target) or self.search(root.right,target)

    def maxDepth(self,root):
        if root is None:
            return 0
        left = self.maxDepth(root.left)
        right = self.maxDepth(root.right)
        return 1 + max(left,right)

tree = TreeNode(1)
tree.left = TreeNode(2)
tree.right = TreeNode(3)
tree.right.left = TreeNode(4)
tree.right.right = TreeNode(5)
print(tree.preorder(tree))
print(tree.inorder(tree))
print(tree.postorder(tree))
print(tree.search(tree,50))
print(tree.maxDepth(tree))