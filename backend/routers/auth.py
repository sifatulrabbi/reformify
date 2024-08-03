from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login")
async def login():
    return None


@auth_router.post("/register")
async def register():
    return None


@auth_router.post("/logout")
async def logout():
    return None
