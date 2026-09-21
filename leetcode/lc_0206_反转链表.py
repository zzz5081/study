"""
题型:链表-3指针(prev/cur/next)
关键点:先存next再反转指向，循环退出时prev是新头
我踩的坑：while cur.next最后一个节点没有被处理;return cur 应为 return prev；自己写的build只有一个节点
,没给next赋值
"""
class ListNode:
    def __init__(self,val=0,next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: ListNode | None) -> ListNode | None:
        prev = None
        cur = head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        return prev

def build(vals):
    dummy = ListNode()
    tail = dummy
    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_list(head):
    li = []
    while head:
        li.append(head.val)
        head = head.next
    return li

if __name__ == "__main__":
    print(to_list(build([1,2,3])))
    assert to_list(Solution().reverseList(build([]))) == []
    assert to_list(Solution().reverseList(build([1]))) == [1]
    assert to_list(Solution().reverseList(build([1,2]))) == [2,1]
    assert to_list(Solution().reverseList(build([1,2,3,4,5]))) == [5,4,3,2,1]
    print("✅ 全部通过")