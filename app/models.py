from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class SinpeTransaction(Base):
    __tablename__ = "sinpe_transactions"

    id = Column(Integer, primary_key=True, index=True)
    reference_number = Column(String, unique=True, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="CRC")  # CRC, USD, etc.
    bank_origin = Column(String, nullable=True)  # BAC, BN, BCR, etc.
    transaction_date = Column(DateTime, nullable=True)  # Fecha del comprobante
    image_hash = Column(String, unique=True, index=True, nullable=True)  # Hash de la imagen recibida
    processed_at = Column(DateTime, default=datetime.utcnow)  # Fecha de procesamiento en sistema