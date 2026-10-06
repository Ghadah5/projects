document.getElementById("registerBtn").addEventListener("click", async () => {

    if (!validateRegister()) return;

    const national_id = document.getElementById("idInput").value.trim();
    const first_name  = document.getElementById("firstNameInput").value.trim();
    const last_name   = document.getElementById("lastNameInput").value.trim();
    const phone       = document.getElementById("mobileInput").value.trim();
    const email       = document.getElementById("emailInput").value.trim();
    const username    = document.getElementById("usernameInput").value.trim();
    const password    = document.getElementById("passwordInput").value.trim();

    const payload = { national_id, first_name, last_name, phone, email, username, password };

    try {
        const response = await fetch("/api/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        localStorage.setItem("first_name",  first_name);
        localStorage.setItem("last_name",   last_name);
        localStorage.setItem("email",       email);
        localStorage.setItem("phone",       phone);
        localStorage.setItem("national_id", national_id);

        if (!response.ok) {
            alert(result.detail || "Registration failed");
            return;
        }

        // ── Save user_id & email so verify-email.html can use them ───
        sessionStorage.setItem("verify_user_id", result.user_id);
        sessionStorage.setItem("verify_email",   email);

        // ── Redirect to verification page ─────────────────────────────
        window.location.href = "verify-email.html";

    } catch (err) {
        console.error(err);
        alert("Backend not reachable. Make sure FastAPI is running.");
    }
});
