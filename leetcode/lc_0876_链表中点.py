"""
题型: 链表-快慢指针
关键点: while fast and fast.next 这两个条件：1.防崩，2.决定返回第二个中点
我踩的坑: 无
"""
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(vals):
    """[1,2,3] → 链表（dummy + tail 套路）"""
    dummy = ListNode()
    tail = dummy
    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head):
    """链表 → [1,2,3]"""
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


class Solution:
    def middleNode(self, head: ListNode | None) -> ListNode | None:
        # ↓↓↓ 把你写好的解法粘到这里 ↓↓↓
        slow = head
        fast = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
        return slow
        # ↑↑↑ 粘完把 pass 删掉 ↑↑↑


if __name__ == "__main__":
    s = Solution()
    # 用 .val 比对（不能直接比节点对象）
    assert s.middleNode(build([1, 2, 3, 4, 5])).val == 3    # 奇数长度
    assert s.middleNode(build([1, 2, 3, 4])).val == 3       # ★ 偶数 → 第二个中点
    assert s.middleNode(build([1])).val == 1                # 单节点
    assert s.middleNode(build([1, 2])).val == 2             # 两节点 → 第二个
    assert s.middleNode(build([1, 2, 3, 4, 5, 6])).val == 4
    print("✅ 全部通过")
