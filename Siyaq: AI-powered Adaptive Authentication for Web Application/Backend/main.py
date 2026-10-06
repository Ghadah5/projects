from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import get_db_connection
from pydantic import BaseModel
from auth import hash_password, verify_password
from security import create_reset_token, verify_reset_token
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT
import smtplib
from email.message import EmailMessage
from context_collector import collect_context
import os
from fastapi.responses import FileResponse, JSONResponse
from email_sender import generate_code, send_verification_email
from datetime import datetime, timedelta
from fastapi.staticfiles import StaticFiles
from user_profile import get_successful_login_history, get_all_trusted_ips, build_user_profile, compare_with_profile
from risk_model_service import predict_risk_ml
from decision import execute_decision, verify_otp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


# ══════════════════════════════════════════════
#  Pydantic Models
# ══════════════════════════════════════════════

class RegisterRequest(BaseModel):
    national_id: str
    first_name: str
    last_name: str
    phone: str | None = None
    email: str
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class VerifyEmailRequest(BaseModel):
    user_id: int
    code: str

class ResendCodeRequest(BaseModel):
    email: str

class VerifyOTPRequest(BaseModel):
    user_id: int
    otp: str
    attempt_id: int | None = None   # passed from /api/login to mark success=1 after MFA

class UsernameRequest(BaseModel):
    username: str


# ══════════════════════════════════════════════
#  Email helper
# ══════════════════════════════════════════════

def send_reset_email(to_email, reset_link):
    msg = EmailMessage()
    msg['Subject'] = 'استعادة كلمة المرور'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(f"اضغط على الرابط لإعادة تعيين كلمة المرور:\n\n{reset_link}")
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print("Error sending email:", e)


# ══════════════════════════════════════════════
#  Page Routes
# ══════════════════════════════════════════════

@app.get("/")
def home():
    return FileResponse(os.path.join(FRONTEND_DIR, "home.html"))

@app.get("/login")
def login_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))

@app.get("/register")
def register_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "register.html"))

@app.get("/about")
def about_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "about.html"))

@app.get("/forgot-password-page")
def forgot_password_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "forgot-password.html"))

@app.get("/reset-page")
def reset_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "reset.html"))


# ══════════════════════════════════════════════
#  DB Test
# ══════════════════════════════════════════════

@app.get("/api/test-db")
def test_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"db_working": True, "result": result[0]}


# ══════════════════════════════════════════════
#  Register
# ══════════════════════════════════════════════

@app.post("/api/register")
def register_user(data: RegisterRequest):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT user_id FROM user WHERE email=%s", (data.email,))
    if cursor.fetchone():
        cursor.close(); conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")

    cursor.execute("SELECT user_id FROM user WHERE username=%s", (data.username,))
    if cursor.fetchone():
        cursor.close(); conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed = hash_password(data.password)

    cursor.execute("""
        INSERT INTO user
        (national_id, first_name, last_name, phone, email, username, password_hash, is_verified)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 0)
    """, (data.national_id, data.first_name, data.last_name,
          data.phone, data.email, data.username, hashed))
    conn.commit()
    user_id = cursor.lastrowid

    # ── Send verification code ──
    code = generate_code()
    now = datetime.now()
    expires_at = now + timedelta(minutes=10)

    cursor.execute("""
        INSERT INTO email_verification
        (user_id, verification_code, expires_at, used)
        VALUES (%s, %s, %s, 0)
    """, (user_id, code, expires_at))
    conn.commit()

    send_verification_email(data.email, data.first_name, code)

    cursor.close(); conn.close()
    return {
        "success": True,
        "message": "User registered. Verification code sent.",
        "user_id": user_id
    }


# ══════════════════════════════════════════════
#  Verify Email  ← FIX: كان مفقود كلياً
# ══════════════════════════════════════════════

@app.post("/api/verify-email")
def verify_email(data: VerifyEmailRequest):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # جيب آخر كود غير مستخدم لهذا المستخدم
    cursor.execute("""
        SELECT * FROM email_verification
        WHERE user_id = %s AND used = 0
        ORDER BY expires_at DESC
        LIMIT 1
    """, (data.user_id,))
    row = cursor.fetchone()

    if not row:
        cursor.close(); conn.close()
        raise HTTPException(status_code=400, detail="لا يوجد رمز تحقق نشط لهذا المستخدم")

    # تحقق من انتهاء الصلاحية
    if datetime.now() > row["expires_at"]:
        cursor.close(); conn.close()
        raise HTTPException(status_code=400, detail="انتهت صلاحية الرمز. اضغط على إعادة الإرسال")

    # تحقق من صحة الكود
    if row["verification_code"] != data.code.strip():
        cursor.close(); conn.close()
        raise HTTPException(status_code=400, detail="الرمز غير صحيح")

    # علّم الكود كمستخدم وفعّل الحساب
    cursor.execute("""
        UPDATE email_verification SET used = 1
        WHERE verification_id = %s
    """, (row["verification_id"],))

    cursor.execute("""
        UPDATE user SET is_verified = 1
        WHERE user_id = %s
    """, (data.user_id,))

    conn.commit()
    cursor.close(); conn.close()

    return {"success": True, "message": "تم التحقق من البريد الإلكتروني بنجاح"}


