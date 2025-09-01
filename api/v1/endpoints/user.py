from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate, UserOut
from crud.user import create_user
from db.session import get_db
from core.security import get_current_user

router = APIRouter()


@router.post("/", response_model=UserOut)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
