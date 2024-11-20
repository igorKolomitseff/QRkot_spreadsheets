from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.models.charity_project import NAME_MAX_LENGTH
from app.schemas.constants import STRING_LENGTH_MIN, FULL_AMOUNT_MIN

FIELD_CANT_BE_NONE = 'Поле {field} не может быть None!'


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=NAME_MAX_LENGTH)
    description: str
    full_amount: PositiveInt = Field(..., example=FULL_AMOUNT_MIN)

    class Config:
        min_anystr_length = STRING_LENGTH_MIN
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, max_length=NAME_MAX_LENGTH)
    description: Optional[str]
    full_amount: Optional[PositiveInt] = Field(None, example=FULL_AMOUNT_MIN)

    @validator('name', 'description', 'full_amount')
    def field_cant_be_none(cls, value: str, field):
        if value is None:
            raise ValueError(FIELD_CANT_BE_NONE.format(field=field.name))
        return value


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
