class TreeNode:
    def __init__(self,val = 0,left = None,right = None):
        self.val = val
        self.left = left
        self.right = right

def maxDepth(node):
    if node is None:
        return 0
    left = maxDepth(node.left)
    right = maxDepth(node.right)
    return max(left,right) + 1

if __name__ == "__main__":
    assert maxDepth(TreeNode(1,TreeNode(2))) == 2
    assert maxDepth(None) == 0
    assert maxDepth(TreeNode(1,TreeNode(1),TreeNode(1))) == 2
    print("通过")