from sqlalchemy.orm import Session
from ..database.models import User
from ..core.security import get_password_hash, verify_password
from ..schemas import UserCreate
from ..core.security import create_refresh_token, REFRESH_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone
from fastapi_mail import FastMail, MessageSchema
from ..mail.mail_conf import conf
from ..core import security
from fastapi import BackgroundTasks


def create_user(db: Session, user: UserCreate, background_tasks: BackgroundTasks):
    db_user = User(email=user.email, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    background_tasks.add_task(send_verification_email, user.email, db)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False

    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(data={"sub": user.email}, expires_delta=refresh_token_expires)

    user.refresh_token = refresh_token
    user.token_expires = datetime.now(timezone.utc) + refresh_token_expires
    db.commit()
    return user


async def send_verification_email(email: str, db: Session):
    token_data = {"sub": email}
    token = security.create_access_token(data=token_data, expires_delta=timedelta(hours=24))
    verification_url = f"http://yourfrontend.com/verify?token={token}"

    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=f"Please click on the link to verify your email: {verification_url}",
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
