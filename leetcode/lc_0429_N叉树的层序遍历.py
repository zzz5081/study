# 题型:BFS
# 关键点：需要把孩子一个个取出来再加入队列中
# 我踩的坑：可以直接遍历孩子，不用range，可以简化代码
from typing import Optional,List
from collections import deque

class Node:
    def __init__(self,val: Optional[int] = None,children: Optional[List['Node']] = None):
        self.val = val
        self.children = children

class Solution:
    def levelOrder(self, root: 'Node') -> List[List[int]]:
        if not root:
            return []
        res = []
        q = deque([root])
        while q:
            n = len(q)
            level = []
            for _ in range(n):
                node = q.popleft()
                if node.children:
                    for child in node.children:
                        q.append(child)
                level.append(node.val)
            res.append(level)
        return res

if __name__ == '__main__':
    s = Solution()
    assert s.levelOrder(None) == []
    assert s.levelOrder(Node(1)) == [[1]]
    assert s.levelOrder(Node(1, [Node(3, [Node(5), Node(6)]), Node(2), Node(4)])) == [[1], [3, 2, 4], [5, 6]]
    # ★ 四层（昨天的教训：测到最深层）
    assert s.levelOrder(Node(1, [Node(2, [Node(3, [Node(4), Node(5)])])])) == [[1], [2], [3], [4, 5]]
    print('通过')