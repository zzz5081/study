class ListNode:
    def __init__(self, data):
        self.val = data
        self.next = None

def append(head,data):
    cur = head
    if head is None:
        head = ListNode(data)
        return head
    else:
        while cur.next is not None:
            cur = cur.next
        cur.next = ListNode(data)
        return head


def print_list(head):
    qur = head
    while qur is not None:
        print(qur.val)
        qur = qur.next

if __name__ == '__main__':
    list0 = None
    list1 = ListNode(1)
    list1.next = ListNode(123)
    list1.next.next = ListNode(456)
    list1 = append(list1,789)
    list0 = append(list0,123)
    print("_________________________________________________")
    print_list(list1)





