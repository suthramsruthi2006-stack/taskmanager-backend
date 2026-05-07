from pydantic import BaseModel
class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    deadline: str | None = None
class ProjectOut(ProjectCreate):
    id: int
    status: str
    class config:
        from_attributes = True