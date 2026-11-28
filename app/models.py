from sqlalchemy import Integer, Column, String, ForeignKey
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    age = Column(Integer)

    hash_password = Column(String(255), nullable=False)

    role = Column(String(20), default="user", nullable=False)  

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255), nullable=False)

    content_type = Column(String(100), nullable=False)

    size = Column(Integer, nullable=False)

    original_filename = Column(String(255), nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )