from pydantic import BaseModel, EmailStr
from datetime import date as Date

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str
class UserLogin(BaseModel):
    email:EmailStr
    password:str
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class WorkoutCreate(BaseModel):
    day_of_week:str
    name:str
    workout_exercises:list[str]
class WorkoutUpdate(BaseModel):
    day_of_week:str
    name:str
    workout_exercises:list[str]
class WorkoutResponse(BaseModel):
    id:int
    day_of_week:str
    name:str
    workout_exercises:list[str]


class MarkWorkoutComplete(BaseModel):
    notes:str | None=None
class HistoryResponse(BaseModel):
    date:Date
    name:str
    completed:bool
    notes:str | None