from fastapi import APIRouter
import datetime
from backend.crud import mark_completed, get_history, get_history_by_date
from backend.schemas import HistoryResponse, MarkWorkoutComplete

router = APIRouter(prefix="/history", tags=["History"])

@router.post("/{workout_id}/complete", response_model=HistoryResponse)
def mark_complete(workout_id:int, workout:MarkWorkoutComplete):
    return mark_completed(user_id=1, workout_id=workout_id, marked_workout=workout)

@router.get("", response_model=list[HistoryResponse])
def get_wo_history():
    history =  get_history(user_id=1)
    return history

@router.get("/{date}", response_model=list[HistoryResponse])
def get_wo_history_by_date(date:datetime.date):
    history = get_history_by_date(user_id=1, date=date)
    return history