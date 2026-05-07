from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Form
)

from sqlalchemy.orm import Session

from database import SessionLocal
from models.user import User

from schemas.user import UserCreate

from utils.hashing import (
    hash_password,
    verify_password
)

from utils.jwt import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# Database Connection
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# Register API
@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }


# Login API
@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.username == username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid username"
        )

    if not verify_password(
        password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.username,
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }