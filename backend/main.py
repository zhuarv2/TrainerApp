import mimetypes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.routes import auth, history, workouts

# Windows' registry-backed mimetypes lookup often reports .js as text/plain,
# which Chrome refuses to register as a service worker script.
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("application/json", ".json")

app = FastAPI()

app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(history.router)


@app.middleware("http")
async def no_cache_static_assets(request, call_next):
    response = await call_next(request)
    # Frontend files have no Cache-Control by default, so browsers apply
    # their own heuristic caching and can serve stale JS/CSS after a deploy.
    # Force revalidation on every request instead (cheap 304s via ETag).
    response.headers["Cache-Control"] = "no-cache"
    return response


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")