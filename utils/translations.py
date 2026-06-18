"""
utils/translations.py
Toutes les chaînes d'interface, indexées par langue ("FR" | "EN").
Usage :
    from utils.translations import T
    st.write(T("btn_start", lang))
"""

_STRINGS: dict[str, dict[str, str]] = {

    # ── Titres globaux ─────────────────────────────────────────────────────
    "app_title":        {"FR": "Quiz officiel INS — PROLOG",
                         "EN": "Official INS Quiz — PROLOG"},
    "app_subtitle":     {"FR": "Évaluation des agents collecteurs · Juin 2026",
                         "EN": "Data Collectors Evaluation · June 2026"},

    # ── Page auth ─────────────────────────────────────────────────────────
    "auth_heading":     {"FR": "🔑 Identification",
                         "EN": "🔑 Identification"},
    "auth_region":      {"FR": "Région",
                         "EN": "Region"},
    "auth_code":        {"FR": "Code commune / région",
                         "EN": "Municipal / regional code"},
    "auth_code_hint":   {"FR": "Ex : C001 ou R001",
                         "EN": "E.g. C001 or R001"},
    "auth_agent_ok":    {"FR": "✅ Agent identifié : **{nom}**",
                         "EN": "✅ Agent identified: **{nom}**"},
    "auth_code_ko":     {"FR": "⚠️ Code non trouvé pour cette région. Vérifiez et réessayez.",
                         "EN": "⚠️ Code not found for this region. Please check and retry."},
    "auth_no_code":     {"FR": "Veuillez saisir votre code commune.",
                         "EN": "Please enter your municipal code."},
    "auth_no_agent":    {"FR": "Code introuvable. Vérifiez le code et la région sélectionnée.",
                         "EN": "Code not found. Check the code and selected region."},
    "btn_start":        {"FR": "🚀 Démarrer le quiz",
                         "EN": "🚀 Start the quiz"},
    "auth_warning":     {"FR": "⚠️ Chaque code ne peut être utilisé qu'une seule fois. Le chronomètre démarre dès l'entrée dans le quiz.",
                         "EN": "⚠️ Each code can only be used once. The timer starts as soon as the quiz begins."},

    # ── Page bloqué ───────────────────────────────────────────────────────
    "blocked_title":    {"FR": "🚫 Accès refusé",
                         "EN": "🚫 Access denied"},
    "blocked_msg":      {"FR": "L'agent **{nom}** (code `{code}`) a déjà soumis le quiz.",
                         "EN": "Agent **{nom}** (code `{code}`) has already submitted the quiz."},
    "blocked_contact":  {"FR": "Contactez l'INS si vous pensez qu'il s'agit d'une erreur.",
                         "EN": "Contact INS if you believe this is an error."},
    "btn_back":         {"FR": "← Retour à l'identification",
                         "EN": "← Back to identification"},

    # ── Page quiz ─────────────────────────────────────────────────────────
    "quiz_progress":    {"FR": "Questions répondues",
                         "EN": "Questions answered"},
    "quiz_page_label":  {"FR": "Page {current} / {total}",
                         "EN": "Page {current} / {total}"},
    "btn_prev":         {"FR": "← Précédent",
                         "EN": "← Previous"},
    "btn_next":         {"FR": "Suivant →",
                         "EN": "Next →"},
    "btn_submit":       {"FR": "✅ Soumettre mes réponses",
                         "EN": "✅ Submit my answers"},
    "quiz_unanswered":  {"FR": "⚠️ {n} question(s) sans réponse. Vous pouvez tout de même soumettre.",
                         "EN": "⚠️ {n} question(s) unanswered. You may still submit."},
    "quiz_time_up":     {"FR": "⏰ Temps écoulé — soumission automatique !",
                         "EN": "⏰ Time's up — auto-submitted!"},

    # ── Page résultats ────────────────────────────────────────────────────
    "results_title":    {"FR": "📊 Résultats",
                         "EN": "📊 Results"},
    "results_saved":    {"FR": "✅ Résultats enregistrés dans `resultats.csv`.",
                         "EN": "✅ Results saved to `resultats.csv`."},
    "mention_pass":     {"FR": "✅ Admis(e)",
                         "EN": "✅ Passed"},
    "mention_avg":      {"FR": "⚠️ Résultat moyen",
                         "EN": "⚠️ Average result"},
    "mention_fail":     {"FR": "❌ Non admis(e)",
                         "EN": "❌ Not passed"},
    "results_raw":      {"FR": "Score brut",
                         "EN": "Raw score"},
    "results_duration": {"FR": "Durée (min)",
                         "EN": "Duration (min)"},
    "results_detail":   {"FR": "📋 Voir le détail des réponses",
                         "EN": "📋 View answer details"},
    "your_answer":      {"FR": "Votre réponse",
                         "EN": "Your answer"},
    "correct_answer":   {"FR": "Bonne réponse",
                         "EN": "Correct answer"},

    # ── Admin ─────────────────────────────────────────────────────────────
    "admin_title":      {"FR": "🛡️ Tableau de bord — INS",
                         "EN": "🛡️ Dashboard — INS"},
    "admin_pwd_prompt": {"FR": "Mot de passe administrateur",
                         "EN": "Admin password"},
    "admin_pwd_wrong":  {"FR": "❌ Mot de passe incorrect.",
                         "EN": "❌ Wrong password."},
    "admin_no_results": {"FR": "Aucun résultat enregistré pour l'instant.",
                         "EN": "No results recorded yet."},
}


def T(key: str, lang: str = "FR", **kwargs) -> str:
    """
    Retourne la chaîne traduite pour `key` dans `lang`.
    Les kwargs sont passés à str.format() si la chaîne contient des placeholders.
    """
    row = _STRINGS.get(key, {})
    text = row.get(lang, row.get("FR", f"[{key}]"))
    if kwargs:
        text = text.format(**kwargs)
    return text
