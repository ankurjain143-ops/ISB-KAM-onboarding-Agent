"""
Loads the FirstGear knowledge base, question bank and demo user/progress data.
Everything here reads from local files under data/ — nothing is hard-coded
that should instead come from the knowledge base, per the build spec.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
KB_DIR = BASE_DIR / "data" / "knowledge_base"
QUESTION_BANK_PATH = BASE_DIR / "data" / "question_bank.json"

# Day 1-15 plan, from 00_Build_Spec.md's induction plan -> knowledge base mapping (§8.1)
INDUCTION_PLAN = [
    {"day": 1, "pillar": "Governance & People", "topic": "Company, values, Code of Conduct, KAM charter intro",
     "file": "Day01_Company_Values_Code_of_Conduct", "owner": "HR (Dev Shetty) + Reporting Boss (Harit Bhasin)"},
    {"day": 2, "pillar": "Products", "topic": "ICE / Hybrid / EV product portfolio",
     "file": "Day02_Product_Portfolio", "owner": "Product / Engineering"},
    {"day": 3, "pillar": "Processes", "topic": "Plant walk: process flow, safety, traceability, logistics",
     "file": "Day03_Plant_Process_Safety_Traceability", "owner": "Plant + SCM"},
    {"day": 4, "pillar": "Governance (Quality)", "topic": "APQP, PPAP, complaint handling, change control",
     "file": "Day04_Quality_APQP_PPAP_Complaints_Change_Control", "owner": "Quality"},
    {"day": 5, "pillar": "People", "topic": "Who owns what across functions",
     "file": "Day05_Who_Owns_What_Directory", "owner": "Reporting Boss + Functions"},
    {"day": 6, "pillar": "Governance (KAM charter)", "topic": "KAM charter, KPIs, approval matrix, escalation map",
     "file": "Day06_KAM_Charter_KPIs_Approval_Matrix_Escalation", "owner": "Reporting Boss"},
    {"day": 7, "pillar": "Processes (RFQ)", "topic": "RFQ intake to quotation SOP",
     "file": "Day07_RFQ_to_Quotation_SOP", "owner": "Sales + Engineering"},
    {"day": 8, "pillar": "Processes (Costing)", "topic": "Cost build-up, margin logic, payment terms",
     "file": "Day08_Costing_Commercial_Basics", "owner": "Finance + Commercial"},
    {"day": 9, "pillar": "Governance (Programme & Quality)", "topic": "Nomination-to-SOP, 8D method",
     "file": "Day09_Programme_Governance_Nomination_to_SOP_8D", "owner": "Programme + Quality"},
    {"day": 10, "pillar": "Practice & check", "topic": "Mock RFQ, pricing scenario, customer escalation",
     "file": "Day10_Practice_Scenarios", "owner": "Mentor + SMEs"},
    {"day": 11, "pillar": "People (Customer context)", "topic": "Customer 360: Aravalli Motors",
     "file": "Day11-12_Customer360_Sample_OEM_Account", "owner": "Mentor / Prior KAM"},
    {"day": 12, "pillar": "People (Customer context)", "topic": "Customer 360: Aravalli Motors (continued)",
     "file": "Day11-12_Customer360_Sample_OEM_Account", "owner": "Mentor / Prior KAM"},
    {"day": 13, "pillar": "People (Stakeholders & history)", "topic": "Stakeholder map, pricing history",
     "file": "Day13-14_Stakeholder_Map_Account_History", "owner": "Mentor + Teams"},
    {"day": 14, "pillar": "People (Stakeholders & history)", "topic": "Stakeholder map, pricing history (continued)",
     "file": "Day13-14_Stakeholder_Map_Account_History", "owner": "Mentor + Teams"},
    {"day": 15, "pillar": "Assessment", "topic": "Consolidated readiness assessment + account brief review",
     "file": None, "owner": "Mentor + Reporting Boss + HR"},
]

DEMO_USERS = {
    "riya": {"name": "Riya Sharma", "role": "kam", "day": 7},
    "arjun": {"name": "Arjun Mehta", "role": "kam", "day": 15},
    "shree": {"name": "Shree Pallavi", "role": "mentor"},
    "harit": {"name": "Harit Bhasin", "role": "manager"},
    "dev": {"name": "Dev Shetty", "role": "hr"},
}


def load_kb_file(file_stem: str) -> str:
    """Read one knowledge-base markdown file by its stem (no extension)."""
    path = KB_DIR / f"{file_stem}.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def load_all_kb_files() -> dict[str, str]:
    """Return {stem: content} for every knowledge-base file, for the chatbot corpus."""
    docs = {}
    for path in sorted(KB_DIR.glob("*.md")):
        docs[path.stem] = path.read_text(encoding="utf-8")
    return docs


def load_question_bank() -> dict:
    return json.loads(QUESTION_BANK_PATH.read_text(encoding="utf-8"))


def questions_for_day(day: int) -> list[dict]:
    bank = load_question_bank()
    day_label = f"Day {day}" if day not in (11, 12, 13, 14) else (
        "Days 11–12" if day in (11, 12) else "Days 13–14"
    )
    for group in bank["daily_checks"]:
        if group["day"] == day_label:
            return group["questions"]
    return []


def day15_questions() -> list[dict]:
    return load_question_bank()["day15_assessment"]


def plan_for_day(day: int) -> dict | None:
    for entry in INDUCTION_PLAN:
        if entry["day"] == day:
            return entry
    return None
