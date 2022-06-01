from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, Extra, Field, PositiveInt


class DonationBase(BaseModel):
    comment: Optional[str] = Field(None)

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: PositiveInt


class DonationDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBsuper(DonationDB):
    user_id: Optional[UUID4]
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime
