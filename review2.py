class Stack:
    def __init__(self):
        self.items = []

    def push(self,data):
        self.items.append(data)

    def pop(self):
        if len(self.items) != 0:
            return self.items.pop()
        else:
            return None

    def peek(self):
        if len(self.items) != 0:
            return self.items[-1]
        else:
            return None

    def is_empty(self):
        return len(self.items) == 0

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