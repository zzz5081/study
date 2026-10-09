# FastAPI 速查表

> 来源：2026-10-05 ~ 10-06（W5）实操
> 用法：忘了怎么跑 / 忘了某个概念就翻这里

---

## 零、怎么运行（最常用的）

```powershell
# ① 进项目目录（有 main.py 的那个）
cd C:\Users\zzz\Desktop\code-practice

# ② 启动
python -m uvicorn main:app --reload

# ③ 浏览器打开
http://127.0.0.1:8000/docs      ← 自动生成的接口文档（能点着测试）
http://127.0.0.1:8000/          ← 你自己写的路由
```

**停止**：终端按 `Ctrl + C`

### 命令怎么读
```
python -m uvicorn main:app --reload
       └──┬───┘ └──┬──┘ └─┬─┘ └──┬───┘
        用模块方式   文件名:对象  改代码自动重启
        main.py 里的 app 变量
```

> ⭐ **`--reload`**：改代码保存 → 服务自动重启 → 刷新浏览器即可，不用重开。

### 常见报错
| 现象 | 解决 |
|---|---|
| `uvicorn` 不是命令 | 用 `python -m uvicorn ...` |
| `Could not import module "main"` | 不在 `main.py` 所在目录 → `cd` 过去 |
| `address already in use` | 加 `--port 8001`（浏览器也改） |
| 浏览器打不开 | 看终端报错；确认是 `http://` 不是 https |

---

## 一、最小可运行骨架

```python
from fastapi import FastAPI

app = FastAPI(title="我的应用")          # 这个名字会显示在 /docs 顶部


@app.get("/")                            # 装饰器：声明"GET / 走这个函数"
def read_root():
    return {"message": "Hello"}
```

---

## 二、三种参数（🔴 判定规则是重点）

```python
@app.get("/users/{user_id}")                 # ← 写在路径 {} 里
def get_user(user_id: int):
    ...

@app.get("/users")                           # ← 不写在路径里
def list_users(skip: int = 5, limit: int = 10):
    ...
```

### 🔑 两条**互相独立**的规则

| 判断 | 依据 | 结果 |
|---|---|---|
| **路径参数 vs 查询参数** | **在不在路径字符串的 `{}` 里** | 在 → `path`；不在 → `query` |
| **必填 vs 可选** | **有没有默认值** | 有 → 可选；没有 → 必填 |

**实测证据**（FastAPI 自己生成的文档数据）：
```
GET /a/{uid}   ->  uid(in=path,  required=True)
GET /b         ->  skip(in=query, required=False)     ← 有默认值
GET /c         ->  start(in=query, required=True)     ← 没默认值，但仍是 query！
```

> ⚠️ **容易搞混的点**：`skip: int`（去掉默认值）**仍然是查询参数**，只是变成必填。
> **「是不是 path」只看 `{}`；「是不是必填」只看默认值。**

### 类型标注会自动转换 + 校验

```
/users/5      → 200  {"user_id": 5}          ← 字符串 "5" 自动转成 int 5
/users/abc    → 422  "Input should be a valid integer..."   ← 转不了就拒绝
/users/-3     → 200  （负数也是合法 int）
/users/5.5    → 422  （5.5 不是 int）
```

**改成 `user_id: str` 就变成 `{"user_id": "5"}`** —— 因为字符串不需要转换。

---

## 三、请求体 + Pydantic

```python
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    age: int = Field(ge=0, le=150)                          # 0 <= age <= 150
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")     # 邮箱格式


@app.post("/users")
def create_user(user: UserCreate):        # ← 参数类型是 Pydantic 模型 → 自动当请求体
    return {"收到": user, "名字": user.name}
```

### Pydantic 做两件事
1. **类型转换**：能转就转（`"22"` → `22`），转不了就 422
2. **必填校验**：**没有默认值的字段都必须给**

