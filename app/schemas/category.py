from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class CategoryCreate(BaseModel):
    name: str = Field(example = "Fitness")
    description: str = Field(example = "Good Health. Good Goals")


class Category(BaseModel):
    category_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(example = "Fitness")
    description: str = Field(example = "Good Health. Good Goals")
    type: str = Field(example = "default")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CategoryUpdate(BaseModel):
    category_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(example = "Fitness")
    description: str = Field(example = "Good Health. Good Goals")
    type: str = Field(example = "default")

