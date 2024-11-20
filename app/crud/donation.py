from app.crud import CRUDBase
from app.models import Donation, User

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDDonation(CRUDBase):

    async def get_all_by_user(
        self,
        session: AsyncSession,
        user: User
    ) -> list[Donation]:
        return (
            await session.execute(
                select(
                    Donation
                ).where(
                    Donation.user_id == user.id
                )
            )
        ).scalars().all()


donation_crud = CRUDDonation(Donation)
