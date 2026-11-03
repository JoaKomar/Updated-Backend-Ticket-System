from pydantic import EmailStr, BaseModel, Field

class RegisterUser(BaseModel):
    name: str = Field(min_length=3, max_length=35)
    age: int = Field(gt=13,le=99)
    email: EmailStr
    password: str = Field(min_length=8,max_length=50)

class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8,max_length=50)

class Profile(BaseModel):
    name: str = Field(min_length=3,max_length=35)
    email: EmailStr

    
