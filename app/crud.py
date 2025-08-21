from sqlalchemy.orm import Session
from app import models
from typing import Optional
import uuid


def create_task(db: Session, task: dict):
    if 'status' in task and isinstance(task['status'], str):
        task['status'] = models.TaskStatus(task['status']).value

    db_task = models.Task(**task)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, status: Optional[str] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Task)

    if status:
        status_enum = models.TaskStatus(status)
        query = query.filter(models.Task.status == status_enum.value)

    return query.offset(skip).limit(limit).all()


def get_task(db: Session, task_id: uuid.UUID):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db: Session, db_task: models.Task, update_data: dict):
    for key, value in update_data.items():
        if key == 'status' and isinstance(value, str):
            value = models.TaskStatus(value).value
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: uuid.UUID):
    task = get_task(db, task_id)
    if task:
        db.delete(task)
        db.commit()
        return True
    return False
