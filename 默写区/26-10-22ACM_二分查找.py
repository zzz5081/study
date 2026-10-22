import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    nums = [int(x) for x in data[idx:idx + n]]
    idx += n
    target = int(data[idx]) 
    
    left = 0
    right = len(nums)
    while left < right:
        mid = (left + right)//2
        if nums[mid] == target:
            print(mid)
            return
        elif nums[mid] > target:
            right = mid
        else:
            left = mid + 1
    print(-1)
if __name__ == "__main__":
    main()
    