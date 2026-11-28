import jwt


from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session


from app.database import get_db
from app.models import User
from app.security import decode_access_token,oauth2_scheme
from app.database import SessionLocal

def comon_parameters(
        skip: int = 0,
        limit: int = 100
):
    return {"skip": skip, "limit": limit}

def get_db():
    print("1.获取数据库连接")
    try:
        db = SessionLocal()
        yield db

    finally:
        print("3.关闭数据库连接")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if not isinstance(user_id, str) or not user_id.isdigit():
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
                headers={"WWW-Authentication": "Bearer"}
            )
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user



def get_admin_user(
        current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )
    return current_user