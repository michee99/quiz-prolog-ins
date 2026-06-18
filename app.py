"""
app.py — Quiz INS PROLOG
Lancement : streamlit run app.py
"""

import streamlit as st

# ── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Quiz PROLOG — Certification Agent Collecteur",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS GLOBAL (design du fichier original) ─────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Fond animé */
.stApp {
    background: linear-gradient(-45deg, #e0e7ff, #c7d2fe, #dbeafe, #bfdbfe);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}
@keyframes gradientBG {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Cache le menu Streamlit et la sidebar */
#MainMenu, footer, [data-testid="stSidebar"] { display: none !important; }

/* ── Header ── */
.header-container {
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 1.5rem 2.5rem;
    margin: 1rem auto 2rem auto;
    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    border: 1px solid rgba(255,255,255,0.2);
    text-align: center;
    position: relative;
    overflow: hidden;
}
.header-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 5px;
    background: linear-gradient(90deg, #16a34a, #facc15, #dc2626);
}
.logo-wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-bottom: 1.2rem;
    gap: 1rem;
}
.logo-placeholder {
    width: 100px; height: 70px;
    background: #f1f5f9;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; color: #94a3b8; font-weight: 600;
    flex-shrink: 0;
}
.connector-text { flex-grow: 1; text-align: center; padding: 0 1rem; }
.connector-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem; font-weight: 700;
    color: #1e3a5f; margin: 0; line-height: 1.2;
}
.connector-desc {
    font-size: 0.8rem; color: #64748b; font-weight: 500;
    margin: 0.2rem 0 0; text-transform: uppercase; letter-spacing: 1px;
}
.header-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem; font-weight: 700;
    color: #1e3a5f; margin: 0.5rem 0; letter-spacing: -0.5px;
}
.header-subtitle { font-size: 0.95rem; color: #64748b; font-weight: 500; margin-top: 0.5rem; }
.lang-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1e40af, #3b82f6);
    color: white; padding: 0.35rem 1.1rem;
    border-radius: 50px; font-size: 0.82rem; font-weight: 600;
    margin-top: 0.8rem; box-shadow: 0 4px 15px rgba(59,130,246,0.4);
}

/* ── Cards ── */
.glass-card {
    background: #ffffff; border-radius: 20px; padding: 2.5rem;
    margin-bottom: 1.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    border: 1px solid #e2e8f0; animation: fadeInUp 0.6s ease-out;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.question-card {
    background: #ffffff; border-radius: 20px; padding: 2rem 2.5rem;
    box-shadow: 0 15px 50px rgba(0,0,0,0.1);
    border: 1px solid #e2e8f0; animation: fadeInUp 0.5s ease-out;
    margin-bottom: 1.2rem;
}
.question-number {
    display: inline-flex; align-items: center; justify-content: center;
    width: 46px; height: 46px;
    background: linear-gradient(135deg, #1e40af, #3b82f6);
    color: white; border-radius: 14px;
    font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;
    box-shadow: 0 6px 18px rgba(59,130,246,0.4);
}
.question-text {
    font-size: 1.15rem; font-weight: 700; color: #0f172a;
    line-height: 1.6; margin-bottom: 1.5rem;
}

/* ── Options (radio Streamlit stylisé) ── */
div[data-testid="stRadio"] > label {
    display: none !important;
}
div[data-testid="stRadio"] > div {
    gap: 0.6rem !important;
}
div[data-testid="stRadio"] > div > label {
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    padding: 1rem 1.4rem !important;
    border: 2px solid #cbd5e1 !important;
    border-radius: 14px !important;
    background: #f8fafc !important;
    cursor: pointer !important;
    transition: all 0.25s !important;
    font-size: 0.97rem !important;
    font-weight: 500 !important;
    color: #1e293b !important;
    margin: 0 !important;
}
div[data-testid="stRadio"] > div > label:hover {
    border-color: #3b82f6 !important;
    background: #eff6ff !important;
    transform: translateX(4px) !important;
    box-shadow: 0 4px 18px rgba(59,130,246,0.15) !important;
}
div[data-testid="stRadio"] > div > label > div:first-child {
    display: none !important;  /* cache le circle radio natif */
}

/* ── Explication ── */
.explanation-box {
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
    border-left: 5px solid #3b82f6;
    padding: 1.3rem 1.5rem; border-radius: 0 16px 16px 0;
    margin-top: 1.2rem; font-size: 0.97rem; color: #1e40af; line-height: 1.7;
    animation: fadeInUp 0.4s ease-out;
}
.explanation-box strong { font-size: 1rem; }

/* ── Boutons ── */
.stButton > button {
    border-radius: 14px !important; padding: 0.85rem 2rem !important;
    font-weight: 700 !important; font-size: 0.97rem !important;
    transition: all 0.3s !important; border: none !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.18) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1e40af, #3b82f6) !important;
    color: white !important;
}

