"""
decision.py
───────────
Decision Module — the single place responsible for:
  1. Translating the ML risk result into a concrete action
  2. Enforcing account lock when risk is High
  3. Generating OTP when risk is Medium (MFA required)
  4. Writing every decision to the auth_decision table
  5. Updating audit_log severity based on actual risk level

Actions (match auth_decision.action ENUM in DB):
  Standard   → Allow — normal login, no friction
  MFA        → Medium risk — send OTP, user must verify
  TempLock   → High risk — lock account temporarily
  AdminLock  → reserved for manual admin action (not triggered here)
"""

import random
import string
from datetime import datetime, timedelta
from email.message import EmailMessage
import smtplib

from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

# ── In-memory OTP store ───────────────────────────────────────────────────────
# { user_id: { "otp": "123456", "expires_at": datetime } }
_otp_store: dict = {}

# ── Thresholds ────────────────────────────────────────────────────────────────
TEMP_LOCK_FAILED_THRESHOLD = 5


# ══════════════════════════════════════════════════════
#  Public API
# ══════════════════════════════════════════════════════

def execute_decision(
    risk_result: dict,
    user: dict,
    attempt_id: int,
    failed_count: int,
    cursor,
    conn,
) -> dict:
    """
    Core decision function — called from main.py after ML model runs.

    Returns dict with keys:
        action        — "Standard" | "MFA" | "TempLock"
        http_status   — 200 | 202 | 403
        message       — human-readable response
        otp_sent      — bool
        risk_level    — forwarded from risk_result
        risk_score    — forwarded from risk_result
    """
    decision   = risk_result["decision"]    # "Allow" | "MFA" | "Block"
    risk_level = risk_result["risk_level"]

    # Map ML decision → DB action
    if decision == "Allow":
        action = "Standard"
    elif decision == "MFA":
        action = "MFA"
    else:
        action = "TempLock"

    # Override: force TempLock if too many consecutive failures
    if failed_count >= TEMP_LOCK_FAILED_THRESHOLD:
        action = "TempLock"

    # Write to auth_decision table
    _save_auth_decision(cursor, conn, attempt_id, action)

    # Update audit_log severity
    _update_audit_severity(cursor, conn, attempt_id, risk_level)

    # Act on decision
    if action == "TempLock":
        _lock_account(cursor, conn, user["user_id"])
        return {
            "action":      "TempLock",
            "http_status": 403,
            "message":     "Account temporarily locked due to suspicious activity.",
            "otp_sent":    False,
            "risk_level":  risk_level,
            "risk_score":  risk_result["risk_score"],
        }

    if action == "MFA":
        otp_sent = _generate_and_send_otp(user["user_id"], user["email"])
        return {
            "action":      "MFA",
            "http_status": 202,
            "message":     "MFA required. A one-time code has been sent to your email.",
            "otp_sent":    otp_sent,
            "risk_level":  risk_level,
            "risk_score":  risk_result["risk_score"],
        }

    # Standard — allow through
    return {
        "action":      "Standard",
        "http_status": 200,
        "message":     "Login successful.",
        "otp_sent":    False,
        "risk_level":  risk_level,
        "risk_score":  risk_result["risk_score"],
    }


def verify_otp(user_id: int, submitted_otp: str) -> bool:
    """
    Returns True if OTP matches and has not expired.
    Clears the OTP from the store on success.
    """
    entry = _otp_store.get(user_id)
    if not entry:
        return False
    if datetime.utcnow() > entry["expires_at"]:
        del _otp_store[user_id]
        return False
    if entry["otp"] != submitted_otp.strip():
        return False
    del _otp_store[user_id]
    return True


# ══════════════════════════════════════════════════════
#  Private helpers
# ══════════════════════════════════════════════════════

def _save_auth_decision(cursor, conn, attempt_id: int, action: str):
    cursor.execute("""
        INSERT INTO auth_decision (attempt_id, action, decision_time)
        VALUES (%s, %s, %s)
    """, (attempt_id, action, datetime.utcnow()))
    conn.commit()


def _update_audit_severity(cursor, conn, attempt_id: int, risk_level: str):
    severity = {"Low": "Low", "Medium": "Medium", "High": "High"}.get(risk_level, "Low")
    cursor.execute("""
        UPDATE audit_log
        SET severity_level = %s, last_update = %s
        WHERE attempt_id = %s
    """, (severity, datetime.utcnow(), attempt_id))
    conn.commit()


def _lock_account(cursor, conn, user_id: int):
    cursor.execute("""
        UPDATE user SET status = 'TempLocked' WHERE user_id = %s
    """, (user_id,))
    conn.commit()
    print(f"[decision] ⛔ User {user_id} TempLocked.")


def _generate_and_send_otp(user_id: int, email: str) -> bool:
    """Generate a 6-digit OTP, store it with 5-min expiry, and email it."""
    otp = "".join(random.choices(string.digits, k=6))
    _otp_store[user_id] = {
        "otp":        otp,
        "expires_at": datetime.utcnow() + timedelta(minutes=1),
    }
    print(f"[decision] 🔑 OTP for user {user_id}: {otp}")  # remove in production
    return _send_otp_email(email, otp)


def _send_otp_email(to_email: str, otp: str) -> bool:
    msg = EmailMessage()
    msg["Subject"] = "رمز التحقق — سياق"
    msg["From"]    = EMAIL_ADDRESS
    msg["To"]      = to_email
    msg.set_content(
        f"رمز التحقق الخاص بك هو:\n\n"
        f"  {otp}\n\n"
        f"صالح لمدة دقيقة واحدة فقط. لا تشاركه مع أحد."
    )
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"[decision] ✅ OTP email sent to {to_email}")
        return True
    except Exception as e:
        print(f"[decision] ⚠️  Failed to send OTP email: {e}")
        return False
