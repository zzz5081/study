#题型：BFS - 队列
#关键点：← 使用队列一层一层取放，先把根放进去再取出来再放它的左右子树
#我踩的坑：← "忘了数 len 就拍平了",结果里只能放值.val

from collections import deque
from tree_utils import TreeNode, build


class Solution:
    def levelOrder(self, root):
        if not root:
            return []
        res = []
        q = deque([root])
        while q:
            n = len(q)
            level = []
            for _ in range(n):
                node = q.popleft()
                level.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(level)
        return res
    
if __name__ == "__main__":
    s = Solution()
    assert s.levelOrder(None) == []
    assert s.levelOrder(build([1])) == [[1]]
    assert s.levelOrder(build([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]]
    assert s.levelOrder(build([1, 2, None, 3])) == [[1], [2], [3]]     # ★ 验证分层
    print("通过")