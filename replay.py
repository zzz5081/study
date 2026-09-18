class Counter:
    def __init__(self,name):
        self.name = name
        self.count = 0

    def add(self):
        self.count += 1

    def show(self):
        print(f"{self.name}:{self.count}")

c = Counter("点击量")
c.add()
c.add()
c.show()

c1 = Counter("第一个")
c2 = Counter("第二个")
c1.add()
c2.add();c2.add()
c1.show()
c2.show()