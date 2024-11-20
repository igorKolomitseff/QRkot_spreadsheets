from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_full_amount,
    check_is_project_closed,
    check_name_duplicate,
    check_project_has_investments
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import donation_crud, charity_project_crud
from app.services.investing import investing
from app.schemas import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех проектов. Доступно для всех пользователей."""

    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
    request_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Добавляет новый проект. Только для суперюзеров."""

    await check_name_duplicate(request_project.name, session)
    new_project = await charity_project_crud.create(
        request_object=request_project,
        session=session
    )
    session.add_all(
        investing(
            target=new_project,
            sources=await donation_crud.get_not_closed(session)
        )
    )
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
    project_id: int,
    request_project: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Обновляет данные о проекте. Только для суперюзеров."""

    database_project = await (
        check_charity_project_exists(project_id, session)
    )
    check_is_project_closed(database_project.fully_invested)
    if request_project.name is not None:
        await check_name_duplicate(request_project.name, session)
    if request_project.full_amount is not None:
        check_full_amount(
            request_project.full_amount,
            database_project.invested_amount
        )
    return await charity_project_crud.update(
        database_object=database_project,
        request_object=request_project,
        session=session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Удаляет проект. Только для суперюзеров."""

    database_project = await (
        check_charity_project_exists(project_id, session)
    )
    check_project_has_investments(database_project.invested_amount)
    check_is_project_closed(database_project.fully_invested)
    return await charity_project_crud.remove(
        database_object=database_project,
        session=session
    )
