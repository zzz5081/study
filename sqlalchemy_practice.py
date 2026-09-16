"""SQLAlchemy 练习册（干净版）

═══════════════════════════════════════════════════════════
怎么用
═══════════════════════════════════════════════════════════
1. 先在终端设置数据库密码（这样密码不会写进代码，也不会被传到 GitHub）：
       $env:MYSQL_PWD="你的MySQL密码"

2. 然后运行：
       python sqlalchemy_practice.py

3. 按顺序完成 TODO-A ~ TODO-F，每完成一个函数就跑一次看结果

═══════════════════════════════════════════════════════════
学习目标
═══════════════════════════════════════════════════════════
- 模型定义：类 = 表，属性 = 列
- CRUD：增删查改
- 外键与关联查询（用户 ↔ 文章）
- 事务：commit / rollback

提示：把 echo=False 改成 echo=True，就能看到 ORM 翻译出的真实 SQL
"""
import os

from sqlalchemy import create_engine, String, Integer, select, ForeignKey, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# ============================================================
# ① 连接配置（密码从环境变量读，不写死在代码里）
# ============================================================
DB_USER = "root"
DB_PASSWORD = os.environ.get("MYSQL_PWD")          # ← 从环境变量读
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "practice_db"

if not DB_PASSWORD:
    raise SystemExit(
        "\n❌ 没读到数据库密码。\n"
        "   请先在终端执行：  $env:MYSQL_PWD=\"你的MySQL密码\"\n"
        "   然后再运行本脚本。\n"
        "   （这样密码不进代码、不进 Git，是项目里的标准做法）\n"
    )

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
engine = create_engine(DB_URL, echo=True)         # 想看 SQL 就把这里改成 True


# ============================================================
# ② 模型定义（类 = 表，属性 = 列）
# ============================================================
class Base(DeclarativeBase):
    pass


