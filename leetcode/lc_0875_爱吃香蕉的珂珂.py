"""
题型：二分查找
关键点：找准边界，向上取整
我踩的坑：一开始以为hours可以直接piles/mid得到，查了向上取整的方法
"""
class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        left = 1
        right = max(piles)
        while left <= right:
            mid = left + (right - left)//2
            hours = 0
            for i in piles:
                hours += (i + mid - 1)//mid
            if hours > h:
                left = mid + 1
            else:
                right = mid - 1
        return right + 1

if __name__ == '__main__':
    s = Solution()
    assert s.minEatingSpeed([3,6,7,11],8) == 4
    assert s.minEatingSpeed(([3]),3) == 1
    assert s.minEatingSpeed([3],1) == 3
    print("测试成功")