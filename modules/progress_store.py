"""
Very small JSON-file "database" for demo progress: which day each KAM is on,
whether today's content/session/check are done, check scores, Day-15 result,
and the draft account brief. Streamlit re-runs the whole script on every
interaction and doesn't share state between browser sessions by default, so
progress is persisted to disk (data/progress.json) rather than kept only in
st.session_state — this is what lets Harit/Dev's dashboard see Riya's and
Arjun's progress in a live demo.

This is an interim approach for the prototype (Review-2). A real deployment
would use a proper database (Postgres, etc.) behind the same interface.
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

from modules.data_store import DEMO_USERS, INDUCTION_PLAN

PROGRESS_PATH = Path(__file__).resolve().parent.parent / "data" / "progress.json"
_lock = threading.RLock()


def _default_state() -> dict:
    state = {"kams": {}}
    for username, u in DEMO_USERS.items():
        if u["role"] != "kam":
            continue
        state["kams"][username] = {
            "name": u["name"],
            "current_day": u["day"],
            "days": {
                str(d["day"]): {"content_read": d["day"] < u["day"],
                                 "session_attended": d["day"] < u["day"],
                                 "check_passed": d["day"] < u["day"],
                                 "check_score": None}
                for d in INDUCTION_PLAN
            },
            "account_brief": "",
            "day15_result": None,
        }
        # Arjun (Day 15 demo user) has completed Days 1-14 and is ready for assessment
    return state


def load() -> dict:
    with _lock:
        if not PROGRESS_PATH.exists():
            state = _default_state()
            save(state)
            return state
        try:
            return json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            state = _default_state()
            save(state)
            return state


def save(state: dict) -> None:
    with _lock:
        PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def get_kam(state: dict, username: str) -> dict:
    return state["kams"][username]


def mark_content_read(state: dict, username: str, day: int) -> None:
    state["kams"][username]["days"][str(day)]["content_read"] = True
    save(state)


def mark_session_attended(state: dict, username: str, day: int) -> None:
    state["kams"][username]["days"][str(day)]["session_attended"] = True
    save(state)


def record_check_result(state: dict, username: str, day: int, score_pct: float, passed: bool) -> None:
    d = state["kams"][username]["days"][str(day)]
    d["check_score"] = score_pct
    d["check_passed"] = passed
    if passed:
        kam = state["kams"][username]
        if kam["current_day"] == day and day < 15:
            kam["current_day"] = day + 1
    save(state)


def save_account_brief(state: dict, username: str, text: str) -> None:
    state["kams"][username]["account_brief"] = text
    save(state)


def record_day15_result(state: dict, username: str, result: dict) -> None:
    state["kams"][username]["day15_result"] = result
    save(state)


def day_is_unlocked(kam: dict, day: int) -> bool:
    if day == 1:
        return True
    if day <= kam["current_day"]:
        return True
    return False


def day_is_complete(kam: dict, day: int) -> bool:
    d = kam["days"].get(str(day))
    return bool(d and d["content_read"] and d["session_attended"] and d["check_passed"])
