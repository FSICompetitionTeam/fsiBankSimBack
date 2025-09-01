from pydantic import BaseModel


class AccountBase(BaseModel):
    bank_name: str


class AccountCreate(AccountBase):
    pass


class AccountOut(AccountBase):
    account_number: str
    balance: int

    class Config:
        orm_mode = True
