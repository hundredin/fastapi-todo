from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    title: str | None = Field(default=None, examples=["세탁소에 맡긴 것을 찾으러 가기"])
    # due_date: datetime.date | None = Field(None, example="2024-12-01") 

class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    done: bool = Field(default=False, description="완료 플래그") 
