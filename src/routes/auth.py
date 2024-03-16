
from ..schemas import UserCreate, Token
from ..repository.users import create_user, authenticate_user
from ..core.security import create_access_token
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from ..database.db import SessionLocal
from jose import jwt, JWTError
from main import limiter
from dotenv import load_dotenv
import os


load_dotenv()


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=Token)
@limiter.limit("5/minute")
def register_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Реєструє нового користувача та відправляє лист з підтвердженням електронної пошти.
    """

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = create_user(db=db, user=user, background_tasks=background_tasks)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: UserCreate, db: Session = Depends(get_db)):
    """
    Входить користувача в систему, перевіряючи його електронну пошту та пароль.
    """
    user = authenticate_user(db, email=form_data.email, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Перевіряє електронну пошту користувача, використовуючи наданий токен.
    """
    try:
        payload = jwt.decode(token, os.getenv('token_secret_key'), algorithms=os.getenv('token_algorithm'))
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid verification link")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_active = True
        db.add(user)
        db.commit()
        return {"message": "Email successfully verified."}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token or token expired")
