from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal
from models.task import Task

from schemas.task import (
    TaskCreate,
    TaskUpdate
)

from dependencies import (
    admin_only,
    get_current_user
)
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/")
def get_tasks(
    db: Session = Depends(get_db)
):
    return db.query(Task).all()


@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):

    new_task = Task(**task.dict())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db)
):

    db_task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db_task.status = task.status

    db.commit()
    db.refresh(db_task)

    return {
        "message": "Task updated successfully"
    }


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    db_task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(db_task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }