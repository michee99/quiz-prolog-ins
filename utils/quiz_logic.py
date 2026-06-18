"""
utils/quiz_logic.py
Logique métier du quiz : mélange des questions, calcul du score, timer.
Aucune dépendance à Streamlit → testable isolément.
"""

from __future__ import annotations

import random
import time
import pandas as pd

DUREE_QUIZ_SEC = 60 * 60          # 60 minutes
QUESTIONS_PAR_PAGE = 10
EN_REGIONS = {"Nord-Ouest", "Sud-Ouest"}


# ── Langue ─────────────────────────────────────────────────────────────────

def get_langue(region: str) -> str:
    """Retourne 'EN' pour les régions anglophones, 'FR' sinon."""
    return "EN" if region in EN_REGIONS else "FR"


# ── Chargement & mélange ───────────────────────────────────────────────────

def build_question_list(df_q: pd.DataFrame, langue: str, seed: int | None = None) -> list[dict]:
    """
    Convertit le DataFrame questions en liste de dicts normalisés et mélange.
    seed = hash(code_agent) → ordre reproductible mais unique par agent.
    """
    suf = "_en" if langue == "EN" else "_fr"
    questions = []
    for _, row in df_q.iterrows():
        questions.append({
            "id":         row["id"],
            "question":   row[f"question{suf}"],
            "A":          row[f"A{suf}"],
            "B":          row[f"B{suf}"],
            "C":          row[f"C{suf}"],
            "D":          row[f"D{suf}"],
            "correct":    str(row["correct"]).strip().upper(),
            "explication": row[f"explication{suf}"],
        })
    rng = random.Random(seed)
    rng.shuffle(questions)
    return questions


# ── Timer ──────────────────────────────────────────────────────────────────

def remaining_seconds(start_time: float) -> float:
    """Secondes restantes (≥ 0) depuis start_time (epoch)."""
    return max(0.0, DUREE_QUIZ_SEC - (time.time() - start_time))


def format_timer(seconds: float) -> str:
    """'MM:SS' pour l'affichage dans la barre de progression."""
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


def is_warning_zone(seconds: float) -> bool:
    """True si < 5 minutes restantes."""
    return seconds < 300


# ── Score ──────────────────────────────────────────────────────────────────

def calculate_score(questions: list[dict], answers: dict[int, str]) -> int:
    """
    Nombre de bonnes réponses.
    answers = {question_index: lettre_choisie}
    """
    return sum(
        1 for i, q in enumerate(questions)
        if answers.get(i, "") == q["correct"]
    )


def score_summary(score: int, total: int) -> dict:
    """Retourne un dict avec toutes les métriques utiles."""
    pct    = round(score / total * 100, 1) if total else 0
    note20 = round(score / total * 20,  1) if total else 0
    if pct >= 70:
        mention_key = "mention_pass"
        color       = "#27ae60"
    elif pct >= 50:
        mention_key = "mention_avg"
        color       = "#f39c12"
    else:
        mention_key = "mention_fail"
        color       = "#e74c3c"
    return {
        "score":       score,
        "total":       total,
        "pct":         pct,
        "note_20":     note20,
        "mention_key": mention_key,
        "color":       color,
    }
