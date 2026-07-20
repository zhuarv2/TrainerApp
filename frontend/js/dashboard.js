requireAuth();

async function init() {
  document.getElementById("today-label").textContent = weekdayFromISO(todayISO());
  const container = document.getElementById("workout-container");

  let workout = null;
  try {
    workout = await apiFetch("/workouts/today");
  } catch (err) {
    workout = null;
  }

  if (!workout) {
    container.innerHTML = `<p>No workout scheduled for today. <a href="planner.html">Plan one</a>.</p>`;
    return;
  }

  renderWorkout(container, workout);
}

function renderWorkout(container, workout) {
  const exercises = [...workout.workout_exercises].sort((a, b) => a.order_index - b.order_index);
  const items = exercises.map((ex) => `<li>${escapeHtml(ex.exercise)}</li>`).join("");
  container.innerHTML = `
    <h2>${escapeHtml(workout.name)}</h2>
    <ul class="exercise-list">${items}</ul>
    <div id="completion-area">Checking status…</div>
  `;
  checkCompletion(workout.id);
}

async function checkCompletion(workoutId) {
  const area = document.getElementById("completion-area");
  let entries = [];
  try {
    entries = await apiFetch(`/history/${todayISO()}`);
  } catch (err) {
    area.innerHTML = `<p class="error-message">${escapeHtml(err.message)}</p>`;
    return;
  }

  if (entries.length > 0) {
    const notes = entries[0].notes;
    area.innerHTML = `<p class="status-complete">✅ Marked complete today${notes ? ": " + escapeHtml(notes) : ""}</p>`;
    return;
  }

  area.innerHTML = `
    <label for="notes-input">Notes (optional)</label>
    <textarea id="notes-input" rows="2"></textarea>
    <button id="complete-btn">Mark as Complete</button>
    <p id="complete-error" class="error-message"></p>
  `;
  document.getElementById("complete-btn").addEventListener("click", () => markComplete(workoutId));
}

async function markComplete(workoutId) {
  const btn = document.getElementById("complete-btn");
  const errorEl = document.getElementById("complete-error");
  const notes = document.getElementById("notes-input").value.trim();
  btn.disabled = true;
  errorEl.textContent = "";

  try {
    await apiFetch(`/history/${workoutId}/complete`, {
      method: "POST",
      body: JSON.stringify({ notes: notes || null }),
    });
    checkCompletion(workoutId);
  } catch (err) {
    errorEl.textContent = err.message;
    btn.disabled = false;
  }
}

init();
