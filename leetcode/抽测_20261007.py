from tree_utils import TreeNode, build


class Solution:
    def maxDepth(self, root):
        # ← 闭卷写
        if not root:
            return 0
        left_Depth = self.maxDepth(root.left)
        right_Depth = self.maxDepth(root.right)
        return max(left_Depth,right_Depth) + 1

    def isSymmetric(self, root):
        # ← 闭卷写
        if not root:
            return True
        def check(a,b):
            if a is None and b is None:
                return True
            if a is None or b is None:
                return False
            return a.val == b.val and check(a.left,b.right) and check(a.right,b.left)
        return check(root.left,root.right)




if __name__ == "__main__":
    s = Solution()

    # ---------- 104 最大深度 ----------
    assert s.maxDepth(None) == 0
    assert s.maxDepth(build([1])) == 1
    assert s.maxDepth(build([1, 2, None, 3])) == 3                    # 左斜
    assert s.maxDepth(build([1, 2, 3, 4, 5, 6, 7])) == 3              # 满二叉树
    assert s.maxDepth(build([3, 9, 20, None, None, 15, 7])) == 3      # 官方

    # ---------- 101 对称二叉树 ----------
    assert s.isSymmetric(None) == True
    assert s.isSymmetric(build([1])) == True
    assert s.isSymmetric(build([1, 2, 2, 3, 4, 4, 3])) == True        # 官方真例
    assert s.isSymmetric(build([1, 2, 2, None, 3, None, 3])) == False # 官方假例
    assert s.isSymmetric(build([1, 2, 3, None, 3, None, 2])) == False # ★ 反例

    print("通过")