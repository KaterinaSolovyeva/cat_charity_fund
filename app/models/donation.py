from fastapi_users_db_sqlalchemy.guid import GUID
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.charity_project import create_date


class Donation(Base):
    user_id = Column(GUID, ForeignKey('user.id'))
    comment = Column(Text)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=create_date)
    close_date = Column(DateTime)
