from fastapi import APIRouter, Depends, HTTPException
import datetime
from backend.crud import mark_completed, get_history, get_history_by_date
from backend.models import User
from backend.schemas import HistoryResponse, MarkWorkoutComplete
from backend.auth import get_current_user

router = APIRouter(prefix="/history", tags=["History"])

@router.post("/{workout_id}/complete", response_model=HistoryResponse)
def mark_complete(workout_id:int, workout:MarkWorkoutComplete, current_user:User=Depends(get_current_user)):
    history =  mark_completed(user_id=current_user.id, workout_id=workout_id, marked_workout=workout)
    if history is None:
        raise HTTPException(status_code=404, detail="Such workout doesn't exist")
    return history

@router.get("", response_model=list[HistoryResponse])
def get_wo_history(current_user:User=Depends(get_current_user)):
    history =  get_history(user_id=current_user.id)
    return history

@router.get("/{date}", response_model=list[HistoryResponse])
def get_wo_history_by_date(date:datetime.date, current_user:User=Depends(get_current_user)):
    history = get_history_by_date(user_id=current_user.id, date=date)
    return history