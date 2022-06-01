from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation, create_date
from app.schemas.charity_project import CharityProjectDB
from app.schemas.donation import DonationDBsuper


async def investing(
    donation,
    project,
    session: AsyncSession
):
    remaining_donations = donation.full_amount - donation.invested_amount
    need = project.full_amount - project.invested_amount
    if need <= remaining_donations:
        project.fully_invested = 1
        project.invested_amount = project.full_amount
        project.close_date = create_date()
        donation.invested_amount = donation.invested_amount + need
        if need == remaining_donations:
            donation.fully_invested = 1
            donation.close_date = create_date()
    elif need > remaining_donations:
        project.invested_amount = project.invested_amount + remaining_donations
        donation.invested_amount = donation.full_amount
        donation.close_date = create_date()
        donation.fully_invested = 1
    session.add(project)
    session.add(donation)


async def investing_donation(
    donation: DonationDBsuper,
    session: AsyncSession
):
    projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == 0
        ).order_by(CharityProject.create_date)
    )
    projects = projects.scalars().all()
    for project in projects:
        await investing(donation, project, session)
    await session.commit()
    await session.refresh(donation)


async def find_donation(
    project: CharityProjectDB,
    session: AsyncSession
):
    donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested == 0
        ).order_by(Donation.create_date)
    )
    donations = donations.scalars().all()
    for donation in donations:
        await investing(donation, project, session)
    await session.commit()
    await session.refresh(project)
