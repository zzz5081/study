"""
题型:二分查找-找边界
关键点:用一个函数找出这个元素刚开始的位置和下一个元素刚开始的位置，下一个开始位置减一即这
个元素的结束位置；当没有元素时的判定
我踩的坑：用线性扫描找开始的和结束的，效率太低
"""

class Solution:
    def searchRange(self, nums: list[int], target: int) -> list[int]:
        n = len(nums) - 1
        def lower_bound(t: int) -> int:
            left = 0
            right = n
            while left <= right:
                mid = left + (right - left)//2
                if nums[mid] < t:
                    left = mid + 1
                else:
                    right = mid - 1
            return left
        first = lower_bound(target)
        last = lower_bound(target + 1) - 1
        if first == len(nums) or nums[first] != target:
            return [-1,-1]
        return [first,last]

if __name__ == "__main__":
    s = Solution()                                          # ← 加括号
    assert s.searchRange([1,2,2,2,2,2,3], 2) == [1, 5]      # ★ 这条最重要，你没测
    assert s.searchRange([1,2,2,2,2,2,3], 3) == [6, 6]
    assert s.searchRange([1,2,2,2,2,2,3], 4) == [-1, -1]    # target 最大 → guard
    assert s.searchRange([], 3) == [-1, -1]                 # 空数组
    print("✅ 全部通过")