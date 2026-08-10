from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self,data):
        self.items.append(data)

    def dequeue(self):
        if len(self.items) == 0:
            return None
        else:
            return self.items.popleft()

    def peek(self):
        if len(self.items) == 0:
            return None
        else:
            return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

q = Queue()
print(q.is_empty())
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
print(q)