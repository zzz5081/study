# 26/10/16闭卷默写 卡点：循环条件
def minEatingSpeed(piles, h):
    max_speed = max(piles)
    min_speed = 1
    while min_speed < max_speed:
        time = 0
        k = (max_speed + min_speed)//2
        for num in piles:
            time += (num + k - 1)//k
        if time <= h:
            max_speed = k
        else:
            min_speed = k + 1
    return min_speed

if __name__ == "__main__":
    # 测试用例
    assert minEatingSpeed([3,6,7,11], 8) == 4
    assert minEatingSpeed([30,11,23,4,20], 5) == 30
    assert minEatingSpeed([30,11,23,4,20], 6) == 23
    assert minEatingSpeed([1], 1) == 1
    assert minEatingSpeed([1000000000], 1) == 1000000000
    print("✅ 全部用例通过")