### 想让字段可选 → 给默认值
```python
age: int | None = None       # 可以不传 → None
email: str = "未填"           # 可以不传 → "未填"
```

### 加约束 → 用 `Field(...)`
```python
Field(min_length=1, max_length=20)   # 字符串长度
Field(ge=0, le=150)                   # 数值范围（ge = greater or equal）
Field(pattern=r"...")                 # 正则
```
**实测全部自动拦截**（422）：
```
age = -5        → "Input should be greater than or equal to 0"
email = 不是邮箱 → "String should match pattern '...'"
name = ""       → "String should have at least 1 character"
```

### 错误信息的结构
```json
{"detail": [{
  "loc": ["body", "age"],        ← 哪个位置（body/query/path）+ 哪个字段
  "msg": "Field required",
  "input": {"name": "张三"}
}]}
```
> **前端可以直接拿 `loc` + `msg` 显示错误提示** —— 生产项目就是这么用的。

---

## 四、错误处理 `HTTPException`

```python
from fastapi import HTTPException

if item_id not in DB:
    raise HTTPException(status_code=404, detail="这个 item 不存在")
```

### 状态码表（项目1 天天用）

| 码 | 含义 | 用在哪 |
|---|---|---|
| **400** | 请求有错 | 参数格式对但语义不对 |
| **401** | **未认证** | 没带 token / token 无效 → 去登录 |
| **403** | **无权限** | 登录了但权限不够 |
| **404** | 找不到 | 资源不存在 |
| **409** | 冲突 | **邮箱已注册**（unique 冲突） |
| **422** | 校验失败 | **FastAPI 自动返回，不用你写** |
| **429** | 请求过多 | **限流** ← 项目1 核心功能 |
| **500** | 服务器错误 | 你的代码 bug |
| **502** | 上游挂了 | **LLM 调用失败** ← 项目1 会用 |

> 🔑 **401 vs 403**：**401 = 我不知道你是谁；403 = 我知道你是谁，但你没权限。**

### 自定义异常（可选）
```python
class LLMError(Exception):
    pass


@app.exception_handler(LLMError)
async def llm_error_handler(request, exc: LLMError):
    return JSONResponse(status_code=502, content={"detail": f"模型调用失败：{exc}"})
```
> 业务代码里随便 `raise LLMError("超时了")`，**状态码统一在一处决定**。

---

## 五、依赖注入 `Depends` ⭐（FastAPI 最有特色）

### 解决什么问题
10 个接口都要"先验证登录" → **不想写 10 遍**（重复代码 = 改动会漏）

### 怎么写

```python
from fastapi import Depends, Header

# ① 把"公共准备工作"抽成一个函数
def get_current_user(token: str = Header(default="")):
    if not token:
        raise HTTPException(401, "缺少 token")
    user = USERS.get(token)
    if user is None:
        raise HTTPException(401, "token 无效")
    return user                    # ← 这个返回值会被"注入"


# ② 接口里一行就够
@app.get("/me")
def read_me(user=Depends(get_current_user)):
    return {"我是": user["name"]}
```

### 三个动作
```
① 【自动调用】 get_current_user()
② 如果它 raise HTTPException → 请求【当场失败】，接口函数根本不执行
③ 成功 → 返回值【注入】给 user 参数
```

### 实测结果
```
不带 token           → 401 缺少 token
错 token             → 401 token 无效
普通用户 /me         → 200
普通用户 /admin      → 403 需要管理员权限
管理员 /admin        → 200
```

### 依赖可以嵌套
```python
def get_admin_user(user=Depends(get_current_user)):    # ← 依赖里再用依赖
    if user["role"] != "admin":
        raise HTTPException(403, "需要管理员权限")
    return user
```
**执行顺序（从外到内）**：取 token → 验证登录 → 验证管理员 → 最后才进接口函数

### 🚀 这就是 W6 做 JWT 的机制
```python
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    ...
```
**接口那边一个字都不用改。**

---

