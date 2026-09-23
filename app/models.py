from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class SinpeTransaction(Base):
    __tablename__ = "sinpe_transactions"

    id = Column(Integer, primary_order=True, primary_key=True, index=True)
    reference_number = Column(String, unique=True, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)