#题型：递归
#关键点：出口返回【节点】不是数字；交换前必须先把一边存起来
#我踩的坑:直接用 == 比 TreeNode 是比内存地址，不是比内容（会一路 AssertionError）
from tree_utils import TreeNode, build, to_list


class Solution:
    def invertTree(self, root):
        if root is None:
            return None
        tmp = root.left
        root.left = self.invertTree(root.right)
        root.right = self.invertTree(tmp)
        return root


if __name__ == "__main__":
    s = Solution()

    assert s.invertTree(None) is None                              # ① 空树（注意用 is）
    assert to_list(s.invertTree(build([1]))) == [1]                # ② 单节点
    assert to_list(s.invertTree(build([1, 2, 3]))) == [1, 3, 2]    # ③ 平衡树

    # ④ LeetCode 官方例子（最强的一条）
    assert to_list(s.invertTree(build([4, 2, 7, 1, 3, 6, 9]))) == [4, 7, 2, 9, 6, 3, 1]

    # ⑤ 左斜 → 变右斜（验证不是"只翻了一边"）
    assert to_list(s.invertTree(build([1, 2, None, 3]))) == [1, None, 2, None, 3]

    print("通过")