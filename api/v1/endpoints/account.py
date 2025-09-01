from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.account import AccountCreate, AccountOut
from crud.account import create_account, get_accounts_by_user, get_account_by_number
from db.session import get_db
from core.security import get_current_user
from models.user import User

router = APIRouter()


@router.post("/", response_model=AccountOut)
async def create_new_account(account: AccountCreate, db: Session = Depends(get_db),
                             current_user: User = Depends(get_current_user)):
    return create_account(db, account, current_user.id)


@router.get("/", response_model=list[AccountOut])
async def get_accounts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_accounts_by_user(db, current_user.id)


@router.get("/{account_number}", response_model=AccountOut)
async def get_account(account_number: str, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    account = get_account_by_number(db, account_number)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
