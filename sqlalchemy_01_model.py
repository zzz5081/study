from sqlalchemy import String,create_engine
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session

URL = "mysql+pymysql://dev:dev123456@localhost/practice_db?charset=utf8mb4"

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__="users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    age: Mapped[int]
    email: Mapped[str] = mapped_column(String(50),unique=True)

if __name__ == "__main__":
    engine = create_engine(URL,echo=True)
    Base.metadata.create_all(engine)
    print("建表完成")