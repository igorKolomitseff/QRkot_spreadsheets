from datetime import datetime
from typing import Optional, Union

from app.crud.base import CRUDBase
from app.models import CharityProject

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession


class CharityProjectCRUD(CRUDBase):

    async def get_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        return (
            await session.execute(
                select(
                    CharityProject.id
                ).where(
                    CharityProject.name == project_name
                )
            )
        ).scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> list[dict[str, Union[str, datetime]]]:
        return (
            await session.execute(
                select([
                    CharityProject.name,
                    CharityProject.create_date,
                    CharityProject.close_date,
                    CharityProject.description
                ]).where(
                    CharityProject.fully_invested.is_(True)
                ).order_by(
                    extract('epoch', CharityProject.close_date) -
                    extract('epoch', CharityProject.create_date)
                )
            )
        ).all()


charity_project_crud = CharityProjectCRUD(CharityProject)
