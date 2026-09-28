class Animal:
    def __init__(self,name):
        self.name = name
    def speak(self):
        return (f'我是{self.name}')
    def __str__(self):
        return f"Animal{self.name}"
class Dog(Animal):
    def __init__(self,name,breed):
        super().__init__(name)
        self.breed = breed
    def speak(self):
        return super().speak() + ",汪汪"
a = Dog('豆米','中华田园犬')
b = Dog('旺财','柴犬')
print(a)
print(a.speak())
print(b)
print(b.speak())
