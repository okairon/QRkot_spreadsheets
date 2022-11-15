from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        db_charity_project_id = db_charity_project_id.scalars().first()
        return db_charity_project_id

    async def get_projects_by_competion_rate(
        self,
        session: AsyncSession
    ) -> list[dict[str, Union[str, int]]]:
        projects = await session.execute(
            select([CharityProject]).where(CharityProject.fully_invested == 1)
        )
        projects = projects.scalars().all()
        projects_list = sorted(
            [
                {
                    'name': project.name,
                    'duration': project.close_date - project.create_date,
                    'description': project.description
                }
                for project in projects
            ],
            key=lambda x: x['duration']
        )
        return projects_list


charity_project_crud = CRUDCharityProject(CharityProject)
