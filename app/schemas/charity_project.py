from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, root_validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    @root_validator(skip_on_failure=True)
    def check_fields_not_none(cls, values):
        if (
            values['description'] or values['name'] or values['full_amount']
        ) is None:
            raise ValueError(
                'Значение поля не должно быть пустым'
            )
        return values


class CharityProgectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
