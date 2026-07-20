redirectIfLoggedIn();

document.getElementById("login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const errorEl = document.getElementById("error-message");
  errorEl.textContent = "";

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  try {
    const data = await apiFetch("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    setToken(data.access_token);
    window.location.href = "dashboard.html";
  } catch (err) {
    errorEl.textContent = err.message;
  }
});
