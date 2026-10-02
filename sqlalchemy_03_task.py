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

def add_and_list(engine,names):
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE users"))
    with Session(engine) as session:
        objs= []
        for i in names:
            u = User(name= i,age =20,email=i+ "@test.com")
            objs.append(u)
        session.add_all(objs)
        session.flush()
        for u in objs:
            print(u.id,u.name,u.age,u.email)
        session.commit()
add_and_list(engine,["张三","李四","王五"])
