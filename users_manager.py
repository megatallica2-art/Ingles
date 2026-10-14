import os
import json
import hashlib
import secrets
from datetime import datetime, date, timedelta

USERS_DATA_FILE = os.path.join("logs", "couple_tracker.json")
LEGACY_TRACKER_FILE = os.path.join("logs", "time_tracker.json")

AVAILABLE_TRACKS = {
    "conversational": {
        "title": "Inglés Práctico, Social & Vida Diaria",
        "tone": "conversational",
        "default_categories": [
            "Conversación & Speaking Libre",
            "Escucha (Series / Podcasts / Música)",
            "Vocabulario Útil de la Vida Real",
            "Writing Casual (Mensajes / Emails / Diario)"
        ],
        "phases": [
            {"phase": 1, "name": "Fase 1: Confianza Básica (A1 ➔ A2)", "min_h": 0.0, "max_h": 40.0, "focus": "Rutinas, gustos, compras, restaurantes"},
            {"phase": 2, "name": "Fase 2: Conversación Cotidiana (A2 ➔ B1)", "min_h": 40.0, "max_h": 100.0, "focus": "Anécdotas, historias, podcasts simples, opiniones"},
            {"phase": 3, "name": "Fase 3: Fluidez Social (B1 ➔ B2)", "min_h": 100.0, "max_h": 180.0, "focus": "Series sin subtítulos, debates, cultura pop"},
            {"phase": 4, "name": "Fase 4: Espontaneidad Natural (B2 ➔ C1)", "min_h": 180.0, "max_h": 250.0, "focus": "Slang, idioms, humor, hablar sin traducir"}
        ]
    },
    "academic": {
        "title": "Académico, IELTS & Posgrado STEM",
        "tone": "academic",
        "default_categories": [
            "Input & SRS (Anki / Papers)",
            "Output (Writing Académico)",
            "Output (Speaking / Shadowing)",
            "Gramática & Técnica IELTS"
        ],
        "phases": [
            {"phase": 1, "name": "Fase 1: Cimientos y Fluidez Base (A2 ➔ B1)", "min_h": 0.0, "max_h": 180.0, "focus": "Gramática de uso, Shadowing, Anki base"},
            {"phase": 2, "name": "Fase 2: Transición STEM & Vocabulario (B1 ➔ B2)", "min_h": 180.0, "max_h": 400.0, "focus": "AWL 570, Physics World, gráficos IELTS Task 1"},
            {"phase": 3, "name": "Fase 3: Consolidación C1 (B2 ➔ C1)", "min_h": 400.0, "max_h": 650.0, "focus": "Papers arXiv, conferencias MIT, inversión sintáctica"},
            {"phase": 4, "name": "Fase 4: Simulacros Oficiales IELTS", "min_h": 650.0, "max_h": 750.0, "focus": "Tiempos estrictos, simulacros Cambridge 15-19"}
        ]
    },
    "business": {
        "title": "Negocios, Trabajo & Entrevistas",
        "tone": "business",
        "default_categories": [
            "Business Communication (Emails / Slack)",
            "Pitching & Presentaciones de Trabajo",
            "Simulación de Entrevistas Laborales",
            "Vocabulario Corporativo & Negociación"
        ],
        "phases": [
            {"phase": 1, "name": "Fase 1: Supervivencia en la Oficina (A2 ➔ B1)", "min_h": 0.0, "max_h": 50.0, "focus": "Emails formales, presentarse, pedir clarificaciones"},
            {"phase": 2, "name": "Fase 2: Comunicación Profesional (B1 ➔ B2)", "min_h": 50.0, "max_h": 120.0, "focus": "Reuniones en vivo, responder preguntas difíciles"},
            {"phase": 3, "name": "Fase 3: Negociación & Liderazgo (B2 ➔ C1)", "min_h": 120.0, "max_h": 200.0, "focus": "Argumentación sólida, persuasión, modismos corporativos"}
        ]
    },
    "travel": {
        "title": "Viajes, Turismo & Aventuras",
        "tone": "conversational",
        "default_categories": [
            "Aeropuertos & Transporte",
            "Hoteles & Alojamientos",
            "Restaurantes & Cafés",
            "Hacer Amigos Viajando"
        ],
        "phases": [
            {"phase": 1, "name": "Fase 1: Viajero Sin Miedo (A1 ➔ A2)", "min_h": 0.0, "max_h": 30.0, "focus": "Migraciones, pedir direcciones, compras"},
            {"phase": 2, "name": "Fase 2: Conectar con Locales (A2 ➔ B1)", "min_h": 30.0, "max_h": 80.0, "focus": "Hacer planes, hablar de tu país, resolver problemas"}
        ]
    }
}

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    return hashed, salt

