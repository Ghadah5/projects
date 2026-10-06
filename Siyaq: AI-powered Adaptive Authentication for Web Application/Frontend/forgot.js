document.addEventListener("DOMContentLoaded", () => {
    setLang("ar");
});

document.getElementById("forgotBtn").addEventListener("click", async (e) => {
    e.preventDefault();

    const email = document.getElementById("forgotEmail").value.trim(); // صححت ال id
    if (!email) {
        alert("الرجاء إدخال البريد الإلكتروني");
        return;
    }

    try {
        const response = await fetch("/api/forgot-password", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.detail || "حدث خطأ عند إرسال رابط الاستعادة");
            return;
        }

        alert("تم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني. تحقق من صندوق البريد أو رابط الاختبار في الـ console.");

        console.log("Reset link (for testing):", result.reset_link);

    } catch (err) {
        console.error(err);
        alert("لا يمكن الوصول إلى الخادم. تأكد أن FastAPI يعمل.");
    }
});