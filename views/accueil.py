"""views/accueil.py — Page d'accueil avec les 3 feature cards."""
import streamlit as st


def render(render_header):
    render_header("Certification Agent Collecteur")

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    cols = st.columns(3)
    features = [
        ("📋", "100 Questions", "Couvre tous les domaines du guide de l'évaluateur PROLOG."),
        ("🌍", "Bilingue", "Disponible en Français (4 régions) et Anglais (NW & SW)."),
        ("⏱️", "60 Minutes", "Chronomètre intégré. Un seul passage par agent."),
    ]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <span class="feature-icon">{icon}</span>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Commencer l'identification", use_container_width=True, type="primary"):
        st.session_state.page = "auth"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
