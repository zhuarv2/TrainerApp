from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///backend/database.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    workout_plans = relationship("WorkoutPlan", back_populates="user", cascade='all, delete-orphan')
    workout_history = relationship('WorkoutHistory', back_populates='user', cascade='all, delete-orphan')

class WorkoutPlan(Base):
    __tablename__ = 'workout_plans'
    id = Column(Integer, primary_key=True)
    day_of_week = Column(String, nullable=False)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='workout_plans')
    workout_exercises = relationship('WorkoutExercise', back_populates='workout_plan', cascade="all, delete-orphan")
    workout_history = relationship('WorkoutHistory', back_populates='workout_plan', cascade="all, delete-orphan")

class WorkoutExercise(Base):
    __tablename__ = 'workout_exercises'
    id = Column(Integer, primary_key=True)
    exercise = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)
    workout_plan_id = Column(Integer, ForeignKey('workout_plans.id'), nullable=False)
    workout_plan = relationship('WorkoutPlan', back_populates='workout_exercises')

class WorkoutHistory(Base):
    __tablename__ = 'workout_history'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    workout_plan_id = Column(Integer, ForeignKey('workout_plans.id'), nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    notes = Column(String, nullable=True)
    user = relationship('User', back_populates='workout_history')
    workout_plan = relationship('WorkoutPlan', back_populates='workout_history')

    @property
    def workout_name(self):
        return self.workout_plan.name

Base.metadata.create_all(engine)