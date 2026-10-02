from sqlalchemy import String, create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

URL = "mysql+pymysql://dev:dev123456@localhost/practice_db?charset=utf8mb4"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    age: Mapped[int]
    email: Mapped[str] = mapped_column(String(50), unique=True)


engine = create_engine(URL)

with Session(engine) as session:
    u1 = User(name = '张三',age = 22,email = 'a.com')
    session.add(u1)
    session.commit()

with Session(engine) as session:
    u = session.get(User,11)
    stmt = select(User).where(User.age >= 22)
    for u in session.scalars(stmt):
        print(u.name)

with Session(engine) as session:
    u = session.get(User,1)
    u.age = 25
    session.commit()

with Session(engine) as session:
    u = session.get(User,1)
    session.delete(u)
    session.commit()