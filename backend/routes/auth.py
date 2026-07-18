from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from backend.schemas import UserResponse, UserCreate, UserLogin
from backend.crud import create_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse)
def register(user:UserCreate):
    try:
        return create_user(user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists.")
    
@router.post("/login", response_model=UserResponse)
def login(user:UserLogin):
    logged_in_user = login_user(user)
    if logged_in_user is None:
        raise HTTPException(status_code=400, detail="Email or password incorrect.")
    return logged_in_user