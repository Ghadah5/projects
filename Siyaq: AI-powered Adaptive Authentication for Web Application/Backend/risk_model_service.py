"""
risk_model_service.py
─────────────────────
Loads auth_model_v5 (XGBoost) once at startup and exposes
predict_risk_ml() for the login flow in main.py.

Falls back to the old rule-based score if the model file is missing,
so the system keeps working during development / first run.
"""

import json
import os
import numpy as np
import pandas as pd

# ── Model is loaded ONCE when the module is imported ──────────────────────────
_BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
_MODEL_PATH  = os.path.join(_BASE_DIR, "model6", "auth_model_v5.json")
_CONFIG_PATH = os.path.join(_BASE_DIR, "model6", "auth_model_v5_config.json")

_model        = None
_config       = None
_MODEL_LOADED = False

try:
    from xgboost import XGBClassifier

    _config = json.load(open(_CONFIG_PATH))
    _model  = XGBClassifier()
    _model.load_model(_MODEL_PATH)
    _MODEL_LOADED = True
    print("[risk_model_service] ✅ XGBoost model v5 loaded successfully.")

except Exception as e:
    print(f"[risk_model_service] ⚠️  Could not load ML model — falling back to rule-based scoring. Reason: {e}")


# ── Feature order must match training exactly ──────────────────────────────────
_MODEL_FEATURES = [
    "failed_attempts_count",
    "is_new_ip",
    "is_new_country",
    "is_new_city",
    "is_unusual_time",
    "is_unusual_day",
    "is_new_os",
    "is_new_browser",
]

_RISK_WEIGHTS     = np.array([0.0, 0.4, 1.0])   # Normal / Suspicious / Critical
_THRESHOLD_ALLOW  = 0.25
_THRESHOLD_BLOCK  = 0.60


# ── ML prediction ──────────────────────────────────────────────────────────────
def predict_risk_ml(comparison: dict, failed_attempts_count: int) -> dict:
    """
    Runs the XGBoost model and returns risk info.

    Parameters
    ----------
    comparison            : dict returned by compare_with_profile()
    failed_attempts_count : int — consecutive failed logins before this attempt

    Returns
    -------
    {
        "risk_score" : float  (0.0 – 1.0 continuous score),
        "risk_level" : "Low" | "Medium" | "High",
        "decision"   : "Allow" | "MFA" | "Block",
        "p_normal"   : float,
        "p_suspicious": float,
        "p_critical" : float,
        "source"     : "ml" | "rule_based"
    }
    """

    # ── No profile → enforce MFA immediately (config override) ────────────────
    if not comparison.get("has_profile", True):
        return {
            "risk_score":    0.5,
            "risk_level":    "Medium",
            "decision":      "MFA",
            "p_normal":      0.0,
            "p_suspicious":  1.0,
            "p_critical":    0.0,
            "source":        "no_profile_override"
        }

    # ── ML path ───────────────────────────────────────────────────────────────
    if _MODEL_LOADED:
        features = {
            "failed_attempts_count": failed_attempts_count,
            "is_new_ip":             comparison.get("is_new_ip",       0),
            "is_new_country":        comparison.get("is_new_country",   0),
            "is_new_city":           comparison.get("is_new_city",      0),
            "is_unusual_time":       comparison.get("is_unusual_time",  0),
            "is_unusual_day":        comparison.get("is_unusual_day",   0),
            "is_new_os":             comparison.get("is_new_os",        0),
            "is_new_browser":        comparison.get("is_new_browser",   0),
        }

        X       = pd.DataFrame([features])[_MODEL_FEATURES]
        proba   = _model.predict_proba(X)[0]               # [P_Normal, P_Suspicious, P_Critical]
        score   = float(proba @ _RISK_WEIGHTS)             # weighted continuous risk score

        if score < _THRESHOLD_ALLOW:
            risk_level = "Low"
            decision   = "Allow"
        elif score < _THRESHOLD_BLOCK:
            risk_level = "Medium"
            decision   = "MFA"
        else:
            risk_level = "High"
            decision   = "Block"

        return {
            "risk_score":     round(score,          4),
            "risk_level":     risk_level,
            "decision":       decision,
            "p_normal":       round(float(proba[0]), 4),
            "p_suspicious":   round(float(proba[1]), 4),
            "p_critical":     round(float(proba[2]), 4),
            "source":         "ml"
        }

    # ── Fallback: rule-based scoring (original logic) ─────────────────────────
    return _rule_based_fallback(comparison, failed_attempts_count)


def _rule_based_fallback(comparison: dict, failed_attempts_count: int) -> dict:
    """Original rule-based scorer — used only if ML model fails to load."""
    score = 0

    if failed_attempts_count >= 2:
        score += 5
    if comparison.get("is_new_country") == 1 or comparison.get("is_new_city") == 1:
        score += 4
    if comparison.get("is_unusual_time") == 1:
        score += 3
    if comparison.get("is_new_os") == 1:
        score += 2
    if comparison.get("is_new_browser") == 1:
        score += 1

    score = min(score, 15)

    if score <= 4:
        risk_level, decision = "Low",    "Allow"
    elif score <= 10:
        risk_level, decision = "Medium", "MFA"
    else:
        risk_level, decision = "High",   "Block"

    return {
        "risk_score":    score,
        "risk_level":    risk_level,
        "decision":      decision,
        "p_normal":      None,
        "p_suspicious":  None,
        "p_critical":    None,
        "source":        "rule_based"
    }