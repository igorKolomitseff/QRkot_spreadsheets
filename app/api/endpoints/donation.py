from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charity_project_crud, donation_crud
from app.models import User
from app.schemas import (
    DonationCreate,
    DonationSuperUserDB,
    DonationUserDB
)
from app.services.investing import investing

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationSuperUserDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Получает список всех пожертвований. Только для суперюзеров."""

    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationUserDB]
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получает список пожертвований для текущего пользователя."""

    return await donation_crud.get_all_by_user(session, user)


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True
)
async def create_new_donation(
    request_donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Добавляет новое пожертвование от текущего пользователя."""

    new_donation = await donation_crud.create(
        request_object=request_donation,
        session=session,
        user=user
    )
    session.add_all(
        investing(
            target=new_donation,
            sources=await charity_project_crud.get_not_closed(session)
        )
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation
