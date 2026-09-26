"""
题型: 链表-dummy哑节点
关键点: 合并分两阶段--循环里挑小的，循环外接上整条tail.next = list1 or list2
我踩的坑: 想在一个while里干完两段，循环条件写成while head，if里塞满None判断 ->两都崩
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
    def mergeTwoLists(self, list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
        # ↓↓↓ 把你写好的解法粘到这里 ↓↓↓
        dummy = ListNode()
        tail = dummy
        while list1 and list2:
            if list1.val < list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        tail.next = list1 or list2
        return dummy.next

        # ↑↑↑ 粘完把 pass 删掉 ↑↑↑


if __name__ == "__main__":
    s = Solution()
    # 必测 5 个用例
    assert to_list(s.mergeTwoLists(build([]), build([]))) == []
    assert to_list(s.mergeTwoLists(build([]), build([1, 2]))) == [1, 2]           # 一个空
    assert to_list(s.mergeTwoLists(build([1, 2]), build([]))) == [1, 2]           # 另一个空
    assert to_list(s.mergeTwoLists(build([1, 2, 4]), build([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
    assert to_list(s.mergeTwoLists(build([1]), build([2]))) == [1, 2]
    print("✅ 全部通过")