## 六、为什么 FastAPI 能"自动校验 + 自动生成 /docs"

### 🔑 因为它在**运行时读你的类型标注**（内省 / 反射）

```python
@app.get("/a/{uid}")       # ← 装饰器告诉它：有个 GET 路由，路径长这样
def a(uid: int):           # ← 函数签名告诉它：参数叫 uid，类型 int，在路径里
```

**FastAPI 启动时"照镜子"读自己** → 生成 `openapi.json` → `/docs` 渲染它。
**全程在你自己电脑上，没有上传给任何服务**（`/openapi.json` 你也能直接访问）。

### 📌 和 SQLAlchemy 是**同一个机制**
```python
id: Mapped[int] = mapped_column(...)   # SQLAlchemy 读这个标注 → 决定列类型
def get_user(user_id: int):            # FastAPI 读这个标注 → 决定参数类型 + 生成文档
```
> **Python 的类型标注有两个消费者**：
> ① 静态检查器（mypy / IDE）—— 写代码时用
> ② **运行时框架（SQLAlchemy / FastAPI / Pydantic）—— 真的读它做事**
>
> **这就是「FastAPI 和 Flask 有什么不同」的标准答案。**

---

## 七、踩过的坑

| 坑 | 说明 |
|---|---|
| **HTTP 请求头只能是 ASCII** | 中文 token → `UnicodeEncodeError`。**这就是为什么 JWT 要 base64 编码** |
| `skip: int` 去掉默认值 | 仍然是 query 参数，只是变成**必填**（不是变成 path） |
| 中文引号 `"…"` 写进双引号字符串 | `SyntaxError` —— 用「」 |
| `response_model` 不写 | **可能把密码哈希返回给前端**（见下节，待补） |

---

## 八、机制七问（2026-10-09 实测整理）

> 这一节回答的是"**为什么这样**"，不是"怎么写"。全是实测输出，不是断言。

### ① `models.py` 里的 Pydantic 类 —— 是"图纸/模具"

| 名字 | 是什么 | 装数据吗 |
|---|---|---|
| `class ChatIn(BaseModel)` | **图纸**（规定请求必须长什么样） | ❌ 不装 |
| `ChatIn(prompt="你好")` | **用图纸压出来的那一个** | ✅ 装，只活一次请求 |

**三个作用：** ① 校验**进**来的请求体 ② 过滤**出**去的响应 ③ 自动生成 `/docs`

### ② `@app.get` / `@app.post` —— 不是"检查"，是**登记路由**

**实测：登记后 `app.routes` 里多了这些**
```
['GET']   /health
['POST']  /v1/chat
['GET']   /v1/usage
```

`@app.get('/health')` = 「把下面这个函数登记进路由表：**用 GET 访问 `/health` 时调用它**」
（`@app.get(...)` 就是 `app.get('/health')(函数)`，把函数存进 `app.routes`）

| 方法 | 语义 | 例子 |
|---|---|---|
| **GET** | **读**，不该改数据 | `/health`、`/v1/usage` |
| **POST** | **提交/创建**，会改数据 | `/auth/login`、`/v1/chat` |

> **为什么 login 必须 POST？** GET 的参数会出现在 URL 里 → 密码进浏览器历史/服务器日志/代理缓存。POST 放在请求体里。

### ③ 冒号后的类名 —— **Python 不检查，FastAPI 才检查**

```python
def f(x: int): return x
f('hello')   # -> 'hello'   ← 标注说 int，传字符串照样跑！不报错
```

**类型标注只是标签/元数据。是 FastAPI 主动读它（`inspect.signature`）才产生校验。**

```
请求进来 → FastAPI 读签名 → 试着用请求体构造 ChatIn
        → 不符合图纸 → 【422】，函数体【一行都不执行】
        → 符合       → 才调用 chat(data, ...)
```

> **422 不是崩溃，是 FastAPI 在挡你。** 所以函数体里不用写任何"字段对不对"的判断。

