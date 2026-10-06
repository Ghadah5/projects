from datetime import datetime, timedelta
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM, RESET_TOKEN_EXPIRE_MINUTES, EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT
from email.message import EmailMessage
import smtplib
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

# ================= JWT =================
def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        return email
    except JWTError:
        return None

# ================= Email =================
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