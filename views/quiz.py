"""views/quiz.py — Moteur du quiz avec design premium."""
import time
import streamlit as st
from utils.quiz_logic  import remaining_seconds, format_timer, is_warning_zone, calculate_score
from utils.database    import save_result

PAGE_SIZE = 10


def render(render_header):
    agent     = st.session_state.agent
    questions = st.session_state.questions
    lang      = agent["langue"]

    # Labels bilingues
    LBL = {
        "progress" : "Questions répondues" if lang=="FR" else "Questions answered",
        "prev"     : "← Précédent"         if lang=="FR" else "← Previous",
        "next"     : "Suivant →"            if lang=="FR" else "Next →",
        "submit"   : "✅ Soumettre mes réponses" if lang=="FR" else "✅ Submit my answers",
        "unanswered": lambda n: f"⚠️ {n} question(s) sans réponse." if lang=="FR"
                                else f"⚠️ {n} question(s) unanswered.",
        "time_up"  : "⏰ Temps écoulé — soumission automatique !" if lang=="FR"
                     else "⏰ Time's up — auto-submitted!",
        "page_lbl" : lambda c,t: f"Page {c} / {t}",
    }

    # Chronomètre
    secs  = remaining_seconds(st.session_state.start_time)
    if secs <= 0 and not st.session_state.submitted:
        _submit(agent, questions, 60*60)
        return

    # ── Header ────────────────────────────────────────────────────────────
    render_header(f"{agent['nom']} · {agent['region']} · {agent['code']}")

    # ── Timer ─────────────────────────────────────────────────────────────
    cls = "timer-warning" if is_warning_zone(secs) else "timer-normal"
    st.markdown(f'<div class="{cls}">⏱ {format_timer(secs)}</div>', unsafe_allow_html=True)

    # ── Progression ───────────────────────────────────────────────────────
    total    = len(questions)
    answered = sum(1 for v in st.session_state.answers.values() if v)
    st.markdown(f'<p class="progress-label">{LBL["progress"]} : {answered} / {total}</p>',
                unsafe_allow_html=True)
    st.progress(answered / total)

    # ── Questions (page courante) ─────────────────────────────────────────
    n_pages  = (total + PAGE_SIZE - 1) // PAGE_SIZE
    page_idx = st.session_state.get("quiz_page", 0)
    start    = page_idx * PAGE_SIZE
    end      = min(start + PAGE_SIZE, total)

    for gi, q in enumerate(questions[start:end], start=start):
        opts    = [f"{k}  —  {q[k]}" for k in ("A","B","C","D")]
        current = st.session_state.answers.get(gi)
        idx     = ("ABCD".index(current)) if current and current in "ABCD" else None

        st.markdown(f"""
        <div class="question-card">
            <div class="question-number">{gi+1}</div>
            <div class="question-text">{q['question']}</div>
        </div>
        """, unsafe_allow_html=True)

        choice = st.radio(
            f"_q{gi}", opts,
            index=idx, key=f"r_{gi}",
            label_visibility="collapsed",
            disabled=st.session_state.submitted,
        )
        if choice:
            st.session_state.answers[gi] = choice[0]

        # Explication après réponse
        if current and st.session_state.submitted:
            ok = (current == q["correct"])
            icon = "✅" if ok else f"❌ (correct : {q['correct']} — {q[q['correct']]})"
            st.markdown(f"""
            <div class="explanation-box">
                <strong>💡 {icon}</strong><br>{q['explication']}
            </div>
            """, unsafe_allow_html=True)

    # ── Navigation ────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if page_idx > 0:
            if st.button(LBL["prev"]):
                st.session_state.quiz_page -= 1
                st.rerun()
    with c2:
        st.markdown(f'<p style="text-align:center;color:#64748b;margin:8px 0;">'
                    f'{LBL["page_lbl"](page_idx+1, n_pages)}</p>', unsafe_allow_html=True)
    with c3:
        if page_idx < n_pages - 1:
            if st.button(LBL["next"]):
                st.session_state.quiz_page += 1
                st.rerun()

    # ── Soumission ────────────────────────────────────────────────────────
    if not st.session_state.submitted:
        st.markdown("---")
        unanswered = total - answered
        if unanswered > 0:
            st.info(LBL["unanswered"](unanswered))
        if st.button(LBL["submit"], use_container_width=True, type="primary"):
            _submit(agent, questions, time.time() - st.session_state.start_time)

    # Rafraîchissement timer
    if not st.session_state.submitted:
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
