"""views/admin.py — Dashboard administrateur INS."""
import io
import streamlit as st
import pandas as pd
from utils.database import load_resultats, load_candidats


def render(render_header):
    render_header("Tableau de bord — INS")

    # ── Auth ─────────────────────────────────────────────────────────────
    if not st.session_state.get("admin_ok"):
        st.markdown("<div class='id-card'>", unsafe_allow_html=True)
        st.markdown("#### 🔐 Accès administrateur")
        pwd = st.text_input("Mot de passe", type="password")
        if st.button("Connexion", type="primary"):
            good = st.secrets.get("admin", {}).get("password", "ins_prolog_2026")
            if pwd == good:
                st.session_state.admin_ok = True
                st.rerun()
            else:
                st.error("❌ Mot de passe incorrect.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ── Données ──────────────────────────────────────────────────────────
    df      = load_resultats()
    n_total = len(load_candidats())

    if df.empty:
        st.info("Aucun résultat enregistré pour l'instant.")
        _logout()
        return

    df["note_20"]   = pd.to_numeric(df["note_20"],   errors="coerce")
    df["pct"]       = pd.to_numeric(df["pct"],       errors="coerce")
    df["duree_min"] = pd.to_numeric(df["duree_min"], errors="coerce")

    n_passes = int((df["pct"] >= 70).sum())

    # ── KPI ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    _kpi(c1, n_total,          "Agents inscrits",   "👥")
    _kpi(c2, len(df),          "Tests complétés",   "✅")
    _kpi(c3, f"{n_passes}/{len(df)}", "Admis (≥70%)", "🏆")
    _kpi(c4, f"{df['note_20'].mean():.1f}/20", "Moyenne", "📊")

    st.markdown("---")

    # ── Filtres ──────────────────────────────────────────────────────────
    regions  = ["Toutes"] + sorted(df["region"].dropna().unique().tolist())
    sel_reg  = st.selectbox("Filtrer par région", regions)
    df_view  = df if sel_reg == "Toutes" else df[df["region"] == sel_reg]

    # ── Tableau ──────────────────────────────────────────────────────────
    st.subheader(f"📋 Résultats — {len(df_view)} agent(s)")
    st.dataframe(
        df_view[["code","nom","region","langue","note_20","pct","duree_min","date"]]
        .rename(columns={"code":"Code","nom":"Nom","region":"Région","langue":"Langue",
                         "note_20":"Note /20","pct":"% Score",
                         "duree_min":"Durée (min)","date":"Date"})
        .sort_values("Note /20", ascending=False).reset_index(drop=True),
        use_container_width=True,
    )

    # ── Graphique ────────────────────────────────────────────────────────
    if len(df_view) > 1:
        st.subheader("📊 Moyenne par région")
        chart = (df_view.groupby("region")["note_20"].mean().round(1)
                 .reset_index().rename(columns={"region":"Région","note_20":"Moyenne /20"})
                 .sort_values("Moyenne /20", ascending=False))
        st.bar_chart(chart.set_index("Région"))

    # ── Export ───────────────────────────────────────────────────────────
    st.subheader("⬇️ Export")
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df_view.to_excel(w, index=False, sheet_name="Résultats")
    st.download_button(
        "📥 Télécharger Excel",
        data=buf.getvalue(),
        file_name="resultats_quiz_prolog.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    _logout()


def _kpi(col, value, label, icon):
    with col:
        st.markdown(f"""
        <div class="admin-kpi">
            <div style="font-size:1.5rem;">{icon}</div>
            <div class="admin-kpi-value">{value}</div>
            <div class="admin-kpi-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)


def _logout():
    st.markdown("---")
    if st.button("🔓 Déconnexion"):
        st.session_state.admin_ok = False
        st.session_state.page     = "accueil"
        st.rerun()
