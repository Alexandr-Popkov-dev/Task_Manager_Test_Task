from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class TaskStatus(Enum):
    PENDING = 'Создано'
    IN_PROGRESS = 'В работе'
    DONE = 'Выполнено'


task_status_enum = PgEnum(
    TaskStatus,
    name="task_status",
    create_type=True,
    values_callable=lambda obj: [e.value for e in obj]
)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    status = Column(
        task_status_enum,
        default=TaskStatus.PENDING.value,
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)
