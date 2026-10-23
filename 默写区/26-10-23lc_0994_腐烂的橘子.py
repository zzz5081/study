from collections import deque

class Solution:
    def orangesRotting(self, grid):
        m = len(grid)
        n = len(grid[0])
        q = deque([])
        fresh = 0
        minite = 0
        for i in range(m) :
            for j in range(n):
                if grid[i][j] == 2:
                    q.append((i,j))
                elif grid[i][j] == 1:
                    fresh += 1
        act = [(1,0),(0,1),(-1,0),(0,-1)]
        if fresh == 0:
            return 0 
        while q:
            num = len(q)
            for _ in range(num):
                x,y = q.popleft()
                for xi,yi in act:
                    if 0 <= xi+x < m and 0 <= yi+y < n and grid[xi+x][yi+y] == 1:
                        grid[xi+x][yi+y] = 2
                        fresh -= 1
                        q.append((xi+x,yi+y))
            minite += 1
        return -1 if fresh != 0 else minite - 1
sol = Solution()
assert sol.orangesRotting([[2,1,1],[1,1,0],[0,1,1]]) == 4
assert sol.orangesRotting([[2,1,1],[0,1,1],[1,0,1]]) == -1
assert sol.orangesRotting([[0,2]]) == 0
print("all pass")
