import httpx
from user_agents import parse
from datetime import datetime


def get_ip_address(request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        ip = forwarded_for.split(",")[0].strip()
    else:
        ip = request.client.host
    return ip


def get_geolocation(ip: str) -> dict:
    if ip in ("127.0.0.1", "::1", "localhost"):
        return {"country": "Local", "city": "Local"}
    try:
        response = httpx.get(
            f"http://ip-api.com/json/{ip}?fields=status,country,city",
            timeout=5.0
        )
        data = response.json()
        if data.get("status") == "success":
            return {"country": data.get("country", "Unknown"), "city": data.get("city", "Unknown")}
        else:
            return {"country": "Unknown", "city": "Unknown"}
    except Exception:
        return {"country": "Unknown", "city": "Unknown"}


def parse_user_agent(user_agent_string: str) -> dict:
    if not user_agent_string:
        return {"os": "Unknown", "browser": "Unknown"}
    ua = parse(user_agent_string)
    return {
        "os": ua.os.family if ua.os.family else "Unknown",
        "browser": ua.browser.family if ua.browser.family else "Unknown"
    }


def get_login_timestamp() -> datetime:
    return datetime.now()


def collect_context(request, cursor, user_id: int) -> dict:
    """
    Collects IP, geolocation, OS, browser, and timestamp.
    NOTE: failed_attempts_count is handled in main.py AFTER saving
    the attempt — so the current attempt is included in the count.
    """
    ip = get_ip_address(request)
    geo = get_geolocation(ip)
    ua_string = request.headers.get("User-Agent", "")
    device = parse_user_agent(ua_string)
    timestamp = get_login_timestamp()

    return {
        "ip_address": ip,
        "geo_country": geo["country"],
        "geo_city": geo["city"],
        "os": device["os"],
        "browser": device["browser"],
        "attempt_time": timestamp
    }