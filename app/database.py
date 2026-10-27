
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# SQLite 数据库文件，首次运行时会自动创建
DATABASE_URL = "sqlite:///./servers.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# 数据库会话工厂
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# 所有数据库模型都继承 Base
class Base(DeclarativeBase):
    pass


# 为每个请求提供数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