def verify_password(stored_hash: str, stored_salt: str, password: str) -> bool:
    if not stored_hash or not stored_salt:
        return False
    check_hash, _ = hash_password(password, stored_salt)
    return check_hash == stored_hash

def get_default_users_dict() -> dict:
    and_hash, and_salt = hash_password("anderson2026")
    tan_hash, tan_salt = hash_password("tania2026")
    
    return {
        "anderson": {
            "id": "anderson",
            "username": "anderson",
            "password_hash": and_hash,
            "salt": and_salt,
            "role": "admin",
            "display_name": "Anderson",
            "emoji": "🔬",
            "role_title": "Física & IELTS Academic (Ruta C1)",
            "track": "academic",
            "target_hours": 700.0,
            "cefr_target": "C1",
            "tone": "academic",
            "interests": ["Física cuántica", "Ciencia", "Investigación", "Tecnología", "Simulaciones"],
            "phases": AVAILABLE_TRACKS["academic"]["phases"],
            "categories": AVAILABLE_TRACKS["academic"]["default_categories"],
            "total_minutes": 0,
            "total_hours": 0.0,
            "sessions": []
        },
        "tania": {
            "id": "tania",
            "username": "tania",
            "password_hash": tan_hash,
            "salt": tan_salt,
            "role": "partner",
            "display_name": "Tania",
            "emoji": "✨",
            "role_title": "Inglés Práctico & Conversación",
            "track": "conversational",
            "target_hours": 200.0,
            "cefr_target": "B2 / Fluidez",
            "tone": "conversational",
            "interests": ["Viajes", "Vida diaria", "Series y películas", "Música", "Café y restaurantes"],
            "phases": AVAILABLE_TRACKS["conversational"]["phases"],
            "categories": AVAILABLE_TRACKS["conversational"]["default_categories"],
            "total_minutes": 0,
            "total_hours": 0.0,
            "sessions": []
        }
    }

