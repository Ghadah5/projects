from collections import Counter


def get_successful_login_history(cursor, user_id: int, limit: int = 50) -> list:
    """
    Get the most recent successful login records for a specific user.
    These records are used to derive the user's normal behavior profile.
    Limit raised to 50 to reduce the chance of forgetting old-but-valid IPs/cities.
    """
    cursor.execute("""
        SELECT attempt_time, geo_country, geo_city, os, browser, ip_address
        FROM context_snapshot
        WHERE user_id = %s AND success = 1
        ORDER BY attempt_time DESC
        LIMIT %s
    """, (user_id, limit))

    return cursor.fetchall()


def get_all_trusted_ips(cursor, user_id: int) -> list:
    """
    Fetch ALL IPs from the full login history — no limit.
    IP is a strong signal and should never be capped at a small window.
    """
    cursor.execute("""
        SELECT DISTINCT ip_address
        FROM context_snapshot
        WHERE user_id = %s AND success = 1 AND ip_address IS NOT NULL
    """, (user_id,))
    rows = cursor.fetchall()
    return [row["ip_address"] for row in rows]


def get_login_count_history(cursor, user_id: int) -> int:
    """
    Returns the total number of successful logins for a user.
    Used as the 'login_count_history' feature for the ML model.
    """
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM context_snapshot
        WHERE user_id = %s AND success = 1
    """, (user_id,))
    row = cursor.fetchone()
    return row["total"] if row else 0


def build_user_profile(history: list, all_ips: list) -> dict:
    """
    Build a behavior profile from successful login history.

    All features now use sets of known values instead of a single most-frequent value:
    - known_countries : all countries ever logged in from
    - known_cities    : all cities ever logged in from
    - known_os        : all OS types ever seen
    - known_browsers  : all browsers ever seen
    - usual_login_hours: deduplicated set of hours
    - usual_login_days : deduplicated set of weekdays
    - trusted_ips     : all IPs from full history (no cap)
    """
    if not history:
        return {
            "has_profile":       False,
            "known_countries":   set(),
            "known_cities":      set(),
            "known_os":          set(),
            "known_browsers":    set(),
            "usual_login_hours": [],
            "usual_login_days":  [],
            "trusted_ips":       []
        }

    countries = [row["geo_country"] for row in history if row.get("geo_country")]
    cities    = [row["geo_city"]    for row in history if row.get("geo_city")]
    oses      = [row["os"]          for row in history if row.get("os")]
    browsers  = [row["browser"]     for row in history if row.get("browser")]

    login_hours = list(set(
        row["attempt_time"].hour for row in history if row.get("attempt_time")
    ))
    login_days = list(set(
        row["attempt_time"].weekday() for row in history if row.get("attempt_time")
    ))

    return {
        "has_profile":       True,
        "known_countries":   set(countries),
        "known_cities":      set(cities),
        "known_os":          set(oses),
        "known_browsers":    set(browsers),
        "usual_login_hours": login_hours,
        "usual_login_days":  login_days,
        "trusted_ips":       list(set(all_ips))
    }


def is_unusual_time(current_hour: int, usual_hours: list, tolerance: int = 2) -> int:
    """
    Check whether the current login hour is unusual compared to previous logins.
    tolerance=2 means ±2 hours is still considered normal.
    """
    if not usual_hours:
        return 0

    for hour in usual_hours:
        if abs(current_hour - hour) <= tolerance:
            return 0

    return 1


def is_unusual_day(current_day: int, usual_days: list) -> int:
    """
    Check whether the current weekday is unusual for this user.
    current_day: integer from datetime.weekday() — 0=Monday … 6=Sunday
    usual_days : list of unique weekday integers from login history.
    Returns 1 if the day has never appeared in the user's history, 0 otherwise.
    """
    if not usual_days:
        return 0

    return 0 if current_day in usual_days else 1


def compare_with_profile(current_context: dict, profile: dict) -> dict:
    """
    Compare current login context with the derived user profile.
    Returns all 8 features required by auth_model_v5.

    All features now check against a set of known values:
    - is_new_country : current country not in known_countries
    - is_new_city    : current city not in known_cities
    - is_new_os      : current OS not in known_os
    - is_new_browser : current browser not in known_browsers
    - is_new_ip      : current IP not in trusted_ips
    """
    if not profile["has_profile"]:
        return {
            "has_profile":     False,
            "is_new_country":  0,
            "is_new_city":     0,
            "is_new_os":       0,
            "is_new_browser":  0,
            "is_new_ip":       0,
            "is_unusual_time": 0,
            "is_unusual_day":  0,
        }

    current_hour = current_context["attempt_time"].hour
    current_day  = current_context["attempt_time"].weekday()

    return {
        "has_profile":     True,
        "is_new_country":  0 if current_context["geo_country"] in profile["known_countries"] else 1,
        "is_new_city":     0 if current_context["geo_city"]    in profile["known_cities"]    else 1,
        "is_new_os":       0 if current_context["os"]          in profile["known_os"]        else 1,
        "is_new_browser":  0 if current_context["browser"]     in profile["known_browsers"]  else 1,
        "is_new_ip":       1 if current_context["ip_address"]  not in profile["trusted_ips"] else 0,
        "is_unusual_time": is_unusual_time(current_hour, profile["usual_login_hours"]),
        "is_unusual_day":  is_unusual_day(current_day,  profile["usual_login_days"]),
    }