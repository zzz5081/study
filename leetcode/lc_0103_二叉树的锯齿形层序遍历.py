#题型:BFS
#关键点:通过队列进行层序遍历，并且用level[::-1]反转队列
#我踩的坑:忘记了可以用level[::-1]反转列表，且习惯性把return []写成了 return None

from tree_utils import TreeNode,build
from collections import deque

class Solution:
    def zigzagLevelOrder(self, root: TreeNode | None) -> list[list[int]]:
        if root is None:
            return []
        res = []
        q = deque([root])
        count = 1
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
            if count % 2 == 0:
                level = level[::-1]
            res.append(level)
            count += 1
        return res

if __name__ == '__main__':
    s = Solution()
    assert s.zigzagLevelOrder(None) == []
    assert s.zigzagLevelOrder(build([1])) == [[1]]
    assert s.zigzagLevelOrder(build([3, 9, 20, None, None, 15, 7])) == [[3], [20, 9], [15, 7]]
    assert s.zigzagLevelOrder(build([1, 2, 3, 4, None, None, 5])) == [[1], [3, 2], [4, 5]]  # ★三层
    # ★★ 四层：三层树测不出「第二次交替」，必须补到第 3 层反转才会被测到
    assert s.zigzagLevelOrder(build([1, 2, 3, 4, 5, 6, 7, 8, 9])) == [[1], [3, 2], [4, 5, 6, 7], [9, 8]]
    print("通过")