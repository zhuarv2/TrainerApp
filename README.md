# TrainerApp

A Progressive Web App for planning your weekly workouts, checking off the one scheduled for today, and looking back at your completion history on a calendar.

Backend is [FastAPI](https://fastapi.tiangolo.com/) + [SQLAlchemy](https://www.sqlalchemy.org/) over SQLite, with JWT authentication. Frontend is plain HTML/CSS/JavaScript — no framework, no build step — served directly by FastAPI as static files.

## Features

- **Accounts** — register/login with JWT bearer auth; passwords hashed with Argon2 via [pwdlib](https://frankie567.github.io/pwdlib/).
- **Weekly planner** — assign one workout (name + ordered list of exercises) to each day of the week; existing days can be edited in place.
- **Today's dashboard** — shows the workout scheduled for the current day and lets you mark it complete with an optional note.
- **History calendar** — a real month-grid calendar (not a table) with completed days marked; hover or tap a marked day to see the workout and notes from that date, with month navigation.
- **Light/dark theme** — manual toggle (not tied to OS preference), persisted in `localStorage`.
- **Responsive** — collapses to a hamburger nav below 640px.
- **Installable PWA** — manifest + service worker cache the app shell for offline loading; API calls always go to the network.

## Tech stack

| | |
|---|---|
| Backend | FastAPI, SQLAlchemy, SQLite, python-jose (JWT), pwdlib (Argon2 password hashing) |
| Frontend | HTML, CSS, vanilla JavaScript, served as static files by FastAPI (same-origin, no CORS needed) |
| Auth | OAuth2 password bearer flow, JWT access tokens |

## Project structure

```
backend/
  main.py          FastAPI app, router registration, static file mount
  auth.py           password hashing, JWT issuing/verification
  database.py       SQLAlchemy engine/session
  models.py         User, WorkoutPlan, WorkoutExercise, WorkoutHistory
  schemas.py        Pydantic request/response models
  crud.py            database operations
  routes/
    auth.py          POST /auth/register, /auth/login
    workouts.py       /workouts CRUD
    history.py         /history read + mark-complete

frontend/
  *.html             one page per view (login, register, dashboard, planner, history)
  css/style.css       shared stylesheet (theme variables, layout, components)
  js/
    api.js             shared fetch helper, auth/theme state, modal + nav helpers
    <page>.js           per-page logic
  manifest.json, sw.js  PWA manifest and service worker
  icons/                app icons (generated, not hand-drawn assets)
```

## Getting started

**Prerequisites:** Python 3.12+ (should work on any recent 3.x).

```bash
git clone https://github.com/zhuarv2/TrainerApp.git
cd TrainerApp

python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt

copy .env.example .env      # Windows
# cp .env.example .env       # macOS/Linux
```

Edit `.env` and set `SECRET_KEY` to your own long random string (used to sign JWTs).

Run the app:

```bash
python -m uvicorn backend.main:app --reload
```

Open **http://127.0.0.1:8000** — it serves both the API and the frontend from the same origin. A SQLite database file is created automatically on first run.

## API reference

All routes except `/auth/register` and `/auth/login` require `Authorization: Bearer <token>`.

| Method | Path | Description |
|---|---|---|
| POST | `/auth/register` | Create an account |
| POST | `/auth/login` | Get an access token |
| POST | `/workouts` | Create a workout for a day (rejects if that day already has one) |
| PUT | `/workouts?workout_id=<id>` | Replace a workout's day/name/exercises |
| GET | `/workouts/today` | The workout scheduled for today, if any |
| GET | `/workouts/` | All of your workouts |
| GET | `/workouts/{id}` | A single workout |
| POST | `/history/{workout_id}/complete` | Mark a workout complete for today, with optional notes |
| GET | `/history` | All completion records |
| GET | `/history/{date}` | Completion records for a specific date (`YYYY-MM-DD`) |

## Known limitations

- A history record doesn't store *which* workout was completed — the frontend infers it by matching the entry's weekday against your *current* weekly plan, so the label can be wrong for a day if you've since reassigned that weekday.
- No delete endpoint for workouts; a day's assignment can only be edited, not removed.
- SQLite is used for local development. There's no production deployment configured yet.
- Installing as a PWA (the browser's "Add to Home Screen" prompt) requires HTTPS — it works on `localhost` for local testing but will need TLS wherever this ends up deployed.

## License

Not yet specified.

## Author

Farouq Hafizhuddin
