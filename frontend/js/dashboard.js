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

  area.innerHTML = `<button id="complete-btn">Mark as Complete</button>`;
  document.getElementById("complete-btn").addEventListener("click", () => openCompleteModal(workoutId));
}

function openCompleteModal(workoutId) {
  openModal(
    `
      <h2>Mark Workout Complete</h2>
      <label for="modal-notes">Notes (optional)</label>
      <textarea id="modal-notes" rows="3" placeholder="How did it go?"></textarea>
      <p id="modal-error" class="error-message"></p>
      <div class="modal-actions">
        <button type="button" class="cancel-btn" id="modal-cancel">Cancel</button>
        <button type="button" id="modal-confirm">Confirm</button>
      </div>
    `,
    {
      onOpen(modal, close) {
        modal.querySelector("#modal-cancel").addEventListener("click", close);
        modal.querySelector("#modal-confirm").addEventListener("click", async () => {
          const confirmBtn = modal.querySelector("#modal-confirm");
          const errorEl = modal.querySelector("#modal-error");
          const notes = modal.querySelector("#modal-notes").value.trim();
          confirmBtn.disabled = true;
          errorEl.textContent = "";

          try {
            await apiFetch(`/history/${workoutId}/complete`, {
              method: "POST",
              body: JSON.stringify({ notes: notes || null }),
            });
            close();
            checkCompletion(workoutId);
          } catch (err) {
            errorEl.textContent = err.message;
            confirmBtn.disabled = false;
          }
        });
      },
    }
  );
}

init();
