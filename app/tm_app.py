from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models
from crud import create_task, get_tasks, get_task, update_task, delete_task
from database import engine, SessionLocal
from schemas import TaskCreate, TaskUpdate, Task as TaskSchema
from typing import List, Optional
import uuid

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/", response_model=TaskSchema)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task.model_dump())  # Используем model_dump() вместо dict()

@app.get("/tasks/", response_model=List[TaskSchema])
def read_tasks(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_tasks(db, status=status, skip=skip, limit=limit)

@app.get("/tasks/{task_id}", response_model=TaskSchema)
def read_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.put("/tasks/{task_id}", response_model=TaskSchema)
def update_existing_task(
    task_id: uuid.UUID,
    task: TaskUpdate,
    db: Session = Depends(get_db)
):
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task(db, db_task, task.model_dump(exclude_unset=True))  # Используем model_dump()

@app.delete("/tasks/{task_id}")
def delete_existing_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    if not delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)