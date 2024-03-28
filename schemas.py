from typing import Optional

from pydantic import BaseModel, ConfigDict, confloat


class BetAdd(BaseModel):
    event_id: str
    final: Optional[str] = None
    cash: confloat(ge=0)


class Bet(BetAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BetID(BaseModel):
    ok: bool = True
    task_id: int


class BetUpdate(BaseModel):
    event_id: int
    final: bool
