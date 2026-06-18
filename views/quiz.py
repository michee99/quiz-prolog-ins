"""views/quiz.py — Une question à la fois avec explication immédiate."""
import time
import streamlit as st
from utils.quiz_logic  import remaining_seconds, format_timer, is_warning_zone, calculate_score
from utils.database    import save_result


def render(render_header):
    agent     = st.session_state.agent
    questions = st.session_state.questions
    lang      = agent["langue"]

    LBL = {
        "submit"  : "✅ Soumettre mes réponses" if lang=="FR" else "✅ Submit my answers",
        "next"    : "Question suivante →"        if lang=="FR" else "Next question →",
        "finish"  : "🏁 Voir mes résultats"      if lang=="FR" else "🏁 View my results",
        "time_up" : "⏰ Temps écoulé !"           if lang=="FR" else "⏰ Time's up!",
        "choose"  : "Choisissez une réponse"     if lang=="FR" else "Choose an answer",
        "correct" : "✅ Bonne réponse !"          if lang=="FR" else "✅ Correct!",
        "wrong"   : "❌ Mauvaise réponse"         if lang=="FR" else "❌ Wrong answer",
        "answer"  : "La bonne réponse était"     if lang=="FR" else "The correct answer was",
        "expl"    : "💡 Explication"              if lang=="FR" else "💡 Explanation",
        "progress": "Question"                   if lang=="FR" else "Question",
    }

    # Chronomètre
    secs = remaining_seconds(st.session_state.start_time)
    if secs <= 0 and not st.session_state.submitted:
        _submit(agent, questions, 60 * 60)
        return

    render_header(f"{agent['nom']} · {agent['region']}")

    # Timer
    cls = "timer-warning" if is_warning_zone(secs) else "timer-normal"
    st.markdown(f'<div class="{cls}">⏱ {format_timer(secs)}</div>',
                unsafe_allow_html=True)

    # Progression
    total   = len(questions)
    current = st.session_state.get("quiz_page", 0)

    st.markdown(
        f'<p class="progress-label">{LBL["progress"]} '
        f'<strong>{current + 1}</strong> / {total}</p>',
        unsafe_allow_html=True,
    )
    st.progress((current + 1) / total)

    # Question courante
    q        = questions[current]
    answered = st.session_state.answers.get(current)

    st.markdown(f"""
    <div class="question-card">
        <div class="question-number">{current + 1}</div>
        <div class="question-text">{q['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Options
    if not answered:
        opts   = [f"{k}  —  {q[k]}" for k in ("A", "B", "C", "D")]
        choice = st.radio(LBL["choose"], opts,
                          index=None, key=f"r_{current}",
                          label_visibility="collapsed")
        if choice:
            st.session_state.answers[current] = choice[0]
            st.rerun()

    # Après réponse : feedback immédiat
    else:
        ok = (answered == q["correct"])

        for letter in ("A", "B", "C", "D"):
            if letter == q["correct"]:
                bg     = "#dcfce7"
                border = "#22c55e"
                icon   = "✅"
            elif letter == answered and not ok:
                bg     = "#fee2e2"
                border = "#ef4444"
                icon   = "❌"
            else:
                bg     = "#f8fafc"
                border = "#cbd5e1"
                icon   = ""

            st.markdown(f"""
            <div style="
                background:{bg}; border:2px solid {border};
                border-radius:14px; padding:1rem 1.4rem;
                margin-bottom:0.5rem; font-size:0.97rem;
                font-weight:500; display:flex; align-items:center; gap:0.8rem;">
                <span style="font-weight:700; min-width:24px;">{letter}</span>
                {q[letter]}
                <span style="margin-left:auto;">{icon}</span>
            </div>
            """, unsafe_allow_html=True)

        # Explication
        if ok:
            st.markdown(f"""
            <div class="explanation-box" style="border-left-color:#22c55e;">
                <strong>{LBL['correct']}</strong><br>
                {LBL['expl']} : {q['explication']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="explanation-box">
                <strong>{LBL['wrong']}</strong> —
                {LBL['answer']} : <strong>{q['correct']} — {q[q['correct']]}</strong><br>
                {LBL['expl']} : {q['explication']}
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # Navigation
        if current < total - 1:
            if st.button(LBL["next"], use_container_width=True, type="primary"):
                st.session_state.quiz_page += 1
                st.rerun()
        else:
            if st.button(LBL["finish"], use_container_width=True, type="primary"):
                _submit(agent, questions,
                        time.time() - st.session_state.start_time)

    # Rafraîchissement timer
    if not answered:
        time.sleep(0.8)
        st.rerun()


def _submit(agent, questions, duree_sec):
    score = calculate_score(questions, st.session_state.answers)
    save_result(agent["code"], agent["nom"], agent["region"], agent["langue"],
                score, len(questions), duree_sec)
    st.session_state.update({
        "submitted": True, "score": score,
        "duree_sec": duree_sec, "page": "resultats",
    })
    st.rerun()