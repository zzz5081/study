# 题型：双指针链表
# 关键点：用双指针找倒数第N个节点的前一个的位置，链表问题先建哑节点
# 我踩的坑：先想只用单指针，遍历一遍数出所有节点再减去n算出要走的节点数，n = 1 时还需要分情况讨论
# 然后又想用快指针和慢指针把要删的节点包起来，但是也需要分情况讨论

class ListNode:
    def __init__(self,val = 0,next = None):
        self.val = val
        self.next = next

def build(vals):
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def to_list(head):
    li = []
    cur = head
    while cur:
        li.append(cur.val)
        cur = cur.next
    return li

class Solution:
    def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
        dummy = ListNode(0,head)
        # 约束：1 <= sz <= 30，1 <= n <= sz
        #   → head 不会为空、n 不会超长，所以这里不做空链表 / 越界保护
        slow = dummy
        fast = dummy.next
        for _ in range(n):
            fast = fast.next
        while fast:
            slow = slow.next
            fast = fast.next
        slow.next = slow.next.next
        return dummy.next

if __name__ == '__main__':
    s = Solution()
    assert to_list(s.removeNthFromEnd(build([1,2,3,4,5]),1)) == [1,2,3,4]
    assert to_list(s.removeNthFromEnd(build([1,2]),2)) == [2]
    assert to_list(s.removeNthFromEnd(build([1,2,3]),2)) == [1,3]
    assert to_list(s.removeNthFromEnd(build([1]),1)) == []
    # assert to_list(s.removeNthFromEnd(build([]),0)) == []
    print('通过')
