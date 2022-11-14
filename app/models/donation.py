from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import BaseAbstractModel


class Donation(BaseAbstractModel):
    """Модель пожертвования"""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
