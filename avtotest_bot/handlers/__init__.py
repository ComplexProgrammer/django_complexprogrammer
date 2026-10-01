# avtotest_bot/handlers/__init__.py
from aiogram import Router

from .start import router as start_router
from .bilet import router as bilet_router
from .quiz import router as quiz_router
from .exam import router as exam_router
from .cdl import router as cdl_router
from .mistakes import router as mistakes_router
from .stats import router as stats_router
from .help import router as help_router
from .admin import router as admin_router

main_router = Router()

main_router.include_router(start_router)
main_router.include_router(bilet_router)
main_router.include_router(quiz_router)
main_router.include_router(exam_router)
main_router.include_router(cdl_router)
main_router.include_router(mistakes_router)
main_router.include_router(stats_router)
main_router.include_router(help_router)
main_router.include_router(admin_router)
