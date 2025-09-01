from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
  amount: int

class TransactionCreate(TransactionBase):
  from_account: str | None = None
  to_account: str | None = None

class DepositCreate(TransactionBase):
  account_number: str

class WithdrawCreate(TransactionBase):
  account_number: str

class TransferCreate(TransactionBase):
  from_account: str
  to_account: str

class TransactionOut(TransactionBase):
  id: int
  from_account: str | None = None
  to_account: str | None = None
  timestamp: datetime
  from_bank_name: str | None = None
  to_bank_name: str | None = None

  class Config:
    from_attributes = True