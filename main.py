from fastapi import FastAPI
from models.user import User
from models.project import Project
from models.task import Task
from database import Base, engine
from routers import auth, projects, tasks
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="Project and Task Management System",
    version="1.0.0"
)
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/")
def home():
    return {
        "message": "Task Manager API Running Successfully"
    }