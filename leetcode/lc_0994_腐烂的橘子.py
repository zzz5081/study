# 题型：BFS层序遍历网格版
# 关键点：使用对列一层就是一分钟，记新鲜橘子的个数，如果结束还不是0的话就返回-1，处理最后一后没有下一分钟
# 我踩的坑：变量名num,num2,num3太差
#         grid[ni][nj] == 2 双等号只比较不赋值，死循环还不报错
#          nj = i + dj 手滑用错，结果错但不崩
#           7条assert全是单元，没测到[多源BFS]

from collections import deque

class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0])
        fresh = 0
        q = deque()
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 2:
                    q.append((i,j))
                if grid[i][j] == 1:
                    fresh += 1
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        minute = -1
        while q:
            n = len(q)
            for _ in range(n):
                i,j = q.popleft()
                for di,dj in dirs:
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if grid[ni][nj] == 1:
                            grid[ni][nj] =2
                            q.append((ni,nj))
                            fresh -= 1
            minute += 1
        return -1 if fresh else max(minute,0)

if __name__ == "__main__":
    s = Solution()
    assert s.orangesRotting([[1,2,1],[1,1,1],[0,0,0]]) == 2
    assert s.orangesRotting([[0,2]]) == 0
    assert s.orangesRotting([[0,2,0],[1,0,0]]) == -1
    assert s.orangesRotting([[0]]) == 0
    assert s.orangesRotting([[2]]) == 0
    assert s.orangesRotting([[1]]) == -1
    assert s.orangesRotting([[1,2]]) == 1
    assert s.orangesRotting([[2, 1, 1, 2]]) == 1
    assert s.orangesRotting([[2, 1, 2], [1, 1, 1], [2, 1, 2]]) == 2
    assert s.orangesRotting([[2, 1, 1], [1, 1, 1], [1, 1, 2]]) == 2
    print("通过")
