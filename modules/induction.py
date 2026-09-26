"""Rendering for the KAM's induction screens: home, journey tracker, day module,
Day-15 assessment, and the Days 11-14 account-brief form."""
from __future__ import annotations

import streamlit as st

from modules.assessment import score_assessment, score_daily_check
from modules.data_store import INDUCTION_PLAN, load_kb_file, plan_for_day, questions_for_day, day15_questions
from modules.progress_store import (
    day_is_complete, day_is_unlocked, mark_content_read, mark_session_attended,
    record_check_result, record_day15_result, save_account_brief,
)


def render_kam_home(state: dict, username: str) -> None:
    kam = state["kams"][username]
    day = kam["current_day"]
    st.markdown(f"## Day {day} of 15")
    if day <= 15:
        plan = plan_for_day(day if day <= 14 else 15)
        if plan:
            st.write(f"**Today's focus:** {plan['pillar']} — {plan['topic']}")
            st.caption(f"Owner: {plan['owner']}")
    days_done = sum(1 for d in INDUCTION_PLAN if d["day"] < 15 and day_is_complete(kam, d["day"]))
    st.progress(days_done / 14, text=f"{days_done} of 14 induction days complete")
    if day == 15 and days_done == 14:
        st.success("Days 1-14 complete. Take the Day-15 readiness assessment from the Journey tab.")


def render_journey_tracker(state: dict, username: str) -> None:
    kam = state["kams"][username]
    st.markdown("## Journey Tracker — Phase 1 (Days 1-15)")
    for d in INDUCTION_PLAN:
        day = d["day"]
        if day == 15:
            continue
        unlocked = day_is_unlocked(kam, day)
        complete = day_is_complete(kam, day)
        is_today = kam["current_day"] == day
        if complete:
            status = "✅ Done"
        elif is_today:
            status = "🟣 Today"
        elif unlocked:
            status = "🟣 Available"
        else:
            status = "🔒 Locked"
        st.write(f"**Day {day}** — {d['pillar']}: {d['topic']} — {status}")

    st.divider()
    day15_state = kam["day15_result"]
    days_done = sum(1 for d in INDUCTION_PLAN if d["day"] < 15 and day_is_complete(kam, d["day"]))
    if days_done == 14:
        if day15_state:
            band_emoji = {"Green": "🟢", "Amber": "🟡", "Red": "🔴"}[day15_state["band"]]
            st.write(f"**Day 15 — Assessment** — {band_emoji} {day15_state['band']} ({day15_state['overall_pct']}%)")
        else:
            st.write("**Day 15 — Assessment** — 🟣 Ready to take")
    else:
        st.write("**Day 15 — Assessment** — 🔒 Locked (complete Days 1-14 first)")

    st.caption("Phase 2 (Days 16-30) is shown as locked — planned for Review-3, not built yet.")
    st.write("🔒 **Days 16-30 — Phase 2** (guided pricing exposure, negotiation practice, certification)")


def render_day_module(state: dict, username: str, day: int) -> None:
    kam = state["kams"][username]
    plan = plan_for_day(day)
    if not plan:
        st.error("Unknown day.")
        return

    st.markdown(f"## Day {day} — {plan['pillar']}")
    st.caption(f"Owner: {plan['owner']}")

    tab_content, tab_session, tab_check = st.tabs(["📖 Learning content", "🧑‍🏫 Session", "✅ Knowledge check"])

    with tab_content:
        content = load_kb_file(plan["file"]) if plan["file"] else ""
        st.markdown(content)
        day_state = kam["days"][str(day)]
        if not day_state["content_read"]:
            if st.button("Mark content as read", key=f"read_{day}"):
                mark_content_read(state, username, day)
                st.rerun()
        else:
            st.success("Content marked as read.")

        if day in (11, 12, 13, 14):
            st.divider()
            st.markdown("### Draft account brief — Aravalli Motors")
            st.caption("Customer strategy, what we supply, account health, top 3 opportunities/risks, 90-day plan. Reviewed by your mentor.")
            brief = st.text_area("Your draft", value=kam.get("account_brief", ""), height=220, key=f"brief_{day}")
            if st.button("Save draft", key=f"save_brief_{day}"):
                save_account_brief(state, username, brief)
                st.success("Saved. Your mentor can review it from the dashboard.")

    with tab_session:
        st.write(f"**Owner:** {plan['owner']}")
        st.write(f"**Topic:** {plan['topic']}")
        day_state = kam["days"][str(day)]
        if not day_state["session_attended"]:
            if st.button("Mark session as attended", key=f"session_{day}"):
                mark_session_attended(state, username, day)
                st.rerun()
        else:
            st.success("Session marked as attended.")

    with tab_check:
        _render_knowledge_check(state, username, day)


