from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from .constants import INVESTED_AMOUNT_DEFAULT
from app.core.db import Base, NonNullableColumn


class AmountDateBase(Base):
    __abstract__ = True

    full_amount = NonNullableColumn(Integer)
    invested_amount = NonNullableColumn(
        Integer,
        default=INVESTED_AMOUNT_DEFAULT
    )
    fully_invested = NonNullableColumn(Boolean, default=False)
    create_date = NonNullableColumn(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='check_full_amount_positive'
        ),
        CheckConstraint(
            '0 <= invested_amount <= full_amount',
            name='check_invested_amount_in_range'
        )
    )

    def __repr__(self):
        return (
            f'{self.full_amount=}. '
            f'{self.invested_amount=}. '
            f'{self.fully_invested=}. '
            f'{self.create_date=}. '
            f'{self.close_date=}.'
        )
