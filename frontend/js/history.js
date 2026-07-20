requireAuth();

let historyByDate = new Map();
let viewYear;
let viewMonth;
let tooltipEl = null;

function ensureTooltip() {
  if (tooltipEl) return tooltipEl;
  tooltipEl = document.createElement("div");
  tooltipEl.className = "day-tooltip";
  document.body.appendChild(tooltipEl);
  return tooltipEl;
}

function showTooltip(cell, entry) {
  const tooltip = ensureTooltip();
  const workoutLabel = escapeHtml(entry.workout_name);
  const notesLabel = entry.notes ? escapeHtml(entry.notes) : "No notes";
  tooltip.innerHTML = `<strong>${workoutLabel}</strong><span>${notesLabel}</span>`;

  const rect = cell.getBoundingClientRect();
  tooltip.style.left = `${rect.left + rect.width / 2}px`;
  tooltip.style.top = `${rect.top}px`;
  tooltip.classList.add("visible");
}

function hideTooltip() {
  if (tooltipEl) tooltipEl.classList.remove("visible");
}

function dateKeyFor(year, month, day) {
  return `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
}

function renderCalendar() {
  const label = document.getElementById("cal-label");
  const monthName = new Date(viewYear, viewMonth, 1).toLocaleDateString("en-US", { month: "long" });
  label.textContent = `${monthName} ${viewYear}`;

  const grid = document.getElementById("calendar-grid");
  grid.innerHTML = "";
  hideTooltip();

  const jsWeekdayOfFirst = new Date(viewYear, viewMonth, 1).getDay();
  const leadingBlanks = (jsWeekdayOfFirst + 6) % 7;
  const daysInMonth = new Date(viewYear, viewMonth + 1, 0).getDate();
  const totalCells = Math.ceil((leadingBlanks + daysInMonth) / 7) * 7;
  const todayKey = todayISO();

  for (let i = 0; i < totalCells; i++) {
    const dayNum = i - leadingBlanks + 1;
    const cell = document.createElement("div");
    cell.className = "day-cell";

    if (dayNum < 1 || dayNum > daysInMonth) {
      cell.classList.add("empty");
      grid.appendChild(cell);
      continue;
    }

    const dateKey = dateKeyFor(viewYear, viewMonth, dayNum);
    cell.textContent = String(dayNum);
    if (dateKey === todayKey) cell.classList.add("today");

    const entry = historyByDate.get(dateKey);
    if (entry) {
      cell.classList.add("completed");
      cell.setAttribute("tabindex", "0");
      cell.addEventListener("mouseenter", () => showTooltip(cell, entry));
      cell.addEventListener("mouseleave", hideTooltip);
      cell.addEventListener("focus", () => showTooltip(cell, entry));
      cell.addEventListener("click", () => showTooltip(cell, entry));
    }

    grid.appendChild(cell);
  }
}

function changeMonth(delta) {
  viewMonth += delta;
  if (viewMonth < 0) {
    viewMonth = 11;
    viewYear -= 1;
  } else if (viewMonth > 11) {
    viewMonth = 0;
    viewYear += 1;
  }
  renderCalendar();
}

document.addEventListener("click", (event) => {
  if (!event.target.closest(".day-cell")) hideTooltip();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") hideTooltip();
});

async function init() {
  const grid = document.getElementById("calendar-grid");

  let history;
  try {
    history = await apiFetch("/history");
  } catch (err) {
    grid.innerHTML = `<p class="error-message">${escapeHtml(err.message)}</p>`;
    return;
  }

  historyByDate = new Map(history.map((entry) => [entry.date, entry]));

  const now = new Date();
  viewYear = now.getFullYear();
  viewMonth = now.getMonth();

  document.getElementById("cal-prev").addEventListener("click", () => changeMonth(-1));
  document.getElementById("cal-next").addEventListener("click", () => changeMonth(1));

  renderCalendar();
}

init();
