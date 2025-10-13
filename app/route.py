from fastapi import APIRouter
from app.routers import admin_routes,student_routes,auth_routes

router = APIRouter()

router.include_router(admin_routes.router, tags=["Admin"])
router.include_router(student_routes.router, tags=["Student"])
router.include_router(auth_routes.router, tags=["Authentication"])