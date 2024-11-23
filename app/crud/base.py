from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.models.constants import INVESTED_AMOUNT_DEFAULT


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(self, object_id: int, session: AsyncSession):
        return (
            await session.execute(
                select(
                    self.model
                ).where(
                    self.model.id == object_id
                )
            )
        ).scalars().first()

    async def get_multi(self, session: AsyncSession):
        return (
            await session.execute(
                select(
                    self.model
                )
            )
        ).scalars().all()

    async def create(
        self,
        request_object,
        session: AsyncSession,
        user: Optional[User] = None,
        commit: bool = False
    ):
        request_object_data = request_object.dict()
        if user is not None:
            request_object_data['user_id'] = user.id
        database_object = self.model(**request_object_data)
        database_object.invested_amount = INVESTED_AMOUNT_DEFAULT
        session.add(database_object)
        if commit:
            await session.commit()
            await session.refresh(database_object)
        return database_object

    async def update(
        self,
        database_object,
        request_object,
        session: AsyncSession,
        commit: bool = False
    ):
        database_object_data = jsonable_encoder(database_object)
        request_object_data = request_object.dict(exclude_unset=True)
        for field in database_object_data:
            if field in request_object_data:
                setattr(database_object, field, request_object_data[field])
        if database_object.full_amount == database_object.invested_amount:
            database_object.fully_invested = True
            database_object.close_date = datetime.now()
        session.add(database_object)
        if commit:
            await session.commit()
            await session.refresh(database_object)
        return database_object

    async def remove(self, database_object, session: AsyncSession):
        await session.delete(database_object)
        await session.commit()
        return database_object

    async def get_not_closed(self, session: AsyncSession):
        return (
            await session.execute(
                select(
                    self.model
                ).where(
                    self.model.fully_invested.is_(False)
                ).order_by(
                    self.model.create_date
                )
            )
        ).scalars().all()
