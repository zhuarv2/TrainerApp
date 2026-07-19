from pydantic import BaseModel, EmailStr, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


class WorkoutCreate(BaseModel):
    day_of_week:str
    name:str
    workout_exercises:list[str]
class WorkoutUpdate(BaseModel):
    day_of_week:str
    name:str
    workout_exercises:list[str]
class WorkoutExerciseResponse(BaseModel):
    exercise:str
    order_index:int
    model_config = ConfigDict(from_attributes=True)
class WorkoutResponse(BaseModel):
    id:int
    day_of_week:str
    name:str
    workout_exercises:list[WorkoutExerciseResponse]
    model_config = ConfigDict(from_attributes=True)


class MarkWorkoutComplete(BaseModel):
    notes:str | None=None
class HistoryResponse(BaseModel):
    date:Date
    completed:bool
    notes:str | None