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
    authenticate_user,
    register_guest,
    update_user_profile,
    change_user_password,
    admin_delete_user,
    log_user_session,
    log_user_evaluation,
    get_current_phase_for_user,
    calculate_streak,
    AVAILABLE_TRACKS,
    toggle_lesson_completion,
    get_user_completed_lessons,
    get_user_security_question,
    reset_password_with_recovery,
    recover_username,
    update_user_security
)
from ai_coach import (
    evaluate_with_ai,
    evaluate_speaking_audio,
    get_prompts_for_user,
    generate_ai_prompt_for_interests
)
from curriculum_data import CURRICULUM

# Configuración de página
st.set_page_config(
    page_title="English Accelerator • Anderson, Tania & Friends",
    page_icon="🇬🇧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS
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
    .user-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-admin { background: #fee2e2; color: #991b1b; }
    .badge-partner { background: #fce7f3; color: #9d174d; }
    .badge-guest { background: #e0e7ff; color: #3730a3; }
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

# Inicializar sesión de autenticación
if "auth_user_id" not in st.session_state:
    st.session_state["auth_user_id"] = None

data = load_couple_data()
users = data.get("users", {})

# ==============================================================================
# PANTALLA DE LOGIN / REGISTRO SI NO ESTÁ AUTENTICADO
# ==============================================================================
if not st.session_state["auth_user_id"] or st.session_state["auth_user_id"] not in users:
    c_left, c_center, c_right = st.columns([1, 2, 1])
    with c_center:
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; margin-bottom: 1.5rem;">
            <h1 style="font-size: 2.5rem; margin-bottom: 0.2rem;">🇬🇧 English Accelerator</h1>
            <p style="color: #9ca3af; font-size: 1.1rem;">Plataforma de estudio para Anderson, Tania y Amigos</p>
        </div>
        """, unsafe_allow_html=True)

        announcement = data.get("system_config", {}).get("announcement")
        if announcement:
            st.info(f"📢 **Aviso:** {announcement}")

        tab_login, tab_register, tab_recover = st.tabs(["🔑 Iniciar Sesión", "📝 Registrarse como Invitado", "🆘 Recuperar Cuenta"])

        # TAB LOGIN
        with tab_login:
            st.subheader("Acceso a tu Espacio")
            with st.form("login_form"):
                uname = st.text_input("Usuario:", placeholder="ej. anderson, tania o tu_usuario")
                pword = st.text_input("Contraseña:", type="password")
                submit_login = st.form_submit_button("Entrar a la Plataforma", use_container_width=True, type="primary")

                if submit_login:
                    auth_u = authenticate_user(uname, pword)
                    if auth_u:
                        st.session_state["auth_user_id"] = auth_u["id"]
                        st.success(f"¡Bienvenido/a de nuevo, {auth_u.get('display_name')}!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos. Por favor verifica o ve a la pestaña '🆘 Recuperar Cuenta'.")

            st.caption("💡 **Cuentas principales:** Anderson y Tania tienen sus cuentas de acceso preconfiguradas.")

        # TAB REGISTER
        with tab_register:
            st.subheader("Crear Cuenta de Invitado / Amigo")
            st.write("Crea tu cuenta para practicar con el cronómetro, recibir correcciones de Gemini IA y guardar tu progreso.")
            
            with st.form("register_form"):
                reg_name = st.text_input("Tu Nombre:", placeholder="Ej. Carlos, Andrea, etc.")
                reg_uname = st.text_input("Nombre de Usuario (para iniciar sesión):", placeholder="ej. carlos24")
                reg_pword = st.text_input("Contraseña:", type="password")
                reg_pword_confirm = st.text_input("Confirmar Contraseña:", type="password")
                
                reg_track = st.selectbox(
                    "¿Cuál es tu enfoque principal de inglés?",
                    options=list(AVAILABLE_TRACKS.keys()),
                    format_func=lambda k: f"{AVAILABLE_TRACKS[k]['title']}"
                )
                
                reg_target = st.number_input("Meta de horas totales de práctica:", min_value=10.0, max_value=1000.0, value=100.0, step=25.0)
                
                st.write("**🛡️ Seguridad para recuperar tu cuenta si olvidas la contraseña:**")
                reg_sec_q = st.selectbox(
                    "Elige tu Pregunta Secreta de Recuperación:",
                    options=[
                        "¿Cuál es tu comida o postre favorito?",
                        "¿Cómo se llamaba tu primera mascota?",
                        "¿En qué ciudad te gustaría vivir?",
                        "¿Cuál es tu película o libro favorito?",
                        "¿Nombre de tu mejor amigo de la infancia?"
                    ]
                )
                reg_sec_a = st.text_input("Respuesta secreta a tu pregunta:", placeholder="Ej. pizza, toby, paris")
                reg_pin = st.text_input("PIN secreto de 4 números (opcional):", placeholder="Ej. 1234", max_chars=6)

                st.write("**Selecciona tus temas de interés (para que la IA te dé temas que te gusten):**")
                all_interests = ["Viajes & Turismo", "Cine & Series", "Trabajo & Negocios", "Música & Cultura", "Tecnología & Programación", "Gastronomía", "Deportes & Fitness", "Ciencia"]
                selected_interests = []
                cols_int = st.columns(2)
                for idx, interest in enumerate(all_interests):
                    col = cols_int[idx % 2]
                    if col.checkbox(interest, value=(idx < 3), key=f"reg_int_{idx}"):
                        selected_interests.append(interest)
                
                submit_reg = st.form_submit_button("Crear Mi Cuenta", use_container_width=True)
                if submit_reg:
                    if reg_pword != reg_pword_confirm:
                        st.error("Las contraseñas no coinciden.")
                    elif not reg_sec_a.strip():
                        st.error("Por favor escribe una respuesta secreta para poder recuperar tu cuenta en el futuro.")
                    else:
                        ok, msg = register_guest(
                            reg_uname,
                            reg_pword,
                            reg_name,
                            reg_track,
                            reg_target,
                            selected_interests,
                            reg_sec_q,
                            reg_sec_a,
                            reg_pin
                        )
                        if ok:
                            st.success(msg)
                            time.sleep(1.5)
                            # Auto-login
                            new_u = authenticate_user(reg_uname, reg_pword)
                            if new_u:
                                st.session_state["auth_user_id"] = new_u["id"]
                                st.rerun()
                        else:
                            st.error(msg)

        # TAB RECUPERACIÓN
        with tab_recover:
            st.subheader("🆘 Recuperación de Usuario o Contraseña")
            recover_mode = st.radio("¿Qué necesitas recuperar?", ["🔑 Olvidé mi Contraseña", "👤 Olvidé mi Usuario"], horizontal=True)

            if recover_mode == "🔑 Olvidé mi Contraseña":
                st.write("Escribe tu nombre de usuario para buscar tu pregunta de seguridad:")
                rec_username_input = st.text_input("Nombre de Usuario:", key="rec_uname_in", placeholder="ej. anderson, tania o tu_usuario")

                if rec_username_input.strip():
                    found, question_text, target_uname = get_user_security_question(rec_username_input)
                    if found:
                        st.info(f"❓ **Pregunta de Seguridad:** {question_text}")
                        with st.form("reset_pwd_form"):
                            rec_answer = st.text_input("Tu Respuesta Secreta o tu PIN de 4 números:", type="password")
                            rec_new_pwd = st.text_input("Nueva Contraseña:", type="password")
                            rec_new_pwd_c = st.text_input("Confirmar Nueva Contraseña:", type="password")
                            submit_reset = st.form_submit_button("Restablecer Contraseña", use_container_width=True, type="primary")

                            if submit_reset:
                                if rec_new_pwd != rec_new_pwd_c:
                                    st.error("Las nuevas contraseñas no coinciden.")
                                else:
                                    ok, msg = reset_password_with_recovery(target_uname, rec_answer, rec_new_pwd)
                                    if ok:
                                        st.success(msg)
                                        time.sleep(1.5)
                                        st.rerun()
                                    else:
                                        st.error(msg)
                    else:
                        st.warning("No encontramos ese usuario. Verifica cómo lo escribiste o usa la opción 'Olvidé mi Usuario'.")

            else: # Olvidé mi Usuario
                st.write("Si no recuerdas tu nombre de usuario, escribe tu nombre visible y tu respuesta secreta:")
                with st.form("recover_user_form"):
                    rec_disp_name = st.text_input("Tu Nombre Visible (ej. Carlos, Tania, Anderson):")
                    rec_user_ans = st.text_input("Tu Respuesta Secreta o PIN de recuperación:", type="password")
                    submit_rec_user = st.form_submit_button("Recordar mi Usuario", use_container_width=True)

                    if submit_rec_user:
                        ok, msg = recover_username(rec_disp_name, rec_user_ans)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)
    st.stop()

# ==============================================================================
# USUARIO AUTENTICADO
# ==============================================================================
curr_user = users[st.session_state["auth_user_id"]]
role = curr_user.get("role", "guest")
is_admin = (role == "admin")
is_partner = (role == "partner")
is_couple = is_admin or is_partner

# Sidebar
with st.sidebar:
    st.markdown(f"### {curr_user.get('emoji', '👤')} {curr_user.get('display_name')}")
    if is_admin:
        st.markdown('<span class="user-pill badge-admin">👑 Administrador (Anderson)</span>', unsafe_allow_html=True)
    elif is_partner:
        st.markdown('<span class="user-pill badge-partner">💖 Co-administradora (Tania)</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="user-pill badge-guest">🌟 Invitado / Amigo</span>', unsafe_allow_html=True)

    st.caption(f"**Enfoque:** {curr_user.get('role_title', 'General')}")
    st.caption(f"🎯 Meta: {curr_user.get('total_hours', 0.0):.1f} / {curr_user.get('target_hours', 100):.0f} h")
    st.markdown("---")

    # Opciones de menú según el rol
    menu_options = []
    if is_couple:
        menu_options.append("💑 Resumen de Pareja (Anderson & Tania)")
    else:
        menu_options.append("📊 Mi Progreso Personal")

    menu_options.extend([
        "🎓 Clases por Niveles (A1 ➔ C1)",
        "⏱️ Mi Estudio & Cronómetro",
        "🤖 Evaluador Gemini IA",
        "📚 Biblioteca de Temas",
        "👤 Mi Perfil & Gustos"
    ])

    if is_admin:
        menu_options.append("🛠️ Panel de Administración")

    menu = st.radio("Navegación:", menu_options)

    st.markdown("---")
    streak = calculate_streak(curr_user.get("sessions", []))
    st.metric("Tu Racha Actual", f"{streak} días 🔥")

    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state["auth_user_id"] = None
        st.rerun()

# ==============================================================================
# PANTALLA 1A: RESUMEN DE PAREJA (SOLO ANDERSON Y TANIA)
# ==============================================================================
if menu == "💑 Resumen de Pareja (Anderson & Tania)":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size: 2.2rem;">💑 English Together: Anderson & Tania</h1>
        <p style="margin-top:0.4rem; opacity:0.9; font-size: 1.1rem;">
            Espacio privado para avanzar juntos, medir sus horas y celebrar cada logro.
        </p>
    </div>
    """, unsafe_allow_html=True)

    u_and = users.get("anderson", {})
    u_tan = users.get("tania", {})

    total_couple_hours = u_and.get("total_hours", 0.0) + u_tan.get("total_hours", 0.0)
    streak_and = calculate_streak(u_and.get("sessions", []))
    streak_tan = calculate_streak(u_tan.get("sessions", []))

    c1, c2, c3 = st.columns(3)
    c1.metric("⏳ Horas Totales en Pareja", f"{total_couple_hours:.1f} h")
    c2.metric(f"🔬 Racha de {u_and.get('display_name', 'Anderson')}", f"{streak_and} días 🔥")
    c3.metric(f"✨ Racha de {u_tan.get('display_name', 'Tania')}", f"{streak_tan} días 🔥")

    st.markdown("### 📊 Progreso de Ambos")
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader(f"{u_and.get('emoji', '🔬')} {u_and.get('display_name')}")
        st.caption(f"**Ruta:** {u_and.get('role_title')}")
        h_and = u_and.get("total_hours", 0.0)
        t_and = u_and.get("target_hours", 700.0)
        pct_and = min(100.0, (h_and / t_and) * 100.0) if t_and > 0 else 0
        st.progress(pct_and / 100.0)
        st.write(f"**{h_and:.1f}** / {t_and:.0f} horas ({pct_and:.1f}%)")
        ph_and = get_current_phase_for_user(u_and)
        st.info(f"📍 **{ph_and.get('name')}**\n\n_{ph_and.get('focus')}_")

    with col_b:
        st.subheader(f"{u_tan.get('emoji', '✨')} {u_tan.get('display_name')}")
        st.caption(f"**Ruta:** {u_tan.get('role_title')}")
        h_tan = u_tan.get("total_hours", 0.0)
        t_tan = u_tan.get("target_hours", 200.0)
        pct_tan = min(100.0, (h_tan / t_tan) * 100.0) if t_tan > 0 else 0
        st.progress(pct_tan / 100.0)
        st.write(f"**{h_tan:.1f}** / {t_tan:.0f} horas ({pct_tan:.1f}%)")
        ph_tan = get_current_phase_for_user(u_tan)
        st.success(f"📍 **{ph_tan.get('name')}**\n\n_{ph_tan.get('focus')}_")

    # Gráfico 7 días
    st.markdown("---")
    st.markdown("### 📈 Actividad Comparativa de los Últimos 7 Días")
    today = date.today()
    last_7 = [today - timedelta(days=i) for i in range(6, -1, -1)]

    def get_mins(sessions, days):
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

    and_c = get_mins(u_and.get("sessions", []), last_7)
    tan_c = get_mins(u_tan.get("sessions", []), last_7)

    df_chart = pd.DataFrame({
        "Fecha": [d.strftime("%a %d") for d in last_7] * 2,
        "Minutos": [and_c[d] for d in last_7] + [tan_c[d] for d in last_7],
        "Estudiante": [u_and.get("display_name")] * 7 + [u_tan.get("display_name")] * 7
    })

    fig = px.bar(
        df_chart,
        x="Fecha",
        y="Minutos",
        color="Estudiante",
        barmode="group",
        color_discrete_map={
            u_and.get("display_name"): "#4f46e5",
            u_tan.get("display_name"): "#ec4899"
        }
    )
    fig.update_layout(height=340, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# PANTALLA 1B: TABLERO DE PROGRESO PERSONAL (PARA INVITADOS)
# ==============================================================================
elif menu == "📊 Mi Progreso Personal":
    st.title(f"📊 Mi Progreso: {curr_user.get('display_name')}")
    st.caption(f"Enfoque: **{curr_user.get('role_title')}**")

    c1, c2, c3 = st.columns(3)
    c1.metric("Horas Acumuladas", f"{curr_user.get('total_hours', 0.0):.1f} h")
    c2.metric("Meta Total", f"{curr_user.get('target_hours', 100):.0f} h")
    c3.metric("Racha de Práctica", f"{calculate_streak(curr_user.get('sessions', []))} días 🔥")

    h = curr_user.get("total_hours", 0.0)
    tgt = curr_user.get("target_hours", 100.0)
    pct = min(100.0, (h / tgt) * 100.0) if tgt > 0 else 0
    st.markdown(f"**Progreso hacia tu meta:** {pct:.1f}%")
    st.progress(pct / 100.0)

    ph = get_current_phase_for_user(curr_user)
    st.info(f"📍 **{ph.get('name')}**\n\n{ph.get('focus')}")

# ==============================================================================
# PANTALLA: CLASES POR NIVELES (A1 ➔ C1)
# ==============================================================================
elif menu == "🎓 Clases por Niveles (A1 ➔ C1)":
    st.title("🎓 Academia de Clases por Niveles (CEFR)")
    st.caption("Plan de estudio estructurado paso a paso con teoría explicada en español, fórmulas, ejemplos de la vida real, quizzes interactivos y retos calificados con Inteligencia Artificial.")

    lvl_keys = list(CURRICULUM.keys())
    lvl_labels = {k: CURRICULUM[k]["title"] for k in lvl_keys}

    selected_lvl_key = st.selectbox(
        "📚 Selecciona el Nivel que deseas estudiar:",
        options=lvl_keys,
        format_func=lambda k: lvl_labels[k]
    )

    lvl_info = CURRICULUM[selected_lvl_key]
    lessons = lvl_info["lessons"]

    completed_lessons = get_user_completed_lessons(curr_user["id"])
    completed_in_lvl = sum(1 for l in lessons if l["id"] in completed_lessons)
    total_in_lvl = len(lessons)
    pct_lvl = (completed_in_lvl / total_in_lvl) * 100.0 if total_in_lvl > 0 else 0

    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.04); border-left: 5px solid {lvl_info.get('badge_color', '#4f46e5')}; padding: 1rem 1.2rem; border-radius: 8px; margin: 1rem 0;">
        <h3 style="margin:0 0 0.3rem 0;">{lvl_info['title']}</h3>
        <p style="margin:0; opacity:0.85;">{lvl_info['description']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.write(f"**Progreso en este Nivel:** {completed_in_lvl} de {total_in_lvl} clases completadas ({pct_lvl:.0f}%)")
    st.progress(pct_lvl / 100.0)
    st.markdown("---")

    for i, lesson in enumerate(lessons, 1):
        is_done = lesson["id"] in completed_lessons
        icon = "✅" if is_done else "📖"
        exp_title = f"{icon} Clase {lesson['id']}: {lesson['title']} • [{lesson['sublevel']}]"

        with st.expander(exp_title, expanded=(i == 1 and not is_done)):
            col_h1, col_h2 = st.columns([3, 1.2])
            with col_h1:
                st.markdown(f"**🎯 Objetivo de la clase:** {lesson['objective']}")
            with col_h2:
                btn_txt = "✅ Completada (desmarcar)" if is_done else "🔘 Marcar como Aprendida"
                if st.button(btn_txt, key=f"mark_btn_{lesson['id']}", use_container_width=True):
                    new_st = toggle_lesson_completion(curr_user["id"], lesson["id"])
                    if new_st:
                        log_user_session(curr_user["id"], 15, "Clases & Gramática", f"Completó la clase {lesson['id']}: {lesson['title']}")
                        st.success(f"¡Felicitaciones! Has completado la clase {lesson['id']} y sumaste 15 min de estudio.")
                    else:
                        st.info(f"Clase {lesson['id']} desmarcada.")
                    time.sleep(0.8)
                    st.rerun()

            st.markdown("#### 📘 Explicación en Español:")
            st.markdown(lesson["explanation_es"])

            if lesson.get("formula"):
                st.markdown("**💡 Estructura / Fórmula Clave:**")
                st.code(lesson["formula"], language="text")

            st.markdown("#### 🗣️ Ejemplos de la Vida Real:")
            for eg in lesson["examples"]:
                st.markdown(f"• 🇬🇧 **{eg['en']}**\n  \n  🇪🇸 _{eg['es']}_")

            mst = lesson.get("common_mistake")
            if mst:
                st.markdown("#### ⚠️ Error Típico a Evitar:")
                st.warning(f"❌ **Incorrecto:** `{mst['wrong']}`\n\n✅ **Correcto:** `{mst['right']}`\n\n📌 **¿Por qué?:** {mst['why']}")

            qz = lesson.get("quiz")
            if qz:
                st.markdown("#### 🧠 Comprobación Rápida (Mini-Quiz):")
                st.write(f"**{qz['question']}**")
                u_pick = st.radio("Selecciona la opción correcta:", qz["options"], key=f"qz_opt_{lesson['id']}")
                if st.button("Verificar Respuesta", key=f"qz_btn_{lesson['id']}"):
                    p_idx = qz["options"].index(u_pick)
                    if p_idx == qz["answer_idx"]:
                        st.success(f"🎉 ¡Excelente! {qz['feedback']}")
                    else:
                        correct_ans = qz["options"][qz["answer_idx"]]
                        st.error(f"¡Casi! La respuesta correcta es: **\"{correct_ans}\"**.\n\n{qz['feedback']}")

            ch = lesson.get("practice_challenge")
            if ch:
                st.markdown("---")
                st.markdown("#### 📝 Reto de Práctica:")
                st.info(f"👉 **Consigna:** {ch}")

                user_txt = st.text_area("Escribe tu respuesta en inglés para que Gemini la revise:", key=f"ch_txt_{lesson['id']}", height=90)
                if st.button("🚀 Evaluar mi Ejercicio con Gemini IA", key=f"ch_btn_{lesson['id']}", type="primary"):
                    if not user_txt.strip():
                        st.warning("Por favor escribe tu respuesta antes de evaluar.")
                    else:
                        with st.spinner("Gemini está evaluando tu ejercicio de esta clase..."):
                            e_res = evaluate_with_ai(curr_user, "writing", user_txt)
                            log_user_evaluation(curr_user["id"], f"Clase {lesson['id']}", user_txt, e_res)
                            st.success("¡Ejercicio evaluado!")
                            
                            if e_res.get("mode") == "academic":
                                st.write(f"• **Banda IELTS:** {e_res.get('overall_band', 0.0)} / 9.0 | **Nivel:** {e_res.get('cefr_level')}")
                                st.code(e_res.get("c1_rewrite", ""))
                            else:
                                st.write(f"• **Puntuación:** {e_res.get('overall_score', 8)} / 10 ⭐ | **Nivel:** {e_res.get('cefr_level')}")
                                st.info(f"🌟 **Feedback:** {e_res.get('praise', '¡Buen trabajo!')}")
                                for cr in e_res.get("grammar_corrections", []):
                                    st.warning(f"👉 `{cr.get('original')}` ➔ **{cr.get('correction')}** ({cr.get('explanation_es')})")
                                st.success(f"📖 **Versión natural:** {e_res.get('natural_rewrite')}")

# ==============================================================================
# PANTALLA 2: MI ESTUDIO & CRONÓMETRO
# ==============================================================================
elif menu == "⏱️ Mi Estudio & Cronómetro":
    st.title(f"⏱️ Espacio de Estudio: {curr_user.get('display_name')}")
    tab_timer, tab_manual = st.tabs(["⏳ Cronómetro Interactivo", "📝 Registro Manual Rápido"])

    with tab_timer:
        c1, c2 = st.columns([1, 2])
        with c1:
            cats = curr_user.get("categories", ["Práctica General"])
            cat_choice = st.selectbox("Categoría:", cats)
            desc = st.text_input("¿Qué vas a practicar?", placeholder="Ej. Escuchar podcast, ver video, escribir")
            dur = st.select_slider("Duración (minutos):", options=[5, 10, 15, 20, 25, 30, 45, 60], value=25)

            if "timer_active" not in st.session_state:
                st.session_state["timer_active"] = False

            if st.button("▶️ Iniciar Cronómetro", type="primary", use_container_width=True):
                st.session_state["timer_active"] = True
                st.session_state["timer_start_t"] = time.time()
                st.session_state["timer_total_s"] = dur * 60
                st.session_state["timer_cat"] = cat_choice
                st.session_state["timer_desc"] = desc
                st.rerun()

        with c2:
            if st.session_state.get("timer_active"):
                elapsed = time.time() - st.session_state["timer_start_t"]
                total = st.session_state["timer_total_s"]
                rem = max(0, total - elapsed)
                rm, rs = divmod(int(rem), 60)
                em, es = divmod(int(elapsed), 60)
                st.subheader(f"En sesión: {st.session_state.get('timer_desc', 'Estudio')}")
                st.markdown(f"### ⏳ Restante: `{rm:02d}:{rs:02d}` | Transcurrido: `{em:02d}:{es:02d}`")
                st.progress(min(1.0, elapsed / total) if total > 0 else 1.0)

                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("⏹️ Terminar y Guardar", use_container_width=True):
                        actual_m = max(1, int(round(elapsed / 60.0)))
                        log_user_session(
                            curr_user["id"],
                            actual_m,
                            st.session_state.get("timer_cat", "General"),
                            st.session_state.get("timer_desc", "Estudio con cronómetro")
                        )
                        st.session_state["timer_active"] = False
                        st.success(f"¡Registrados {actual_m} minutos en tu historial!")
                        time.sleep(1.2)
                        st.rerun()
                with col_btn2:
                    if st.button("❌ Cancelar", use_container_width=True):
                        st.session_state["timer_active"] = False
                        st.rerun()
            else:
                st.info("💡 **Consejo de consistencia:** Una sesión de 20 minutos todos los días produce mejores resultados que estudiar muchas horas una sola vez por semana.")

    with tab_manual:
        st.subheader("Registrar Minutos Estudiados")
        with st.form("manual_log"):
            man_m = st.number_input("Minutos dedicados:", min_value=1, max_value=360, value=25)
            man_c = st.selectbox("Categoría:", curr_user.get("categories", ["General"]))
            man_d = st.text_input("Descripción:", placeholder="Ej. Duolingo en el bus, lectura de artículo en inglés")
            man_n = st.text_area("Notas o vocabulario nuevo (opcional):")
            
            sub_m = st.form_submit_button("Guardar en mi Historial", use_container_width=True)
            if sub_m:
                log_user_session(curr_user["id"], man_m, man_c, man_d, man_n)
                st.success(f"¡{man_m} minutos guardados!")
                time.sleep(1)
                st.rerun()

    st.markdown("---")
    st.subheader("📜 Tus Últimas Sesiones")
    sess = curr_user.get("sessions", [])
    if sess:
        df_s = pd.DataFrame([{
            "Fecha": s.get("timestamp", "")[:16].replace("T", " "),
            "Minutos": s.get("minutes", 0),
            "Categoría": s.get("category", ""),
            "Descripción": s.get("description", ""),
            "Notas": s.get("notes", "")
        } for s in reversed(sess[-8:])])
        st.dataframe(df_s, use_container_width=True)
    else:
        st.write("Aún no tienes sesiones registradas.")

# ==============================================================================
# PANTALLA 3: EVALUADOR GEMINI IA
# ==============================================================================
elif menu == "🤖 Evaluador Gemini IA":
    st.title("🤖 Entrenador Inteligente con Gemini IA")
    st.caption(f"Adaptado a: **{curr_user.get('display_name')}** ({curr_user.get('role_title')})")

    # Botón mágico para generar tema con IA basado en sus intereses
    col_ia1, col_ia2 = st.columns([1, 1])
    with col_ia1:
        if st.button("🪄 Generar Tema Sorpresa con IA según mis Gustos", use_container_width=True):
            with st.spinner("Gemini está creando una consigna personalizada para ti..."):
                gen_p = generate_ai_prompt_for_interests(curr_user)
                st.session_state["active_prompt_title"] = gen_p.get("title")
                st.session_state["active_prompt_text"] = gen_p.get("prompt")
                st.session_state["active_prompt_tip"] = gen_p.get("tip_es")

    with col_ia2:
        user_prompts = get_prompts_for_user(curr_user)
        p_titles = ["-- Escribir libremente --"] + [p["title"] for p in user_prompts]
        selected_p_title = st.selectbox("O elige un tema sugerido:", p_titles)
        if selected_p_title != "-- Escribir libremente --":
            for p in user_prompts:
                if p["title"] == selected_p_title:
                    st.session_state["active_prompt_title"] = p["title"]
                    st.session_state["active_prompt_text"] = p["prompt"]
                    st.session_state["active_prompt_tip"] = ""

    if st.session_state.get("active_prompt_text"):
        st.info(f"**Tema:** {st.session_state.get('active_prompt_title')}\n\n> {st.session_state.get('active_prompt_text')}\n\n_{st.session_state.get('active_prompt_tip', '')}_")

    input_method = st.radio(
        "Elige cómo deseas practicar:",
        ["🎙️ Grabar con Micrófono en Vivo (Speaking)", "📝 Escribir Texto (Writing)", "⌨️ Pegar Transcripción de Audio"],
        horizontal=True
    )

    # 1. CASO MICRÓFONO EN VIVO
    if input_method == "🎙️ Grabar con Micrófono en Vivo (Speaking)":
        st.write("🎙️ **Graba tu voz hablando en inglés** (puedes responder al tema sugerido de arriba o hablar libremente de 15 a 60 segundos):")
        audio_recorded = st.audio_input("Presiona el botón rojo para comenzar a hablar:")

        if audio_recorded is not None:
            st.audio(audio_recorded)
            if st.button("🚀 Evaluar mi Pronunciación y Speaking con Gemini IA", type="primary", use_container_width=True):
                with st.spinner("Gemini está escuchando tu audio, analizando tu pronunciación, ritmo y fluidez..."):
                    try:
                        audio_bytes = audio_recorded.read()
                        res_audio = evaluate_speaking_audio(curr_user, audio_bytes)
                        log_user_evaluation(curr_user["id"], "speaking_audio", res_audio.get("transcript", "Audio en vivo"), res_audio)
                        st.success("¡Análisis de Speaking completado!")
                        st.markdown("---")

                        # Transcripción detectada
                        st.markdown("### 🎙️ Lo que Gemini escuchó en tu audio:")
                        st.info(f"🗣️ *\"{res_audio.get('transcript', 'No se detectó voz clara')}\"*")

                        mode = res_audio.get("mode", "conversational_speaking")
                        if mode == "academic_speaking":
                            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                            col_m1.metric("Banda IELTS Speaking", f"{res_audio.get('overall_band', 6.5)} / 9.0")
                            col_m2.metric("Pronunciación (PR)", f"{res_audio.get('pronunciation_score', 6.0)} / 9.0")
                            col_m3.metric("Fluidez (FC)", f"{res_audio.get('fluency_score', 6.5)} / 9.0")
                            col_m4.metric("Nivel CEFR", res_audio.get("cefr_level", "B2"))

                            p_tips = res_audio.get("pronunciation_feedback", [])
                            if p_tips:
                                st.markdown("#### 🗣️ Feedback de Pronunciación & Fonética:")
                                for pt in p_tips:
                                    st.warning(f"• **Palabra:** `{pt.get('word')}` | **Sonó:** `{pt.get('detected_sound')}` ➔ **Fonética correcta:** `{pt.get('correct_phonetics')}`\n\n📌 **Tip:** {pt.get('tip')}")

                            st.markdown("#### 📝 Reescritura Oral C1 (Fluidez Formal):")
                            st.code(res_audio.get("c1_rewrite", ""), language="text")
                            st.info(f"🎯 **Siguiente recomendación:** {res_audio.get('next_action_item', 'Seguir practicando')}")

                        else:
                            st.markdown(f"""
                            <div class="praise-box">
                                <h3 style="margin:0 0 0.4rem 0;">🌟 ¡Qué gran valentía al hablar!</h3>
                                <p style="font-size:1.05rem; margin:0;">{res_audio.get('praise', '¡Se nota tu entusiasmo!')}</p>
                            </div>
                            """, unsafe_allow_html=True)

                            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                            col_s1.metric("Calificación Global", f"{res_audio.get('overall_score', 8.5)} / 10 ⭐")
                            col_s2.metric("Pronunciación", f"{res_audio.get('pronunciation_score', 8)} / 10 🗣️")
                            col_s3.metric("Fluidez y Ritmo", f"{res_audio.get('fluency_score', 8.5)} / 10 🌊")
                            col_s4.metric("Nivel Detectado", res_audio.get("cefr_level", "B1"))

                            # Tips de pronunciación amigables
                            tips = res_audio.get("pronunciation_tips", [])
                            if tips:
                                st.markdown("### 🗣️ Cómo pronunciar palabras clave (guía fonética en español):")
                                for t in tips:
                                    st.info(f"• **Palabra:** **\"{t.get('word')}\"**\n\n👉 **Así se pronuncia fácil:** **`/{t.get('how_to_pronounce_es')}/`**\n\n💡 **Consejo:** {t.get('explanation')}")

                            corrs = res_audio.get("grammar_oral_corrections", [])
                            if corrs:
                                st.markdown("### 🔍 Ajustes gramaticales al hablar:")
                                for c in corrs:
                                    st.warning(f"**Dijiste:** *\"{c.get('original')}\"* ➔ 👉 **La forma correcta es:** **\"{c.get('correction')}\"** ({c.get('explanation_es')})")

                            st.markdown("### 📖 Así sonaría tu mensaje si lo dijera un nativo de forma fluida:")
                            st.success(res_audio.get("natural_rewrite", ""))

                            ch = res_audio.get("challenge_for_next_time", "")
                            if ch:
                                st.markdown(f"""
                                <div style="background:#fef3c7; border-left: 5px solid #f59e0b; padding:1rem; border-radius:8px; color:#92400e;">
                                    <strong>🎯 Tu mini-reto para el próximo audio:</strong> {ch}
                                </div>
                                """, unsafe_allow_html=True)

                    except Exception as ex:
                        st.error(f"Error al analizar el audio: {ex}")
        else:
            st.info("👆 Haz clic en el botón rojo de arriba para grabar tu audio desde tu celular o computadora.")

    # 2. CASO TEXTO O TRANSCRIPCIÓN ESCRITA
    else:
        user_input_text = st.text_area("Tu texto en inglés:", height=170, placeholder="Escribe o pega aquí tu texto en inglés...")

        if st.button("🚀 Evaluar Texto con Gemini IA", type="primary", use_container_width=True):
            if not user_input_text.strip():
                st.warning("Por favor escribe algo en inglés para evaluar.")
            else:
                with st.spinner("Gemini está analizando detalladamente tu texto..."):
                    res = evaluate_with_ai(
                        curr_user,
                        "writing" if "Writing" in input_method else "speaking",
                        user_input_text
                    )
                    log_user_evaluation(curr_user["id"], "writing" if "Writing" in input_method else "speaking", user_input_text, res)
                    st.success("¡Evaluación completada!")
                    st.markdown("---")

                    mode = res.get("mode", "conversational")
                    if mode == "academic":
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Banda IELTS Estimada", f"{res.get('overall_band', 0.0)} / 9.0")
                        m2.metric("Nivel CEFR", res.get("cefr_level", "B2"))
                        m3.metric("Task Response", res.get("task_response", 0.0))
                        m4.metric("Gramática", res.get("grammatical_accuracy", 0.0))

                        errs = res.get("critical_grammar_errors", [])
                        if errs:
                            st.markdown("#### ❌ Errores Gramaticales:")
                            for e in errs:
                                st.error(f"**`{e.get('error')}`** ➔ **`{e.get('fix')}`**\n\n_{e.get('rule')}_")

                        st.markdown("#### 📝 Reescritura C1 Académica:")
                        st.code(res.get("c1_rewrite", ""), language="text")
                    else:
                        st.markdown(f"""
                        <div class="praise-box">
                            <h3 style="margin:0 0 0.4rem 0;">🌟 ¡Excelente esfuerzo!</h3>
                            <p style="font-size:1.05rem; margin:0;">{res.get('praise', '¡Muy bien hecho!')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        c_s1, c_s2, c_s3, c_s4 = st.columns(4)
                        c_s1.metric("Puntuación General", f"{res.get('overall_score', 8)} / 10 ⭐")
                        c_s2.metric("Nivel Estimado", res.get("cefr_level", "B1"))
                        c_s3.metric("Fluidez", f"{res.get('fluency_score', 8)} / 10")
                        c_s4.metric("Vocabulario", f"{res.get('vocabulary_score', 8)} / 10")

                        corrs = res.get("grammar_corrections", [])
                        if corrs:
                            st.markdown("### 🔍 Cositas para corregir (fáciles de recordar):")
                            for c in corrs:
                                st.warning(f"**Dijiste:** *\"{c.get('original')}\"*\n\n👉 **Forma correcta:** **\"{c.get('correction')}\"**\n\n💡 **¿Por qué?:** {c.get('explanation_es')}")

                        nats = res.get("natural_alternatives", [])
                        if nats:
                            st.markdown("### ✨ Cómo lo diría un nativo:")
                            for n in nats:
                                st.info(f"**Original:** *\"{n.get('original')}\"* ➔ 🔥 **Más natural:** **\"{n.get('more_natural')}\"** ({n.get('context', '')})")

                        st.markdown("### 📖 Versión reescrita recomendada:")
                        st.success(res.get("natural_rewrite", ""))

                        ch = res.get("challenge_for_next_time", "")
                        if ch:
                            st.info(f"🎯 **Tu mini-reto:** {ch}")

# ==============================================================================
# PANTALLA 4: BIBLIOTECA DE TEMAS
# ==============================================================================
elif menu == "📚 Biblioteca de Temas":
    st.title("📚 Biblioteca de Práctica Personalizada")
    st.write(f"Consignas sugeridas basadas en tu enfoque: **{curr_user.get('role_title')}**")

    user_prompts = get_prompts_for_user(curr_user)
    for idx, p in enumerate(user_prompts, 1):
        with st.expander(f"{idx}. {p.get('title')}", expanded=(idx == 1)):
            st.markdown(f"**Consigna:**\n\n> {p.get('prompt')}")
            st.caption("Copia la consigna y ve a la pestaña '🤖 Evaluador Gemini IA' para responderla.")

# ==============================================================================
# PANTALLA 5: MI PERFIL & GUSTOS
# ==============================================================================
elif menu == "👤 Mi Perfil & Gustos":
    st.title(f"👤 Mi Perfil: {curr_user.get('display_name')}")
    st.caption("Personaliza tus gustos, tu enfoque de aprendizaje y tu contraseña.")

    with st.form("profile_form"):
        p_name = st.text_input("Tu Nombre Visible:", value=curr_user.get("display_name", ""))
        p_emoji = st.text_input("Tu Emoji / Avatar:", value=curr_user.get("emoji", "👤"))

        p_track = st.selectbox(
            "Tu Enfoque de Estudio:",
            options=list(AVAILABLE_TRACKS.keys()),
            index=list(AVAILABLE_TRACKS.keys()).index(curr_user.get("track", "conversational")) if curr_user.get("track") in AVAILABLE_TRACKS else 0,
            format_func=lambda k: f"{AVAILABLE_TRACKS[k]['title']}"
        )

        p_target = st.number_input("Tu Meta de Horas Totales:", min_value=10.0, max_value=2000.0, value=float(curr_user.get("target_hours", 100.0)), step=25.0)

        st.write("**Tus Temas de Interés (La IA usará esto para proponerte ejercicios):**")
        all_possible = ["Viajes & Turismo", "Cine & Series", "Trabajo & Negocios", "Música & Cultura", "Tecnología & Programación", "Gastronomía & Cafés", "Deportes & Salud", "Ciencia & Física", "Videojuegos", "Moda & Arte"]
        user_ints = curr_user.get("interests", [])
        new_ints = []
        c_i1, c_i2 = st.columns(2)
        for idx, item in enumerate(all_possible):
            col = c_i1 if (idx % 2 == 0) else c_i2
            if col.checkbox(item, value=(item in user_ints), key=f"edit_int_{idx}"):
                new_ints.append(item)

        submit_p = st.form_submit_button("💾 Guardar Mi Perfil", use_container_width=True)
        if submit_p:
            update_user_profile(curr_user["id"], p_name, p_emoji, p_track, p_target, new_ints)
            st.success("¡Perfil y preferencias actualizadas exitosamente!")
            time.sleep(1)
            st.rerun()

    st.markdown("---")
    st.subheader("🔒 Cambiar Mi Contraseña")
    with st.form("pwd_form"):
        old_p = st.text_input("Contraseña Actual:", type="password")
        new_p = st.text_input("Nueva Contraseña:", type="password")
        new_p_c = st.text_input("Confirmar Nueva Contraseña:", type="password")
        submit_pwd = st.form_submit_button("Actualizar Contraseña")

        if submit_pwd:
            if new_p != new_p_c:
                st.error("Las nuevas contraseñas no coinciden.")
            else:
                ok, msg = change_user_password(curr_user["id"], old_p, new_p)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

    st.markdown("---")
    st.subheader("🛡️ Pregunta Secreta y PIN de Recuperación")
    st.caption("Si alguna vez olvidas tu contraseña o usuario, el sistema te pedirá esta respuesta o este PIN para recuperarlos.")
    with st.form("security_form"):
        curr_q = curr_user.get("security_question", "¿Cuál es tu palabra o comida favorita?")
        new_q = st.text_input("Tu Pregunta Secreta:", value=curr_q)
        new_a = st.text_input("Nueva Respuesta Secreta (déjala en blanco si no deseas cambiarla):", type="password")
        curr_pin = curr_user.get("recovery_pin", "1234")
        new_pin = st.text_input("Tu PIN Secreto de 4 números:", value=curr_pin, max_chars=6)
        submit_sec = st.form_submit_button("Actualizar Seguridad de Recuperación")

        if submit_sec:
            update_user_security(curr_user["id"], new_q, new_a, new_pin)
            st.success("¡Datos de recuperación actualizados exitosamente!")
            time.sleep(1)
            st.rerun()

# ==============================================================================
# PANTALLA 6: PANEL DE ADMINISTRACIÓN (SOLO ANDERSON)
# ==============================================================================
elif menu == "🛠️ Panel de Administración" and is_admin:
    st.title("🛠️ Panel Maestro de Administración (Anderson)")
    st.caption("Control global del sistema, gestión de cuentas de invitados y configuración.")

    tab_users_mgmt, tab_sys_cfg = st.tabs(["👥 Gestión de Usuarios e Invitados", "⚙️ Configuración del Sistema"])

    with tab_users_mgmt:
        st.subheader("Cuentas Registradas en la Plataforma")
        all_u = list(users.values())

        table_rows = []
        for u in all_u:
            table_rows.append({
                "Usuario": u.get("username", u.get("id")),
                "Nombre": f"{u.get('emoji', '')} {u.get('display_name')}",
                "Rol": u.get("role", "guest").upper(),
                "Enfoque": u.get("role_title", ""),
                "Horas": f"{u.get('total_hours', 0.0):.1f} / {u.get('target_hours', 100):.0f} h",
                "Sesiones": len(u.get("sessions", []))
            })
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

        st.markdown("---")
        st.subheader("Acciones de Administrador")
        guest_ids = [uid for uid, u in users.items() if u.get("role") == "guest"]

        if guest_ids:
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                st.write("**Restablecer Contraseña de un Invitado:**")
                sel_guest_pwd = st.selectbox("Seleccionar Usuario:", guest_ids, key="sel_g_pwd")
                new_guest_pwd = st.text_input("Nueva Contraseña:", key="in_g_pwd")
                if st.button("Actualizar Contraseña del Invitado"):
                    if len(new_guest_pwd) < 4:
                        st.error("Debe tener al menos 4 caracteres.")
                    else:
                        ok, msg = change_user_password(sel_guest_pwd, "", new_guest_pwd, is_admin_override=True)
                        st.success(f"Contraseña de {sel_guest_pwd} restablecida.")

            with col_act2:
                st.write("**Eliminar Cuenta de Invitado:**")
                sel_guest_del = st.selectbox("Seleccionar Invitado a Eliminar:", guest_ids, key="sel_g_del")
                if st.button("🗑️ Eliminar Usuario Definitivamente", type="secondary"):
                    ok, msg = admin_delete_user(sel_guest_del)
                    if ok:
                        st.success(msg)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.info("Aún no tienes amigos registrados como invitados. Cuando tus amigos creen su cuenta, aparecerán aquí para que puedas gestionarlos.")

    with tab_sys_cfg:
        st.subheader("Configuración Global")
        curr_cfg = data.get("system_config", {})

        with st.form("sys_cfg_form"):
            allow_reg = st.checkbox("Permitir que nuevos amigos se registren como invitados", value=curr_cfg.get("allow_guest_registration", True))
            ann_text = st.text_input("Mensaje de Anuncio (visible en la pantalla de bienvenida):", value=curr_cfg.get("announcement", ""))

            save_cfg = st.form_submit_button("Guardar Configuración Global")
            if save_cfg:
                data["system_config"]["allow_guest_registration"] = allow_reg
                data["system_config"]["announcement"] = ann_text.strip()
                save_couple_data(data)
                st.success("Configuración del sistema guardada exitosamente.")
                time.sleep(1)
                st.rerun()
