from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    full_amount: Optional[PositiveInt]
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    full_amount: PositiveInt


class DonationUpdate(BaseModel):
    pass


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    comment: Optional[str]
    user_id: int
    invested_amount: int
    fully_invested: bool

    class Config:
        orm_mode = True
