# 26/10/17闭卷默写 一次写对(哑节点用在141上是不必要的)
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        slow = head
        fast = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if slow == fast:
                return True
        return False


# ========== assert 测试代码 ==========
def build_cyclic_list(arr, pos):
    """构建带环链表，pos=-1无环"""
    if not arr:
        return None
    nodes = [ListNode(v) for v in arr]
    for i in range(len(nodes)-1):
        nodes[i].next = nodes[i+1]
    if pos != -1:
        nodes[-1].next = nodes[pos]
    return nodes[0]

sol = Solution()

# 测试用例1
head1 = build_cyclic_list([3,2,0,-4], 1)
assert sol.hasCycle(head1) == True

# 测试用例2
head2 = build_cyclic_list([1,2], 0)
assert sol.hasCycle(head2) == True

# 测试用例3
head3 = build_cyclic_list([1], -1)
assert sol.hasCycle(head3) == False

# 测试用例4 空链表
head4 = build_cyclic_list([], -1)
assert sol.hasCycle(head4) == False

# 测试用例5 单节点带环
head5 = build_cyclic_list([5], 0)
assert sol.hasCycle(head5) == True

print("全部测试通过！")
