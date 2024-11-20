from sqlalchemy import String, Text


from .base import AmountDateBase
from .constants import NAME_MAX_LENGTH
from app.core.db import NonNullableColumn


class CharityProject(AmountDateBase):
    name = NonNullableColumn(String(NAME_MAX_LENGTH), unique=True)
    description = NonNullableColumn(Text)

    def __repr__(self):
        return (
            f'{self.name=}. '
            f'{self.description=}. '
            f'{super().__repr__()}'
        )
