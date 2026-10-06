document.getElementById("loginBtn").addEventListener("click", async () => {

    if (!validateLogin()) return;

    const username = document.getElementById("usernameInput").value.trim();
    const password = document.getElementById("passwordInput").value.trim();

    try {
        const response = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const result = await response.json();

        // ── البريد غير محقق ──────────────────────────────────────────
        if (response.status === 403 && result.detail === "EMAIL_NOT_VERIFIED") {
            // جيب user_id وإيميل المستخدم
            try {
                const infoRes = await fetch("/api/user-id-by-username", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username })
                });
                if (infoRes.ok) {
                    const info = await infoRes.json();
                    sessionStorage.setItem("verify_user_id", info.user_id);
                    sessionStorage.setItem("verify_email",   info.email);
                }
            } catch {}
            alert("يجب التحقق من بريدك الإلكتروني أولاً. تم إرسال رمز جديد.");
            window.location.href = "/frontend/verify-email.html";
            return;
        }

        // ── أي خطأ آخر ───────────────────────────────────────────────
        if (!response.ok) {
            alert(result.detail || "فشل تسجيل الدخول");
            return;
        }

        // ── MFA مطلوب (202) ───────────────────────────────────────────
        if (response.status === 202 || result.otp_required) {
            sessionStorage.setItem("otp_user_id",    result.user_id);
            sessionStorage.setItem("otp_attempt_id", result.attempt_id || "");

            // جيب الإيميل الحقيقي لعرضه للمستخدم
            try {
                const infoRes = await fetch("/api/user-id-by-username", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username })
                });
                if (infoRes.ok) {
                    const info = await infoRes.json();
                    sessionStorage.setItem("otp_email", info.email);
                } else {
                    sessionStorage.setItem("otp_email", username);
                }
            } catch {
                sessionStorage.setItem("otp_email", username);
            }

            // حفظ مستوى الخطر لعرضه في صفحة MFA
            if (result.risk_level) {
                sessionStorage.setItem("otp_risk_level", result.risk_level);
            }
            window.location.href = "/frontend/mfa.html";
            return;
        }

        // ── تسجيل دخول ناجح (Standard) ───────────────────────────────
        localStorage.setItem("user_id",     result.user_id);
        localStorage.setItem("username",    result.username    || "");
        localStorage.setItem("role",        result.role        || "");
        localStorage.setItem("first_name",  result.first_name  || "");
        localStorage.setItem("last_name",   result.last_name   || "");
        localStorage.setItem("email",       result.email       || "");
        localStorage.setItem("phone",       result.phone       || "");
        localStorage.setItem("national_id", result.national_id || "");

        window.location.href = "/frontend/home.html";

    } catch (err) {
        console.error(err);
        alert("لا يمكن الوصول إلى الخادم. تأكد أن FastAPI يعمل.");
    }
});