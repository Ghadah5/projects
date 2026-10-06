// ── Read data passed from register.js via sessionStorage ──────────────
const userId    = parseInt(sessionStorage.getItem("verify_user_id")  || "0");
const userEmail = sessionStorage.getItem("verify_email") || "";

document.getElementById("displayEmail").textContent = userEmail || "—";

// ── OTP boxes behaviour ───────────────────────────────────────────────
const boxes = document.querySelectorAll(".otp-box");

boxes.forEach((box, i) => {
    box.addEventListener("input", () => {
        box.value = box.value.replace(/\D/g, "").slice(-1);
        box.classList.toggle("filled", box.value !== "");
        if (box.value && i < boxes.length - 1) boxes[i + 1].focus();
    });

    box.addEventListener("keydown", (e) => {
        if (e.key === "Backspace" && !box.value && i > 0) {
            boxes[i - 1].value = "";
            boxes[i - 1].classList.remove("filled");
            boxes[i - 1].focus();
        }
    });

    box.addEventListener("paste", (e) => {
        e.preventDefault();
        const pasted = (e.clipboardData || window.clipboardData)
            .getData("text").replace(/\D/g, "").slice(0, 6);
        pasted.split("").forEach((ch, j) => {
            if (boxes[j]) {
                boxes[j].value = ch;
                boxes[j].classList.add("filled");
            }
        });
        const next = Math.min(pasted.length, boxes.length - 1);
        boxes[next].focus();
    });
});

function getCode() {
    return Array.from(boxes).map(b => b.value).join("");
}

// ── Timer (10 min countdown) ──────────────────────────────────────────
let timerSecs = 1* 60;
const timerEl  = document.getElementById("timer");
const resendEl = document.getElementById("resendLink");

function formatTime(s) {
    const m   = String(Math.floor(s / 60)).padStart(2, "0");
    const sec = String(s % 60).padStart(2, "0");
    return `${m}:${sec}`;
}

const timerInterval = setInterval(() => {
    timerSecs--;
    if (timerSecs <= 0) {
        clearInterval(timerInterval);
        timerEl.textContent = "انتهت صلاحية الرمز";
        timerEl.classList.add("expired");
        resendEl.style.display = "inline";
    } else {
        timerEl.textContent = `ينتهي خلال ${formatTime(timerSecs)}`;
    }
}, 1000);
timerEl.textContent = `ينتهي خلال ${formatTime(timerSecs)}`;

// ── Status helper ─────────────────────────────────────────────────────
function setStatus(msg, type) {
    const el = document.getElementById("statusMsg");
    el.textContent = msg;
    el.className = type === "error" ? "msg-error" : "msg-success";
}

// ── Verify ────────────────────────────────────────────────────────────
document.getElementById("verifyBtn").addEventListener("click", async () => {
    const code = getCode();
    if (code.length < 6) {
        setStatus("الرجاء إدخال الرمز المكوّن من 6 أرقام", "error");
        return;
    }
    if (!userId) {
        setStatus("خطأ: لم يتم العثور على بيانات المستخدم. أعد التسجيل.", "error");
        return;
    }

    const btn = document.getElementById("verifyBtn");
    btn.disabled    = true;
    btn.textContent = "جارٍ التحقق...";

    try {
        const res  = await fetch("/api/verify-email", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, code })
        });
        const data = await res.json();

        if (!res.ok) {
            setStatus(data.detail || "رمز غير صحيح", "error");
            btn.disabled    = false;
            btn.textContent = "تحقق";
            return;
        }

        setStatus("✓ تم التحقق بنجاح! جارٍ التوجيه...", "success");
        sessionStorage.removeItem("verify_user_id");
        sessionStorage.removeItem("verify_email");
        setTimeout(() => { window.location.href = "login.html"; }, 1800);

    } catch (err) {
        setStatus("تعذّر الاتصال بالخادم", "error");
        btn.disabled    = false;
        btn.textContent = "تحقق";
    }
});

// ── Resend ────────────────────────────────────────────────────────────
resendEl.addEventListener("click", async () => {
    if (!userId) return;
    resendEl.style.display = "none";
    setStatus("جارٍ إرسال رمز جديد...", "success");

    try {
        const res  = await fetch("/api/resend-code", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: userEmail })
        });
        const data = await res.json();

        if (!res.ok) {
            setStatus(data.detail || "فشل الإرسال", "error");
            resendEl.style.display = "inline";
            return;
        }

        setStatus("✓ تم إرسال رمز جديد إلى بريدك", "success");
        timerSecs = 10 * 60;
        timerEl.textContent = `ينتهي خلال ${formatTime(timerSecs)}`;
        timerEl.classList.remove("expired");
        boxes.forEach(b => { b.value = ""; b.classList.remove("filled"); });
        boxes[0].focus();

    } catch {
        setStatus("تعذّر الاتصال بالخادم", "error");
        resendEl.style.display = "inline";
    }
});
