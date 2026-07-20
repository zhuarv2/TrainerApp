requireAuth();

async function init() {
  const body = document.getElementById("history-body");

  let history;
  let workouts;
  try {
    [history, workouts] = await Promise.all([apiFetch("/history"), apiFetch("/workouts/")]);
  } catch (err) {
    body.innerHTML = `<tr><td colspan="3" class="error-message">${escapeHtml(err.message)}</td></tr>`;
    return;
  }

  if (history.length === 0) {
    body.innerHTML = `<tr><td colspan="3">No completed workouts yet.</td></tr>`;
    return;
  }

  const byDay = {};
  workouts.forEach((w) => {
    byDay[w.day_of_week] = w;
  });

  const sorted = [...history].sort((a, b) => b.date.localeCompare(a.date));

  body.innerHTML = sorted
    .map((entry) => {
      const weekday = weekdayFromISO(entry.date);
      const workout = byDay[weekday];
      const workoutLabel = workout ? escapeHtml(workout.name) : `(${weekday})`;
      return `
        <tr>
          <td>${escapeHtml(entry.date)}</td>
          <td>${workoutLabel}</td>
          <td>${entry.notes ? escapeHtml(entry.notes) : "&mdash;"}</td>
        </tr>
      `;
    })
    .join("");
}

init();
