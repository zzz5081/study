"""
题型:二分查找-找插入点
关键点：找不到target的时候要return left
我踩的坑:1忘记了缩小边界；
"""

class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
        return left

if __name__ == '__main__':
    s = Solution()
    assert s.searchInsert([1,3,5,6],0) == 0
    assert s.searchInsert([1,3,5,6],3) == 1
    assert s.searchInsert([1,3,5,6],7) == 4
    print("测试通过")