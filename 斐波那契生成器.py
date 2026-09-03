from typing import Iterator

def fib(limit: int) -> Iterator[int]:
    n,a,b = 0,0,1
    while n < limit:
        yield b
        a,b = b,a+b
        n += 1

for x in fib(5):
    print(x)