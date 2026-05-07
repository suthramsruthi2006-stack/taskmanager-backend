from pydantic import BaseModel
class TaskCreate(BaseModel):
    project_id: int
    assigned_to: int
    title: str
    description: str | None = None
    priority: str = "Medium"
class TaskUpdate(BaseModel):
    status: str
class TaskOut(TaskCreate):
    id: int
    status:str 
class config:
    from_attributes = True