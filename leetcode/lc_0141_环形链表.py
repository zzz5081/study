"""
题型:链表-快慢指针追赶问题
关键点：用慢指针追赶快指针，如果追上了即是链表中存在环，否则快指针到终点了即是无环,and会短路，所以fast为空时
不会访问fast.next
我踩的坑：没确定好循环停止条件
"""
class ListNode:
    def __init__(self,val=0,next=None):
        self.val = val
        self.next = next

def build_cycle(vals,pos):
    """pos = -1代表无环,否则让尾节点的next指向pos"""
    if not vals:
        return None
    nodes = [ListNode(v) for v in vals]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if pos != -1:
        nodes[-1].next = nodes[pos]
    return nodes[0]

class Solution:
    def hasCycle(self, head: ListNode|None) -> bool:
        slow = head
        fast = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast == slow:
                return True
        return False

if __name__ == "__main__":
    s = Solution()
    cur = build_cycle([3,2,0,4],1)
    cur1 = build_cycle([1,2],0)
    cur2 = build_cycle([1],-1)
    cur3 = build_cycle([],0)
    cur4 = build_cycle([3,2,0,4],3)
    assert s.hasCycle(None) == False
    assert s.hasCycle(cur) == True
    assert s.hasCycle(cur1) == True
    assert s.hasCycle(cur2) == False
    assert s.hasCycle(cur3) == False
    assert s.hasCycle(cur4) == True
    print("测试成功")