/* ── Barre de progression ── */
.progress-wrap { margin-bottom: 1.5rem; }
.progress-label {
    text-align: center; color: #334155;
    font-size: 0.92rem; font-weight: 600; margin-bottom: 0.6rem;
}
.stProgress > div > div { border-radius: 50px !important; }

/* ── Timer ── */
.timer-normal {
    background: linear-gradient(135deg, #1e40af, #3b82f6);
    color: white; border-radius: 14px; padding: 0.8rem 1.5rem;
    text-align: center; font-size: 1.5rem; font-weight: 800;
    margin-bottom: 1.2rem; box-shadow: 0 6px 20px rgba(59,130,246,0.35);
    letter-spacing: 2px;
}
.timer-warning {
    background: linear-gradient(135deg, #dc2626, #ef4444);
    animation: pulse 1s infinite;
    color: white; border-radius: 14px; padding: 0.8rem 1.5rem;
    text-align: center; font-size: 1.5rem; font-weight: 800;
    margin-bottom: 1.2rem; box-shadow: 0 6px 20px rgba(220,38,38,0.4);
    letter-spacing: 2px;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50%       { transform: scale(1.02); }
}

/* ── Blocage ── */
.blocked-box {
    background: linear-gradient(135deg, #fee2e2, #fef2f2);
    border: 2px solid #ef4444; border-radius: 20px;
    padding: 2.5rem; text-align: center;
    box-shadow: 0 10px 30px rgba(239,68,68,0.15);
}

/* ── Score ── */
.score-circle {
    width: 170px; height: 170px; border-radius: 50%;
    background: linear-gradient(135deg, #1e40af, #3b82f6, #06b6d4);
    color: white; display: flex; align-items: center; justify-content: center;
    font-size: 2.8rem; font-weight: 800;
    margin: 0 auto 1.5rem;
    box-shadow: 0 20px 60px rgba(59,130,246,0.45);
    border: 6px solid rgba(255,255,255,0.3);
    animation: pulse 2s infinite;
}
.score-pct { font-size: 3.2rem; font-weight: 800; color: #0f172a; margin: 0.3rem 0; text-align:center; }
.score-mention {
    font-size: 1.2rem; font-weight: 600;
    padding: 0.8rem 2rem; border-radius: 14px;
    display: inline-block; margin: 0.8rem 0;
}
.score-excellent  { background: linear-gradient(135deg,#dcfce7,#bbf7d0); color:#166534; }
.score-bien       { background: linear-gradient(135deg,#dbeafe,#bfdbfe); color:#1e40af; }
.score-passable   { background: linear-gradient(135deg,#fef9c3,#fde047); color:#854d0e; }
.score-insuffisant{ background: linear-gradient(135deg,#fee2e2,#fecaca); color:#991b1b; }

/* ── Feature cards (page accueil) ── */
.feature-card {
    background: #f8fafc; border-radius: 16px; padding: 1.5rem 1rem;
    text-align: center; border: 1px solid #e2e8f0;
    transition: all 0.3s ease; height: 100%;
}
.feature-card:hover {
    background: #fff; transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}
.feature-icon  { font-size: 2.3rem; margin-bottom: 0.4rem; display: block; }
.feature-title { font-weight: 700; color: #1e3a5f; margin-bottom: 0.25rem; font-size: 0.98rem; }
.feature-desc  { font-size: 0.83rem; color: #64748b; }

/* ── Identification ── */
.id-card {
    background: #ffffff; border-radius: 20px; padding: 2rem 2.5rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    border: 1px solid #e2e8f0; margin-bottom: 1.2rem;
}
.id-card label { font-weight: 600 !important; color: #1e3a5f !important; }

/* ── Recap résultats ── */
.recap-item {
    padding: 0.9rem 1.2rem; border-radius: 12px;
    margin-bottom: 0.5rem; font-size: 0.93rem; transition: all 0.2s;
}
.recap-item:hover { transform: translateX(4px); }
.recap-ok  { background:#f0fdf4; border:1px solid #bbf7d0; color:#166534; }
.recap-ko  { background:#fef2f2; border:1px solid #fecaca; color:#991b1b; }

/* ── Footer ── */
.footer {
    text-align: center; color: #94a3b8; font-size: 0.82rem;
    margin-top: 2.5rem; padding: 1.2rem;
    border-top: 1px solid #e2e8f0;
}

/* ── Admin ── */
.admin-kpi {
    background: #fff; border-radius: 16px; padding: 1.4rem;
    text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid #e2e8f0;
}
.admin-kpi-value { font-size: 2rem; font-weight: 800; color: #1e40af; }
.admin-kpi-label { font-size: 0.82rem; color: #64748b; font-weight: 500; margin-top: 0.2rem; }
</style>
""", unsafe_allow_html=True)

# ── Init session ─────────────────────────────────────────────────────────────
DEFAULTS = {
    "page": "accueil", "agent": None, "questions": None,
    "answers": {}, "quiz_page": 0, "start_time": None,
    "submitted": False, "score": None, "duree_sec": None,
    "admin_ok": False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Admin via query param
if st.query_params.get("page") == "admin":
    st.session_state.page = "admin"

# ── Header commun ─────────────────────────────────────────────────────────────
def render_header(subtitle="Certification Agent Collecteur"):
    lang = (st.session_state.agent or {}).get("langue", "FR")
    badge = "Anglais 🇬🇧" if lang == "EN" else "Français 🇫🇷"
    st.markdown(f"""
    <div class="header-container">
        <div class="logo-wrapper">
            <img src="https://raw.githubusercontent.com/michee99/quiz-prolog-ins/master/assets/logo_ins.png" class="logo-img">
            <div class="connector-text" style="flex:1; text-align:center;">
                <div class="connector-title">Partenariat Stratégique</div>
                <div class="connector-desc">MINDDEVEL · Banque Mondiale</div>
            </div>
            <img src="https://raw.githubusercontent.com/michee99/quiz-prolog-ins/master/assets/logo_prolog.png" class="logo-img">
        </div>
        <h1 class="header-title">Quiz PROLOG</h1>
        <p class="header-subtitle">{subtitle}</p>
        <span class="lang-badge">{badge}</span>
    </div>
    """, unsafe_allow_html=True)

# ── Routeur ──────────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "accueil":
    from views.accueil import render
    render(render_header)

elif page == "auth":
    from views.auth import render
    render(render_header)

elif page == "bloque":
    from views.auth import render_blocked
    render_blocked(render_header)

elif page == "quiz":
    from views.quiz import render
    render(render_header)

elif page == "resultats":
    from views.results import render
    render(render_header)

elif page == "admin":
    from views.admin import render
    render(render_header)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    © 2026 PROLOG — MINDDEVEL &amp; INS Cameroun<br>
    Financement IDA 72130-CM · Banque Mondiale
</div>
""", unsafe_allow_html=True)
