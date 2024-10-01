import datetime
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str | None = Field(None, example="세탁소에 맡긴 것을 찾으러 가기")
    # due_date: datetime.date | None = Field(None, example="2024-12-01") 

class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True


class Task(TaskBase):
    id: int
    done: bool = Field(False, description="완료 플래그") 

    class Config:
        from_attributes = True
