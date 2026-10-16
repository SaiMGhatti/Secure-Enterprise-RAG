from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: str
    roles: list[str] = Field(default_factory=list)
    groups: list[str] = Field(default_factory=list)