from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session
from dependencies import admin_only
from database import SessionLocal
from models.project import Project
from schemas.project import ProjectCreate


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/")
def get_projects(
    db: Session = Depends(get_db)
):
    return db.query(Project).all()


@router.post("/")
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(admin_only)
):

    new_project = Project(**project.dict())

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project

    new_project = Project(**project.dict())

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project