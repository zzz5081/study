from sqlalchemy import String,ForeignKey,create_engine
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session,relationship

URL = "mysql+pymysql://dev:dev123456@localhost/practice_db?charset=utf8mb4"
engine = create_engine(URL)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id :Mapped[int] = mapped_column(primary_key = True)
    name :Mapped[str] = mapped_column(String(20))
    age :Mapped[int]
    email :Mapped[str] = mapped_column(String(50),unique = True)

    posts :Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id :Mapped[int] = mapped_column(primary_key = True)
    title :Mapped[str] = mapped_column(String(20))
    user_id :Mapped[int] = mapped_column(ForeignKey("users.id"))

    author :Mapped["User"] = relationship(back_populates="posts")


with Session(engine) as session:
    u = User(name = '张三',age=22,email = "zs@test.com")
    u.posts.append(Post(title="第一篇"))
    u.posts.append(Post(title="第二篇"))
    session.add(u)
    session.commit()

with Session(engine) as session:
    user = session.get(User,1)
    print([p.title for p in user.posts])