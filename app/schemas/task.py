from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.common import TaskPriority, TaskStatus

class TaskBase(BaseModel):
    title: str = Field(...,min_length=1,max_length=100, description="the title of the task")
    description: Optional[str] = Field(None, max_length=500, description="the description of the task")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="the title of the task")
    description: Optional[str] = Field(None, max_length=500)
    priority: Optional[TaskPriority] = Field(None)
    status: Optional[TaskStatus] = Field(None)

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)