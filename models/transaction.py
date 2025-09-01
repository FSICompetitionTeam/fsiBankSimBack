from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from db.base import Base
from datetime import datetime


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    from_account = Column(String)
    to_account = Column(String)
    amount = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    from_bank_name = Column(String)
    to_bank_name = Column(String)
