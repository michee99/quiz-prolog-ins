"""views/results.py — Page résultats avec score animé."""
import streamlit as st
from datetime import datetime
from utils.quiz_logic import score_summary


def render(render_header):
    agent     = st.session_state.agent
    questions = st.session_state.questions
    answers   = st.session_state.answers
    score     = st.session_state.score
    duree_sec = st.session_state.duree_sec or 0
    lang      = agent["langue"]
    total     = len(questions)

    s         = score_summary(score, total)
    duree_min = round(duree_sec / 60, 1)

    # Mention
    MENTIONS = {
        "mention_pass": ("score-excellent", "✅ Admis(e)"      if lang=="FR" else "✅ Passed"),
        "mention_avg":  ("score-passable",  "⚠️ Résultat moyen" if lang=="FR" else "⚠️ Average"),
        "mention_fail": ("score-insuffisant","❌ Non admis(e)"  if lang=="FR" else "❌ Not passed"),
    }
    css_cls, mention_txt = MENTIONS[s["mention_key"]]

    render_header("Résultats du quiz" if lang=="FR" else "Quiz Results")

    # ── Score circle ──────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <div class="score-circle">{score}/{total}</div>
        <div class="score-pct">{s['pct']}%</div>
        <div style="font-size:1.1rem; color:#64748b; margin:0.3rem 0;">
            {"Note" if lang=="FR" else "Grade"} : <strong>{s['note_20']} / 20</strong>
        </div>
        <span class="score-mention {css_cls}">{mention_txt}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI ligne ─────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    c1.metric("Score brut" if lang=="FR" else "Raw score", f"{score}/{total}")
    c2.metric("Note /20",  f"{s['note_20']}")
    c3.metric("Durée (min)" if lang=="FR" else "Duration (min)", f"{duree_min}")

    # ── Détail ────────────────────────────────────────────────────────────
    label = "📊 Voir le détail" if lang=="FR" else "📊 View details"
    with st.expander(label):
        for i, q in enumerate(questions):
            user = answers.get(i, "—")
            ok   = (user == q["correct"])
            css  = "recap-ok" if ok else "recap-ko"
            icon = "✅" if ok else "❌"
            user_txt  = f"{user} — {q.get(user,'—')}" if user in "ABCD" else "—"
            corr_txt  = f"{q['correct']} — {q[q['correct']]}"
            wrong_html = (
                f'<br><span>{"Bonne réponse" if lang=="FR" else "Correct"} : '
                f'<strong>{corr_txt}</strong></span>'
            ) if not ok else ""

            st.markdown(f"""
            <div class="recap-item {css}">
                <strong>{icon} Q{i+1}.</strong> {q['question']}<br>
                {"Votre réponse" if lang=="FR" else "Your answer"} :
                <strong>{user_txt}</strong>{wrong_html}<br>
                <em style="font-size:.83rem; opacity:.8;">{q['explication']}</em>
            </div>
            """, unsafe_allow_html=True)

    st.success("✅ Résultats enregistrés." if lang=="FR" else "✅ Results saved.")
    st.caption(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
