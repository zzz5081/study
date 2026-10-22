def search(nums, target):
    left = 0
    right = len(nums)
    while left < right:
        mid = (left+right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] > target:
            right = mid
        else:
            left = mid + 1
    return -1 


if __name__ == "__main__":
    assert search([-1,0,3,5,9,12], 9) == 4
    assert search([-1,0,3,5,9,12], 2) == -1
    assert search([5], 5) == 0
    assert search([5], 3) == -1
    print("all passed")
