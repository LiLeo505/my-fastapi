from app.database import SessionLocal
from app.models import User

db = SessionLocal()

try:
    user = db.query(User).filter(
        User.username == "leo"
    ).first()


    if user is None:
        print("用户不存在")
    else:
        user.role = "admin"
        db.commit()
        print("管理员设置成功")

finally:
    db.close()