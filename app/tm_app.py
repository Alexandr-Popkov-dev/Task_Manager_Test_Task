from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models
from app.crud import create_task, get_tasks, get_task, update_task, delete_task
from app.database import engine, SessionLocal
from app.schemas import TaskCreate, TaskUpdate, Task as TaskSchema
from typing import List, Optional
import uuid

models.Base.metadata.create_all(bind=engine)

application = FastAPI(title="Task Manager API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#
@application.post("/tasks/", response_model=TaskSchema,
                  summary="Добавление Задачи",
                  description="При отправке запроса в"
                              "базу данных добавляется новая задача")
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task.model_dump())


@application.get("/tasks/", response_model=List[TaskSchema],
                 summary="Получение продуктов",
                 description="При запросе выводятся все "
                             "задачи, с выбранным статусом содержащиеся в базе данных")
def read_tasks(
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return get_tasks(db, status=status, skip=skip, limit=limit)


@application.get("/tasks/{task_id}", response_model=TaskSchema,
                 summary="Получение задачи по его uuid",
                 description="При отправке запросе выводится запрашиваемая задача")
def read_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@application.put("/tasks/{task_id}", response_model=TaskSchema,
                 summary="Изменение информации о задаче",
                 description="При отправке запросе в "
                             "базе данных изменяется информация о задаче")
def update_existing_task(
        task_id: uuid.UUID,
        task: TaskUpdate,
        db: Session = Depends(get_db)
):
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task(db, db_task, task.model_dump(exclude_unset=True))  # Используем model_dump()


@application.delete("/tasks/{task_id}",
                    summary="Удаление задачи по uuid",
                    description="При отправке запросе удаляются"
                                "данные о задаче")
def delete_existing_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    if not delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(application, host="0.0.0.0", port=8000)
