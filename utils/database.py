"""
utils/database.py
Couche d'accès aux données.

Backends :
  - Google Sheets  → si gcp_credentials.json + SHEET_ID dans secrets.toml
  - CSV local      → fallback automatique si Google Sheets indisponible

Seul ce fichier change entre un déploiement local et un déploiement en ligne.
Le reste de l'app (pages/, app.py) ne voit jamais la différence.
"""

from __future__ import annotations

import json
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
from functools import lru_cache

log = logging.getLogger(__name__)

# ── Chemins ────────────────────────────────────────────────────────────────
ROOT          = Path(__file__).resolve().parent.parent
DATA_DIR      = ROOT / "data"
CANDIDATS_XLS = DATA_DIR / "candidats.xlsx"
QUESTIONS_XLS = DATA_DIR / "questions.xlsx"
RESULTATS_CSV = ROOT / "resultats.csv"
CREDS_FILE    = ROOT / "gcp_credentials.json"

_RESULT_COLS = [
    "code", "nom", "region", "langue",
    "score", "total", "pct", "note_20",
    "date", "duree_min",
]

# En-têtes du Google Sheet (ligne 1)
_GS_HEADERS = [
    "Code", "Nom", "Région", "Langue",
    "Score /100", "Total", "% Score", "Note /20",
    "Date", "Durée (min)",
]


# ══════════════════════════════════════════════════════════════════════════════
# CONNEXION GOOGLE SHEETS
# ══════════════════════════════════════════════════════════════════════════════

def _get_sheet():
    """
    Retourne le worksheet Google Sheets "Résultats" ou None si indisponible.
    Mise en cache pour éviter de ré-authentifier à chaque appel.
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        import streamlit as st

        sheet_id = st.secrets.get("google_sheets", {}).get("sheet_id", "")
        if not sheet_id or not CREDS_FILE.exists():
            return None

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds  = Credentials.from_service_account_file(str(CREDS_FILE), scopes=scopes)
        client = gspread.authorize(creds)
        sh     = client.open_by_key(sheet_id)

        # Crée l'onglet "Résultats" s'il n'existe pas
        try:
            ws = sh.worksheet("Résultats")
        except gspread.WorksheetNotFound:
            ws = sh.add_worksheet(title="Résultats", rows=500, cols=len(_GS_HEADERS))
            ws.append_row(_GS_HEADERS)

        return ws

    except Exception as e:
        log.warning(f"Google Sheets indisponible : {e}")
        return None


# ══════════════════════════════════════════════════════════════════════════════
# CANDIDATS & QUESTIONS  (toujours depuis Excel local)
# ══════════════════════════════════════════════════════════════════════════════

@lru_cache(maxsize=1)
def load_candidats() -> pd.DataFrame:
    """Charge la liste officielle des agents depuis candidats.xlsx."""
    df = pd.read_excel(CANDIDATS_XLS, sheet_name="Agents_Candidats", dtype=str)
    df.columns = df.columns.str.strip()
    df["Code Commune"] = df["Code Commune"].str.strip().str.upper()
    df["Région"]       = df["Région"].str.strip()
    return df


@lru_cache(maxsize=1)
def load_questions() -> pd.DataFrame:
    """Charge les 100 questions depuis questions.xlsx."""
    return pd.read_excel(QUESTIONS_XLS, sheet_name="Questions", dtype=str)


def find_agent(code: str, region: str, df: pd.DataFrame) -> pd.Series | None:
    """Retourne la ligne de l'agent ou None si non trouvé."""
    mask = (
        (df["Code Commune"] == code.strip().upper()) &
        (df["Région"].str.lower() == region.strip().lower())
    )
    match = df[mask]
    return match.iloc[0] if not match.empty else None


# ══════════════════════════════════════════════════════════════════════════════
# RÉSULTATS — écriture
# ══════════════════════════════════════════════════════════════════════════════

def save_result(
    code: str, nom: str, region: str, langue: str,
    score: int, total: int, duree_sec: float,
) -> None:
    """
    Persiste le résultat dans Google Sheets ET dans le CSV local (double sécurité).
    """
    pct      = round(score / total * 100, 1)
    note_20  = round(score / total * 20,  1)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    duree    = round(duree_sec / 60, 1)

    # ── 1. Google Sheets ───────────────────────────────────────────────────
    ws = _get_sheet()
    if ws:
        try:
            ws.append_row([
                code.upper(), nom, region, langue,
                score, total, pct, note_20,
                date_str, duree,
            ])
        except Exception as e:
            log.error(f"Erreur écriture Google Sheets : {e}")

    # ── 2. CSV local (fallback + sauvegarde offline) ───────────────────────
    _save_csv(code, nom, region, langue, score, total, pct, note_20, date_str, duree)


def _save_csv(code, nom, region, langue, score, total, pct, note_20, date_str, duree):
    df = _load_csv()
    row = {
        "code": code.upper(), "nom": nom, "region": region, "langue": langue,
        "score": str(score), "total": str(total),
        "pct": str(pct), "note_20": str(note_20),
        "date": date_str, "duree_min": str(duree),
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(RESULTATS_CSV, index=False)


# ══════════════════════════════════════════════════════════════════════════════
# RÉSULTATS — lecture
# ══════════════════════════════════════════════════════════════════════════════

def already_passed(code: str) -> bool:
    """
    True si le code a déjà soumis. Vérifie Google Sheets en priorité,
    sinon le CSV local.
    """
    ws = _get_sheet()
    if ws:
        try:
            codes = ws.col_values(1)[1:]   # colonne A sans l'en-tête
            return code.strip().upper() in [c.strip().upper() for c in codes]
        except Exception:
            pass
    # Fallback CSV
    df = _load_csv()
    return code.strip().upper() in df["code"].str.strip().str.upper().values


def load_resultats() -> pd.DataFrame:
    """
    Retourne tous les résultats pour le dashboard admin.
    Priorité Google Sheets, fallback CSV.
    """
    ws = _get_sheet()
    if ws:
        try:
            data = ws.get_all_records()   # list[dict] avec les en-têtes comme clés
            if data:
                df = pd.DataFrame(data)
                # Renomme les colonnes GS → noms internes
                df = df.rename(columns={
                    "Code":        "code",
                    "Nom":         "nom",
                    "Région":      "region",
                    "Langue":      "langue",
                    "Score /100":  "score",
                    "Total":       "total",
                    "% Score":     "pct",
                    "Note /20":    "note_20",
                    "Date":        "date",
                    "Durée (min)": "duree_min",
                })
                return df
        except Exception as e:
            log.warning(f"Lecture Google Sheets échouée : {e}")

    return _load_csv()


def _load_csv() -> pd.DataFrame:
    if RESULTATS_CSV.exists():
        return pd.read_csv(RESULTATS_CSV, dtype=str)
    return pd.DataFrame(columns=_RESULT_COLS)
