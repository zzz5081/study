# 题型：DP，以i为结尾i
#  关键点，以i为结尾，算每一个以i结尾的组合大小
# 我踩的坑：没有算每一个，就只算了以最后一位结尾
from functools import lru_cache

class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        @lru_cache(maxsize=None)
        def f(n):
            if n == 0:
                return nums[0]
            return max(nums[n],f(n-1) + nums[n])
        return max([f(x) for x in range(len(nums))])
class Solution1:
    def maxSubArray(self, nums: list[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        prev = nums[0]
        best = nums[0]
        for i in range(1,len(nums)):
            cur = max(prev + nums[i],nums[i])
            prev = cur
            best = max(best,cur)
        return best
if __name__ == '__main__':
    s = Solution()
    c = Solution1()
    assert s.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert c.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert s.maxSubArray([1]) == 1
    assert c.maxSubArray([1]) == 1
    assert s.maxSubArray([5, 4, -1, 7, 8]) == 23
    assert c.maxSubArray([5, 4, -1, 7, 8]) == 23
    assert s.maxSubArray([-1]) == -1  # ★ 全是负数
    assert c.maxSubArray([-1]) == -1  # ★ 全是负数
    assert s.maxSubArray([-3, -1, -2]) == -1  # ★ 全负 → 挑最大的那个单个元素
    assert c.maxSubArray([-3, -1, -2]) == -1  # ★ 全负 → 挑最大的那个单个元素
    assert s.maxSubArray([-2, -1]) == -1
    assert c.maxSubArray([-2, -1]) == -1
    import random
    big = [random.randint(-100,100) for _ in range(10000)]
    assert  c.maxSubArray(big) == s.maxSubArray(big)
    print("通过")