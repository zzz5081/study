# 题型：DP（不计算重复的）
# 关键点：时间复杂度，可以直接递归时间复杂度太大，可以使用@lru_cache装饰器或者迭代方法
# 我踩的坑：把数学的 = 写进了 Python -- 数学的 = 是'定义为',要翻成 return;f(1) = 1要翻成if n==1: return 1
#         @lru_cache 挂在方法上,但是方法里递归的是没有装饰器的内层f
#             缓存hit=0,等于没挂.装饰器必须挂在会自己调用自己的那个函数上
#           而且结果全对,只是慢 - 不跑计时根本发现不了

# 解法A: 朴素递归（指数级，n=35 要 0.66 秒）
class SolutionA:
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2
        return self.climbStairs(n-1) + self.climbStairs(n-2)

# 解法B: 记忆化递归（递归 + @lru_cache）
from functools import lru_cache
class SolutionB:
    @lru_cache()
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2
        return self.climbStairs(n-1) + self.climbStairs(n-2)
# 解法C: 迭代 / 自底向上 DP（O(n) 时间，O(1) 空间）
class SolutionC:
    def climbStairs(self, n: int) -> int:
        a = 1
        b = 2
        if n == 1:
            return a
        for _ in range(3,n+1):
            a,b = b,a+b
        return b
if __name__ == '__main__':
    s = SolutionB()
    a = SolutionA()
    c = SolutionC()
    assert s.climbStairs(1) == 1
    assert s.climbStairs(2) == 2
    assert s.climbStairs(3) == 3
    assert s.climbStairs(4) == 5
    assert s.climbStairs(5) == 8
    assert a.climbStairs(35) == s.climbStairs(35)
    assert c.climbStairs(35) == s.climbStairs(35)
    import time
    t = time.time()
    print(a.climbStairs(35))
    print("A用了", time.time() - t, "秒")
    t = time.time()
    print(s.climbStairs(35))
    print("B用了", time.time() - t, "秒")
    t = time.time()
    print(c.climbStairs(35))
    print("C用了", time.time() - t, "秒")
    print('通过')