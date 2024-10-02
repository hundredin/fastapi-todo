from pydantic import BaseModel, ConfigDict


class DoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
