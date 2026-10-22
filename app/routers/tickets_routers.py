from fastapi import APIRouter, HTTPException, Depends

router = APIRouter(prefix="/tickets")



@router.get("/me")
async def user_profile():
    pass
