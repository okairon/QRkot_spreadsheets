from fastapi import APIRouter

from app.api.endpoints.charity_project import router as charity_project_router
from app.api.endpoints.donation import router as donation_router
from app.api.endpoints.google_api import router as google_router
from app.api.endpoints.user import router as user_router

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['Charity Projects']
)
main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['Donations']
)
main_router.include_router(
    google_router,
    prefix='/google',
    tags=['Google']
)
