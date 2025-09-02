from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.account import get_account_by_number
from models.user import User
from schemas.transaction import TransactionCreate, TransactionOut
from crud.transaction import create_transaction, get_transactions_by_account
from db.session import get_db
from core.security import get_current_user

router = APIRouter()


@router.post("/transfer", response_model=TransactionOut)
async def transfer(transaction: TransactionCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    from_acc = get_account_by_number(db, transaction.from_account)
    if from_acc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your account")
    to_acc = get_account_by_number(db, transaction.to_account)
    if not to_acc:
        raise HTTPException(status_code=404, detail="To account not found")
    if from_acc.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    from_acc.balance -= transaction.amount
    to_acc.balance += transaction.amount
    db_transaction = create_transaction(db, transaction)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.get("/", response_model=list[TransactionOut])
async def get_transactions(account_number: str, limit: int = 10, db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    return get_transactions_by_account(db, account_number, limit)
