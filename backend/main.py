from schemas import UserCreate
from crud import create_user

user = UserCreate(
    username="admin",
    email="admin@workout.id",
    password="admin123"
)

create_user(user)