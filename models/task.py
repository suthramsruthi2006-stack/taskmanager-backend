from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey
)

from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    assigned_to = Column(
        Integer,
        ForeignKey("users.id")
    )

    title = Column(
        String(150),
        nullable=False
    )

    description = Column(Text)

    priority = Column(
        String(10),
        default="Medium"
    )

    status = Column(
        String(20),
        default="Todo"
    )