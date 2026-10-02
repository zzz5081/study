# SQLAlchemy 速查表

> 来源：2026-10-01 ~ 10-02（W4）实操 + 实测报错
> 用法：写 ORM 前扫一眼；面试前重点看「Session 三层」和「N+1」

---

## 零、连接串

```
mysql+pymysql://dev:dev123456@localhost/practice_db?charset=utf8mb4
```

> ⚠️ **应用不要用 root 连数据库**（最小权限原则）。`dev` 账号只对 `practice_db` 有权限。
>
> ⚠️ MySQL 8 默认 `caching_sha2_password` → **pymysql 需要 `cryptography` 库**，
> 否则报 `Access denied ... (using password: NO)`（CLI 能连、Python 连不上就是这个原因）。

---

## 一、三大件 + 第一个模型

| 东西 | 是什么 | 类比 |
|---|---|---|
| `create_engine(URL)` | **连数据库**的引擎（管连接池） | ☎️ 电话线 |
| `Base`（继承 `DeclarativeBase`） | **模型基类** | 📐 图纸的族谱 |
| `Session(engine)` | **会话**，增删改查都通过它 | 🗣 通话窗口 |
| `practice_db` | 真正的数据库 | 🏢 电话那头 |

```python
from sqlalchemy import String, create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

URL = "mysql+pymysql://dev:dev123456@localhost/practice_db?charset=utf8mb4"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"                             # 表名，一律小写
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    age: Mapped[int]                                    # 不需要额外细节就只写标注
    email: Mapped[str] = mapped_column(String(50), unique=True)


engine = create_engine(URL, echo=True)   # echo=True → 打印真实 SQL（重要！）
Base.metadata.create_all(engine)         # 建表
```

### 🔑 列定义那一行的结构

```
 id   :   Mapped[int]   =   mapped_column(primary_key=True)
 ↑         ↑                      ↑
属性名   ①标注（冒号）          ②赋值（等号）
```

| | 写什么 | 作用 | 是什么 |
|---|---|---|---|
| ① | `: Mapped[int]` | 这列**是什么类型** | 进 `__annotations__`，**不是值** |
| ② | `= mapped_column(...)` | 这列的**细节**（主键/长度/唯一） | **是真的值** |

> ⚠️ `mapped_column` 是**独立函数**（从 `sqlalchemy.orm` import），**不是 `Mapped` 的方法**。
> ❌ `Mapped[int].mapped_column(...)`

### `Base` 的机制（实测）

```
① 刚定义 Base                → Base.metadata.tables = []
② 写下 class User(Base)      → Base.metadata.tables = ['users']      ← 自动登记！
③ 再写 class Post(Base)      → Base.metadata.tables = ['users', 'posts']
```

**继承 `DeclarativeBase` 的类被创建时，会自动进 `Base.metadata` 登记册。**
`create_all()` = "把登记册里每张表翻译成 `CREATE TABLE` 建出来"。

### ⚠️ `create_all` 的两个坑

1. **表存在就跳过**（日志里那句 `DESCRIBE` 就是它在检查）→ **它永远不改已存在的表**
   → 加字段必须 `DROP TABLE` 重建（正式项目要用迁移工具 **Alembic**）
2. **表名大小写**：Windows 上 MySQL 不区分，**Linux 上区分**
   → **表名一律小写**，否则"本地正常、上线表不存在"

---

## 二、CRUD（必须闭卷能写）

```python
# 清空表 + 重置自增（让脚本可重复跑）
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE users"))

# ---------- C 增 ----------
with Session(engine) as session:
    u = User(name="张三", age=22, email="zhangsan@test.com")
    session.add(u)                 # 或 session.add_all([u1, u2])
    session.commit()

# ---------- R 查 ----------
with Session(engine) as session:
    user = session.get(User, 1)                          # 按主键 → 对象或 None

    stmt = select(User).where(User.age >= 22).order_by(User.age.desc())
    for u in session.scalars(stmt):                      # 复数！遍历多条
        print(u.name)

# ---------- U 改 ----------
with Session(engine) as session:
    user = session.get(User, 1)
    user.age = 23                  # 只改属性，不用 add（脏检查）
    session.commit()

# ---------- D 删 ----------
with Session(engine) as session:
    user = session.get(User, 1)
    session.delete(user)           # 🔑 是 session.delete(u)，不是 u.delete()
    session.commit()
```

### 📌 一句话总结

```
开会话 → with Session(engine) as session:
增     → session.add(对象)    + commit()
查     → session.get(User, id)  /  session.scalars(select(User).where(...))
改     → 对象.属性 = 新值     + commit()
删     → session.delete(对象) + commit()
```