# ══════════════════════════════════════════════
#  Resend Verification Code  ← FIX: كان مفقود
# ══════════════════════════════════════════════

@app.post("/api/resend-code")
def resend_code(data: ResendCodeRequest):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT user_id, first_name, is_verified
        FROM user WHERE email = %s
    """, (data.email,))
    user = cursor.fetchone()

    if not user:
        cursor.close(); conn.close()
        raise HTTPException(status_code=404, detail="البريد الإلكتروني غير موجود")

    if user["is_verified"]:
        cursor.close(); conn.close()
        raise HTTPException(status_code=400, detail="الحساب محقق مسبقاً")

    # أبطل الكودات القديمة
    cursor.execute("""
        UPDATE email_verification SET used = 1
        WHERE user_id = %s AND used = 0
    """, (user["user_id"],))

    # أنشئ كود جديد
    code = generate_code()
    expires_at = datetime.now() + timedelta(minutes=1)

    cursor.execute("""
        INSERT INTO email_verification
        (user_id, verification_code, expires_at, used)
        VALUES (%s, %s, %s, 0)
    """, (user["user_id"], code, expires_at))
    conn.commit()

    send_verification_email(data.email, user["first_name"], code)

    cursor.close(); conn.close()
    return {"success": True, "message": "تم إرسال رمز تحقق جديد"}


# ══════════════════════════════════════════════
#  Get user info by username (for frontend)
# ══════════════════════════════════════════════

@app.post("/api/user-id-by-username")
def get_user_id_by_username(data: UsernameRequest):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT user_id, email FROM user WHERE username = %s",
        (data.username,)
    )
    user = cursor.fetchone()
    cursor.close(); conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user["user_id"], "email": user["email"]}


# ══════════════════════════════════════════════
#  Login
# ══════════════════════════════════════════════

@app.post("/api/login")
def login_user(data: LoginRequest, request: Request):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ── Find user ──
    cursor.execute("SELECT * FROM user WHERE username=%s", (data.username,))
    user = cursor.fetchone()

    if not user:
        cursor.close(); conn.close()
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # ── Account status ──
    if user["status"] != "Active":
        cursor.close(); conn.close()
        raise HTTPException(status_code=403, detail=f"Account is {user['status']}")

    # ── Email not verified ──
    if not user["is_verified"]:
        # أرسل كود تحقق جديد تلقائياً
        cursor.execute("""
            UPDATE email_verification SET used = 1
            WHERE user_id = %s AND used = 0
        """, (user["user_id"],))

        code = generate_code()
        expires_at = datetime.now() + timedelta(minutes=1)
        cursor.execute("""
            INSERT INTO email_verification
            (user_id, verification_code, expires_at, used)
            VALUES (%s, %s, %s, 0)
        """, (user["user_id"], code, expires_at))
        conn.commit()

        send_verification_email(user["email"], user["first_name"], code)

        cursor.close(); conn.close()
        raise HTTPException(status_code=403, detail="EMAIL_NOT_VERIFIED")

    # ── Verify password ──
    password_correct = verify_password(data.password, user["password_hash"])

    # ── Collect context ──
    context = collect_context(request, cursor, user["user_id"])

    # ── Save attempt ──
    # Always insert success=0 here. It will only be flipped to 1 after the
    # full auth flow completes (password + MFA if required). This prevents
    # a partially-authenticated attempt from polluting the user's profile.
    cursor.execute("""
        INSERT INTO context_snapshot
        (user_id, attempt_time, success, failed_attempts_count,
         ip_address, geo_country, geo_city, os, browser)
        VALUES (%s, %s, 0, 0, %s, %s, %s, %s, %s)
    """, (
        user["user_id"], context["attempt_time"],
        context["ip_address"], context["geo_country"],
        context["geo_city"], context["os"], context["browser"]
    ))
    conn.commit()
    attempt_id = cursor.lastrowid

    # ── Count consecutive password failures ──
    # We only count attempts where the password itself was wrong.
    # An attempt that reached auth_decision means the password was correct
    # (the user just failed or skipped MFA), so we exclude it from this count.
    # This way OTP failures never inflate the failed_attempts_count.
    cursor.execute("""
        SELECT cs.attempt_id, cs.success
        FROM context_snapshot cs
        WHERE cs.user_id = %s AND cs.attempt_id != %s
        ORDER BY cs.attempt_time DESC
        LIMIT 20
    """, (user["user_id"], attempt_id))

    rows = cursor.fetchall()
    failed_count = 0
    if not password_correct:
        failed_count = 1  # count the current attempt itself

    for row in rows:
        # If this attempt has a record in auth_decision, password was correct —
        # skip it when counting password failures.
        cursor.execute("""
            SELECT 1 FROM auth_decision WHERE attempt_id = %s
        """, (row["attempt_id"],))
        reached_decision = cursor.fetchone()

        if row["success"] == 1 or reached_decision:
            # Hit a successful login or a password-correct attempt — stop counting
            break
        else:
            failed_count += 1

    cursor.execute("""
        UPDATE context_snapshot SET failed_attempts_count=%s
        WHERE attempt_id=%s
    """, (failed_count, attempt_id))
    conn.commit()

    # ── Audit log (preliminary) ──
    severity = "Low" if password_correct else "High"
    cursor.execute("""
        INSERT INTO audit_log (attempt_id, user_id, event_time, last_update, severity_level)
        VALUES (%s, %s, %s, %s, %s)
    """, (attempt_id, user["user_id"], context["attempt_time"],
          context["attempt_time"], severity))
    conn.commit()

    # ── Wrong password ──
    if not password_correct:
        cursor.close(); conn.close()
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # ── Risk analysis ──
    history  = get_successful_login_history(cursor, user["user_id"])
    all_ips  = get_all_trusted_ips(cursor, user["user_id"])
    profile  = build_user_profile(history, all_ips)
    comparison = compare_with_profile(context, profile)

    print("User Profile:",      profile)
    print("Comparison Result:", comparison)

    risk_result = predict_risk_ml(comparison, failed_count)
    print("Risk Result (ML):",  risk_result)

    # ── Decision (MFA / Block / Allow) ──
    decision_result = execute_decision(
        risk_result=risk_result,
        user=user,
        attempt_id=attempt_id,
        failed_count=failed_count,
        cursor=cursor,
        conn=conn,
    )

    # ── TempLock ──
    if decision_result["action"] == "TempLock":
        cursor.close(); conn.close()
        raise HTTPException(
            status_code=403,
            detail="تم تأمين الحساب مؤقتاً بسبب نشاط مشبوه. تواصل مع الدعم."
        )

    # ── MFA required ──
    # Do NOT mark success=1 yet. The attempt_id is forwarded to /api/verify-otp
    # which flips it only after the OTP is confirmed.
    if decision_result["action"] == "MFA":
        cursor.close(); conn.close()
        print(f"[login] returning attempt_id={attempt_id} to frontend")
        return JSONResponse(status_code=202, content={
            "otp_required": True,
            "user_id":      user["user_id"],
            "attempt_id":   attempt_id,
            "message":      "تم إرسال رمز التحقق إلى بريدك الإلكتروني",
            "risk_level":   risk_result["risk_level"],
        })

    # ── Standard login — mark attempt as fully successful now ──
    cursor.execute("UPDATE context_snapshot SET success = 1 WHERE attempt_id = %s", (attempt_id,))
    conn.commit()
    cursor.close(); conn.close()

    return {
        "success":  True,
        "message":  "Login successful",
        "user_id":  user["user_id"],
        "username": user["username"],
        "role":     user.get("user_role"),
        "first_name":  user.get("first_name"),
        "last_name":   user.get("last_name"),
        "email":       user.get("email"),
        "phone":       user.get("phone"),
        "national_id": user.get("national_id"),
        "risk":     risk_result,
    }


# ══════════════════════════════════════════════
#  Verify OTP (MFA)  ← جديد
# ══════════════════════════════════════════════

@app.post("/api/verify-otp")
def verify_otp_endpoint(data: VerifyOTPRequest):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user WHERE user_id=%s", (data.user_id,))
    user = cursor.fetchone()
    cursor.close(); conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_otp(data.user_id, data.otp):
        raise HTTPException(status_code=400, detail="الرمز غير صحيح أو انتهت صلاحيته")
    print(f"[verify-otp] user_id={data.user_id} attempt_id={data.attempt_id} otp={data.otp}")
    # OTP confirmed — now it is safe to mark the attempt as fully successful.
    # This is the step that makes the IP/city/browser count toward the profile.
    if data.attempt_id:
        conn2 = get_db_connection()
        cur2  = conn2.cursor()
        cur2.execute("UPDATE context_snapshot SET success = 1 WHERE attempt_id = %s", (data.attempt_id,))
        conn2.commit()
        cur2.close(); conn2.close()

    return {
        "success":     True,
        "message":     "تم التحقق بنجاح",
        "user_id":     user["user_id"],
        "username":    user["username"],
        "role":        user.get("user_role"),
        "first_name":  user.get("first_name"),
        "last_name":   user.get("last_name"),
        "email":       user.get("email"),
        "phone":       user.get("phone"),
        "national_id": user.get("national_id"),
    }


# ══════════════════════════════════════════════
#  Resend OTP (MFA)
# ══════════════════════════════════════════════

class ResendOTPRequest(BaseModel):
    user_id: int
    email: str

@app.post("/api/resend-otp")
def resend_otp_endpoint(data: ResendOTPRequest):
    from decision import _generate_and_send_otp
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM user WHERE user_id=%s AND email=%s",
                   (data.user_id, data.email))
    user = cursor.fetchone()
    cursor.close(); conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")

    sent = _generate_and_send_otp(data.user_id, data.email)
    if not sent:
        raise HTTPException(status_code=500, detail="فشل إرسال الرمز")

    return {"success": True, "message": "تم إرسال رمز جديد"}


# ══════════════════════════════════════════════
#  Forgot / Reset Password
# ══════════════════════════════════════════════

@app.post("/api/forgot-password")
async def forgot_password(data: ForgotPasswordRequest, request: Request):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM user WHERE email=%s", (data.email,))
    user = cursor.fetchone()
    cursor.close(); conn.close()

    if not user:
        return {"message": "If the email exists, a reset link has been sent."}

    token = create_reset_token(data.email)
    base_url = str(request.base_url).rstrip("/")
    reset_link = f"{base_url}/reset-page?token={token}"

    send_reset_email(data.email, reset_link)
    print(f"Reset link (for testing): {reset_link}")
    return {"message": "Reset link sent", "reset_link": reset_link}


@app.post("/api/reset-password")
def reset_password(data: ResetPasswordRequest):
    email = verify_reset_token(data.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    conn = get_db_connection()
    cursor = conn.cursor()
    hashed = hash_password(data.new_password)
    cursor.execute("UPDATE user SET password_hash=%s WHERE email=%s", (hashed, email))
    conn.commit()
    cursor.close(); conn.close()
    return {"message": "Password has been reset successfully"}


# ══════════════════════════════════════════════
#  Admin helpers
# ══════════════════════════════════════════════

def require_admin(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_role FROM user WHERE user_id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close(); conn.close()
    if not user or user["user_role"] != "Admin":
        raise HTTPException(status_code=403, detail="Admin only")

# ══════════════════════════════════════════════
#  Admin Stats
# ══════════════════════════════════════════════

@app.get("/api/admin/stats")
def admin_stats(user_id: int):

    require_admin(user_id)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS c FROM user")
    total_users = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) AS c FROM user WHERE status='Active'")
    active_users = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) AS c FROM user WHERE status='Locked'")
    locked_users = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) AS c FROM context_snapshot")
    total_attempts = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) AS c FROM context_snapshot WHERE success=1")
    success_attempts = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) AS c FROM context_snapshot WHERE success=0")
    failed_attempts = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) AS c FROM audit_log WHERE severity_level='High'")
    high_severity = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) AS c FROM user WHERE is_verified=0")
    unverified_users = cursor.fetchone()["c"]

    cursor.close()
    conn.close()

    return {
        "total_users": total_users,
        "active_users": active_users,
        "locked_users": locked_users,
        "total_attempts": total_attempts,
        "success_attempts": success_attempts,
        "failed_attempts": failed_attempts,
        "high_severity": high_severity,
        "unverified_users": unverified_users
    }


# ══════════════════════════════════════════════
#  Admin Users
# ══════════════════════════════════════════════

@app.get("/api/admin/users")
def admin_users(user_id: int):

    require_admin(user_id)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            user_id,
            first_name,
            last_name,
            username,
            email,
            status,
            is_verified,
            user_role
        FROM user
        ORDER BY user_id DESC
    """)

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users


# ══════════════════════════════════════════════
#  Admin Attempts
# ══════════════════════════════════════════════

@app.get("/api/admin/attempts")
def admin_attempts(user_id: int):

    require_admin(user_id)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            cs.attempt_id,
            u.username,
            cs.attempt_time,
            cs.success,
            cs.failed_attempts_count,
            cs.ip_address,
            cs.geo_country,
            cs.browser
        FROM context_snapshot cs
        JOIN user u
            ON cs.user_id = u.user_id
        ORDER BY cs.attempt_time DESC
    """)

    attempts = cursor.fetchall()

    cursor.close()
    conn.close()

    return attempts


# ══════════════════════════════════════════════
#  Admin Audit Log
# ══════════════════════════════════════════════

@app.get("/api/admin/audit")
def admin_audit(user_id: int):

    require_admin(user_id)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            a.log_id,
            u.username,
            a.event_time,
            a.last_update,
            a.severity_level
        FROM audit_log a
        JOIN user u
            ON a.user_id = u.user_id
        ORDER BY a.event_time DESC
    """)

    logs = cursor.fetchall()

    cursor.close()
    conn.close()

    return logs