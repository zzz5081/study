#题型：递归 - 返回集合
#关键点：出口返回【列表】不是数字；三段用 + 拼接，单个值要用 [] 包起来
#我踩的坑:用逗号写成了元组 (left, val, right)；列表不能直接 + 整数
from tree_utils import TreeNode, build, to_list


class Solution:
    def inorderTraversal(self, root):
        if not root:
            return []
        left = self.inorderTraversal(root.left)
        right = self.inorderTraversal(root.right)
        return left + [root.val] + right        # ← 你只需要改这一行


if __name__ == "__main__":
    s = Solution()
    assert s.inorderTraversal(None) == []                            # 出口
    assert s.inorderTraversal(build([1])) == [1]                     # 单节点
    assert s.inorderTraversal(build([1, None, 2, 3])) == [1, 3, 2]   # 官方例子
    assert s.inorderTraversal(build([1, 2, 3])) == [2, 1, 3]         # 左根右（关键）
    assert s.inorderTraversal(build([3, 1, 2])) == [1, 3, 2]         # 换一棵，防碰巧
    print("通过")