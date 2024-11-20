from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject


CHARITY_PROJECT_EXISTS = (
    'Благотворительный проект с таким именем уже существует!'
)
CHARITY_PROJECT_DOES_NOT_EXIST = (
    'Благотворительный проект не найден!'
)
CHARITY_PROJECT_HAS_INVESTED_AMOUNT = (
    'Нельзя удалить благотворительны проект, в который уже инвестировали!'
)
CHARITY_PROJECT_IS_FULLY_INVESTED = (
    'Нельзя изменить или удалить закрытый благотворительный проект!'
)
INCORRECT_FULL_AMOUNT = (
    'Значение требуемой суммы не может быть меньше уже инвестированной: '
    '{invested_amount}!'
)


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession
) -> None:
    project_id = await (
        charity_project_crud.get_id_by_name(
            project_name,
            session
        )
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CHARITY_PROJECT_EXISTS
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    database_project = await charity_project_crud.get(project_id, session)
    if database_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=CHARITY_PROJECT_DOES_NOT_EXIST
        )
    return database_project


def check_full_amount(
    request_full_amount: int,
    database_invested_amount: int
) -> None:
    if request_full_amount < database_invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=INCORRECT_FULL_AMOUNT.format(
                invested_amount=database_invested_amount
            )
        )


def check_project_has_investments(
    database_invested_amount: int
) -> None:
    if database_invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CHARITY_PROJECT_HAS_INVESTED_AMOUNT
        )


def check_is_project_closed(
    database_fully_invested: bool
) -> None:
    if database_fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CHARITY_PROJECT_IS_FULLY_INVESTED
        )
