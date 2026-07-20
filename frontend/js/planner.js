requireAuth();

async function init() {
  const grid = document.getElementById("planner-grid");
  grid.innerHTML = "";

  let workouts;
  try {
    workouts = await apiFetch("/workouts/");
  } catch (err) {
    grid.innerHTML = `<p class="error-message">${escapeHtml(err.message)}</p>`;
    return;
  }

  const byDay = {};
  workouts.forEach((w) => {
    byDay[w.day_of_week] = w;
  });

  DAYS.forEach((day) => {
    grid.appendChild(buildDayCard(day, byDay[day]));
  });
}

function buildDayCard(day, workout) {
  const card = document.createElement("div");
  card.className = "day-card";
  renderViewMode(card, day, workout);
  return card;
}

function renderViewMode(card, day, workout) {
  if (workout) {
    const exercises = [...workout.workout_exercises].sort((a, b) => a.order_index - b.order_index);
    const items = exercises.map((ex) => `<li>${escapeHtml(ex.exercise)}</li>`).join("");
    card.innerHTML = `
      <h3>${day}</h3>
      <p class="workout-name">${escapeHtml(workout.name)}</p>
      <ul class="exercise-list">${items}</ul>
      <button class="edit-btn">Edit</button>
    `;
    card.querySelector(".edit-btn").addEventListener("click", () => renderFormMode(card, day, workout));
  } else {
    card.innerHTML = `
      <h3>${day}</h3>
      <p class="empty-hint">No workout assigned</p>
      <button class="add-btn">+ Add Workout</button>
    `;
    card.querySelector(".add-btn").addEventListener("click", () => renderFormMode(card, day, null));
  }
}

function renderFormMode(card, day, workout) {
  const exerciseNames = workout
    ? [...workout.workout_exercises].sort((a, b) => a.order_index - b.order_index).map((e) => e.exercise)
    : [""];

  card.innerHTML = `
    <h3>${day}</h3>
    <form class="workout-form">
      <label>Workout name</label>
      <input type="text" class="wo-name" required value="${escapeHtml(workout ? workout.name : "")}" />
      <label>Exercises</label>
      <div class="exercise-inputs"></div>
      <button type="button" class="add-exercise-btn">+ Add exercise</button>
      <p class="form-error error-message"></p>
      <div class="form-actions">
        <button type="submit">${workout ? "Save" : "Create"}</button>
        <button type="button" class="cancel-btn">Cancel</button>
      </div>
    </form>
  `;

  const exerciseContainer = card.querySelector(".exercise-inputs");
  exerciseNames.forEach((name) => addExerciseRow(exerciseContainer, name));

  card.querySelector(".add-exercise-btn").addEventListener("click", () => addExerciseRow(exerciseContainer, ""));
  card.querySelector(".cancel-btn").addEventListener("click", () => renderViewMode(card, day, workout));

  card.querySelector(".workout-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const errorEl = card.querySelector(".form-error");
    errorEl.textContent = "";

    const name = card.querySelector(".wo-name").value.trim();
    const exerciseValues = [...exerciseContainer.querySelectorAll("input.exercise-input")]
      .map((input) => input.value.trim())
      .filter((v) => v.length > 0);

    if (exerciseValues.length === 0) {
      errorEl.textContent = "Add at least one exercise.";
      return;
    }

    const payload = { day_of_week: day, name, workout_exercises: exerciseValues };

    try {
      let saved;
      if (workout) {
        saved = await apiFetch(`/workouts?workout_id=${workout.id}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
      } else {
        saved = await apiFetch("/workouts", {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }
      renderViewMode(card, day, saved);
    } catch (err) {
      errorEl.textContent = err.message;
    }
  });
}

function addExerciseRow(container, value) {
  const row = document.createElement("div");
  row.className = "exercise-row";

  const input = document.createElement("input");
  input.type = "text";
  input.className = "exercise-input";
  input.value = value;
  input.placeholder = "Exercise name";

  const removeBtn = document.createElement("button");
  removeBtn.type = "button";
  removeBtn.className = "remove-exercise-btn";
  removeBtn.textContent = "×";
  removeBtn.addEventListener("click", () => row.remove());

  row.appendChild(input);
  row.appendChild(removeBtn);
  container.appendChild(row);
}

init();