def _render_knowledge_check(state: dict, username: str, day: int) -> None:
    kam = state["kams"][username]
    day_state = kam["days"][str(day)]
    questions = questions_for_day(day)

    if not questions:
        st.info("No knowledge check configured for this day.")
        return

    if day_state["check_passed"]:
        st.success(f"Already passed ({day_state['check_score']}%). You may retake it.")

    answers = {}
    for q in questions:
        st.markdown(f"**{q['question']}**")
        options = list(q["options"].items())
        choice = st.radio(
            "Choose one", options=[k for k, _ in options],
            format_func=lambda k, opts=dict(options): f"{k}) {opts[k]}",
            key=f"q_{day}_{q['id']}", index=None,
        )
        answers[q["id"]] = choice
        st.divider()

    if st.button("Submit check", key=f"submit_{day}"):
        if any(v is None for v in answers.values()):
            st.warning("Please answer all questions.")
            return
        result = score_daily_check(questions, answers)
        record_check_result(state, username, day, result["pct"], result["passed"])
        if result["passed"]:
            st.success(f"Passed! {result['correct']}/{result['total']} ({result['pct']}%). Next day unlocked.")
        else:
            st.error(f"Not yet — {result['correct']}/{result['total']} ({result['pct']}%). 80% needed; retake anytime.")
        for q in questions:
            correct = answers[q["id"]] == q["answer"]
            icon = "✅" if correct else "❌"
            st.caption(f"{icon} {q['id']}: correct answer **{q['answer']}) {q['options'][q['answer']]}** — {q['explanation']} ({q['source']})")


def render_day15_assessment(state: dict, username: str) -> None:
    kam = state["kams"][username]
    days_done = sum(1 for d in INDUCTION_PLAN if d["day"] < 15 and day_is_complete(kam, d["day"]))

    st.markdown("## Day 15 — Readiness Assessment")
    if days_done < 14:
        st.warning("Complete Days 1-14 first to unlock the Day-15 assessment.")
        return

    if kam.get("day15_result"):
        _render_day15_result(kam["day15_result"])
        if not st.button("Retake assessment"):
            return

    questions = day15_questions()
    answers = {}
    for q in questions:
        st.markdown(f"**[{q['pillar']}] {q['question']}**")
        options = list(q["options"].items())
        choice = st.radio(
            "Choose one", options=[k for k, _ in options],
            format_func=lambda k, opts=dict(options): f"{k}) {opts[k]}",
            key=f"d15_{q['id']}", index=None,
        )
        answers[q["id"]] = choice
        st.divider()

    if st.button("Submit assessment", type="primary"):
        if any(v is None for v in answers.values()):
            st.warning("Please answer all questions.")
            return
        result = score_assessment(answers)
        record_day15_result(state, username, result)
        st.rerun()


def _render_day15_result(result: dict) -> None:
    band_emoji = {"Green": "🟢", "Amber": "🟡", "Red": "🔴"}[result["band"]]
    st.markdown(f"### Result: {band_emoji} {result['band']} — {result['overall_pct']}%")
    st.write(f"**Recommended action:** {result['recommended_action']}")
    cols = st.columns(4)
    for col, (pillar, pct) in zip(cols, result["pillar_scores"].items()):
        col.metric(pillar, f"{pct:.0f}%")
    with st.expander("Question-by-question detail"):
        for d in result["detail"]:
            icon = "✅" if d["is_correct"] else "❌"
            st.caption(f"{icon} [{d['pillar']}] {d['question']} — correct: {d['correct_answer']} ({d['source']})")
