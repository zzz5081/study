#题型:递归，深度优先DFS
#关键点:假装小一号的问题已经解决，再拼出自己的答案  边界,子树深度都取大再加上自己这层
#我踩的坑:没想到直接调用自己还想用迭代循环思想
class TreeNode:
    def __init__(self,val=0,left=None,right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0
        left_Depth = self.maxDepth(root.left)
        right_Depth = self.maxDepth(root.right)
        return max(left_Depth,right_Depth) + 1

if __name__ == "__main__":
    s = Solution()
    assert s.maxDepth(None) == 0  # 空树 ← 递归边界，最容易漏

    # 平衡树
    assert s.maxDepth(TreeNode(1, TreeNode(2), TreeNode(3))) == 2

    # ⚠️ 左斜树（只有左孩子）—— 验证你真的用了 max，而不是只看了某一边
    n3 = TreeNode(3)
    assert s.maxDepth(TreeNode(1, TreeNode(2, n3))) == 3

    # ⚠️ 右斜树（只有右孩子）—— 上一题的镜像
    r3 = TreeNode(3)
    assert s.maxDepth(TreeNode(1, None, TreeNode(2, None, r3))) == 3
    print('通过')