def load_couple_data() -> dict:
    os.makedirs("logs", exist_ok=True)
    defaults = get_default_users_dict()

    if not os.path.exists(USERS_DATA_FILE):
        initial = {
            "users": defaults,
            "evaluations": [],
            "system_config": {
                "allow_guest_registration": True,
                "announcement": "¡Bienvenidos! Practica cada día para alcanzar fluidez."
            }
        }
        save_couple_data(initial)
        return initial

    try:
        with open(USERS_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            users = data.setdefault("users", {})

            # Si existía el usuario con id legacy "novia", migrarlo a "tania"
            if "novia" in users and "tania" not in users:
                users["tania"] = users.pop("novia")
                users["tania"]["id"] = "tania"
                users["tania"]["username"] = "tania"

            # Asegurar que Anderson y Tania tengan sus campos completos
            for uid in ["anderson", "tania"]:
                if uid not in users:
                    users[uid] = defaults[uid]
                else:
                    # Garantizar password si era cuenta vieja sin hash
                    u = users[uid]
                    if not u.get("password_hash") or not u.get("salt"):
                        def_pass = "anderson2026" if uid == "anderson" else "tania2026"
                        h, s = hash_password(def_pass)
                        u["password_hash"] = h
                        u["salt"] = s
                    if not u.get("role"):
                        u["role"] = "admin" if uid == "anderson" else "partner"
                    if not u.get("username"):
                        u["username"] = uid
                    if not u.get("interests"):
                        u["interests"] = defaults[uid]["interests"]
                    if not u.get("track"):
                        u["track"] = defaults[uid]["track"]

                    # Recalcular horas por consistencia
                    t_min = sum(s.get("minutes", 0) for s in u.get("sessions", []))
                    u["total_minutes"] = t_min
                    u["total_hours"] = round(t_min / 60.0, 2)

            data.setdefault("system_config", {
                "allow_guest_registration": True,
                "announcement": "¡Bienvenidos! Practica cada día para alcanzar fluidez."
            })
            return data
    except Exception:
        return {
            "users": defaults,
            "evaluations": [],
            "system_config": {"allow_guest_registration": True}
        }

def save_couple_data(data: dict):
    os.makedirs("logs", exist_ok=True)
    with open(USERS_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def authenticate_user(username: str, password: str):
    data = load_couple_data()
    users = data.get("users", {})
    uname_clean = username.strip().lower()

    for uid, u in users.items():
        if u.get("username", "").strip().lower() == uname_clean:
            if verify_password(u.get("password_hash", ""), u.get("salt", ""), password):
                return u
    return None

def register_guest(username: str, password: str, display_name: str, track_choice: str = "conversational", target_hours: float = 100.0, interests_list: list = None):
    data = load_couple_data()
    users = data.get("users", {})
    
    if not data.get("system_config", {}).get("allow_guest_registration", True):
        return False, "El registro de nuevos usuarios está deshabilitado temporalmente por el Administrador."

    uname_clean = username.strip().lower()
    if not uname_clean or len(uname_clean) < 3:
        return False, "El usuario debe tener al menos 3 caracteres."
    if not password or len(password) < 4:
        return False, "La contraseña debe tener al menos 4 caracteres."

    for uid, u in users.items():
        if u.get("username", "").strip().lower() == uname_clean:
            return False, f"El usuario '{uname_clean}' ya existe. Por favor elige otro."

    new_id = f"guest_{uname_clean}"
    h, s = hash_password(password)
    track_info = AVAILABLE_TRACKS.get(track_choice, AVAILABLE_TRACKS["conversational"])

    new_user = {
        "id": new_id,
        "username": uname_clean,
        "password_hash": h,
        "salt": s,
        "role": "guest",
        "display_name": display_name.strip() or uname_clean.capitalize(),
        "emoji": "🌟",
        "role_title": track_info["title"],
        "track": track_choice,
        "target_hours": float(target_hours),
        "cefr_target": "Fluidez Personal",
        "tone": track_info["tone"],
        "interests": interests_list or ["Vida diaria", "Trabajo", "Viajes", "Música"],
        "phases": track_info["phases"],
        "categories": track_info["default_categories"],
        "total_minutes": 0,
        "total_hours": 0.0,
        "sessions": []
    }

    data["users"][new_id] = new_user
    save_couple_data(data)
    return True, "¡Cuenta creada exitosamente! Ya puedes iniciar sesión."

def update_user_profile(user_id: str, display_name: str, emoji: str, track: str, target_hours: float, interests: list):
    data = load_couple_data()
    u = data["users"].get(user_id)
    if not u:
        return False
    
    u["display_name"] = display_name.strip()
    u["emoji"] = emoji.strip() or "👤"
    u["target_hours"] = float(target_hours)
    u["interests"] = [i.strip() for i in interests if i.strip()]
    
    # Si cambió de track, actualizar categorías y fases
    if track != u.get("track") and track in AVAILABLE_TRACKS:
        u["track"] = track
        track_info = AVAILABLE_TRACKS[track]
        u["role_title"] = track_info["title"]
        u["tone"] = track_info["tone"]
        u["phases"] = track_info["phases"]
        u["categories"] = track_info["default_categories"]
        
    save_couple_data(data)
    return True

def change_user_password(user_id: str, old_pass: str, new_pass: str, is_admin_override: bool = False):
    data = load_couple_data()
    u = data["users"].get(user_id)
    if not u:
        return False, "Usuario no encontrado."
        
    if not is_admin_override:
        if not verify_password(u.get("password_hash"), u.get("salt"), old_pass):
            return False, "La contraseña actual es incorrecta."
            
    if len(new_pass) < 4:
        return False, "La nueva contraseña debe tener al menos 4 caracteres."
        
    h, s = hash_password(new_pass)
    u["password_hash"] = h
    u["salt"] = s
    save_couple_data(data)
    return True, "Contraseña actualizada exitosamente."

def admin_delete_user(user_id: str):
    data = load_couple_data()
    # No permitir borrar a Anderson ni a Tania
    if user_id in ["anderson", "tania"]:
        return False, "No se puede eliminar la cuenta de Anderson ni de Tania."
    if user_id in data.get("users", {}):
        del data["users"][user_id]
        save_couple_data(data)
        return True, "Usuario eliminado correctamente."
    return False, "Usuario no encontrado."

def log_user_session(user_id: str, minutes: int, category: str, description: str, notes: str = "") -> dict:
    if minutes <= 0:
        return {}
    data = load_couple_data()
    user_data = data["users"].get(user_id)
    if not user_data:
        return {}

    now_iso = datetime.now().isoformat()
    entry = {
        "timestamp": now_iso,
        "minutes": minutes,
        "category": category,
        "description": description,
        "notes": notes
    }
    user_data["sessions"].append(entry)
    user_data["total_minutes"] = sum(s.get("minutes", 0) for s in user_data["sessions"])
    user_data["total_hours"] = round(user_data["total_minutes"] / 60.0, 2)
    save_couple_data(data)

    # Google Sheets webhook sync si aplica
    try:
        from scripts.sheets_sync import sync_study_session
        user_label = f"[{user_data.get('display_name')}] {category}"
        sync_study_session(now_iso[:16].replace("T", " "), minutes, user_data["total_hours"], user_label, description, notes)
    except Exception:
        pass

    return entry

def log_user_evaluation(user_id: str, submission_type: str, text: str, metrics: dict):
    data = load_couple_data()
    user_data = data["users"].get(user_id, {})
    entry = {
        "user_id": user_id,
        "user_name": user_data.get("display_name", user_id),
        "timestamp": datetime.now().isoformat(),
        "type": submission_type,
        "input_text": text,
        "metrics": metrics
    }
    data.setdefault("evaluations", []).append(entry)
    save_couple_data(data)

def get_current_phase_for_user(user_data: dict) -> dict:
    total_h = user_data.get("total_hours", 0.0)
    phases = user_data.get("phases", [])
    for p in phases:
        if p["min_h"] <= total_h < p["max_h"]:
            return p
    return phases[-1] if phases else {"phase": 1, "name": "General", "focus": "Práctica general"}

def calculate_streak(sessions: list) -> int:
    if not sessions:
        return 0
    dates_set = set()
    for s in sessions:
        ts = s.get("timestamp", "")
        if ts:
            try:
                dt = datetime.fromisoformat(ts).date()
                dates_set.add(dt)
            except Exception:
                continue

    if not dates_set:
        return 0

    today = date.today()
    yesterday = today - timedelta(days=1)
    current_check = today if today in dates_set else (yesterday if yesterday in dates_set else None)
    if not current_check:
        return 0

    streak = 0
    while current_check in dates_set:
        streak += 1
        current_check -= timedelta(days=1)
    return streak

def toggle_lesson_completion(user_id: str, lesson_id: str) -> bool:
    data = load_couple_data()
    u = data["users"].get(user_id)
    if not u:
        return False
    completed = u.setdefault("completed_lessons", [])
    if lesson_id in completed:
        completed.remove(lesson_id)
        is_done = False
    else:
        completed.append(lesson_id)
        is_done = True
    save_couple_data(data)
    return is_done

def get_user_completed_lessons(user_id: str) -> list:
    data = load_couple_data()
    u = data["users"].get(user_id, {})
    return u.get("completed_lessons", [])

