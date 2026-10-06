"""
email_sender.py — سياق
Sends verification code emails using Gmail SMTP.
Reads credentials from config.py
"""

import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ADDRESS, EMAIL_PASSWORD


def generate_code(length: int = 6) -> str:
    """Generate a random 6-digit numeric code."""
    return "".join(random.choices(string.digits, k=length))


def send_verification_email(to_email: str, first_name: str, code: str) -> bool:
    """
    Send an HTML verification email.
    Returns True on success, False on failure.
    """
    subject = "رمز التحقق من البريد الإلكتروني — سياق"

    html_body = f"""
    <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 520px;
         margin: auto; background: #0d1117; color: #e6edf3;
         border-radius: 12px; padding: 36px;">

      <h2 style="color:#58a6ff; margin-bottom:8px;">مرحباً {first_name}،</h2>
      <p style="color:#8b949e; margin-bottom:28px;">
        شكراً لتسجيلك في <strong style="color:#e6edf3;">سياق</strong>.
        استخدم الرمز أدناه للتحقق من بريدك الإلكتروني.
        الرمز صالح لمدة <strong>10 دقائق</strong> فقط.
      </p>

      <div style="background:#161b22; border:1px solid #30363d;
                  border-radius:10px; padding:28px; text-align:center;
                  margin-bottom:28px;">
        <span style="font-size:42px; font-weight:bold;
                     letter-spacing:14px; color:#58a6ff;">
          {code}
        </span>
      </div>

      <p style="color:#8b949e; font-size:13px;">
        إذا لم تقم بإنشاء هذا الحساب، يُرجى تجاهل هذا البريد.
      </p>

      <hr style="border-color:#30363d; margin:24px 0;">
      <p style="color:#484f58; font-size:12px; text-align:center;">
        سياق — خدمة المصادقة الرقمية
      </p>
    </div>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        return True
    except Exception as e:
        print("❌ EMAIL FAILED")
        print(e)
        return False