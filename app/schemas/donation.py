from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.schemas.constants import FULL_AMOUNT_MIN


class DonationCreate(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt = Field(..., example=FULL_AMOUNT_MIN)

    class Config:
        extra = Extra.forbid


class DonationUserDB(BaseModel):
    id: int
    comment: Optional[str]
    full_amount: PositiveInt
    create_date: datetime

    class Config:
        orm_mode = True


class DonationSuperUserDB(DonationUserDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
