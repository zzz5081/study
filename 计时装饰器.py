import time
from typing import Callable,Any

def timer(func: Callable) ->Callable:
    def wrapper(*args: Any,**kwargs: Any) -> Any:
        start = time.time()
        result = func(*args,**kwargs)
        print(f"耗时: {time.time() - start:.4f}秒")
        return result
    return wrapper

@timer
def slow_add(a: int,b: int) -> int:
    time.sleep(0.1)
    return a + b

print(slow_add(1,2))