from fastapi import APIRouter, HTTPException, Depends
from app.schemas.users_schemas import RegisterUser, LoginUser
from app.database.database import get_db
from app.auth.jwt import verify_password,hash_password, create_token
from app.models.users_models import Users


router = APIRouter(prefix="/auth")


@router.post("/register")
async def register_user(user: RegisterUser,db: str = Depends(get_db)):

    already_exists = db.query(Users).filter(Users.email == user.email).first()

    if already_exists is not None:
        raise HTTPException(status_code=409,
                            detail="User already exists")

    password_hashed = hash_password(user.password)

    new_user = Users(name=user.name,
                     age=user.age,
                     password_hash=password_hashed,
                     email=user.email
                     )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"user created correctly"}

@router.post("/login")
async def login_user(user: LoginUser,db: str = Depends(get_db)):

    searched_user = db.query(Users).filter(Users.email == user.email).first()

    if searched_user is None:
        raise HTTPException(status_code=404,detail="User Not Found")

    verify = verify_password(user.password, searched_user.password_hash)

    if not verify:
        raise HTTPException(status_code=401,detail="Not Authorized")

    token = create_token(searched_user)

    return {"access_token" : token,
            "token_type" : "Bearer"}

