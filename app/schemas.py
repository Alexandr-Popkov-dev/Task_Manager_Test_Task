from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid


class TaskStatus(str, Enum):
    PENDING = 'Создано'
    IN_PROGRESS = 'В работе'
    DONE = 'Выполнено'


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.PENDING


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
