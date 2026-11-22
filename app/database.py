from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 创建数据库连接
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"#告诉你数据库在哪里，这个./test.db是相对路径，表示在当前目录下创建一个test.db文件，然后去这里面读写数据，其实就是相当于一个本地的数据库


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# 创建会话类
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)#工厂，先建工厂，才有产品Session

# 创建基类
Base = declarative_base()#所有的父类

# 创建会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


 