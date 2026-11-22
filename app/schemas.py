from pydantic import BaseModel, ConfigDict,Field

class UserCreate(BaseModel):
    username: str = Field(min_length=1,max_length=50)
    age: int = Field(ge=0)


class UserResponse(BaseModel):
    id: int
    username: str
    age: int

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: str = Field(min_length=1,max_length=50)
    age: int = Field(ge=0)

class UserRegister(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0)
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    username: str
    password: str
     