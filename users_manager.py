import os
import json
from datetime import datetime, date, timedelta

USERS_DATA_FILE = os.path.join("logs", "couple_tracker.json")
LEGACY_TRACKER_FILE = os.path.join("logs", "time_tracker.json")

DEFAULT_PROFILES = {
    "anderson": {
        "id": "anderson",
        "display_name": "Anderson",
        "emoji": "🔬",
        "role_title": "Física & IELTS Academic (Ruta C1)",
        "target_hours": 700.0,
        "cefr_target": "C1",
        "tone": "academic",
        "phases": [
            {
                "phase": 1,
                "name": "Fase 1: Cimientos y Fluidez Base (A2 ➔ B1)",
                "min_h": 0.0,
                "max_h": 180.0,
                "focus": "English Grammar in Use, Shadowing, BBC 6-Minute, Anki base"
            },
            {
                "phase": 2,
                "name": "Fase 2: Transición STEM & Vocabulario (B1 ➔ B2)",
                "min_h": 180.0,
                "max_h": 400.0,
                "focus": "Academic Word List (570), Physics World, Gráficos IELTS Task 1, método PEEL"
            },
            {
                "phase": 3,
                "name": "Fase 3: Consolidación C1 (B2 ➔ C1)",
                "min_h": 400.0,
                "max_h": 650.0,
                "focus": "Papers arXiv, conferencias Perimeter/MIT, inversión sintáctica, ensayos complejos"
            },
            {
                "phase": 4,
                "name": "Fase 4: Técnica de Examen & Simulacros Oficiales",
                "min_h": 650.0,
                "max_h": 750.0,
                "focus": "Cambridge IELTS 15-19, tiempos estrictos, simulacros semanales"
            }
        ],
        "categories": [
            "Input & SRS (Anki / Papers)",
            "Output (Writing Académico)",
            "Output (Speaking / Shadowing)",
            "Gramática & Técnica IELTS"
        ]
    },
    "novia": {
        "id": "novia",
        "display_name": "Tania",
        "emoji": "✨",
        "role_title": "Inglés General, Práctico & Conversación",
        "target_hours": 200.0,
        "cefr_target": "B2 / Fluidez",
        "tone": "conversational",
        "phases": [
            {
                "phase": 1,
                "name": "Fase 1: Perder el Miedo & Confianza (A1 ➔ A2)",
                "min_h": 0.0,
                "max_h": 50.0,
                "focus": "Rutinas diarias, preguntas clave, frases para viajes y restaurantes, pronunciación básica"
            },
            {
                "phase": 2,
                "name": "Fase 2: Conversación Real & Fluidez (A2 ➔ B1)",
                "min_h": 50.0,
                "max_h": 110.0,
                "focus": "Contar anécdotas, describir situaciones, podcasts fáciles, hablar de hobbies y gustos"
            },
            {
                "phase": 3,
                "name": "Fase 3: Trabajo, Series & Social (B1 ➔ B2)",
                "min_h": 110.0,
                "max_h": 170.0,
                "focus": "Emails de trabajo, vocabulario profesional, entender series sin subtítulos en español"
            },
            {
                "phase": 4,
                "name": "Fase 4: Fluidez Natural & Espontaneidad (B2 ➔ C1)",
                "min_h": 170.0,
                "max_h": 250.0,
                "focus": "Expresiones cotidianas (idioms), hablar rápido con seguridad, humor y opiniones fluidas"
            }
        ],
        "categories": [
            "Conversación & Speaking Libre",
            "Escucha (Series / Podcasts / Música)",
            "Vocabulario Útil de la Vida Real",
            "Writing Casual (Mensajes / Emails / Diario)"
        ]
    }
}

def load_couple_data() -> dict:
    os.makedirs("logs", exist_ok=True)
    if not os.path.exists(USERS_DATA_FILE):
        # Migrar datos de legacy si existen
        anderson_sessions = []
        if os.path.exists(LEGACY_TRACKER_FILE):
            try:
                with open(LEGACY_TRACKER_FILE, "r", encoding="utf-8") as f:
                    leg = json.load(f)
                    anderson_sessions = leg.get("sessions", [])
            except Exception:
                anderson_sessions = []

        total_min_anderson = sum(s.get("minutes", 0) for s in anderson_sessions)
        
        initial = {
            "users": {
                "anderson": {
                    **DEFAULT_PROFILES["anderson"],
                    "total_minutes": total_min_anderson,
                    "total_hours": round(total_min_anderson / 60.0, 2),
                    "sessions": anderson_sessions
                },
                "novia": {
                    **DEFAULT_PROFILES["novia"],
                    "total_minutes": 0,
                    "total_hours": 0.0,
                    "sessions": []
                }
            },
            "evaluations": []
        }
        save_couple_data(initial)
        return initial

    try:
        with open(USERS_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Asegurar que ambos perfiles existan
            for uid, profile in DEFAULT_PROFILES.items():
                if uid not in data.get("users", {}):
                    data.setdefault("users", {})[uid] = {
                        **profile,
                        "total_minutes": 0,
                        "total_hours": 0.0,
                        "sessions": []
                    }
                else:
                    # recalcular totales por consistencia
                    u = data["users"][uid]
                    t_min = sum(s.get("minutes", 0) for s in u.get("sessions", []))
                    u["total_minutes"] = t_min
                    u["total_hours"] = round(t_min / 60.0, 2)
            return data
    except Exception:
        # Respaldo de seguridad
        return {
            "users": {
                uid: {**prof, "total_minutes": 0, "total_hours": 0.0, "sessions": []}
                for uid, prof in DEFAULT_PROFILES.items()
            },
            "evaluations": []
        }

def save_couple_data(data: dict):
    os.makedirs("logs", exist_ok=True)
    with open(USERS_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_user_name(user_id: str, new_name: str):
    data = load_couple_data()
    if user_id in data.get("users", {}):
        data["users"][user_id]["display_name"] = new_name.strip()
        save_couple_data(data)

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

    # Mantener sync legacy para Anderson si aplica
    if user_id == "anderson":
        try:
            legacy = {
                "target_hours": user_data["target_hours"],
                "total_minutes": user_data["total_minutes"],
                "total_hours": user_data["total_hours"],
                "sessions": user_data["sessions"]
            }
            with open(LEGACY_TRACKER_FILE, "w", encoding="utf-8") as f:
                json.dump(legacy, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    # Sincronización Google Sheets si está configurada
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

    # Sync a sheets
    try:
        from scripts.sheets_sync import sync_evaluation_result
        sync_evaluation_result(entry["timestamp"][:16].replace("T", " "), f"[{entry['user_name']}] {submission_type.upper()}", metrics, user_data.get("total_hours", 0.0))
    except Exception:
        pass

def get_current_phase_for_user(user_data: dict) -> dict:
    total_h = user_data.get("total_hours", 0.0)
    phases = user_data.get("phases", [])
    for p in phases:
        if p["min_h"] <= total_h < p["max_h"]:
            return p
    return phases[-1] if phases else {"phase": 1, "name": "General", "focus": "Práctica general"}

def calculate_streak(sessions: list) -> int:
    """Calcula la racha de días consecutivos de estudio."""
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

    # Verificar si estudió hoy o ayer para mantener racha activa
    current_check = today if today in dates_set else (yesterday if yesterday in dates_set else None)
    if not current_check:
        return 0

    streak = 0
    while current_check in dates_set:
        streak += 1
        current_check -= timedelta(days=1)

    return streak
