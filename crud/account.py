from sqlalchemy.orm import Session
from models.account import Account
from schemas.account import AccountCreate
import random


def create_account(db: Session, account: AccountCreate, user_id: int):
    account_number = ''.join(str(random.randint(0, 9)) for _ in range(14))  # 랜덤 14자리 숫자 생성
    db_account = Account(user_id=user_id, account_number=account_number, balance=0, bank_name=account.bank_name)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def get_accounts_by_user(db: Session, user_id: int):
    return db.query(Account).filter(Account.user_id == user_id).all()


def get_account_by_number(db: Session, account_number: str):
    return db.query(Account).filter(Account.account_number == account_number).first()