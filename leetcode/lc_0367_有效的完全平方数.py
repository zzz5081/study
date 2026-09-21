"""
题型：二分查找
关键点：只需要判断完全平方数是不是整数
"""
class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        left = 0
        right = num
        while left <= right:
            mid = left + (right - left) // 2
            if mid * mid == num:
                return True
            elif mid * mid < num:
                left = mid + 1
            else:
                right = mid - 1
        return False

if __name__ == "__main__":
    s = Solution()
    assert s.isPerfectSquare(25) == True
    assert s.isPerfectSquare(0) == True
    assert s.isPerfectSquare(17) == False
    print("测试成功")