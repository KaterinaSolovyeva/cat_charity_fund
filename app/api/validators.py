from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_charity_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект пожертвования не найден!'
        )
    return charity_project


async def check_invested_amount_is_none(
    project_id: int,
    session: AsyncSession,
) -> None:
    invested_amount = await session.execute(
        select(CharityProject.invested_amount).where(
            CharityProject.id == project_id
        )
    )
    invested_amount = invested_amount.scalars().first()
    if invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='В этот проект уже пожертвованы деньги. Нельзя удалить!'
        )
