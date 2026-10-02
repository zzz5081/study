from sqlalchemy import String,create_engine,select,text #复制的
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session #复制的

URL = "mysql+pymysql://dev:dev123456@localhost/practice_db?charset=utf8mb4" #复制的

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "User"
    id:Mapped[int] = mapped_column(primary_key = True)
    name:Mapped[str]=mapped_column(String(20))
    age:Mapped[int]
    email:Mapped[str]=mapped_column(String(50),unique=True)

if __name__ =="__main__":
    engine = create_engine(URL,echo=True)
    with Session.begin():
        Session.execute(text(""))

    with Session()