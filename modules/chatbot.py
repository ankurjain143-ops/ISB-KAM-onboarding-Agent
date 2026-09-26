"""
The FirstGear chatbot: answers only from the knowledge base, cites sources,
flags illustrative content, declines pricing/commitment questions, and knows
which day/pillar the KAM is on. This calls the real Anthropic API — no
simulated or hard-coded answers.

Requires an API key in Streamlit secrets (ANTHROPIC_API_KEY) or the
environment. See README.md for local + Streamlit Cloud setup.
"""
from __future__ import annotations

import os

import streamlit as st

from modules.data_store import load_all_kb_files

SYSTEM_PROMPT_TEMPLATE = """You are FirstGear, the onboarding assistant for new Key Account Managers at Padmini VNA (PVNA Group).
The employee is {name}, on Day {day} of the induction, studying {pillar}: {topic}.

Answer ONLY from the knowledge documents below. For every answer, name the source file and section, \
e.g. "Source: HR Policies – Travel Policy (PVNA HR Manual, p.66-68)".
If the answer comes from a section tagged [Illustrative - Team 8], say it is illustrative sample \
content for the prototype, not a real Padmini VNA fact.
If the documents don't cover the question, say so plainly and suggest who to ask (the day's owner, \
the mentor Shree Pallavi, the KAM Head Harit Bhasin, or HR Dev Shetty). Do not guess or use outside \
knowledge to fill the gap.
Never make or approve pricing, discounts, delivery dates, compensation or other customer commitments; \
explain the process and the approver from the Day 6 approval matrix instead.
Keep answers short and practical, using steps for processes. Where helpful, link the answer to \
today's module or the next task.

[KNOWLEDGE DOCUMENTS]
{knowledge_documents}
"""


def _get_api_key() -> str | None:
    key = None
    try:
        key = st.secrets.get("ANTHROPIC_API_KEY")  # type: ignore[union-attr]
    except Exception:
        key = None
    return key or os.environ.get("ANTHROPIC_API_KEY")


def build_system_prompt(name: str, day: int, pillar: str, topic: str) -> str:
    docs = load_all_kb_files()
    knowledge_documents = "\n\n---\n\n".join(
        f"### {stem}\n{content}" for stem, content in docs.items()
    )
    return SYSTEM_PROMPT_TEMPLATE.format(
        name=name, day=day, pillar=pillar, topic=topic,
        knowledge_documents=knowledge_documents,
    )


def ask_chatbot(messages: list[dict], name: str, day: int, pillar: str, topic: str) -> str:
    """
    messages: list of {"role": "user"|"assistant", "content": str}, most recent last.
    Returns the assistant's reply text, or an error string starting with '⚠️'.
    """
    api_key = _get_api_key()
    if not api_key:
        return (
            "⚠️ No ANTHROPIC_API_KEY is configured, so I can't call the real model yet. "
            "Add it to .streamlit/secrets.toml locally, or to the app's Secrets on "
            "Streamlit Community Cloud. (See README.md.)"
        )

    try:
        import anthropic
    except ImportError:
        return "⚠️ The `anthropic` package isn't installed. Run: pip install -r requirements.txt"

    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = build_system_prompt(name, day, pillar, topic)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=800,
            system=system_prompt,
            messages=[{"role": m["role"], "content": m["content"]} for m in messages],
        )
        return response.content[0].text
    except Exception as exc:  # noqa: BLE001 - surface any API error plainly in the demo
        return f"⚠️ Chatbot error calling the Anthropic API: {exc}"
