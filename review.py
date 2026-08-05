class ListNode:
    def __init__(self,val):
        self.val = val
        self.next = None

def append(head,data):
    tmp = ListNode(data)
    if head is None:
        return tmp
    cur = head
    while cur.next is not None:
        cur = cur.next
    cur.next = tmp
    return head

def insert(head,ver,data):
    cur = head
    count = 1
    if ver == 0 or head is None:
        data.next = head
        return data
    else:
        while count != ver:
            cur = cur.next
            count += 1
            if cur.next is None:
                cur.next = data
                return head
        tmp = cur.next
        cur.next = data
        cur = cur.next
        cur.next = tmp
        return head

def delete(head,data):
    if head is None:
        return None
    cur = head
    if data == head.val:
        head = head.next
    while cur.next != data:
        cur = cur.next
        if cur.next is None:
            return head
    cur.next = cur.next.next
    return head

def find(head,data):
    if head is None:
        return None
    cur = head
    count = 1
    while cur.val != data:
        cur = cur.next
        count += 1
        if cur is None:
            return None
    return count

def get_length(head):
    cur = head
    count = 0
    while cur is not None:
        cur = cur.next
        count += 1
    return count

list1 = None
list1 = append(list1, 1)
list1 = append(list1, 2)
list1 = append(list1, 3)

list1 = delete(list1, 1)     # [2, 3]
list1 = delete(list1, 9)     # [2, 3] 不变
print(find(list1, 2))        # 1
print(find(list1, 9))        # None
print(get_length(list1))     # 2
print(get_length(None))      # 0







