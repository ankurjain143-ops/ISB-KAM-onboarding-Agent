"""Mentor / Manager / HR dashboard: every KAM's day, completion, scores, band."""
from __future__ import annotations

import streamlit as st

from modules.data_store import INDUCTION_PLAN
from modules.progress_store import add_new_hire, day_is_complete


def render_dashboard(state: dict, allow_add_hire: bool = False) -> None:
    st.markdown("## Induction Dashboard")
    st.caption("Visible to Mentor, Reporting Boss (KAM Head) and HR")

    if allow_add_hire:
        st.subheader("Add a new hire")
        with st.form("add_new_hire_form"):
            name = st.text_input("Full name", key="new_hire_name")
            submitted = st.form_submit_button("Add KAM", type="primary")

        if submitted:
            try:
                username = add_new_hire(state, name)
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.success(f"Added {name.strip()} as a Day 1 KAM. Login ID: {username}")

    for username, kam in state["kams"].items():
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                st.markdown(f"### {kam['name']}")
                st.write(f"Day **{kam['current_day']}** of 15")
            with col2:
                days_done = sum(
                    1 for d in INDUCTION_PLAN if d["day"] < 15 and day_is_complete(kam, d["day"])
                )
                pct_complete = round(100 * days_done / 14, 0)
                st.metric("Days 1-14 complete", f"{days_done}/14", f"{pct_complete:.0f}%")
            with col3:
                result = kam.get("day15_result")
                if result:
                    band_color = {"Green": "🟢", "Amber": "🟡", "Red": "🔴"}[result["band"]]
                    st.metric("Day-15 result", f"{band_color} {result['band']}", f"{result['overall_pct']}%")
                else:
                    st.write("Day-15: not yet taken")

            with st.expander("Day-by-day detail"):
                rows = []
                for d in INDUCTION_PLAN:
                    if d["day"] == 15:
                        continue
                    day_state = kam["days"].get(str(d["day"]), {})
                    rows.append({
                        "Day": d["day"],
                        "Pillar": d["pillar"],
                        "Content read": "✅" if day_state.get("content_read") else "—",
                        "Session attended": "✅" if day_state.get("session_attended") else "—",
                        "Check score": f"{day_state['check_score']}%" if day_state.get("check_score") is not None else "—",
                        "Passed": "✅" if day_state.get("check_passed") else "—",
                    })
                st.dataframe(rows, hide_index=True, use_container_width=True)

            if kam.get("account_brief"):
                with st.expander("Account brief (Days 11-14)"):
                    st.write(kam["account_brief"])

            if kam.get("day15_result"):
                with st.expander("Day-15 pillar breakdown"):
                    result = kam["day15_result"]
                    for pillar, pct in result["pillar_scores"].items():
                        st.write(f"**{pillar}:** {pct:.0f}%")
                    st.info(f"Recommended action: {result['recommended_action']}")
