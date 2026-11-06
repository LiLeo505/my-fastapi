from http.client import HTTPException

from FastAPI import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    age: int


users = {

}

@app.post("/users/")
def create_user(user: UserCreate):
    user_id = max(users.keys(), default=0) + 1
    users[user_id] = {
        "id": user_id,
        "name": user.name, 
        "age": user.age
    }
    return users[user_id]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = users.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )      
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate):
    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    users[user_id].update(user.dict())
    return users[user_id]   

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    del users[user_id]
    return {"message": "User deleted successfully"}