import os
import json
import time
from datetime import datetime, date, timedelta
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from users_manager import (
    load_couple_data,
    save_couple_data,
    log_user_session,
    log_user_evaluation,
    update_user_name,
    get_current_phase_for_user,
    calculate_streak,
    DEFAULT_PROFILES
)
from ai_coach import evaluate_with_ai, PRACTICE_PROMPTS

# Configuración de página
st.set_page_config(
    page_title="English Accelerator • Pareja",
    page_icon="🇬🇧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para una interfaz moderna, limpia y romántica/profesional
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
        padding: 1.8rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.2);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .user-badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .praise-box {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 5px solid #10b981;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        color: #065f46;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Cargar datos
data = load_couple_data()
users = data.get("users", {})

# Sidebar: Selector de Usuario y Navegación
with st.sidebar:
    st.markdown("### 👥 ¿Quién está practicando?")
    
    user_keys = list(users.keys())
    user_labels = {
        k: f"{users[k].get('emoji', '👤')} {users[k].get('display_name', k)}"
        for k in user_keys
    }
    
    # Mantener selección en estado de sesión
    if "current_user_id" not in st.session_state:
        st.session_state["current_user_id"] = "anderson"
        
    selected_uid = st.selectbox(
        "Seleccionar Perfil:",
        options=user_keys,
        format_func=lambda k: user_labels[k],
        index=user_keys.index(st.session_state["current_user_id"]) if st.session_state["current_user_id"] in user_keys else 0
    )
    st.session_state["current_user_id"] = selected_uid
    
    curr_user = users[selected_uid]
    
    st.markdown("---")
    st.caption(f"**Enfoque de {curr_user.get('display_name')}:**")
    st.info(f"🎯 **{curr_user.get('role_title')}**\n\nMeta: {curr_user.get('target_hours'):.0f} h | Nivel: {curr_user.get('cefr_target')}")
    
    st.markdown("---")
    menu = st.radio(
        "Menú Principal",
        [
            "💑 Resumen de Pareja",
            "⏱️ Cronómetro & Estudio",
            "🤖 Evaluador Gemini IA",
            "📚 Biblioteca de Temas",
            "⚙️ Configuración"
        ]
    )
    
    st.markdown("---")
    # Racha activa
    streak = calculate_streak(curr_user.get("sessions", []))
    st.metric(f"Racha de {curr_user.get('display_name')}", f"{streak} días 🔥")

# ==============================================================================
# PANTALLA 1: RESUMEN DE PAREJA (COUPLE DASHBOARD)
# ==============================================================================
if menu == "💑 Resumen de Pareja":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size: 2.2rem;">💑 English Together: Anderson & Tania</h1>
        <p style="margin-top:0.4rem; opacity:0.9; font-size: 1.1rem;">
            Acompañándose paso a paso para dominar el inglés, cada uno a su propio ritmo.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    u_anderson = users.get("anderson", {})
    u_novia = users.get("novia", {})
    
    total_couple_hours = u_anderson.get("total_hours", 0.0) + u_novia.get("total_hours", 0.0)
    streak_anderson = calculate_streak(u_anderson.get("sessions", []))
    streak_novia = calculate_streak(u_novia.get("sessions", []))
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("⏳ Horas Totales en Pareja", f"{total_couple_hours:.1f} h")
    with c2:
        st.metric(f"🔥 Racha de {u_anderson.get('display_name')}", f"{streak_anderson} días")
    with c3:
        st.metric(f"✨ Racha de {u_novia.get('display_name')}", f"{streak_novia} días")
        
    st.markdown("### 📊 Progreso Individual")
    col_a, col_b = st.columns(2)
    
    # Tarjeta Anderson
    with col_a:
        st.subheader(f"{u_anderson.get('emoji')} {u_anderson.get('display_name')}")
        st.caption(f"**Ruta:** {u_anderson.get('role_title')}")
        h_and = u_anderson.get("total_hours", 0.0)
        target_and = u_anderson.get("target_hours", 700.0)
        pct_and = min(100.0, (h_and / target_and) * 100.0) if target_and > 0 else 0
        st.progress(pct_and / 100.0)
        st.write(f"**{h_and:.1f}** / {target_and:.0f} horas ({pct_and:.1f}%)")
        
        phase_and = get_current_phase_for_user(u_anderson)
        st.info(f"📍 **{phase_and.get('name')}**\n\n_{phase_and.get('focus')}_")
        
    # Tarjeta Novia
    with col_b:
        st.subheader(f"{u_novia.get('emoji')} {u_novia.get('display_name')}")
        st.caption(f"**Ruta:** {u_novia.get('role_title')}")
        h_nov = u_novia.get("total_hours", 0.0)
        target_nov = u_novia.get("target_hours", 200.0)
        pct_nov = min(100.0, (h_nov / target_nov) * 100.0) if target_nov > 0 else 0
        st.progress(pct_nov / 100.0)
        st.write(f"**{h_nov:.1f}** / {target_nov:.0f} horas ({pct_nov:.1f}%)")
        
        phase_nov = get_current_phase_for_user(u_novia)
        st.success(f"📍 **{phase_nov.get('name')}**\n\n_{phase_nov.get('focus')}_")

    st.markdown("---")
    st.markdown("### 📈 Actividad de los últimos 7 días")
    
    # Preparar datos últimos 7 días
    today = date.today()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    
    def get_mins_per_day(sessions, days):
        counts = {d: 0 for d in days}
        for s in sessions:
            ts = s.get("timestamp", "")
            if ts:
                try:
                    d = datetime.fromisoformat(ts).date()
                    if d in counts:
                        counts[d] += s.get("minutes", 0)
                except Exception:
                    pass
        return counts

    and_counts = get_mins_per_day(u_anderson.get("sessions", []), last_7_days)
    nov_counts = get_mins_per_day(u_novia.get("sessions", []), last_7_days)
    
    chart_data = pd.DataFrame({
        "Fecha": [d.strftime("%a %d") for d in last_7_days] * 2,
        "Minutos": [and_counts[d] for d in last_7_days] + [nov_counts[d] for d in last_7_days],
        "Estudiante": [u_anderson.get("display_name")] * 7 + [u_novia.get("display_name")] * 7
    })
    
    fig = px.bar(
        chart_data,
        x="Fecha",
        y="Minutos",
        color="Estudiante",
        barmode="group",
        color_discrete_map={
            u_anderson.get("display_name"): "#4f46e5",
            u_novia.get("display_name"): "#ec4899"
        }
    )
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# PANTALLA 2: CRONÓMETRO Y ESTUDIO
# ==============================================================================
elif menu == "⏱️ Cronómetro & Estudio":
    st.title(f"⏱️ Espacio de Estudio: {curr_user.get('display_name')}")
    st.caption("Usa el cronómetro interactivo o registra manualmente los minutos estudiados en el día.")
    
    tab_timer, tab_manual = st.tabs(["⏳ Cronómetro de Práctica", "📝 Registro Manual Rápido"])
    
    with tab_timer:
        c1, c2 = st.columns([1, 2])
        with c1:
            categories = curr_user.get("categories", ["General"])
            cat_choice = st.selectbox("Categoría de Práctica", categories)
            desc = st.text_input("¿Qué vas a practicar hoy?", placeholder="Ej. Escuchar podcast, ver un video, practicar con IA")
            mins_selected = st.select_slider("Duración del Bloque (minutos)", options=[5, 10, 15, 20, 25, 30, 45, 60, 90], value=25)
            
            # Control de Timer con Streamlit Session State
            if "timer_running" not in st.session_state:
                st.session_state["timer_running"] = False
                st.session_state["timer_start"] = 0
                st.session_state["timer_total"] = 0
            
            start_btn = st.button("▶️ Iniciar Sesión", use_container_width=True, type="primary")
            if start_btn:
                st.session_state["timer_running"] = True
                st.session_state["timer_start"] = time.time()
                st.session_state["timer_total"] = mins_selected * 60
                st.session_state["timer_cat"] = cat_choice
                st.session_state["timer_desc"] = desc
                st.session_state["timer_mins"] = mins_selected
                st.rerun()

        with c2:
            if st.session_state.get("timer_running", False):
                elapsed = time.time() - st.session_state["timer_start"]
                total = st.session_state["timer_total"]
                remaining = max(0, total - elapsed)
                
                rem_m, rem_s = divmod(int(remaining), 60)
                elap_m, elap_s = divmod(int(elapsed), 60)
                
                pct = min(1.0, elapsed / total) if total > 0 else 1.0
                
                st.subheader(f"En sesión: {st.session_state.get('timer_desc', 'Estudio')}")
                st.markdown(f"### ⏳ Restante: `{rem_m:02d}:{rem_s:02d}` | Transcurrido: `{elap_m:02d}:{elap_s:02d}`")
                st.progress(pct)
                
                c_stop, c_finish = st.columns(2)
                with c_stop:
                    if st.button("⏹️ Terminar y Guardar Tiempo Real", use_container_width=True):
                        actual_mins = max(1, int(round(elapsed / 60.0)))
                        log_user_session(
                            selected_uid,
                            actual_mins,
                            st.session_state.get("timer_cat", "General"),
                            st.session_state.get("timer_desc", "Estudio con cronómetro")
                        )
                        st.session_state["timer_running"] = False
                        st.success(f"¡Genial! Guardaste {actual_mins} minutos en tu historial.")
                        time.sleep(1.5)
                        st.rerun()
                with c_finish:
                    if st.button("❌ Cancelar sin Guardar", use_container_width=True):
                        st.session_state["timer_running"] = False
                        st.rerun()
            else:
                st.info("💡 **Consejo:** 20 a 25 minutos de práctica diaria enfocada (Shadowing, escuchar videos o escribir) tienen más impacto que estudiar muchas horas un solo día.")
                
    with tab_manual:
        st.subheader("Registro Manual de Minutos")
        st.write("Si practicaste fuera de la app (en el celular, viendo una película en inglés, en Duolingo o leyendo un libro):")
        
        with st.form("manual_entry_form"):
            man_mins = st.number_input("Minutos dedicados:", min_value=1, max_value=360, value=20)
            man_cat = st.selectbox("Categoría:", curr_user.get("categories", ["General"]))
            man_desc = st.text_input("Descripción:", placeholder="Ej. 20 min video de YouTube en inglés con subtítulos en inglés")
            man_notes = st.text_area("Notas o palabras nuevas aprendidas (opcional):", placeholder="Palabras o frases que llamaron tu atención")
            
            submit_manual = st.form_submit_button("✅ Guardar en mi Progreso", use_container_width=True)
            if submit_manual:
                log_user_session(selected_uid, man_mins, man_cat, man_desc, man_notes)
                st.success(f"¡Registrados {man_mins} minutos exitosamente para {curr_user.get('display_name')}!")
                time.sleep(1)
                st.rerun()

    # Historial de sesiones recientes
    st.markdown("---")
    st.subheader(f"📜 Historial de {curr_user.get('display_name')}")
    sessions = curr_user.get("sessions", [])
    if sessions:
        rows = []
        for s in reversed(sessions[-10:]):
            rows.append({
                "Fecha": s.get("timestamp", "")[:16].replace("T", " "),
                "Minutos": s.get("minutes", 0),
                "Categoría": s.get("category", "General"),
                "Descripción": s.get("description", ""),
                "Notas": s.get("notes", "")
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.write("Aún no tienes sesiones registradas. ¡Inicia tu primera sesión hoy!")

# ==============================================================================
# PANTALLA 3: EVALUADOR GEMINI IA
# ==============================================================================
elif menu == "🤖 Evaluador Gemini IA":
    st.title("🤖 Entrenador Inteligente con Gemini")
    
    is_academic = curr_user.get("tone") == "academic"
    
    if is_academic:
        st.caption(f"Evaluador oficial riguroso para **{curr_user.get('display_name')}** (Estándar IELTS Academic, vocabulario STEM y estructura formal para posgrado).")
    else:
        st.caption(f"Tutora personal cálida y didáctica para **{curr_user.get('display_name')}** (Enfoque en vida cotidiana, fluidez real, trabajo y pronunciación).")

    # Selección de tema sugerido
    col_t1, col_t2 = st.columns([1, 1])
    with col_t1:
        task_type = st.radio("Tipo de Práctica:", ["Writing (Texto escrito)", "Speaking (Transcripción de voz / Diálogo)"], horizontal=True)
    with col_t2:
        user_prompts = PRACTICE_PROMPTS.get(selected_uid, PRACTICE_PROMPTS["novia"])
        prompt_titles = ["-- Escribir libremente sin tema sugerido --"] + [p["title"] for p in user_prompts]
        chosen_prompt_title = st.selectbox("💡 ¿Quieres un tema sugerido?", prompt_titles)

    active_prompt_desc = ""
    if chosen_prompt_title != "-- Escribir libremente sin tema sugerido --":
        for p in user_prompts:
            if p["title"] == chosen_prompt_title:
                active_prompt_desc = p["prompt"]
                st.info(f"**Tema:** {active_prompt_desc}")
                break

    # Área de texto
    user_text = st.text_area(
        "Pega o escribe tu texto en inglés:",
        height=180,
        placeholder="Type or paste your English text here..."
    )
    
    evaluate_btn = st.button("🚀 Evaluar con IA", type="primary", use_container_width=True)
    
    if evaluate_btn:
        if not user_text.strip():
            st.warning("Por favor escribe o pega algo en inglés antes de evaluar.")
        else:
            with st.spinner("Gemini está leyendo y analizando detalladamente tu texto..."):
                try:
                    result = evaluate_with_ai(
                        curr_user,
                        "writing" if "Writing" in task_type else "speaking",
                        user_text
                    )
                    
                    # Guardar evaluación
                    log_user_evaluation(selected_uid, "writing" if "Writing" in task_type else "speaking", user_text, result)
                    
                    st.success("¡Evaluación completada!")
                    st.markdown("---")
                    
                    # RENDER SEGÚN EL PERFIL
                    if result.get("mode") == "academic":
                        # Vista Académica para Anderson
                        band = result.get("overall_band", 0.0)
                        cefr = result.get("cefr_level", "B2")
                        
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Banda IELTS Estimada", f"{band} / 9.0")
                        m2.metric("Nivel CEFR", cefr)
                        m3.metric("Task Response", result.get("task_response", 0.0))
                        m4.metric("Grammar Range", result.get("grammatical_accuracy", 0.0))
                        
                        col_scores1, col_scores2 = st.columns(2)
                        with col_scores1:
                            st.write(f"• **Coherencia y Cohesión:** {result.get('coherence_cohesion', 0.0)} / 9.0")
                            st.write(f"• **Recurso Léxico:** {result.get('lexical_resource', 0.0)} / 9.0")
                        with col_scores2:
                            prec = result.get('accuracy_percentage', 0)
                            st.write(f"• **Precisión General:** {prec}%")
                            
                        # Errores críticos
                        errors = result.get("critical_grammar_errors", [])
                        if errors:
                            st.markdown("#### ❌ Errores Gramaticales Críticos:")
                            for err in errors:
                                st.error(f"**Original:** `{err.get('error')}` ➔ **Corrección:** `{err.get('fix')}`\n\n_{err.get('rule')}_")
                                
                        # Vocabulario
                        acad_vocab = result.get("academic_vocab_used", [])
                        if acad_vocab:
                            st.markdown("#### 📚 Vocabulario Académico Detectado:")
                            st.success(", ".join(acad_vocab))
                            
                        # Upgrades
                        upgrades = result.get("weak_phrases_to_upgrade", [])
                        if upgrades:
                            st.markdown("#### 💡 Upgrades a Nivel C1:")
                            for u in upgrades:
                                st.write(f"• `{u.get('original')}` ➔ **{u.get('c1_alternative')}**")
                                
                        # Reescritura C1
                        st.markdown("#### 📝 Reescritura C1 para Publicación / Paper:")
                        st.code(result.get("c1_rewrite", ""), language="text")
                        
                        st.info(f"🎯 **Siguiente acción recomendada:** {result.get('next_action_item', 'Seguir practicando')}")

                    else:
                        # Vista Conversacional y Empática para la Novia
                        score = result.get("overall_score", 8.0)
                        cefr = result.get("cefr_level", "B1")
                        praise = result.get("praise", "¡Excelente trabajo!")
                        
                        st.markdown(f"""
                        <div class="praise-box">
                            <h3 style="margin:0 0 0.5rem 0;">🌟 ¡Qué bien lo hiciste!</h3>
                            <p style="font-size:1.1rem; margin:0;">{praise}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        c_s1, c_s2, c_s3, c_s4 = st.columns(4)
                        c_s1.metric("Puntuación General", f"{score} / 10 ⭐")
                        c_s2.metric("Nivel Estimado", cefr)
                        c_s3.metric("Fluidez", f"{result.get('fluency_score', 8)} / 10")
                        c_s4.metric("Vocabulario", f"{result.get('vocabulary_score', 8)} / 10")
                        
                        # Correcciones amigables
                        corrections = result.get("grammar_corrections", [])
                        if corrections:
                            st.markdown("### 🔍 Cositas para corregir (fáciles de recordar):")
                            for c in corrections:
                                st.warning(f"**Dijiste:** *\"{c.get('original')}\"*\n\n👉 **La forma correcta es:** **\"{c.get('correction')}\"**\n\n💡 **¿Por qué?:** {c.get('explanation_es')}")
                        else:
                            st.success("🎉 ¡No tuviste ningún error gramatical grave! Tu mensaje se entiende perfectamente.")

                        # Cómo lo diría un nativo
                        naturals = result.get("natural_alternatives", [])
                        if naturals:
                            st.markdown("### ✨ Cómo lo diría un hablante nativo (más natural):")
                            for n in naturals:
                                st.info(f"**Tu frase:** *\"{n.get('original')}\"*\n\n🔥 **Suena más natural:** **\"{n.get('more_natural')}\"**\n\n📌 **Contexto:** {n.get('context', '')}")

                        # Frases útiles para guardar
                        phrases = result.get("useful_phrases_to_learn", [])
                        if phrases:
                            st.markdown("### 💬 Frases útiles para tu día a día:")
                            for p in phrases:
                                st.markdown(f"• **{p.get('phrase')}** ➔ *{p.get('meaning')}* (Ejemplo: *\"{p.get('example')}\"*)")

                        # Versión reescrita
                        st.markdown("### 📖 Así de lindo y natural se lee tu texto completo:")
                        st.success(result.get("natural_rewrite", ""))

                        # Reto
                        challenge = result.get("challenge_for_next_time", "")
                        if challenge:
                            st.markdown(f"""
                            <div style="background:#fef3c7; border-left: 5px solid #f59e0b; padding:1rem; border-radius:8px; color:#92400e;">
                                <strong>🎯 Tu mini-reto para la próxima:</strong> {challenge}
                            </div>
                            """, unsafe_allow_html=True)
                            
                except Exception as ex:
                    st.error(f"Error durante la evaluación: {ex}")

# ==============================================================================
# PANTALLA 4: BIBLIOTECA DE TEMAS
# ==============================================================================
elif menu == "📚 Biblioteca de Temas":
    st.title("📚 Biblioteca de Práctica & Vocabulario")
    
    st.write(f"Temas recomendados según el perfil activo: **{curr_user.get('display_name')}** ({curr_user.get('role_title')})")
    
    user_prompts = PRACTICE_PROMPTS.get(selected_uid, PRACTICE_PROMPTS["novia"])
    
    for i, p in enumerate(user_prompts, 1):
        with st.expander(f"{i}. {p.get('title')}", expanded=(i == 1)):
            st.markdown(f"**Consigna:**\n\n> {p.get('prompt')}")
            st.caption("Copia esta consigna y ve a la pestaña '🤖 Evaluador Gemini IA' para responderla.")

# ==============================================================================
# PANTALLA 5: CONFIGURACIÓN
# ==============================================================================
elif menu == "⚙️ Configuración":
    st.title("⚙️ Configuración & Compartir la Web")
    
    st.markdown("### 👤 Personalizar Nombres y Metas")
    
    with st.form("settings_form"):
        st.write("Puedes personalizar los nombres y metas de estudio:")
        name_anderson = st.text_input("Nombre de Anderson:", value=users.get("anderson", {}).get("display_name", "Anderson"))
        name_novia = st.text_input("Nombre de Tania:", value=users.get("novia", {}).get("display_name", "Tania"))
        
        target_and = st.number_input("Meta de horas de Anderson:", min_value=10.0, max_value=2000.0, value=float(users.get("anderson", {}).get("target_hours", 700.0)), step=50.0)
        target_nov = st.number_input("Meta de horas de Tania:", min_value=10.0, max_value=1000.0, value=float(users.get("novia", {}).get("target_hours", 200.0)), step=25.0)
        
        save_btn = st.form_submit_button("💾 Guardar Cambios")
        if save_btn:
            data["users"]["anderson"]["display_name"] = name_anderson.strip()
            data["users"]["anderson"]["target_hours"] = target_and
            
            data["users"]["novia"]["display_name"] = name_novia.strip()
            data["users"]["novia"]["target_hours"] = target_nov
            
            save_couple_data(data)
            st.success("¡Configuración guardada exitosamente!")
            time.sleep(1)
            st.rerun()

    st.markdown("---")
    st.markdown("### 🌐 ¿Cómo compartirla con Tania para usarla en el celular?")
    st.write("""
    Para que Tania pueda abrirla desde su celular en cualquier momento, el proceso es 100% gratis y se hace en 3 pasos:
    
    1. **Subir este proyecto a un repositorio privado de GitHub** (puedes crear una cuenta gratis en github.com).
    2. **Entrar a [share.streamlit.io](https://share.streamlit.io/)** e iniciar sesión con tu cuenta de GitHub.
    3. **Dar clic en 'New App'**, seleccionar este repositorio, poner `app.py` como archivo principal y en **Advanced Settings / Secrets** agregar tu clave de Gemini:
       ```toml
       GEMINI_API_KEY = "tu_clave_de_gemini"
       ```
    ¡Y listo! Te dará un enlace web (ejemplo: `https://ingles-pareja.streamlit.app`) que le puedes mandar por WhatsApp a ella para que lo abra desde su celular y lo guarde en su pantalla de inicio como una app.
    """)
