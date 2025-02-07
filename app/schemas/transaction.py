from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: float = Field(example = 125.78)
    comment: str = Field(example = "Good Health. Good Goals")
    category_id: uuid.UUID = Field(default_factory=uuid.uuid4)

class Transaction(BaseModel):
    transaction_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    amount: float = Field(example = 125.78)
    comment: str = Field(example = "Good Health. Good Goals")
    category_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TransactionUpdate(BaseModel):
    transaction_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    amount: float = Field(example = 125.78)
    comment: str = Field(example = "Good Health. Good Goals")
    category_id: uuid.UUID = Field(default_factory=uuid.uuid4)
