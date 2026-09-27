"""Simple demo login: pick a role/user and sign in without a password."""
from __future__ import annotations

import streamlit as st

from modules.data_store import DEMO_USERS
from modules.progress_store import load as load_progress

ROLE_LABELS = {
    "kam": "New KAM",
    "mentor": "Mentor",
    "manager": "Reporting Boss / KAM Head",
    "hr": "HR",
}


def login_accounts(state: dict) -> dict:
    accounts = DEMO_USERS.copy()
    for username, kam in state.get("kams", {}).items():
        accounts.setdefault(username, {"name": kam["name"], "role": "kam"})
    return accounts


def render_login() -> None:
    st.markdown("## Welcome to FirstGear")
    st.caption("Accelerate towards productivity with an AI-enabled assistant")
    accounts = login_accounts(load_progress())

    def format_account(username: str) -> str:
        account = accounts[username]
        if username not in DEMO_USERS:
            return f"{account['name']} - {ROLE_LABELS[account['role']]}"
        return f"{account['name']} — {ROLE_LABELS[account['role']]}"

    with st.form("login_form", clear_on_submit=False):
        username = st.selectbox(
            "Choose your demo account",
            options=list(accounts.keys()),
            format_func=format_account,
        )
        submitted = st.form_submit_button("Log in", type="primary")

    if submitted:
        user = accounts[username]
        st.session_state["auth_user"] = username
        st.session_state["auth_role"] = user["role"]
        st.session_state["auth_name"] = user["name"]
        st.rerun()


def current_user() -> dict | None:
    if "auth_user" not in st.session_state:
        return None
    return {
        "username": st.session_state["auth_user"],
        "role": st.session_state["auth_role"],
        "name": st.session_state["auth_name"],
    }


def logout() -> None:
    for key in ("auth_user", "auth_role", "auth_name"):
        st.session_state.pop(key, None)
    st.rerun()
