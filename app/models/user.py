from sqlalchemy import Column, String, DateTime, Boolean, UUID, func
from sqlalchemy.orm import relationship
from main import Base
import datetime

class User(Base):
    __tablename__ = "user"

    user_id = Column(UUID, primary_key=True, index=True)
    first_name = Column(String, nullable = False)
    last_name = Column(String)
    username = Column(String, nullable = False)
    password = Column(String, nullable = False)
    is_disabled = Column(Boolean)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default = func.now())
    contact_num = Column(String)

    # categories = relationship("Category", back_populates="owner")
    # transactions = relationship("Transaction", back_populates="user_id")

    def __init__(self, user_id, first_name: str, last_name: str, username: str, password: str, contact_num: str = None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.contact_num = contact_num
        self.is_disabled = False


    def _repr_dict(self):
        return {
            'user_id': str(self.user_id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'is_disabled': self.is_disabled,
            'created_at': self.created_at.isoformat(),
            'contact_num': self.contact_num,
            'password': self.password
        }
