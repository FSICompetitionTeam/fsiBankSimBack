from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_number = Column(String, unique=True, index=True)
    balance = Column(Integer, default=0)
    bank_name = Column(String)
