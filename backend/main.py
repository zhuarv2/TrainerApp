from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.routes import auth, history, workouts

app = FastAPI()

app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(history.router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")