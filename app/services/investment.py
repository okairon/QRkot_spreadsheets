from datetime import datetime as dt
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest_to_charity_project(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession
) -> Union[CharityProject, Donation]:
    investing_model = CharityProject if type(obj_in) is Donation else Donation
    donation_objs = await check_free_funds_to_or_for_invest(
        investing_model, session)
    if donation_objs is None:
        return obj_in
    update_objects(obj_in, donation_objs, session)
    await session.commit()
    await session.refresh(obj_in)
    return obj_in


async def check_free_funds_to_or_for_invest(
    model: Union[CharityProject, Donation],
    session: AsyncSession
) -> Union[list[Donation], list[CharityProject]]:
    open = await session.execute(
        select(model).where(model.fully_invested == 0))
    return open.scalars().all()


def update_objects(
    obj_in: Union[CharityProject, Donation],
    donation_objs: Union[list[CharityProject], list[Donation]],
    session: AsyncSession
) -> None:
    uninvested_amount = obj_in.full_amount - obj_in.invested_amount
    for obj in donation_objs:
        avail_amount = obj.full_amount - obj.invested_amount
        if avail_amount == uninvested_amount:
            process_obj(obj_in, obj, session)
            break
        elif avail_amount > uninvested_amount:
            process_obj(obj_in, obj, session,
                        uninvested_amount=uninvested_amount)
            break
        else:
            process_obj(obj_in, obj, session, avail_amount=avail_amount)
            uninvested_amount -= avail_amount


def process_obj(
    obj_in: Union[CharityProject, Donation],
    obj: Union[CharityProject, Donation],
    session: AsyncSession,
    uninvested_amount: int = None,
    avail_amount: int = None
) -> None:
    obj_in.invested_amount = (
        obj_in.invested_amount + avail_amount if avail_amount
        is not None else obj_in.full_amount
    )
    obj.invested_amount = (
        obj.invested_amount + uninvested_amount if uninvested_amount
        is not None else obj.full_amount
    )
    obj_in.fully_invested = True if (
        obj_in.invested_amount == obj_in.full_amount
    ) else False
    obj.fully_invested = True if (
        obj.invested_amount == obj.full_amount
    ) else False
    obj_in.close_date = dt.now() if obj_in.fully_invested is True else None
    obj.close_date = dt.now() if obj.fully_invested is True else None
    session.add_all([obj_in, obj])
