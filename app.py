"""
FirstGear — KAM Induction Website + Chatbot (Streamlit rebuild)

Entry point. Role-based routing via st.session_state, matching the screens
in 00_Build_Spec.md: login, KAM home, journey tracker, day module,
Day-15 assessment, and the Mentor/Manager/HR dashboard, with the chatbot
available on every screen.
"""
from __future__ import annotations

import streamlit as st

from modules.auth import current_user, logout, render_login
from modules.chatbot import ask_chatbot
from modules.dashboard import render_dashboard
from modules.data_store import plan_for_day
from modules.induction import render_day15_assessment, render_day_module, render_journey_tracker, render_kam_home
from modules.progress_store import load as load_progress

st.set_page_config(page_title="FirstGear", page_icon="🧭", layout="wide")

PLUM = "#7B2D6E"
st.markdown(
    f"""
    <style>
    .stApp {{ background-color: #FAF7F9; }}
    h1, h2, h3 {{ color: {PLUM}; }}
    .stButton>button[kind="primary"] {{ background-color: {PLUM}; border-color: {PLUM}; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def render_chatbot_panel(user: dict, state: dict) -> None:
    with st.sidebar:
        st.markdown("### 💬 FirstGear Assistant")
        st.caption("Answers only from the FirstGear Knowledge Base, with sources cited.")

        if user["role"] == "kam":
            kam = state["kams"][user["username"]]
            day = kam["current_day"]
            plan = plan_for_day(min(day, 15)) or {"pillar": "General", "topic": "Induction"}
        else:
            day, plan = 0, {"pillar": "General", "topic": "General enquiry"}

        history_key = f"chat_history_{user['username']}"
        if history_key not in st.session_state:
            st.session_state[history_key] = []

        for msg in st.session_state[history_key]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        prompt = st.chat_input("Ask FirstGear...")
        if prompt:
            st.session_state[history_key].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Checking the knowledge base..."):
                    reply = ask_chatbot(
                        st.session_state[history_key], user["name"], day,
                        plan["pillar"], plan["topic"],
                    )
                st.markdown(reply)
            st.session_state[history_key].append({"role": "assistant", "content": reply})

        if st.session_state[history_key] and st.button("Clear chat"):
            st.session_state[history_key] = []
            st.rerun()


def render_kam_app(user: dict, state: dict) -> None:
    kam = state["kams"][user["username"]]
    tabs = st.tabs(["🏠 Home", "🗺️ Journey", "📘 Today's module", "📝 Day-15 assessment"])
    with tabs[0]:
        render_kam_home(state, user["username"])
    with tabs[1]:
        render_journey_tracker(state, user["username"])
    with tabs[2]:
        day = kam["current_day"]
        if day <= 14:
            render_day_module(state, user["username"], day)
        else:
            st.info("Day 15 is the readiness assessment — see the 'Day-15 assessment' tab.")
    with tabs[3]:
        render_day15_assessment(state, user["username"])


def main() -> None:
    st.title("FirstGear")
    st.caption("Accelerate towards productivity with an AI-enabled assistant")

    user = current_user()
    if not user:
        render_login()
        return

    state = load_progress()

    with st.sidebar:
        st.write(f"Logged in as **{user['name']}**")
        if st.button("Log out"):
            logout()
        st.divider()

    if user["role"] == "kam":
        render_kam_app(user, state)
    elif user["role"] in ("mentor", "manager", "hr"):
        render_dashboard(state, allow_add_hire=user["role"] == "hr")
    else:
        st.error("Unknown role.")

    render_chatbot_panel(user, state)


if __name__ == "__main__":
    main()
