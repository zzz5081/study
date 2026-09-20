"""
题型：二分查找-答案空间
关键点：选择<或<=决定结果要不要分类讨论
我踩的坑：只用普通暴力求解，效率极低
"""


class Solution:
    def mySqrt(self, x: int) -> int:
        left = 0
        right = x
        while left <= right:
            mid = left + (right - left)//2
            if mid*mid < x:
                left = mid + 1
            else:
                right = mid - 1
        return left if left*left <= x else left-1
