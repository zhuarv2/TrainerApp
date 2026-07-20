from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from datetime import date
from backend.models import User, WorkoutPlan, WorkoutExercise, WorkoutHistory
from backend.database import SessionLocal
from backend.auth import hash_password, verify_password, create_token_access, get_current_user
from backend.schemas import UserCreate, UserLogin, WorkoutCreate, WorkoutUpdate, MarkWorkoutComplete

def create_exercise_objects(exercises: list[str]) -> list[WorkoutExercise]:
    exercise_objects = []
    for index, exercise in enumerate(exercises):
        exercise_objects.append(
            WorkoutExercise(
                exercise=exercise, 
                order_index=index
            ))
    return exercise_objects

def get_workout_with_exercises(session, workout_id):
    return (
        session.query(WorkoutPlan)
        .options(selectinload(WorkoutPlan.workout_exercises))
        .filter(WorkoutPlan.id == workout_id)
        .first()
    )

def create_user(user: UserCreate):
    session = SessionLocal()
    try:
        password_hash = hash_password(user.password)
        new_user = User(username=user.username,
                        email=user.email,
                        password_hash=password_hash)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except IntegrityError:
        session.rollback()
        raise
    finally:
        session.close()

def login_user(entered_user: UserLogin):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email==entered_user.email).first()
        if user is None:
            return None
        if not verify_password(entered_user.password, user.password_hash):
            return None
        token = create_token_access(data={"sub":str(user.id)})
        return {
            "access_token":token,
            "token_type":"bearer"
        }
    finally:
        session.close()

def create_workout(workout: WorkoutCreate, current_user:User=Depends(get_current_user)):
    session = SessionLocal()
    try:
        current_user_id = current_user.id
        existing = session.query(WorkoutPlan).options(selectinload(WorkoutPlan.workout_exercises)).filter(
            WorkoutPlan.user_id == current_user_id,
            WorkoutPlan.day_of_week == workout.day_of_week,
        ).first()
        if existing:
            return None
        exercise_objects = create_exercise_objects(workout.workout_exercises)
            
        workout_plan = WorkoutPlan(
            user_id=current_user_id,
            day_of_week=workout.day_of_week,
            name=workout.name,
            workout_exercises=exercise_objects)
        session.add(workout_plan)
        session.commit()
        workout_plan = get_workout_with_exercises(session,workout_plan.id)
        return workout_plan
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def update_workout(workout_id:int, updated_workout: WorkoutUpdate, current_user:User=Depends(get_current_user)):
    session = SessionLocal()
    try:
        current_user_id = current_user.id
        existing = session.query(WorkoutPlan).options(selectinload(WorkoutPlan.workout_exercises)).filter(
            WorkoutPlan.user_id == current_user_id,
            WorkoutPlan.day_of_week == updated_workout.day_of_week,
            WorkoutPlan.id != workout_id
        ).first()
        if existing:
            return None
        workout = session.query(WorkoutPlan).filter(WorkoutPlan.user_id == current_user_id, WorkoutPlan.id==workout_id).first()
        if workout is None:
            return None
        workout.day_of_week = updated_workout.day_of_week
        workout.name = updated_workout.name
        exercise_objects = create_exercise_objects(updated_workout.workout_exercises)
        workout.workout_exercises = exercise_objects
        session.commit()
        workout = get_workout_with_exercises(session, workout_id)
        return workout

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_today_workout(current_user:User=Depends(get_current_user)):
    session = SessionLocal()
    try:
        current_user_id = current_user.id
        today = date.today().strftime("%A")
        workout_plan = session.query(WorkoutPlan).options(selectinload(WorkoutPlan.workout_exercises)).filter(WorkoutPlan.user_id == current_user_id, WorkoutPlan.day_of_week==today).first()
        if workout_plan is None:
            return None
        return workout_plan
    except Exception:
        raise
    finally:
        session.close()

def get_all_workouts(current_user:User=Depends(get_current_user)):
    session = SessionLocal()
    try:
        current_user_id = current_user.id
        workout_plan = session.query(WorkoutPlan).options(selectinload(WorkoutPlan.workout_exercises)).filter(WorkoutPlan.user_id==current_user_id).all()
        return workout_plan
    except Exception:
        raise
    finally:
        session.close()

def get_workout_by_id(user_id:int,workout_id:int):
    session = SessionLocal()
    try:
        workout_plan = session.query(WorkoutPlan).options(selectinload(WorkoutPlan.workout_exercises)).filter(WorkoutPlan.user_id==user_id,WorkoutPlan.id==workout_id).first()
        if workout_plan is None:
            return None
        return workout_plan
    except Exception:
        raise
    finally:
        session.close()

def mark_completed(user_id:int, workout_id:int, marked_workout:MarkWorkoutComplete):
    session = SessionLocal()
    try:
        existing = session.query(WorkoutHistory).filter(
            WorkoutHistory.user_id == user_id,
            WorkoutHistory.workout_plan_id == workout_id,
            WorkoutHistory.date == date.today()
        ).first()
        if existing:
            return existing
        history = WorkoutHistory(
            user_id=user_id,
            workout_plan_id=workout_id,
            date=date.today(),
            completed=True,
            notes=marked_workout.notes
        )
        session.add(history)
        session.commit()
        session.refresh(history)
        return history
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_history(user_id:int):
    session = SessionLocal()
    try:
        workout = session.query(WorkoutHistory).filter(WorkoutHistory.user_id==user_id).all()
        return workout
    except Exception:
        raise
    finally:
        session.close()

def get_history_by_date(user_id:int, date:date):
    session = SessionLocal()
    try:
        workout = session.query(WorkoutHistory).filter(WorkoutHistory.user_id==user_id, WorkoutHistory.date==date).all()
        return workout
    except Exception:
        raise
    finally:
        session.close()