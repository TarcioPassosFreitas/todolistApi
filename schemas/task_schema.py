from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from schemas.enums import TaskStatus
from pydantic import ConfigDict


class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, description="The title of the task. Must not be empty.")
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.PENDING
    created_at: Optional[datetime] = None


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskSchema(TaskCreateSchema):
    id: int
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
