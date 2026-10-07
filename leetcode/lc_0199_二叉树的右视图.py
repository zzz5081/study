#题型：BFS - 队列（102 模板变形）
#关键点：← 通过运用队列层序遍历，每层只要最后一个
#我踩的坑：← 转发孩子的代码写两遍有点隐患

from collections import deque
from tree_utils import TreeNode, build


class Solution:
    def rightSideView(self, root):
        if not root:
            return []
        res = []
        q = deque([root])
        while q:
            n = len(q)
            for _ in range(n):
                node = q.popleft()
                last = node.val
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(last)
        return res

if __name__ == "__main__":
    s = Solution()
    assert s.rightSideView(None) == []
    assert s.rightSideView(build([1])) == [1]
    assert s.rightSideView(build([1, 2, 3, None, 5, None, 4])) == [1, 3, 4]
    assert s.rightSideView(build([1, None, 2, None, 3])) == [1, 2, 3]     # ★ 右斜
    assert s.rightSideView(build([1, 2, None, 3])) == [1, 2, 3]           # ★ 左斜
    print("通过")