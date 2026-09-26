"""
Day-15 readiness assessment scoring, per §8.3: 20 questions tagged by pillar,
weighted Governance 25% / People 20% / Process 30% / Product 25%, banded
Green (>=80%) / Amber (60-79%) / Red (<60%).
"""
from __future__ import annotations

from modules.data_store import day15_questions

PILLAR_WEIGHTS = {"Governance": 0.25, "People": 0.20, "Process": 0.30, "Product": 0.25}


def score_assessment(answers: dict[str, str]) -> dict:
    """
    answers: {question_id: chosen_option_letter}
    Returns: {
        "pillar_scores": {pillar: pct_correct},
        "overall_pct": float,
        "band": "Green"|"Amber"|"Red",
        "weakest_pillar": str,
        "recommended_action": str,
        "detail": [{"id", "question", "your_answer", "correct_answer", "is_correct", "pillar"}],
    }
    """
    questions = day15_questions()
    by_pillar: dict[str, list[bool]] = {p: [] for p in PILLAR_WEIGHTS}
    detail = []

    for q in questions:
        pillar = q["pillar"]
        chosen = answers.get(q["id"])
        correct = chosen == q["answer"]
        by_pillar.setdefault(pillar, []).append(correct)
        detail.append({
            "id": q["id"], "question": q["question"], "pillar": pillar,
            "your_answer": chosen, "correct_answer": q["answer"],
            "is_correct": correct, "explanation": q["explanation"], "source": q["source"],
        })

    pillar_scores = {
        pillar: (100.0 * sum(results) / len(results) if results else 0.0)
        for pillar, results in by_pillar.items()
    }

    overall = sum(pillar_scores[p] * w for p, w in PILLAR_WEIGHTS.items())

    if overall >= 80:
        band = "Green"
        action = "Proceed to Phase 2 (Days 16-30)."
    elif overall >= 60:
        band = "Amber"
        action = "3-5 day targeted refresh on the weakest pillar before Phase 2."
    else:
        band = "Red"
        action = "Phase 2 paused; remediation plan required with Mentor, Reporting Boss and HR."

    weakest_pillar = min(pillar_scores, key=pillar_scores.get) if pillar_scores else ""

    return {
        "pillar_scores": pillar_scores,
        "overall_pct": round(overall, 1),
        "band": band,
        "weakest_pillar": weakest_pillar,
        "recommended_action": action,
        "detail": detail,
    }


def score_daily_check(questions: list[dict], answers: dict[str, str]) -> dict:
    """Score a 5-question daily knowledge check. 80% (4/5) to pass."""
    total = len(questions)
    correct = sum(1 for q in questions if answers.get(q["id"]) == q["answer"])
    pct = round(100.0 * correct / total, 1) if total else 0.0
    return {"correct": correct, "total": total, "pct": pct, "passed": pct >= 80}
