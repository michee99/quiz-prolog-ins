"""views/auth.py — Identification de l'agent."""
import time
import streamlit as st
from utils.database   import load_candidats, find_agent, already_passed, load_questions
from utils.quiz_logic import get_langue, build_question_list

REGIONS = ["Adamaoua", "Est", "Extrême-Nord", "Nord", "Nord-Ouest", "Sud-Ouest"]


def render(render_header):
    render_header("Identification de l'agent")

    st.markdown("<div class='id-card'>", unsafe_allow_html=True)
    st.markdown("#### 🔑 Vos informations")

    df_agents = load_candidats()

    with st.form("form_id"):
        region = st.selectbox("Région de déploiement", REGIONS)
        code   = st.text_input("Code commune / région", placeholder="Ex : C001 ou R001",
                               max_chars=10).strip().upper()
        submit = st.form_submit_button("✅ Valider et démarrer", use_container_width=True,
                                       type="primary")

    if submit:
        if not code:
            st.error("⚠️ Veuillez saisir votre code commune.")
        else:
            row = find_agent(code, region, df_agents)
            if row is None:
                st.error("❌ Code introuvable pour cette région. Vérifiez et réessayez.")
            elif already_passed(code):
                st.session_state.update({
                    "page":  "bloque",
                    "agent": {"code": code, "nom": str(row["Nom et Prénom"]).strip(),
                              "region": region},
                })
                st.rerun()
            else:
                nom       = str(row["Nom et Prénom"]).strip()
                langue    = get_langue(region)
                questions = build_question_list(load_questions(), langue, seed=hash(code))
                st.session_state.update({
                    "page":       "quiz",
                    "agent":      {"code": code, "nom": nom, "region": region, "langue": langue},
                    "questions":  questions,
                    "answers":    {},
                    "quiz_page":  0,
                    "start_time": time.time(),
                    "submitted":  False,
                    "score":      None,
                    "duree_sec":  None,
                })
                st.rerun()
    else:
        # Aperçu en temps réel si code déjà saisi
        if code:
            df_agents = load_candidats()
            row = find_agent(code, region, df_agents)
            if row:
                st.success(f"✅ Agent identifié : **{str(row['Nom et Prénom']).strip()}**")

    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("⚠️ Chaque code ne peut être utilisé qu'une seule fois. Le chronomètre démarre immédiatement.")


def render_blocked(render_header):
    render_header("Accès refusé")
    agent = st.session_state.get("agent", {})

    st.markdown(f"""
    <div class="blocked-box">
        <h2 style="color:#991b1b; margin-bottom:1rem;">🚫 Test déjà soumis</h2>
        <p style="font-size:1.05rem; color:#7f1d1d;">
            L'agent <strong>{agent.get('nom','')}</strong>
            (code <code style="background:#fecaca; padding:2px 6px; border-radius:4px;">
            {agent.get('code','')}</code>)
            a déjà passé le quiz.
        </p>
        <p style="color:#991b1b; margin-top:0.8rem; font-size:0.92rem;">
            Contactez l'INS si vous pensez qu'il s'agit d'une erreur.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("← Retour à l'identification"):
        st.session_state.page = "auth"
        st.rerun()
