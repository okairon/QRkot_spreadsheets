from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class CRUDDonation(CRUDBase):

    async def get_donation_by_user(
        self,
        user: User,
        session: AsyncSession
    ) -> list[Donation]:
        user_donations = await session.execute(select(Donation).where(
            Donation.user_id == user.id)
        )
        return user_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
