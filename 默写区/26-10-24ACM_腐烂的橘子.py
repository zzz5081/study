import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    idx = 0
    m = int(data[idx]); idx += 1
    n = int(data[idx]); idx += 1
    grid = []
    for _ in range(m):
        grid.append([int(x) for x in data[idx:idx + n]])
        idx += n

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
        print(0)
        return 
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
    if fresh != 0:
        print(-1)
    else:
        print(minite - 1)

if __name__ == "__main__":
    main()