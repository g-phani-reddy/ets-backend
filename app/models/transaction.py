from main import Base
import datetime

from sqlalchemy import Column, DECIMAL, DateTime, String, Boolean, ForeignKey, UUID, func
from sqlalchemy.orm import relationship

class Transaction(Base):

    __tablename__ = "transaction"

    transaction_id = Column(UUID, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("user.user_id"), nullable=False)
    amount = Column(DECIMAL(10, 2))
    category_id = Column(UUID, ForeignKey("category.category_id"), nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default = func.now())
    last_updated_at = Column(
        DateTime,
        nullable=False,
        server_default = func.now())
    comment = Column(String)
    is_deleted = Column(Boolean)

    def __init__(self, transaction_id, user_id, amount, category_id, comment):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.amount = amount
        self.category_id = category_id
        self.comment = comment

    def __repr__(self):
        return f"<Transaction(transaction_id={self.transaction_id}, user_id={self.user_id}, amount={self.amount}, category_id={self.category_id})>"

    def _repr_dict(self):
        return {
            "transaction_id": str(self.transaction_id),
            "user_id": str(self.user_id),
            "amount": float(self.amount),
            "category_id": str(self.category_id),
            "created_at": self.created_at.isoformat(),
            "last_updated_at": self.last_updated_at.isoformat(),
            "comment": self.comment,
            "is_deleted": self.is_deleted,
        }
