from sqlalchemy import String,ForeignKey,create_engine,select,text
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session,relationship
from sqlalchemy import event
from sqlalchemy.orm import selectinload
URL = "mysql+pymysql://dev:dev123456@localhost/practice_db?charset=utf8mb4"

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(20))
    age:Mapped[int]
    email:Mapped[str] = mapped_column(String(50),unique = True)

    posts:Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id:Mapped[int] = mapped_column(primary_key= True)
    title:Mapped[str] = mapped_column(String(100))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")

if __name__ == "__main__":
    engine = create_engine(URL,echo=True)

    counter = {"select": 0}

    @event.listens_for(engine, "before_cursor_execute")
    def _count(conn,cursor,statement,params,context,executemany):
        if statement.strip().upper().startswith("SELECT"):
            counter["select"] += 1

    Base.metadata.create_all(engine)
    print("建表完成")

    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.execute(text("TRUNCATE TABLE posts"))
        conn.execute(text("TRUNCATE TABLE users"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    with Session(engine) as session:
        for i in range(1,6):
            u = User(name=f"用户{i}",age=20 + i,email=f"u{i}@test.com")
            u.posts.append(Post(title=f"文章{i}-A"))
            u.posts.append(Post(title=f"文章{i}-B"))
            session.add(u)
        session.commit()
    print("\n造了 5 个用户，每人 2 篇文章")

    counter["select"] = 0
    with Session(engine) as session:
        for u in session.scalars(select(User)):
            titles = [p.title for p in u.posts]
    print("\n【朴素遍历】SELECT 数量 =",counter["select"])

    counter["select"] = 0
    with Session(engine) as session:
        stmt = select(User).options(selectinload(User.posts))
        for u in session.scalars(stmt):
            titles = [p.title for p in u.posts]
    print("【selectinload】SELECT 数量 = ",counter["select"])

    with Session(engine) as session:
        u = User(name="张三",age=22,email="zs@test.com")
        u.posts.append(Post(title="第一篇"))
        u.posts.append(Post(title="第二篇"))
        session.add(u)
        session.commit()
        print("插入完成 -> user.id=",u.id,"| posts 数量 = ",len(u.posts))

    with Session(engine) as session:
        user = session.get(User,1)
        print("用户 -> 文章：")
        for p in user.posts:
            print("   ",p.title)

        post = session.get(Post,1)
        print(("文章 -> 用户:",post.author.name))