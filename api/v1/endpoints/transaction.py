from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.account import get_account_by_number, get_accounts_by_user
from models.transaction import Transaction
from schemas.transaction import DepositCreate, WithdrawCreate, TransferCreate, TransactionOut
from crud.transaction import create_transaction, get_transactions_by_account
from db.session import get_db
from core.security import get_current_user
from models.user import User

router = APIRouter()


@router.post("/deposit", response_model=TransactionOut)
async def deposit(transaction: DepositCreate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    if transaction.account_number not in [acc.account_number for acc in get_accounts_by_user(db, current_user.id)]:
        raise HTTPException(status_code=403, detail="Not your account")
    acc = get_account_by_number(db, transaction.account_number)
    acc.balance += transaction.amount
    db_transaction = Transaction(
        from_account=None,
        to_account=transaction.account_number,
        amount=transaction.amount,
        from_bank_name=None,
        to_bank_name=acc.bank_name
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.post("/withdraw", response_model=TransactionOut)
async def withdraw(transaction: WithdrawCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    if transaction.account_number not in [acc.account_number for acc in get_accounts_by_user(db, current_user.id)]:
        raise HTTPException(status_code=403, detail="Not your account")
    acc = get_account_by_number(db, transaction.account_number)
    if acc.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    acc.balance -= transaction.amount
    db_transaction = Transaction(
        from_account=transaction.account_number,
        to_account=None,
        amount=-transaction.amount,
        from_bank_name=acc.bank_name,
        to_bank_name=None
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.post("/transfer", response_model=TransactionOut)
async def transfer(transaction: TransferCreate, db: Session = Depends(get_db),
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
    db_transaction = Transaction(
        from_account=transaction.from_account,
        to_account=transaction.to_account,
        amount=transaction.amount,
        from_bank_name=from_acc.bank_name,
        to_bank_name=to_acc.bank_name
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.get("/", response_model=list[TransactionOut])
async def get_transactions(account_number: str, limit: int = 10, db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    return get_transactions_by_account(db, account_number, limit)
