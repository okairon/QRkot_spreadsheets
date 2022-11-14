from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_fully_invested, check_name_duplicate,
                                check_new_summ, check_not_invested)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProgectDB,
                                         CharityProjectCreate,
                                         CharityProjectUpdate)
from app.services.investment import invest_to_charity_project

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProgectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для авторизованных пользователей"""
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session)
    new_charity_project = await invest_to_charity_project(
        new_charity_project, session)
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProgectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProgectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    check_fully_invested(charity_project)
    await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        check_new_summ(obj_in, charity_project)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return await invest_to_charity_project(charity_project, session)


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProgectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        charity_project_id, session)
    check_not_invested(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project, session)
    return charity_project