### ⚠️ 易错点

| 错法 | 正确 | 为什么 |
|---|---|---|
| `u = ('张三', 22, 'a.com')` | `u = User(name=..., age=...)` | 元组不是模型对象，`add()` 会拒绝 |
| `session.scalar(stmt)` | `session.scalars(stmt)` | **单数只取第一条**，多条要用复数 |
| `.where(u.age >= 22)` | `.where(User.age >= 22)` | `User.age` 是**列定义**；`u.age` 是值，且 `u` 可能是 `None` |
| `u.delete(User)` | `session.delete(u)` | `delete` 长在 **Session** 身上（`hasattr(User,'delete')` → False） |
| `session.get(User, 0)` | id 从 **1** 开始 | 自增主键从 1 起，查 0 得到 `None` |

---

## 三、🔑 Session 三层：`add` / `flush` / `commit`

```
session.add_all(objs)     → 【登记】session 知道"这几个要存"，数据库无动静
                             ⚠️ 此时 obj.id 还是 None

session.flush()           → 【发 SQL】INSERT 真发出去
                             ✅ 数据库生成 id 并回填到对象
                             ✅ 对象【不过期】
                             ❌ 未 COMMIT（还在事务里，可回滚）

session.commit()          → 【提交】= flush() + COMMIT
                             ✅ 永久生效
                             ⚠️ 把 session 里【所有对象标记为过期】
```

---

## 四、🔴 N+1 查询问题（面试高频）

### 现象

```python
session.add_all(objs)
session.commit()
for u in objs:
    print(u.id, u.name)       # ← 这里偷偷发了 3 条 SELECT
```

`echo=True` 的日志：
```
INSERT ... ×3
COMMIT
SELECT ... WHERE users.id = 1     ← 不是 INSERT 的一部分！
SELECT ... WHERE users.id = 2
SELECT ... WHERE users.id = 3
```

### 原因：`expire_on_commit` 默认 `True`

**`commit()` 之后所有对象被标记为过期**（因为数据库可能有触发器/默认值改了它们）。
**之后每访问一个属性 → SQLAlchemy 重新查一次数据库。**

```
3 个对象   → 3 次查询
1000 个对象 → 1000 次查询        ← 这就是 N+1
```

### 四种写法实测对比

| 写法 | id 对不对 | N+1 查询 |
|---|---|---|
| 打印在 `commit` 前 | ❌ 是 `None` | ✅ 0 条 |
| 打印在 `commit` 后（默认） | ✅ 正确 | 🔴 有（碰几个对象就几条） |
| **中间加 `session.flush()`** | ✅ 正确 | ✅ **0 条** |
| **`Session(engine, expire_on_commit=False)`** | ✅ 正确 | ✅ **0 条** |

### 两个解法

```python
# 解法 A（推荐）：flush 后打印，最后再 commit
session.add_all(objs)
session.flush()                    # 发 SQL 拿 id，但不提交、不过期
for u in objs:
    print(u.id, ...)               # id 已回填
session.commit()

# 解法 B：不让对象过期
with Session(engine, expire_on_commit=False) as session:
    ...
    session.commit()
    for u in objs:
        print(u.id, ...)
```

> **为什么推荐 A**：`flush()` 之后**还能改主意** —— 可以先检查、再改，最后才 `commit()`。
> 「先发出去看看，再决定提不提交」是很常用的模式。
>
> 相关考点还有 **`joinedload` 预加载**（解决关联对象的 N+1），项目里会用到。

---

## 五、本表踩过的坑（血泪）

| 坑 | 正确 |
|---|---|
| `id = Mapped[int].mapped_column(...)` | `id: Mapped[int] = mapped_column(...)`（**冒号 + 独立函数**） |
| `u1 = ('张三','22','a.com')` | `u1 = User(name=..., age=22, ...)`；**age 是 int 不是 '22'** |
| `session.delect(u)` | `session.delete(u)`（拼写 + 主语） |
| 缺 `session.commit()` | 不 commit，数据根本没进数据库 |
| `DELETE FROM` 清表后 id 从 3 开始 | **`TRUNCATE TABLE` 才重置自增计数器** |
| 硬编码 `session.get(User, 1)` | **用刚插入对象的 `.id`**（我踩过这个） |
| `age = 20 + id` | **`id` 是 Python 内置函数**！用 `enumerate(names, start=1)` 拿序号 |
| 函数里 `with` 后面没缩进 | `IndentationError` |

> 💡 **读报错技巧**：Python 3.12 的 `AttributeError` 自带拼写建议 ——
> `'Session' object has no attribute 'delect'. Did you mean: 'delete'?`
