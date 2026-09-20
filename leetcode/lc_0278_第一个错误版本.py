"""
题型:二分查找-找边界
关键点:判断条件改为用函数验证
我踩的坑：忘记//2
"""

is_bad_start = 1

def isBadVersion(version:int):
    return version >= is_bad_start

class Solution:
    def firstBadVersion(self, n: int) -> int:
        left = 1
        right = n
        while left <= right:
            mid = left + (right - left)//2
            if isBadVersion(mid):
                right = mid - 1
            else:
                left = mid + 1
        return left

if __name__ == "__main__":
    for bad in (1, 2, 3, 5):              # 逐个改替身的"答案"
        is_bad_start = bad
        got = Solution().firstBadVersion(5)
        assert got == bad, f"第一个坏版本={bad} 时该返回 {bad}，实际 {got}"
    print("✅ 全部通过")