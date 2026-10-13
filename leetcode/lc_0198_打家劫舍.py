# 题型：DP取最大情况
# 关键点：递归思想：站在最后一步的位置想有几种选择，每一种选择归成更小的问题加当前代价
# 我踩的坑：没想清楚f(i)代表什么
# 忘记在外面写return内部函数,忘加len()
# import了 lru_cache但是忘加了装饰器 -> 指数级 ->会TLE
#     （连续第二题栽在缓存未生效上：昨天挂错层，今天忘挂了）
#       教训：结果全对 ≠ 对；归档前必须【计时】或看 cache_info


from functools import lru_cache

class Solution:
    def rob(self, nums: list[int]) -> int:
        @lru_cache
        def f(i):
            if i == 1:
                return nums[0]
            if i == 2:
                return max(nums[0],nums[1])
            return max(nums[i-1]+f(i-2),f(i-1))
        result = f(len(nums))
        print(f.cache_info())
        return result
# 解法B（迭代，有余力）：O(n) 时间，O(1) 空间
# def rob(self, nums):
#     n = len(nums)
#     if n == 1:
#         return nums[0]
#     prev2, prev1 = 0, nums[0]              # f(0), f(1)
#     for i in range(2, n + 1):
#         prev2, prev1 = prev1, max(prev1, prev2 + nums[i - 1])
#     return prev1
if __name__ == '__main__':
    s = Solution()
    assert s.rob([1, 2, 3, 1]) == 4
    assert s.rob([2, 7, 9, 3, 1]) == 12
    assert s.rob([5]) == 5  # 只有一栋
    assert s.rob([2, 1]) == 2  # ★ 两栋 -> 挑大的（你原来错在这）
    assert s.rob([2, 7, 9, 3, 1, 10]) == 21
    print('通过')