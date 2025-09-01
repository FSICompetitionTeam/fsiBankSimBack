from sqlalchemy.orm import Session
from models.transaction import Transaction
from crud.account import get_account_by_number
from schemas.transaction import TransactionCreate


def create_transaction(db: Session, transaction: TransactionCreate):
    from_account = get_account_by_number(db, transaction.from_account)
    to_account = get_account_by_number(db, transaction.to_account)
    if not from_account or not to_account:
        raise ValueError("Account not found")
    if from_account.balance < transaction.amount:
        raise ValueError("Insufficient balance")

    from_account.balance -= transaction.amount
    to_account.balance += transaction.amount

    db_transaction = Transaction(
        from_account=transaction.from_account,
        to_account=transaction.to_account,
        amount=transaction.amount,
        from_bank_name=from_account.bank_name,
        to_bank_name=to_account.bank_name
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions_by_account(db: Session, account_number: str, limit: int = 10):
    return db.query(Transaction).filter(
        (Transaction.from_account == account_number) | (Transaction.to_account == account_number)
    ).order_by(Transaction.timestamp.desc()).limit(limit).all()
