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
    return head

def insert(head, index,data):
    cur = head
    count = 1
    if index == 0:
        head = ListNode(data)
        head.next = cur
        return head
    elif index >= 1:
        while index != count:
            count = count + 1
            cur = cur.next
        new_data = ListNode(data)
        new_data.next = cur.next
        cur.next = new_data
    return head

def delete(head,data):
    if head is None:
        return None
    cur = head
    if head.val == data:
        head = cur.next
    else:
        qur = head
        cur = cur.next
        while cur.val != data and cur.next is not None:
            cur = cur.next
            qur = qur.next
        if cur.val == data:
            last = cur.next
            qur.next = last
    return head
#
# def find(head,data):
#     cur = head
#     count = 1
#     if cur is None:
#         return None
#     else:
#         while cur.val != data and cur.next is not None:
#             cur = cur.next
#             count += 1
#             if cur.val == data:
#                 return count
#             elif cur.val !=data and cur.next is None:
#                 return None
#         return 1

def find(head,data):
    cur = head
    count = 1
    while cur is not None:
        if cur.val == data:
            return count
        cur = cur.next
        count += 1
    return None

def get_length(head):
    cur = head
    count = 0
    while cur is not None:
        cur = cur.next
        count += 1
    return count


if __name__ == '__main__':
    list0 = None
    list1 = ListNode(1)
    list1.next = ListNode(123)
    list1.next.next = ListNode(456)
    print(find(list1,1))
    # print_list(list1)
    print(get_length(list0))






