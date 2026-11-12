from fastapi import APIRouter
router=APIRouter()

@router.get("/auth/")
def get_current_user():
    return {"user":"authinticated"}