# 26/10/20 闭卷重写 34 · 卡点：右边界不会写 + 收缩时 right=mid-1 把候选丢了
# 正确做法：一个 lower_bound 干两件事（target 找左，target+1 减 1 找右）

def searchRange(nums, target):
    def start(nums,target):
        left = 0
        right = len(nums) 
        while left < right:
            mid = (left + right)//2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid 
        return left
    if start(nums,target) == len(nums) or nums[start(nums,target)] != target:
        return [-1,-1]
    return [start(nums,target),start(nums,target+1)-1]
            

# assert 测试用例
if __name__ == "__main__":
    assert searchRange([5,7,7,8,8,10], 8) == [3,4]
    assert searchRange([5,7,7,8,8,10], 6) == [-1,-1]
    assert searchRange([], 0) == [-1,-1]
    assert searchRange([2,2], 2) == [0,1]
    assert searchRange([1],1) == [0,0]
    assert searchRange([1],2) == [-1,-1]
    print("全部通过")
