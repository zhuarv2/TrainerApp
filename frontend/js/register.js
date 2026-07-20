redirectIfLoggedIn();

document.getElementById("register-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const errorEl = document.getElementById("error-message");
  const successEl = document.getElementById("success-message");
  errorEl.textContent = "";
  successEl.textContent = "";

  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  try {
    await apiFetch("/auth/register", {
      method: "POST",
      body: JSON.stringify({ username, email, password }),
    });
    successEl.textContent = "Account created! Redirecting to login…";
    setTimeout(() => {
      window.location.href = "login.html";
    }, 1000);
  } catch (err) {
    errorEl.textContent = err.message;
  }
});
