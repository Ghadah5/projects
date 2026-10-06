function isValidPassword(pw) {
    return /[0-9]/.test(pw) && /[!@#$%^&*(),.?":{}|<>]/.test(pw);
}

function validateRegister() {

    const id = document.getElementById("idInput").value.trim();
    const firstName = document.getElementById("firstNameInput").value.trim();
    const lastName = document.getElementById("lastNameInput").value.trim();
    const mobile = document.getElementById("mobileInput").value.trim();
    const email = document.getElementById("emailInput").value.trim();
    const username = document.getElementById("usernameInput").value.trim();
    const password = document.getElementById("passwordInput").value.trim();
    const confirm = document.getElementById("confirmInput").value.trim();

    let messages = [];

    if (!/^\d{10,15}$/.test(id)) {
        messages.push("الرجاء إدخال رقم هوية/إقامة صحيح");
    }

    if (firstName.length < 2 || firstName.length > 15) {
        messages.push("الاسم الأول يجب أن يكون بين 2 و15 حرفاً");
    }

    if (lastName.length < 2 || lastName.length > 15) {
        messages.push("اسم العائلة يجب أن يكون بين 2 و15 حرفاً");
    }

    if (!/^(05\d{8}|\+9665\d{8})$/.test(mobile)) {
        messages.push("الرجاء إدخال رقم جوال صالح");
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        messages.push("الرجاء إدخال بريد إلكتروني صالح");
    }

    if (username.length < 8 || username.length > 15) {
        messages.push("اسم المستخدم يجب أن يكون بين 8 و15 حرفاً");
    }

    if (password.length < 8 || password.length > 30 || !isValidPassword(password)) {
        messages.push("كلمة المرور يجب أن تحتوي على أرقام ورموز");
    }

    if (password !== confirm) {
        messages.push("تأكيد كلمة المرور لا يطابق كلمة المرور");
    }

    if (messages.length > 0) {
        alert(messages.join("\n"));
        return false;
    }

    return true;
}

function validateLogin() {

    const username = document.getElementById("usernameInput").value.trim();
    const password = document.getElementById("passwordInput").value.trim();

    let messages = [];

    if (username.length < 8 || username.length > 15) {
        messages.push("اسم المستخدم يجب أن يكون بين 8 و15 حرفاً");
    }

    if (password.length < 8 || password.length > 30 || !isValidPassword(password)) {
        messages.push("كلمة المرور يجب أن تكون 8 أحرف على الأقل وتحتوي على أرقام ورموز");
    }

    if (messages.length > 0) {
        alert(messages.join("\n"));
        return false;
    }

    return true;

}
