from sqlalchemy import create_engine,String,ForeignKey,Boolean
from sqlalchemy.orm import mapped_column,DeclarativeBase,Mapped,relationship,Session,sessionmaker
from sqlalchemy import select

URL = "mysql+pymysql://dev:dev123456@localhost/practice_db?charset=utf8mb4"

engine = create_engine(URL,echo=False)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "todo_users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50),unique=True,index=True) 
    pwd_hash: Mapped[str] = mapped_column(String(255))
    todos :Mapped[list["Todo"]] = relationship(back_populates= "owner")

class Todo(Base):
    __tablename__ = "todos"
    id :Mapped[int] = mapped_column(primary_key=True)
    title :Mapped[str] = mapped_column(String(200))
    done :Mapped[bool] = mapped_column(Boolean,default=False)
    owner_id :Mapped[int] = mapped_column(ForeignKey("todo_users.id"))
    owner :Mapped["User"] = relationship(back_populates="todos") 

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_name(session: Session,username: str) -> User | None:
    return session.scalars(select(User).where(User.username == username)).first()

def add_user(session: Session,username: str,pwd_hash: str) -> User:
    u = User(username = username,pwd_hash = pwd_hash)
    session.add(u)
    session.commit()
    session.refresh(u)
    return u 