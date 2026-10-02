from sqlalchemy import String,create_engine,select,text
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session

URL = "mysql+pymysql://dev:dev123456@localhost/practice_db?charset=utf8mb4"

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(20))
    age:Mapped[int]
    email:Mapped[str] = mapped_column(String(50),unique=True)

if __name__ == '__main__':
    engine = create_engine(URL,echo=True)
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE users"))

    with Session(engine) as session:
        u1 = User(name="张三",age=22,email="zhangsan@test.com")
        u2 = User(name="李四",age=25,email="lisi@test.com")
        session.add_all([u1,u2])
        session.commit()
        print("C 插入完成 ->u1.id = ",u1.id,"| u2.id =",u2.id)

    with Session(engine) as session:
        user = session.get(User,1)
        print("按主键:",user.name if user else "没有")

        stmt = select(User).where(User.age >= 22).order_by(User.age.desc())
        for u in session.scalars(stmt):
            print("按条件查:",u.id,u.name,u.age,u.email)

    with Session(engine) as session:
        user = session.get(User,1)
        user.age = 23
        session.commit()
        print("U 改完 -> 张三的 age = ",user.age)

    with Session(engine) as session:
        user = session.get(User,2)
        session.delete(user)
        session.commit()
        print("D 删除完成(李四)")