### ④ `secrets` 怎么造 token

```
secrets.token_hex(8) → 向操作系统要 8 字节真随机数（os.urandom）→ 16 个十六进制字符
                     → 64 位 = 2^64 ≈ 1.8×10¹⁹ 种可能
```

**实测为什么不能用 `random`：**
```
random.seed(1); [random.randint(0,9) for _ in range(8)] -> [2,9,1,4,1,7,7,7]
random.seed(1); [random.randint(0,9) for _ in range(8)] -> [2,9,1,4,1,7,7,7]  ← 完全一样！
```
`random` 是伪随机，**种子一样结果就一样** → 能被推算 → **不能做密钥**。

### ⑤ `response_model` vs `responses` —— 名字像，作用相反

| | 干什么 | 会动数据吗 |
|---|---|---|
| **`response_model=ChatOut`** | 把 `return` 的东西**过滤+转换**成 ChatOut 的形状 | ✅ **真的删字段** |
| **`responses={401: {...}}`** | 只是写进 `/docs` 的一句说明 | ❌ **完全不动数据** |

**实测（删掉 `responses` 会怎样）：**
```
带 responses 的 openapi: ['200', '401']
不带 responses 的 openapi: ['200']      -> 运行时行为完全一样
```

> 🔑 **`response_model` = 安全边界**（靠它挡住密码）／**`responses` = 给调用方看的合同说明**

### ⑥ `Depends` —— 不是"检查"，是**真的调用**

```
请求进来
  → FastAPI 解析 Header 拿到 token
  → 【真的调用】get_current_user(token)
        ├─ raise HTTPException(401) → 【请求在这里结束】，chat 函数不执行
        └─ 没抛异常 → 返回 user dict
  → 把 user dict 塞进 chat 的 user 参数
  → 才调用 chat(data, user)
```

> 所以 `Depends` **不只是取值，还是一个关口** —— `/v1/chat` 不带 token 返回 401，
> 就是因为依赖抛了异常，函数体压根没跑。依赖还能**嵌套**。

**⚠️ 坑：`Depends(f)` 不加括号**
```
Depends(get_current_user)    -> dependency=<function get_current_user>   ✅
Depends(get_current_user())  -> dependency={'username': 'zhong'}         ❌ 一个 dict
→ TypeError: {'username': 'zhong'} is not a callable object（装饰器求值时当场炸，服务起不来）
```

### ⑦ `user['username']` 的数据从哪来（完整链路）

```
【起点】auth.py 写死的：
   USERS = {"zhong": {"username": "zhong", "password": "123456"}}
                                       ↑ 键名就叫 'username'

   ↓ 有人登录
【login】TOKENS[token] = data.username
   TOKENS = {'7180804c': 'zhong'}          ← 存下 "token → 用户名"

   ↓ 有人带 token 调 /v1/chat
【get_current_user】两次换：
   ① username = TOKENS[token]   -> 'zhong'
   ② return USERS[username]     -> {'username': 'zhong', 'password': '123456'}

   ↓ 返回值被塞进 chat 的 user 参数
【chat】user['username'] -> 'zhong'
```

> ## 🔑 引号规则（这一条搞懂，5 次的老毛病就断根）
> **这个键，是你"直接写出来的"，还是"从别处拿来的"？**
>
> | 想拿的东西 | 写什么 | 为什么 |
> |---|---|---|
> | dict 里那个**叫 username 的字段** | `user['username']` | 键名**写死在代码里** → **加引号** |
> | 名字**存在变量 `name` 里** | `user[name]` | 键名在**变量**里 → 不加引号 |
> | 用户对象 `data` 的 username 属性 | `USERS[data.username]` | 键名从**对象**取 → 不加引号 |
>
> ```
> 'username'       ← 字典"出厂"就带好的固定名字，永远不变
>  data.username   ← 要运行到这一步才知道是啥
> ```
