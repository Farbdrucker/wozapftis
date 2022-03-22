from typing import Optional

from pydantic import BaseModel


class CreateBase(BaseModel):
    beer: str
    timestamp: float
    user: Optional[str]


class CreateVote(CreateBase):
    pass


class Vote(CreateBase):
    id: int
    venue_id: int
