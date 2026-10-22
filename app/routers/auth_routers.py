from fastapi import APIRouter, HTTPException, Depends
from app.schemas.users_schemas import RegisterUser, LoginUser
from app.database.database import get_db
from app.auth.jwt import verify_password,hash_password, create_token
from app.models.users_models import Users


router = APIRouter(prefix="auth/")


@router.post("/register")
async def register_user(user: RegisterUser,db: str = Depends(get_db)):
    password_hash = hash_password(user.password)

    user.password = password_hash
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"user created correctly"}

@router.post("/login")
async def login_user(user: LoginUser,db: str = Depends(get_db)):

    search_email = db.query(Users).filter(Users.email == user.email).first()

    if search_email is None:
        raise HTTPException(status_code=404,detail="User Not Found")

    verify = verify_password(user.password, search_email.password_hash)

    if not verify:
        raise HTTPException(status_code=401,detail="Not Authorized")

    token = create_token(user)

    return {"access_token" : token,
            "token_type" : "Bearer"}

