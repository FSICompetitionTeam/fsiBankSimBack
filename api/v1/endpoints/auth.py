from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import Token, UserBase
from crud.user import get_user_by_phone
from core.security import create_access_token, get_current_user
from db.session import get_db

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(user: UserBase, db: Session = Depends(get_db)):
    db_user = get_user_by_phone(db, phone_number=user.phone_number)
    if not db_user or db_user.name != user.name:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.phone_number}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Logged out"}
