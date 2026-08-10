class Stack:
    def __init__(self):
        self.stack = []

    def push(self,data):
        self.stack.append(data)

    def pop(self):
        if len(self.stack) == 0:
            return None
        else:
            return self.stack.pop()

    def peek(self):
        if len(self.stack) == 0:
            return None
        else:
            return self.stack[-1]

    def is_empty(self):
        if len(self.stack) == 0:
            return True
        else:
            return False

s = Stack()
print(s.is_empty())   # True

s.push(1)
s.push(2)
s.push(3)

print(s.is_empty())   # False
print(s.peek())       # 3
print(s.pop())        # 3
print(s.pop())        # 2
print(s.pop())        # 1
print(s.pop())        # None

        