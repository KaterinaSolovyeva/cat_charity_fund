from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.db import Base


def create_date():
    return datetime.utcnow()


class CharityProject(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=create_date)
    close_date = Column(DateTime)
