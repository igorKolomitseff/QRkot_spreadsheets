from typing import Optional

from app.crud.base import CRUDBase
from app.models import CharityProject

from sqlalchemy import select
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


charity_project_crud = CharityProjectCRUD(CharityProject)
