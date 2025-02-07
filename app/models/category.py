from sqlalchemy import Column, String, DateTime, ForeignKey, UUID, func
from sqlalchemy.orm import relationship

from main import Base
import datetime
# from uuid import UUID

class Category(Base):
    __tablename__ = "category"

    category_id = Column(UUID, primary_key=True, index=True)
    name = Column(String, nullable = False)
    description = Column(String)
    type = Column(String)
    owner = Column(UUID, ForeignKey("user.user_id"), nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default = func.now())


    def __init__(self, category_id, name, description, type, owner):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.type = type
        self.owner = owner
    

    def repr_name(self):
        return {
            "category_id": str(self.category_id),
            "name": self.name,
            "description": self.description,
            "owner": str(self.owner),
            "created_at": self.created_at,
            "type": self.type
        }
