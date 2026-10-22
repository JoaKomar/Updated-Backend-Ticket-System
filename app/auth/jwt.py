from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import bcrypt
from app.models.users_models import Users
from datetime import datetime, timedelta,timezone
from app.config.config import ALGORITHM, SECRET_KEY_TOKEN
from app.database.database import get_db


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login/user")

def create_token(user: Users):

    expire = datetime.now(timezone.utc) + timedelta(days=3)

    payload = {"sub" : user.id,
               "exp" : expire}

    token = jwt.encode(payload,
                       SECRET_KEY_TOKEN,
                       algorithm=ALGORITHM)

    return token


def verify_token(token):
    try:

        payload = jwt.decode(token,
                             SECRET_KEY_TOKEN,
                             algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=409,detail="Invalid authorization")
    return payload


def hash_password(password:str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()


def verify_password(password: str,hashed:str):
    return bcrypt.checkpw(password.encode(), hashed.encode())


def get_current_user(token: str = Depends(oauth_scheme), db: str = Depends(get_db)):

    payload = verify_token(token)

    user_id = int(payload["sub"])    

    user = db.query(Users).filter(Users.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404,
        detail="Not found")

    if user.deleted is True:
        raise HTTPException(status_code=403,
        detail="Not authorized")

    return user

def get_current_admin(user: Users = Depends(get_current_user)):
    if user.role == "user":
        raise HTTPException(status_code=403,
        detail="Not authorized")
    return user