from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import User
from app.schemas import UserRegister,UserResponse,UserLogin
from app.security import get_password_hash,verify_password,create_access_token

router = APIRouter(
    prefix="/auth",
    tags=['身份认证']
)

@router.post("/register", response_model=UserResponse, status_code=201)
def registergist(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    hashed_password = get_password_hash(user_data.password)

    user = User(
        username = user_data.username,
        age=user_data.age,
        hash_password=hashed_password
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )
    return user

@router.post("/login")
def login(
    user_data:UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == user_data.username
    ).first()
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    if not verify_password(
        user_data.password,
        user.hash_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }