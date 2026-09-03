from typing import Callable,Any

status = "未登录"

def login_required(func: Callable) -> Callable:
    def wrapper(*args: Any,**kwargs: Any) -> Any:
        if status == "未登录":
            print("请先登录")
            return None
        return func(*args,**kwargs)
    return wrapper

@login_required
def add(a: int,b: int) ->int:
    return a+b

print(add(1,2))