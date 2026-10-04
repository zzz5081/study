#题型：递归 - 树 DFS
#关键点：← minDepth(None)=0是哨兵值，不能参与min比较
#我踩的坑：← 漏写出口，两个提前return漏了+1,会把自己这层漏掉

from tree_utils import TreeNode, build, to_list


class Solution:
    def minDepth(self, root):
        if root is None:
            return 0
        if root.left is None:
            return self.minDepth(root.right) + 1
        if root.right is None:
            return self.minDepth(root.left) + 1
        left = self.minDepth(root.left)
        right = self.minDepth(root.right)
        return min(left,right) + 1


if __name__ == "__main__":
    s = Solution()
    assert s.minDepth(None) == 0
    assert s.minDepth(build([1])) == 1
    assert s.minDepth(build([1, 2])) == 2                     # ★ 抓"照抄104"
    assert s.minDepth(build([3, 9, 20, None, None, 15, 7])) == 2
    assert s.minDepth(build([1, 2, None, 3])) == 3
    print("通过")