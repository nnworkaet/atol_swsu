from sqlalchemy import Column, String, Text
from utils.database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    uuid = Column(String, primary_key=True, index=True)
    receipt_callback = Column(Text, nullable=True)
    created_at = Column(String, nullable=False)
