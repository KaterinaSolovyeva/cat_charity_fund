from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationDB, DonationDBsuper
from app.schemas.user import UserDB
from app.services.invest import investing_donation

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDBsuper],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Возвращает список всех пожертвований.
    """
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user),
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(
        donation, session, user
    )
    await investing_donation(new_donation, session)
    return new_donation


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude={'user_id'},
)
async def get_my_donation(
    session: AsyncSession = Depends(get_async_session),
    user: UserDB = Depends(current_user)
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations
