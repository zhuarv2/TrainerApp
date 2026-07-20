from fastapi import APIRouter, Depends, HTTPException
from backend.auth import get_current_user
from backend.crud import create_workout, update_workout, get_today_workout, get_all_workouts, get_workout_by_id
from backend.models import User
from backend.schemas import WorkoutResponse, WorkoutCreate, WorkoutUpdate

router = APIRouter(prefix="/workouts", tags=["Workouts"])

@router.post("",response_model=WorkoutResponse)
def create_wo(workout:WorkoutCreate, current_user:User=Depends(get_current_user)):
    created = create_workout(user_id=current_user.id,workout=workout)
    if created is None:
        raise HTTPException(status_code=409, detail="Workout for this specific day has been assigned previously")
    return created

@router.put("",response_model=WorkoutResponse)
def update_wo(workout_id:int, workout:WorkoutUpdate, current_user:User=Depends(get_current_user)):
    updated = update_workout(user_id=current_user.id,workout_id=workout_id, updated_workout=workout)
    if updated is None:
        raise HTTPException(status_code=404, detail="Workout not found or day already assigned.")
    return updated

@router.get("/today", response_model=WorkoutResponse)
def get_today_wo(current_user:User=Depends(get_current_user)):
    workout_plan = get_today_workout(user_id=current_user.id)
    if workout_plan is None:
        raise HTTPException(status_code=404, detail="Today's workout not found")
    return workout_plan

@router.get("/", response_model=list[WorkoutResponse])
def get_all_wo(current_user:User=Depends(get_current_user)):
    return get_all_workouts(user_id=current_user.id)

@router.get("/{workout_id}",response_model=WorkoutResponse)
def get_wo_by_id(workout_id:int, current_user:User=Depends(get_current_user)):
    workout_plan_by_id = get_workout_by_id(user_id=current_user.id, workout_id=workout_id)
    if workout_plan_by_id is None:
        raise HTTPException(status_code=404, detail="This day's workout not found")
    return workout_plan_by_id