class User(Base):
    """用户表 —— 已写好，作为参考"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    age: Mapped[int] = mapped_column(Integer)


class Article(Base):
    """文章表 —— 已写好，注意最后那行外键"""
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(String(500))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))   # ← 外键：指向 users.id


# ============================================================
# ③ 工具函数（已写好，直接用）
# ============================================================
def create_tables():
    """建表（已存在的表会自动跳过）"""
    Base.metadata.create_all(engine)
    print("✅ 建表完成：users / articles —— 去 DBeaver Refresh 看看")


def reset_data():
    """清空数据（重复练习时用；注意先删文章，因为有外键依赖）"""
    with Session(engine) as session:
        session.execute(delete(Article))
        session.execute(delete(User))
        session.commit()
    print("🧹 数据已清空")


def show_counts():
    """看两张表各有几条数据"""
    with Session(engine) as session:
        user_count = len(session.scalars(select(User)).all())
        article_count = len(session.scalars(select(Article)).all())
    print(f"📊 当前数据：users = {user_count} 条，articles = {article_count} 条")


# ============================================================
# ④ 增（Create）—— TODO-A
# ============================================================
def add_data():
    """插入 2 个用户 + 2 篇文章"""
    with Session(engine) as session:
        # TODO-A：写你的代码
        #
        # 步骤提示：
        #   1) 创建两个用户对象：user1 = User(username="小明", age=20)  user2 = User(username="小红", age=21)
        #   2) session.add_all([user1, user2])
        #   3) session.flush()      # 刷新后对象就拿到自增 id（还没提交，但 id 已经有了）
        #   4) 用 user1.id 作为 author_id 创建两篇文章：
        #        Article(title="我的第一篇博客", content="今天学了 SQLAlchemy", author_id=user1.id)
        #   5) session.add_all([文章1, 文章2])
        #   6) session.commit()     # ⚠️ 不提交不生效！
        user1 = User(username = "小明",age = 20)
        user2 = User(username = "小红",age = 21)
        session.add([user1,user2])
        session.flush()
        article1 = Article(title = "我的第一篇博客",content = "我今天学习了 SQLAlchemy",author_id = user1.id)
        article2 = Article(title = "我的第二篇博客",content = "SQLAlchemy很有趣",author_id = user1.id)
        session.add([article1,article2])
        session.commit()
    show_counts()


# ============================================================
# ⑤ 查（Read）—— TODO-B / TODO-C
# ============================================================
def query_data():
    with Session(engine) as session:
        # TODO-B：查出所有用户，打印 id / username / age
        #   提示：users = session.scalars(select(User)).all()
        users = session.scalars(select(User)).all()
        print(users)

    with Session(engine) as session:
        # TODO-C：查出 username == "小明" 的用户，打印他的年龄
        #   提示：u = session.scalars(select(User).where(User.username == "小明")).first()
        u = session.scalars(select(User).where(User.username == "小明")).first()
        print(u)

def query_with_join():
    """⭐ 挑战：查每篇文章 + 它的作者名（外键关联查询）"""
    with Session(engine) as session:
        # TODO-D：用 join 一次查出「文章标题 + 作者用户名」
        #   提示：
        #     rows = session.execute(
        #         select(Article.title, User.username)
        #         .join(User, Article.author_id == User.id)
        #     ).all()
        #     for title, username in rows:
        #         print(f"{title} —— 作者：{username}")
        pass


# ============================================================
# ⑥ 改（Update）—— TODO-E
# ============================================================
def update_data():
    with Session(engine) as session:
        # TODO-E：把小明的年龄改成 21，然后 commit
        #   提示：先查出来 → 改属性 → commit
        pass


# ============================================================
# ⑦ 删（Delete）—— TODO-F
# ============================================================
def delete_data():
    with Session(engine) as session:
        # TODO-F：删掉一篇文章（先查出来 → session.delete(对象) → commit）
        pass
    show_counts()


# ============================================================
# ⑧ 事务体验（已写好，直接跑，观察输出）
# ============================================================
def transaction_demo():
    """体验事务：改了不提交 → 数据没变；rollback → 彻底撤销"""
    with Session(engine) as session:
        u = session.scalars(select(User)).first()
        if not u:
            print("⚠️ 没有用户数据，先完成 TODO-A")
            return
        original = u.age
        print(f"【事务演示】{u.username} 原始年龄 = {original}")
        u.age = 99
        session.flush()                                   # 发给数据库（事务内）
        print(f"  改成 99 并 flush 后 = {session.get(User, u.id).age}")   # 能看到 99
        session.rollback()                                # 撤销！
        print(f"  rollback 之后 = {session.get(User, u.id).age}")        # 回到原值 ✅
        print("  → 这就是事务：**没提交就不算数**")


# ============================================================
# 主流程
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    create_tables()
    print("=" * 55)

    # 第一次练习时，如果想从干净状态开始，把下面这行的注释去掉
    # reset_data()

    add_data()
    print("=" * 55)
    query_data()
    print("=" * 55)
    query_with_join()
    print("=" * 55)
    update_data()
    print("=" * 55)
    delete_data()
    print("=" * 55)
    transaction_demo()


# ═══════════════════════════════════════════════════════════
# 参考答案（卡住 20 分钟以上再看！）
# ═══════════════════════════════════════════════════════════
#
# TODO-A  add_data：
#     user1 = User(username="小明", age=20)
#     user2 = User(username="小红", age=21)
#     session.add_all([user1, user2])
#     session.flush()
#     session.add_all([
#         Article(title="我的第一篇博客", content="今天学了 SQLAlchemy", author_id=user1.id),
#         Article(title="外键是什么", content="一张表指向另一张表", author_id=user1.id),
#     ])
#     session.commit()
#
# TODO-B  所有用户：
#     for u in session.scalars(select(User)).all():
#         print(u.id, u.username, u.age)
#
# TODO-C  条件查询：
#     u = session.scalars(select(User).where(User.username == "小明")).first()
#     print("小明的年龄:", u.age)
#
# TODO-D  join 查询：
#     rows = session.execute(
#         select(Article.title, User.username).join(User, Article.author_id == User.id)
#     ).all()
#     for title, username in rows:
#         print(f"{title} —— 作者：{username}")
#
# TODO-E  更新：
#     u = session.scalars(select(User).where(User.username == "小明")).first()
#     u.age = 21
#     session.commit()
#
# TODO-F  删除：
#     a = session.scalars(select(Article)).first()
#     session.delete(a)
#     session.commit()
