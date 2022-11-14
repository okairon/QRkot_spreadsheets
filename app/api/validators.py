from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession
) -> None:
    charity_pjct_id = await charity_project_crud.get_charity_project_by_name(
        charity_project_name, session)
    if charity_pjct_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


def check_not_invested(
    obj_db
) -> None:
    if obj_db.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def check_fully_invested(obj_db) -> None:
    if obj_db.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


def check_new_summ(
    obj_in,
    obj_db,
) -> None:
    if obj_db.invested_amount > obj_in.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Новая требуемая сумма должна быть больше уже внесенной!'
        )


async def check_charity_project_exists(
        charity_pjct_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_pjct_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project
