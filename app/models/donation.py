from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import AmountDateBase
from app.core.db import NonNullableColumn


class Donation(AmountDateBase):
    user_id = NonNullableColumn(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)

    def __repr__(self):
        return (
            f'{self.user_id=}. '
            f'{self.comment=}. '
            f'{super().__repr__()}'
        )
