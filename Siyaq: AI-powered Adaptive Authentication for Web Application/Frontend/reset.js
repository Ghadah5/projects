// جلب التوكن من الرابط

const urlParams =
new URLSearchParams(window.location.search);

const token =
urlParams.get("token");



document.getElementById("resetForm")

.addEventListener("submit", async (e) => {

e.preventDefault();



const newPassword =
document.getElementById("newPassword").value.trim();


const confirmPassword =
document.getElementById("confirmPassword").value.trim();



// التحقق من التطابق

if(newPassword !== confirmPassword){

alert("كلمة المرور غير متطابقة");

return;

}



// التحقق من الطول

if(newPassword.length < 8){

alert("كلمة المرور يجب أن تكون 8 أحرف على الأقل");

return;

}



// التحقق من حرف كبير

if(!/[A-Z]/.test(newPassword)){

alert("يجب أن تحتوي كلمة المرور على حرف كبير");

return;

}



// التحقق من حرف صغير

if(!/[a-z]/.test(newPassword)){

alert("يجب أن تحتوي كلمة المرور على حرف صغير");

return;

}



// التحقق من رقم

if(!/[0-9]/.test(newPassword)){

alert("يجب أن تحتوي كلمة المرور على رقم");

return;

}

if (!token) {
  alert("الرابط غير صالح أو التوكن مفقود");
  return;
}

const payload = {

token: token,

new_password: newPassword

};



try{


const response =
await fetch("/api/reset-password",

{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify(payload)

}

);



const result =
await response.json();



// لو فيه خطأ

if(!response.ok){

alert(result.detail || "حدث خطأ");

return;

}



// نجاح

alert("تم تغيير كلمة المرور بنجاح");



window.location.href="/frontend/login.html";


}


catch(err){

console.log(err);

alert("السيرفر غير متصل");

}


});