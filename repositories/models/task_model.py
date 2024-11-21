from datetime import datetime, timezone
from typing import Dict

from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum, func

from repositories.models import EntityMeta
from schemas.enums import TaskStatus


class Task(EntityMeta):
    __tablename__: str = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    status = Column(SqlEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=func.now())

    def normalize(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": TaskStatus.from_value(self.status).value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


